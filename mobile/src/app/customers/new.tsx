import { useRouter } from 'expo-router'
import { useState } from 'react'
import { KeyboardAvoidingView, Platform, ScrollView, StyleSheet, Text, View } from 'react-native'

import { Button } from '@/components/Button'
import { TextField } from '@/components/TextField'
import { api, ApiError } from '@/lib/api'
import type { Customer } from '@/lib/types'
import { colors, radius, spacing } from '@/theme'

const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

export default function NewCustomerScreen() {
  const router = useRouter()
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [phone, setPhone] = useState('')
  const [submitted, setSubmitted] = useState(false)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const nameError = submitted && !name.trim() ? 'Name is required' : null
  const emailError = submitted && email.trim() && !EMAIL_PATTERN.test(email.trim()) ? 'Enter a valid email address' : null

  async function handleSave() {
    setSubmitted(true)
    if (!name.trim() || (email.trim() && !EMAIL_PATTERN.test(email.trim()))) return
    setSaving(true)
    setError(null)
    try {
      await api.post<Customer>('/crm/customers', {
        name: name.trim(),
        email: email.trim() || null,
        phone: phone.trim() || null,
      })
      router.back()
    } catch (e) {
      setError(e instanceof ApiError ? e.message : 'Could not save the customer.')
    } finally {
      setSaving(false)
    }
  }

  return (
    <KeyboardAvoidingView style={styles.flex} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
      <ScrollView style={styles.screen} contentContainerStyle={styles.content} keyboardShouldPersistTaps="handled">
        <View style={styles.card}>
          <TextField label="Name" value={name} onChangeText={setName} placeholder="Acme Corp" error={nameError} autoFocus />
          <TextField
            label="Email (optional)"
            value={email}
            onChangeText={setEmail}
            placeholder="billing@acme.com"
            keyboardType="email-address"
            autoCapitalize="none"
            autoCorrect={false}
            error={emailError}
          />
          <TextField
            label="Phone (optional)"
            value={phone}
            onChangeText={setPhone}
            placeholder="+1 555 0100"
            keyboardType="phone-pad"
          />
          {error ? <Text style={styles.error}>{error}</Text> : null}
          <Button title="Save customer" onPress={handleSave} loading={saving} />
          <Button title="Cancel" variant="secondary" onPress={() => router.back()} style={styles.cancel} />
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  )
}

const styles = StyleSheet.create({
  flex: { flex: 1 },
  screen: { flex: 1, backgroundColor: colors.background },
  content: { padding: spacing.lg },
  card: { padding: spacing.xl, borderRadius: radius.lg, borderWidth: 1, borderColor: colors.border, backgroundColor: colors.surface },
  error: { color: colors.danger, marginBottom: spacing.lg },
  cancel: { marginTop: spacing.md },
})
