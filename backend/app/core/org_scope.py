"""
Per-organization data isolation for ERP records.

Every model that mixes in ``OrgScopedMixin`` gets an ``organization_id`` column, and
two session-wide hooks enforce isolation without each query having to remember it:

* ``do_orm_execute`` adds ``organization_id = <session organization>`` to every ORM
  SELECT / UPDATE / DELETE that touches a scoped model (including joins, subqueries
  and relationship loads of the rows it returns).
* ``before_flush`` stamps the session organization onto new rows and refuses writes
  that belong to, or point at, another organization's records.

The session organization is set from the signed-in user in ``get_current_user``.
Code that runs outside a request (seed scripts) calls ``set_session_organization``
itself. Using a scoped model on a session with no organization raises instead of
silently returning everything.
"""
from typing import Optional

from sqlalchemy import Column, ForeignKey, Integer, event, inspect, select
from sqlalchemy.orm import MANYTOONE, ORMExecuteState, Session, declared_attr, with_loader_criteria

SESSION_ORGANIZATION_KEY = "organization_id"


class OrganizationScopeError(RuntimeError):
    """A scoped model was used on a session that has no organization set."""


class CrossOrganizationReferenceError(ValueError):
    """A write tried to touch or reference another organization's record."""


class OrgScopedMixin:
    """Marks a model as owned by a single organization."""

    @declared_attr
    def organization_id(cls):
        return Column(Integer, ForeignKey("organizations.id"), nullable=False, index=True)


def set_session_organization(session: Session, organization_id: Optional[int]) -> None:
    session.info[SESSION_ORGANIZATION_KEY] = organization_id


def get_session_organization(session: Session) -> Optional[int]:
    return session.info.get(SESSION_ORGANIZATION_KEY)


def _is_scoped(cls) -> bool:
    return isinstance(cls, type) and issubclass(cls, OrgScopedMixin)


@event.listens_for(Session, "do_orm_execute")
def _apply_organization_criteria(execute_state: ORMExecuteState) -> None:
    if not (execute_state.is_select or execute_state.is_update or execute_state.is_delete):
        return
    # Lazy/relationship loads inherit the criteria from the statement that loaded the parent
    if execute_state.is_column_load or execute_state.is_relationship_load:
        return

    # The criteria is always attached, not only when a scoped model is at the top level:
    # Query.count() and other wrappers nest the real SELECT in a subquery, which
    # ``all_mappers`` does not see. The option is a no-op for statements without scoped models.
    organization_id = get_session_organization(execute_state.session)
    if organization_id is not None:
        criteria = with_loader_criteria(
            OrgScopedMixin,
            lambda cls: cls.organization_id == organization_id,
            include_aliases=True,
        )
    else:
        if any(_is_scoped(mapper.class_) for mapper in execute_state.all_mappers):
            raise OrganizationScopeError(
                "Query on organization-scoped data without an organization on the session"
            )
        # Nested scoped selects without an organization match nothing
        criteria = with_loader_criteria(
            OrgScopedMixin,
            lambda cls: cls.organization_id.is_(None),
            include_aliases=True,
        )

    execute_state.statement = execute_state.statement.options(criteria)


def _scoped_tables(mapper) -> set:
    return {m.local_table for m in mapper.registry.mappers if _is_scoped(m.class_)}


def _check_references(session: Session, obj, organization_id: int) -> None:
    """Reject foreign keys that point at another organization's rows."""
    state = inspect(obj)
    mapper = state.mapper

    # Related objects assigned in memory (FK value may not be populated until flush)
    for rel in mapper.relationships:
        if rel.direction is not MANYTOONE or not _is_scoped(rel.mapper.class_):
            continue
        related = state.dict.get(rel.key)
        if related is not None and related.organization_id not in (None, organization_id):
            raise CrossOrganizationReferenceError(f"{rel.key} belongs to another organization")

    # Plain FK values: look up the owner of the referenced row
    scoped_tables = _scoped_tables(mapper)
    for column in mapper.local_table.columns:
        for fk in column.foreign_keys:
            target = fk.column.table
            if target not in scoped_tables:
                continue
            prop = mapper.get_property_by_column(column)
            if not (state.pending or state.attrs[prop.key].history.has_changes()):
                continue
            value = state.dict.get(prop.key)
            if value is None:
                continue
            # Core select on the Table, so the ORM criteria hook is not involved
            owner = session.execute(
                select(target.c.organization_id).where(fk.column == value)
            ).scalar()
            if owner is not None and owner != organization_id:
                raise CrossOrganizationReferenceError(
                    f"{prop.key}={value} belongs to another organization"
                )


@event.listens_for(Session, "before_flush")
def _stamp_and_validate_organization(session: Session, flush_context, instances) -> None:
    new_objects = [obj for obj in session.new if isinstance(obj, OrgScopedMixin)]
    changed_objects = [obj for obj in session.dirty if isinstance(obj, OrgScopedMixin)]
    deleted_objects = [obj for obj in session.deleted if isinstance(obj, OrgScopedMixin)]
    if not (new_objects or changed_objects or deleted_objects):
        return

    organization_id = get_session_organization(session)
    if organization_id is None:
        raise OrganizationScopeError(
            "Write to organization-scoped data without an organization on the session"
        )

    # Stamp first so references between objects created in the same flush line up
    for obj in new_objects:
        if obj.organization_id is None:
            obj.organization_id = organization_id

    for obj in new_objects + changed_objects + deleted_objects:
        if obj.organization_id != organization_id:
            raise CrossOrganizationReferenceError(
                f"{type(obj).__name__} belongs to another organization"
            )

    for obj in new_objects + changed_objects:
        _check_references(session, obj, organization_id)
