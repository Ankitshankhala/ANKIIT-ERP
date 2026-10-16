"""One organization must never see, change or reference another organization's ERP data."""
from datetime import datetime, timedelta

import pytest

API = "/api/v1"

# (collection path, list key, create payload, update payload, has GET by id, has DELETE)
RESOURCES = [
    ("/crm/customers", "customers", {"name": "Alpha Customer"}, {"name": "Hijacked"}, False, True),
    ("/crm/leads", "leads", {"name": "Alpha Lead"}, {"name": "Hijacked"}, False, True),
    ("/crm/opportunities", "opportunities", {"name": "Alpha Deal", "value": "1000"}, {"name": "Hijacked"}, False, True),
    ("/inventory/products", "products", {"sku": "ALPHA-1", "name": "Alpha Widget"}, {"name": "Hijacked"}, True, True),
    ("/inventory/suppliers", "suppliers", {"name": "Alpha Supplier"}, {"name": "Hijacked"}, True, True),
    ("/inventory/warehouses", "warehouses", {"code": "ALPHA-WH", "name": "Alpha Warehouse"}, {"name": "Hijacked"}, True, True),
    ("/hr/employees", "employees", {"first_name": "Al", "last_name": "Pha", "email": "al@alpha.test"}, {"title": "Hijacked"}, False, False),
    ("/finance/accounts", "accounts",
     {"code": "6200_ALPHA", "name": "Alpha Expense", "account_type": "expense", "category": "operating_expenses"},
     {"name": "Hijacked"}, True, True),
]
RESOURCE_IDS = [r[0].strip("/").replace("/", "-") for r in RESOURCES]


@pytest.fixture
def orgs(make_org_admin):
    """Two organizations, each with a user holding every permission (not superusers)."""
    a_user, a_headers = make_org_admin(organization_name="Alpha Traders")
    b_user, b_headers = make_org_admin(organization_name="Beta Retail")
    assert a_user["organization_id"] != b_user["organization_id"]
    return {"a": a_headers, "b": b_headers, "a_user": a_user, "b_user": b_user}


def _list_ids(client, headers, path, key):
    response = client.get(f"{API}{path}", headers=headers, params={"limit": 100})
    assert response.status_code == 200, response.text
    return {item["id"] for item in response.json()[key]}


def _create(client, headers, path, payload):
    response = client.post(f"{API}{path}", json=payload, headers=headers)
    assert response.status_code == 201, response.text
    return response.json()


def _account_id(client, headers, code):
    accounts = client.get(f"{API}/finance/accounts", headers=headers, params={"limit": 100}).json()["accounts"]
    return next(a["id"] for a in accounts if a["code"] == code)


@pytest.mark.parametrize("path, key, payload, _update, _get, _delete", RESOURCES, ids=RESOURCE_IDS)
def test_records_are_invisible_to_other_organization(client, orgs, path, key, payload, _update, _get, _delete):
    def b_total():
        return client.get(f"{API}{path}", headers=orgs["b"]).json()["total"]

    b_total_before = b_total()
    record = _create(client, orgs["a"], path, payload)

    assert record["id"] in _list_ids(client, orgs["a"], path, key)
    assert record["id"] not in _list_ids(client, orgs["b"], path, key)
    # Totals come from Query.count(), which wraps the query in a subquery
    assert b_total() == b_total_before


@pytest.mark.parametrize("path, key, payload, update, has_get, has_delete", RESOURCES, ids=RESOURCE_IDS)
def test_other_organization_cannot_read_update_or_delete(client, orgs, path, key, payload, update, has_get, has_delete):
    record = _create(client, orgs["a"], path, payload)
    item_url = f"{API}{path}/{record['id']}"

    if has_get:
        assert client.get(item_url, headers=orgs["b"]).status_code == 404
    assert client.put(item_url, json=update, headers=orgs["b"]).status_code == 404
    if has_delete:
        assert client.delete(item_url, headers=orgs["b"]).status_code == 404

    # Organization A's record is still there and unchanged
    listed = client.get(f"{API}{path}", headers=orgs["a"], params={"limit": 100}).json()[key]
    mine = next(item for item in listed if item["id"] == record["id"])
    assert "Hijacked" not in mine.values()


def test_same_codes_are_allowed_in_each_organization(client, orgs):
    payload = {"sku": "SHARED-SKU", "name": "Widget"}
    _create(client, orgs["a"], "/inventory/products", payload)
    _create(client, orgs["b"], "/inventory/products", payload)

    duplicate = client.post(f"{API}/inventory/products", json=payload, headers=orgs["a"])
    assert duplicate.status_code in (400, 409), duplicate.text


def test_each_organization_gets_its_own_chart_of_accounts(client, orgs):
    a_cash = _account_id(client, orgs["a"], "1000_CASH")
    b_cash = _account_id(client, orgs["b"], "1000_CASH")
    assert a_cash != b_cash


def test_cannot_reference_another_organizations_records(client, orgs):
    a_customer = _create(client, orgs["a"], "/crm/customers", {"name": "Alpha Only"})
    a_product = _create(client, orgs["a"], "/inventory/products", {"sku": "ALPHA-REF", "name": "Alpha Ref"})
    b_warehouse = _create(client, orgs["b"], "/inventory/warehouses", {"code": "BETA-WH", "name": "Beta WH"})
    a_cash = _account_id(client, orgs["a"], "1000_CASH")
    a_revenue = _account_id(client, orgs["a"], "4000_REVENUE")
    a_invoice = _create(client, orgs["a"], "/finance/invoices", {
        "customer_name": "Alpha Customer",
        "due_date": (datetime.now() + timedelta(days=30)).isoformat(),
        "items": [{"description": "Service", "quantity": "1", "unit_price": "100"}],
    })

    attempts = [
        ("/crm/leads", {"name": "Sneaky lead", "customer_id": a_customer["id"]}),
        ("/crm/opportunities", {"name": "Sneaky deal", "customer_id": a_customer["id"]}),
        ("/inventory/stock/receive", {"product_id": a_product["id"], "quantity": "5", "to_warehouse_id": b_warehouse["id"]}),
        ("/finance/transactions", {"transaction_type": "journal_entry", "description": "Sneaky",
                                   "amount": "10", "debit_account_id": a_cash, "credit_account_id": a_revenue}),
        ("/finance/payments", {"invoice_id": a_invoice["id"], "amount": "10", "payment_method": "cash"}),
    ]
    for path, payload in attempts:
        response = client.post(f"{API}{path}", json=payload, headers=orgs["b"])
        assert response.status_code in (400, 404), f"{path}: {response.status_code} {response.text}"

    # Nothing leaked into either organization
    assert _list_ids(client, orgs["b"], "/crm/leads", "leads") == set()
    assert _list_ids(client, orgs["b"], "/crm/opportunities", "opportunities") == set()
    assert _list_ids(client, orgs["b"], "/finance/payments", "payments") == set()
    assert _list_ids(client, orgs["a"], "/finance/transactions", "transactions") == set()


def test_financial_reports_only_cover_own_organization(client, orgs):
    before = client.get(f"{API}/finance/reports/summary", headers=orgs["b"]).json()

    txn = _create(client, orgs["a"], "/finance/transactions", {
        "transaction_type": "receipt", "description": "Owner investment", "amount": "2500",
        "debit_account_id": _account_id(client, orgs["a"], "1000_CASH"),
        "credit_account_id": _account_id(client, orgs["a"], "3000_EQUITY"),
    })
    posted = client.post(f"{API}/finance/transactions/{txn['id']}/post", headers=orgs["a"])
    assert posted.status_code == 200, posted.text

    assert client.get(f"{API}/finance/reports/summary", headers=orgs["a"]).json()["cash_balance"] != before["cash_balance"]
    assert client.get(f"{API}/finance/reports/summary", headers=orgs["b"]).json() == before


def test_users_and_organizations_are_scoped(client, orgs):
    a_user, b_user = orgs["a_user"], orgs["b_user"]

    b_users = {u["id"] for u in client.get(f"{API}/users/", headers=orgs["b"]).json()}
    assert b_user["id"] in b_users and a_user["id"] not in b_users
    assert client.get(f"{API}/users/{a_user['id']}", headers=orgs["b"]).status_code == 404

    b_orgs = {o["id"] for o in client.get(f"{API}/organizations/", headers=orgs["b"]).json()}
    assert b_orgs == {b_user["organization_id"]}
    assert client.get(f"{API}/organizations/{a_user['organization_id']}", headers=orgs["b"]).status_code == 404


def test_cannot_move_user_into_another_organization(client, orgs):
    b_user = orgs["b_user"]
    response = client.put(
        f"{API}/users/{b_user['id']}",
        json={"organization_id": orgs["a_user"]["organization_id"]},
        headers=orgs["b"],
    )
    assert response.status_code == 200
    assert response.json()["organization_id"] == b_user["organization_id"]


def test_recent_activity_only_shows_own_organization(client, orgs):
    client.get(f"{API}/crm/customers", headers=orgs["a"])
    activity = client.get(f"{API}/dashboard/recent-activity", headers=orgs["b"]).json()
    assert {entry["user"] for entry in activity} <= {str(orgs["b_user"]["id"])}


def test_superuser_erp_data_is_scoped_too(client, orgs, admin_headers):
    record = _create(client, orgs["a"], "/crm/customers", {"name": "Alpha Private"})
    assert record["id"] not in _list_ids(client, admin_headers, "/crm/customers", "customers")


def test_flush_rejects_foreign_keys_into_another_organization(client, orgs):
    """The session guard holds even when a service forgets to validate an ID."""
    from app.core.database import SessionLocal
    from app.core.org_scope import CrossOrganizationReferenceError, set_session_organization
    from app.models.crm import Customer, Lead

    a_customer = _create(client, orgs["a"], "/crm/customers", {"name": "Alpha FK Target"})
    db = SessionLocal()
    try:
        set_session_organization(db, orgs["b_user"]["organization_id"])
        db.add(Lead(name="Cross-org lead", customer_id=a_customer["id"]))
        with pytest.raises(CrossOrganizationReferenceError):
            db.flush()
        db.rollback()

        # Same for an object assigned through the relationship
        set_session_organization(db, orgs["a_user"]["organization_id"])
        alpha_customer = db.query(Customer).filter(Customer.id == a_customer["id"]).one()
        set_session_organization(db, orgs["b_user"]["organization_id"])
        db.add(Lead(name="Cross-org lead 2", customer=alpha_customer))
        with pytest.raises(CrossOrganizationReferenceError):
            db.flush()
    finally:
        db.rollback()
        db.close()


def test_scoped_query_without_organization_fails_closed(client):
    from app.core.database import SessionLocal
    from app.core.org_scope import OrganizationScopeError
    from app.models.crm import Customer

    db = SessionLocal()
    try:
        with pytest.raises(OrganizationScopeError):
            db.query(Customer).all()
        db.add(Customer(name="Orphan"))
        with pytest.raises(OrganizationScopeError):
            db.flush()
    finally:
        db.rollback()
        db.close()
