import { ListRow } from '@/components/ListRow'
import { PagedList } from '@/components/PagedList'
import { titleCase } from '@/lib/format'
import type { Employee } from '@/lib/types'
import { usePagedList } from '@/lib/usePagedList'

const STATUS_TONES: Record<string, 'success' | 'warning' | 'neutral'> = {
  active: 'success',
  on_leave: 'warning',
}

export default function EmployeesScreen() {
  const list = usePagedList<Employee>('/hr/employees', 'employees')

  return (
    <PagedList
      list={list}
      noun="employees"
      searchPlaceholder="Search employees"
      emptyTitle="No employees yet"
      emptyMessage="Employees added in the web app show up here."
      renderItem={(employee) => (
        <ListRow
          title={`${employee.first_name} ${employee.last_name}`}
          subtitle={[employee.title, employee.department].filter(Boolean).join(' · ') || employee.email}
          badge={employee.status ? { label: titleCase(employee.status), tone: STATUS_TONES[employee.status] ?? 'neutral' } : null}
        />
      )}
    />
  )
}
