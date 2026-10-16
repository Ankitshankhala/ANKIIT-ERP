import Ionicons from '@expo/vector-icons/Ionicons'
import { useRef, useState, type ComponentRef } from 'react'
import {
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native'
import { SafeAreaView } from 'react-native-safe-area-context'

import { Button } from '@/components/Button'
import { TextField } from '@/components/TextField'
import { ApiError } from '@/lib/api'
import { useAuth } from '@/lib/auth'
import { colors, radius, spacing } from '@/theme'

export default function LoginScreen() {
  const { signIn, server: savedServer } = useAuth()
  const [identifier, setIdentifier] = useState('')
  const [password, setPassword] = useState('')
  // Until edited, follow the saved address (it arrives after launch-time session restore)
  const [serverInput, setServerInput] = useState<string | null>(null)
  const server = serverInput ?? savedServer
  const [showPassword, setShowPassword] = useState(false)
  const [showServer, setShowServer] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const passwordRef = useRef<ComponentRef<typeof TextInput>>(null)

  const canSubmit = identifier.trim().length > 0 && password.length > 0 && !submitting

  async function handleSubmit() {
    if (!canSubmit) return
    setSubmitting(true)
    setError(null)
    try {
      await signIn(identifier, password, server)
    } catch (e) {
      if (e instanceof ApiError && e.status === 0) {
        setShowServer(true)
        setError(`${e.message}. Check the server address below and that the backend is running.`)
      } else if (e instanceof ApiError && e.status === 401) {
        setError('Incorrect email/username or password.')
      } else {
        setError(e instanceof Error ? e.message : 'Sign-in failed.')
      }
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
          <View style={styles.brand}>
            <View style={styles.logo}>
              <Text style={styles.logoText}>A</Text>
            </View>
            <Text style={styles.heading}>Sign in to ANKIIT ERP</Text>
            <Text style={styles.subheading}>Welcome back! Please sign in to your account.</Text>
          </View>

          <View style={styles.card}>
            <TextField
              label="Email or username"
              value={identifier}
              onChangeText={setIdentifier}
              placeholder="you@company.com"
              autoCapitalize="none"
              autoCorrect={false}
              autoComplete="username"
              textContentType="username"
              keyboardType="email-address"
              returnKeyType="next"
              onSubmitEditing={() => passwordRef.current?.focus()}
            />
            <View>
              <TextField
                ref={passwordRef}
                label="Password"
                value={password}
                onChangeText={setPassword}
                placeholder="Your password"
                secureTextEntry={!showPassword}
                autoCapitalize="none"
                autoComplete="current-password"
                textContentType="password"
                returnKeyType="go"
                onSubmitEditing={handleSubmit}
                style={styles.passwordInput}
              />
              <Pressable
                onPress={() => setShowPassword((v) => !v)}
                style={styles.eye}
                hitSlop={8}
                accessibilityRole="button"
                accessibilityLabel={showPassword ? 'Hide password' : 'Show password'}
              >
                <Ionicons name={showPassword ? 'eye-off-outline' : 'eye-outline'} size={22} color={colors.textMuted} />
              </Pressable>
            </View>

            {error ? (
              <View style={styles.errorBox} accessibilityLiveRegion="polite">
                <Text style={styles.errorText}>{error}</Text>
              </View>
            ) : null}

            <Button title="Sign in" onPress={handleSubmit} loading={submitting} disabled={!canSubmit} />

            <Pressable
              onPress={() => setShowServer((v) => !v)}
              style={styles.serverToggle}
              accessibilityRole="button"
              accessibilityLabel={`Server: ${server}. ${showServer ? 'Hide' : 'Change'} server address`}
              accessibilityState={{ expanded: showServer }}
            >
              <Ionicons name="server-outline" size={16} color={colors.textMuted} />
              <Text style={styles.serverToggleText} numberOfLines={1}>Server: {server}</Text>
              <Ionicons name={showServer ? 'chevron-up' : 'chevron-down'} size={16} color={colors.textMuted} />
            </Pressable>
            {showServer ? (
              <TextField
                label="Server address"
                value={server}
                onChangeText={setServerInput}
                placeholder="http://192.168.1.20:8000"
                autoCapitalize="none"
                autoCorrect={false}
                keyboardType="url"
              />
            ) : null}
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  )
}

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: colors.background },
  flex: { flex: 1 },
  content: { flexGrow: 1, justifyContent: 'center', padding: spacing.xl, maxWidth: 480, width: '100%', alignSelf: 'center' },
  brand: { alignItems: 'center', marginBottom: spacing.xl },
  logo: {
    width: 56,
    height: 56,
    borderRadius: radius.lg,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.lg,
  },
  logoText: { color: '#fff', fontSize: 26, fontWeight: '700' },
  heading: { fontSize: 24, fontWeight: '700', color: colors.text, textAlign: 'center' },
  subheading: { marginTop: spacing.xs, fontSize: 14, color: colors.textMuted, textAlign: 'center' },
  card: {
    padding: spacing.xl,
    borderRadius: radius.lg,
    backgroundColor: colors.surface,
    borderWidth: 1,
    borderColor: colors.border,
  },
  passwordInput: { paddingRight: 48 },
  eye: { position: 'absolute', right: spacing.md, top: 34 },
  errorBox: { backgroundColor: colors.dangerSoft, borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  errorText: { color: colors.danger, fontSize: 14 },
  serverToggle: { flexDirection: 'row', alignItems: 'center', gap: spacing.xs, marginTop: spacing.lg, marginBottom: spacing.sm },
  serverToggleText: { flex: 1, fontSize: 13, color: colors.textMuted },
})
