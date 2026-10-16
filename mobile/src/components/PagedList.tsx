import Ionicons from '@expo/vector-icons/Ionicons'
import type { ReactElement } from 'react'
import { ActivityIndicator, FlatList, RefreshControl, StyleSheet, Text, TextInput, View } from 'react-native'

import type { PagedListState } from '@/lib/usePagedList'
import { colors, radius, spacing } from '@/theme'
import { EmptyView, ErrorView, LoadingView } from './StateView'

interface PagedListProps<T extends { id: number }> {
  list: PagedListState<T>
  renderItem: (item: T) => ReactElement
  searchPlaceholder: string
  emptyTitle: string
  emptyMessage?: string
  /** Noun for the count line, e.g. "customers" */
  noun: string
}

export function PagedList<T extends { id: number }>({
  list, renderItem, searchPlaceholder, emptyTitle, emptyMessage, noun,
}: PagedListProps<T>) {
  const searchBar = (
    <View style={styles.searchBar}>
      <Ionicons name="search" size={18} color={colors.textMuted} />
      <TextInput
        value={list.search}
        onChangeText={list.setSearch}
        placeholder={searchPlaceholder}
        placeholderTextColor={colors.textMuted}
        style={styles.searchInput}
        autoCapitalize="none"
        autoCorrect={false}
        returnKeyType="search"
        clearButtonMode="while-editing"
        accessibilityLabel={searchPlaceholder}
      />
    </View>
  )

  if (list.error && list.items.length === 0) {
    return (
      <View style={styles.screen}>
        {list.error.isForbidden ? null : searchBar}
        <ErrorView error={list.error} onRetry={list.refresh} />
      </View>
    )
  }

  return (
    <View style={styles.screen}>
      {searchBar}
      {list.loading && list.items.length === 0 ? (
        <LoadingView />
      ) : (
        <FlatList
          data={list.items}
          keyExtractor={(item) => String(item.id)}
          renderItem={({ item }) => renderItem(item)}
          ItemSeparatorComponent={() => <View style={styles.separator} />}
          ListHeaderComponent={
            list.items.length > 0 ? (
              <Text style={styles.count}>{list.total} {noun}</Text>
            ) : undefined
          }
          ListEmptyComponent={
            <EmptyView
              title={list.search ? 'No matches' : emptyTitle}
              message={list.search ? `Nothing matches "${list.search}".` : emptyMessage}
            />
          }
          ListFooterComponent={list.loadingMore ? <ActivityIndicator style={styles.footer} color={colors.primary} /> : undefined}
          onEndReached={list.loadMore}
          onEndReachedThreshold={0.4}
          refreshControl={<RefreshControl refreshing={list.refreshing} onRefresh={list.refresh} tintColor={colors.primary} />}
          contentContainerStyle={list.items.length === 0 ? styles.emptyContent : styles.content}
          keyboardShouldPersistTaps="handled"
          keyboardDismissMode="on-drag"
        />
      )}
    </View>
  )
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: colors.background },
  searchBar: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.sm,
    margin: spacing.lg,
    marginBottom: spacing.sm,
    paddingHorizontal: spacing.md,
    minHeight: 44,
    borderRadius: radius.md,
    borderWidth: 1,
    borderColor: colors.border,
    backgroundColor: colors.surface,
  },
  searchInput: { flex: 1, fontSize: 16, color: colors.text, paddingVertical: spacing.sm },
  count: { paddingHorizontal: spacing.lg, paddingVertical: spacing.sm, fontSize: 13, color: colors.textMuted },
  separator: { height: StyleSheet.hairlineWidth, backgroundColor: colors.border, marginLeft: spacing.lg },
  content: { paddingBottom: spacing.xl },
  emptyContent: { flexGrow: 1 },
  footer: { padding: spacing.lg },
})
