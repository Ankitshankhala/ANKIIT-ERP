import { StyleSheet, Text, View } from 'react-native'

import { colors, radius, spacing } from '@/theme'

type BadgeTone = 'neutral' | 'success' | 'warning' | 'danger' | 'info'

const BADGE_COLORS: Record<BadgeTone, { bg: string; fg: string }> = {
  neutral: { bg: colors.background, fg: colors.textMuted },
  success: { bg: colors.successSoft, fg: colors.success },
  warning: { bg: colors.warningSoft, fg: colors.warning },
  danger: { bg: colors.dangerSoft, fg: colors.danger },
  info: { bg: colors.primarySoft, fg: colors.primary },
}

export function Badge({ label, tone = 'neutral' }: { label: string; tone?: BadgeTone }) {
  const palette = BADGE_COLORS[tone]
  return (
    <View style={[styles.badge, { backgroundColor: palette.bg }]}>
      <Text style={[styles.badgeText, { color: palette.fg }]}>{label}</Text>
    </View>
  )
}

interface ListRowProps {
  title: string
  subtitle?: string | null
  /** Right-aligned value, e.g. an amount */
  value?: string | null
  badge?: { label: string; tone?: BadgeTone } | null
}

export function ListRow({ title, subtitle, value, badge }: ListRowProps) {
  return (
    <View style={styles.row} accessible accessibilityLabel={[title, subtitle, value, badge?.label].filter(Boolean).join(', ')}>
      <View style={styles.main}>
        <Text style={styles.title} numberOfLines={1}>{title}</Text>
        {subtitle ? <Text style={styles.subtitle} numberOfLines={1}>{subtitle}</Text> : null}
      </View>
      <View style={styles.side}>
        {value ? <Text style={styles.value}>{value}</Text> : null}
        {badge ? <Badge {...badge} /> : null}
      </View>
    </View>
  )
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    backgroundColor: colors.surface,
    gap: spacing.md,
  },
  main: { flex: 1, minWidth: 0 },
  title: { fontSize: 16, fontWeight: '500', color: colors.text },
  subtitle: { marginTop: 2, fontSize: 13, color: colors.textMuted },
  side: { alignItems: 'flex-end', gap: spacing.xs },
  value: { fontSize: 15, fontWeight: '600', color: colors.text, fontVariant: ['tabular-nums'] },
  badge: { paddingHorizontal: spacing.sm, paddingVertical: 2, borderRadius: radius.sm },
  badgeText: { fontSize: 12, fontWeight: '600' },
})
