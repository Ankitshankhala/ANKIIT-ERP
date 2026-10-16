import { StyleSheet, Text, View } from 'react-native'

import { colors, radius, spacing } from '@/theme'

interface StatCardProps {
  label: string
  value: string
  tone?: 'default' | 'positive' | 'negative'
}

export function StatCard({ label, value, tone = 'default' }: StatCardProps) {
  return (
    <View style={styles.card} accessible accessibilityLabel={`${label}: ${value}`}>
      <Text style={styles.label}>{label}</Text>
      <Text
        style={[
          styles.value,
          tone === 'positive' && { color: colors.success },
          tone === 'negative' && { color: colors.danger },
        ]}
        numberOfLines={1}
        adjustsFontSizeToFit
      >
        {value}
      </Text>
    </View>
  )
}

const styles = StyleSheet.create({
  card: {
    flexGrow: 1,
    flexBasis: '45%',
    padding: spacing.lg,
    borderRadius: radius.lg,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  label: { fontSize: 13, color: colors.textMuted, marginBottom: spacing.xs },
  value: { fontSize: 22, fontWeight: '700', color: colors.text, fontVariant: ['tabular-nums'] },
})
