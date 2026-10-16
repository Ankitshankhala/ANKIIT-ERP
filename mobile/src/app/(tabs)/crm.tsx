import Ionicons from '@expo/vector-icons/Ionicons'
import { useFocusEffect, useRouter } from 'expo-router'
import { useCallback, useRef } from 'react'
import { Pressable, StyleSheet, View } from 'react-native'

import { ListRow } from '@/components/ListRow'
import { PagedList } from '@/components/PagedList'
import { useAuth } from '@/lib/auth'
import type { Customer } from '@/lib/types'
import { usePagedList } from '@/lib/usePagedList'
import { colors, spacing } from '@/theme'

export default function CustomersScreen() {
  const router = useRouter()
  const { can } = useAuth()
  const list = usePagedList<Customer>('/crm/customers', 'customers')

  // Pick up customers added from the "New customer" screen
  const firstFocus = useRef(true)
  const { refresh } = list
  useFocusEffect(
    useCallback(() => {
      if (firstFocus.current) {
        firstFocus.current = false
        return
      }
      void refresh()
    }, [refresh]),
  )

  return (
    <View style={styles.screen}>
      <PagedList
        list={list}
        noun="customers"
        searchPlaceholder="Search customers"
        emptyTitle="No customers yet"
        emptyMessage={can('crm:customer:create') ? 'Tap + to add your first customer.' : undefined}
        renderItem={(customer) => (
          <ListRow
            title={customer.name}
            subtitle={[customer.email, customer.phone].filter(Boolean).join(' · ') || null}
            badge={customer.is_active ? null : { label: 'Inactive' }}
          />
        )}
      />
      {can('crm:customer:create') ? (
        <Pressable
          style={({ pressed }) => [styles.fab, pressed && styles.fabPressed]}
          onPress={() => router.push('/customers/new')}
          accessibilityRole="button"
          accessibilityLabel="Add customer"
        >
          <Ionicons name="add" size={28} color="#fff" />
        </Pressable>
      ) : null}
    </View>
  )
}

const styles = StyleSheet.create({
  screen: { flex: 1 },
  fab: {
    position: 'absolute',
    right: spacing.lg,
    bottom: spacing.lg,
    width: 56,
    height: 56,
    borderRadius: 28,
    backgroundColor: colors.primary,
    alignItems: 'center',
    justifyContent: 'center',
    elevation: 4,
    shadowColor: '#000',
    shadowOpacity: 0.2,
    shadowRadius: 6,
    shadowOffset: { width: 0, height: 3 },
  },
  fabPressed: { backgroundColor: colors.primaryPressed },
})
