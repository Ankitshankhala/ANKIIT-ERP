import { useCallback, useState } from 'react'
import { RefreshControl, ScrollView, StyleSheet, Text, View } from 'react-native'
import { useFocusEffect } from 'expo-router'

import { Badge, ListRow } from '@/components/ListRow'
import { StatCard } from '@/components/StatCard'
import { LoadingView } from '@/components/StateView'
import { api, ApiError } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { formatDate, formatMoney, titleCase } from '@/lib/format'
import type { FinancialSummary, Invoice } from '@/lib/types'
import { colors, radius, spacing } from '@/theme'

type Section<T> = { data: T | null; error: ApiError | null }

interface HomeData {
  summary: Section<FinancialSummary>
  invoices: Section<Invoice[]>
  counts: { label: string; value: number | null }[]
}

const INVOICE_TONES: Record<string, 'success' | 'danger' | 'info' | 'neutral'> = {
  paid: 'success',
  overdue: 'danger',
  sent: 'info',
}

async function section<T>(load: () => Promise<T>): Promise<Section<T>> {
  try {
    return { data: await load(), error: null }
  } catch (e) {
    return { data: null, error: e instanceof ApiError ? e : new ApiError(0, String(e)) }
  }
}

async function countOf(path: string): Promise<number | null> {
  try {
    const response = await api.get<{ total: number }>(path, { limit: 1 })
    return response.total
  } catch {
    return null
  }
}

async function loadHome(): Promise<HomeData> {
  // Each section fails on its own: a role without finance access still sees the rest
  const [summary, invoices, customers, products, employees] = await Promise.all([
    section(() => api.get<FinancialSummary>('/finance/reports/summary')),
    section(async () => (await api.get<{ invoices: Invoice[] }>('/finance/invoices', { limit: 5 })).invoices),
    countOf('/crm/customers'),
    countOf('/inventory/products'),
    countOf('/hr/employees'),
  ])
  return {
    summary,
    invoices,
    counts: [
      { label: 'Customers', value: customers },
      { label: 'Products', value: products },
      { label: 'Employees', value: employees },
    ],
  }
}

export default function HomeScreen() {
  const { user, organizationName } = useAuth()
  const [data, setData] = useState<HomeData | null>(null)
  const [refreshing, setRefreshing] = useState(false)

  const reload = useCallback(async () => {
    setData(await loadHome())
  }, [])

  // Refresh whenever the tab comes back into view (e.g. after adding a customer)
  useFocusEffect(
    useCallback(() => {
      void reload()
    }, [reload]),
  )

  const onRefresh = useCallback(async () => {
    setRefreshing(true)
    try {
      await reload()
    } finally {
      setRefreshing(false)
    }
  }, [reload])

  if (!data) return <LoadingView />

  const { summary, invoices, counts } = data
  const netIncome = Number.parseFloat(summary.data?.net_income ?? '0')

  return (
    <ScrollView
      style={styles.screen}
      contentContainerStyle={styles.content}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />}
    >
      <Text style={styles.greeting}>Hello, {user?.first_name}</Text>
      {organizationName ? <Text style={styles.organization}>{organizationName}</Text> : null}

      <Text style={styles.sectionTitle}>Finance</Text>
      {summary.data ? (
        <View style={styles.grid}>
          <StatCard label="Cash" value={formatMoney(summary.data.cash_balance)} />
          <StatCard label="Net income" value={formatMoney(summary.data.net_income)}
            tone={netIncome > 0 ? 'positive' : netIncome < 0 ? 'negative' : 'default'} />
          <StatCard label="Receivable" value={formatMoney(summary.data.accounts_receivable)} />
          <StatCard label="Payable" value={formatMoney(summary.data.accounts_payable)} />
        </View>
      ) : (
        <SectionNote error={summary.error} />
      )}

      <Text style={styles.sectionTitle}>At a glance</Text>
      <View style={styles.countRow}>
        {counts.map((count) => (
          <View key={count.label} style={styles.countCard} accessible accessibilityLabel={`${count.label}: ${count.value ?? 'not available'}`}>
            <Text style={styles.countValue}>{count.value ?? '—'}</Text>
            <Text style={styles.countLabel}>{count.label}</Text>
          </View>
        ))}
      </View>

      <Text style={styles.sectionTitle}>Recent invoices</Text>
      {invoices.data ? (
        invoices.data.length > 0 ? (
          <View style={styles.listCard}>
            {invoices.data.map((invoice, index) => (
              <View key={invoice.id} style={index > 0 ? styles.listDivider : undefined}>
                <ListRow
                  title={invoice.customer_name}
                  subtitle={`${invoice.invoice_number} · due ${formatDate(invoice.due_date)}`}
                  value={formatMoney(invoice.total_amount)}
                  badge={{ label: titleCase(invoice.status), tone: INVOICE_TONES[invoice.status] ?? 'neutral' }}
                />
              </View>
            ))}
          </View>
        ) : (
          <Text style={styles.note}>No invoices yet.</Text>
        )
      ) : (
        <SectionNote error={invoices.error} />
      )}
    </ScrollView>
  )
}

function SectionNote({ error }: { error: ApiError | null }) {
  if (error?.isForbidden) {
    return (
      <View style={styles.noteRow}>
        <Badge label="No access" />
        <Text style={styles.note}>{"Your role can't view this section."}</Text>
      </View>
    )
  }
  return <Text style={[styles.note, styles.noteError]}>{error?.message ?? "Couldn't load."}</Text>
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg, paddingBottom: spacing.xl * 2 },
  greeting: { fontSize: 24, fontWeight: '700', color: colors.text },
  organization: { marginTop: 2, fontSize: 15, color: colors.textMuted },
  sectionTitle: { marginTop: spacing.xl, marginBottom: spacing.md, fontSize: 13, fontWeight: '600', color: colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.5 },
  grid: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.md },
  countRow: { flexDirection: 'row', gap: spacing.md },
  countCard: {
    flex: 1,
    alignItems: 'center',
    paddingVertical: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  countValue: { fontSize: 22, fontWeight: '700', color: colors.text, fontVariant: ['tabular-nums'] },
  countLabel: { marginTop: 2, fontSize: 13, color: colors.textMuted },
  listCard: { borderRadius: radius.lg, overflow: 'hidden', borderWidth: 1, borderColor: colors.border, backgroundColor: colors.surface },
  listDivider: { borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: colors.border },
  noteRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.sm },
  note: { fontSize: 14, color: colors.textMuted },
  noteError: { color: colors.danger },
})
