import Constants from 'expo-constants'
import { useState } from 'react'
import { ScrollView, StyleSheet, Text, View } from 'react-native'

import { Button } from '@/components/Button'
import { useAuth } from '@/lib/auth'
import { initials, titleCase } from '@/lib/format'
import { colors, radius, spacing } from '@/theme'

export default function ProfileScreen() {
  const { user, organizationName, server, signOut } = useAuth()
  const [signingOut, setSigningOut] = useState(false)

  if (!user) return null

  const details: [string, string][] = [
    ['Username', user.username],
    ['Email', user.email],
    ['Role', titleCase(user.role_name) || '—'],
    ['Organization', organizationName ?? '—'],
    ['Server', server],
    ['App version', Constants.expoConfig?.version ?? '—'],
  ]

  async function handleSignOut() {
    setSigningOut(true)
    try {
      await signOut()
    } finally {
      setSigningOut(false)
    }
  }

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{initials(user.first_name, user.last_name)}</Text>
        </View>
        <Text style={styles.name}>{user.full_name ?? `${user.first_name} ${user.last_name}`}</Text>
      </View>

      <View style={styles.card}>
        {details.map(([label, value], index) => (
          <View key={label} style={[styles.detailRow, index > 0 && styles.detailDivider]}>
            <Text style={styles.detailLabel}>{label}</Text>
            <Text style={styles.detailValue} numberOfLines={1} selectable>{value}</Text>
          </View>
        ))}
      </View>

      <Button title="Sign out" variant="danger" onPress={handleSignOut} loading={signingOut} style={styles.signOut} />
    </ScrollView>
  )
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg, paddingBottom: spacing.xl * 2 },
  header: { alignItems: 'center', marginVertical: spacing.xl },
  avatar: {
    width: 72,
    height: 72,
    borderRadius: 36,
    backgroundColor: colors.primarySoft,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  avatarText: { fontSize: 26, fontWeight: '700', color: colors.primary },
  name: { fontSize: 20, fontWeight: '700', color: colors.text },
  card: { borderRadius: radius.lg, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.surface },
  detailRow: { flexDirection: 'row', justifyContent: 'space-between', gap: spacing.lg, paddingVertical: spacing.md, paddingHorizontal: spacing.lg },
  detailDivider: { borderTopWidth: StyleSheet.hairlineWidth, borderTopColor: colors.border },
  detailLabel: { fontSize: 15, color: colors.textMuted },
  detailValue: { flexShrink: 1, fontSize: 15, color: colors.text, textAlign: 'right' },
  signOut: { marginTop: spacing.xl },
})
