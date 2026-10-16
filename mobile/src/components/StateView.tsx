import Ionicons from '@expo/vector-icons/Ionicons'
import { ActivityIndicator, StyleSheet, Text, View } from 'react-native'

import type { ApiError } from '@/lib/api'
import { colors, spacing } from '@/theme'
import { Button } from './Button'

export function LoadingView() {
  return (
    <View style={styles.container}>
      <ActivityIndicator size="large" color={colors.primary} />
    </View>
  )
}

export function EmptyView({ title, message }: { title: string; message?: string }) {
  return (
    <View style={styles.container}>
      <Ionicons name="file-tray-outline" size={40} color={colors.textMuted} />
      <Text style={styles.title}>{title}</Text>
      {message ? <Text style={styles.message}>{message}</Text> : null}
    </View>
  )
}

export function ErrorView({ error, onRetry }: { error: ApiError; onRetry?: () => void }) {
  if (error.isForbidden) {
    return (
      <View style={styles.container}>
        <Ionicons name="lock-closed-outline" size={40} color={colors.textMuted} />
        <Text style={styles.title}>No access</Text>
        <Text style={styles.message}>{"Your role doesn't include this module. Ask an administrator for access."}</Text>
      </View>
    )
  }
  return (
    <View style={styles.container}>
      <Ionicons name="cloud-offline-outline" size={40} color={colors.danger} />
      <Text style={styles.title}>{"Couldn't load"}</Text>
      <Text style={styles.message}>{error.message}</Text>
      {onRetry ? <Button title="Try again" variant="secondary" onPress={onRetry} style={styles.retry} /> : null}
    </View>
  )
}

const styles = StyleSheet.create({
  container: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl, gap: spacing.sm },
  title: { fontSize: 17, fontWeight: '600', color: colors.text, textAlign: 'center' },
  message: { fontSize: 14, color: colors.textMuted, textAlign: 'center', maxWidth: 320 },
  retry: { marginTop: spacing.md, alignSelf: 'stretch', maxWidth: 240, width: '100%' },
})
