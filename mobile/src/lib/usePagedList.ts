import { useCallback, useEffect, useRef, useState } from 'react'

import { api, ApiError } from './api'

interface FirstPageResult<T> {
  id: number
  page: { rows: T[]; total: number } | null
  error: ApiError | null
}

interface PagedResponse {
  total: number
  [key: string]: unknown
}

export interface PagedListState<T> {
  items: T[]
  total: number
  loading: boolean
  refreshing: boolean
  loadingMore: boolean
  error: ApiError | null
  search: string
  setSearch: (value: string) => void
  refresh: () => Promise<void>
  loadMore: () => void
}

/**
 * Loads one of the API's `{ <key>: T[], total }` list endpoints that take skip/limit/q,
 * with debounced search, pull-to-refresh and infinite scroll.
 */
export function usePagedList<T>(path: string, key: string, pageSize = 20): PagedListState<T> {
  const [items, setItems] = useState<T[]>([])
  const [total, setTotal] = useState(0)
  const [loading, setLoading] = useState(true)
  const [refreshing, setRefreshing] = useState(false)
  const [loadingMore, setLoadingMore] = useState(false)
  const [error, setError] = useState<ApiError | null>(null)
  const [search, setSearch] = useState('')
  const [query, setQuery] = useState('')
  const requestId = useRef(0)

  // Debounce typing in the search box
  useEffect(() => {
    const timer = setTimeout(() => setQuery(search.trim()), 300)
    return () => clearTimeout(timer)
  }, [search])

  const fetchPage = useCallback(async (skip: number) => {
    const response = await api.get<PagedResponse>(path, { skip, limit: pageSize, q: query })
    return { rows: (response[key] as T[]) ?? [], total: response.total ?? 0 }
  }, [path, key, pageSize, query])

  /** Fetch the first page, tagged with a request id so stale responses can be dropped */
  const fetchFirstPage = useCallback(async (): Promise<FirstPageResult<T>> => {
    const id = ++requestId.current
    try {
      return { id, page: await fetchPage(0), error: null }
    } catch (e) {
      return { id, page: null, error: e instanceof ApiError ? e : new ApiError(0, String(e)) }
    }
  }, [fetchPage])

  const applyFirstPage = useCallback((result: FirstPageResult<T>) => {
    if (result.id !== requestId.current) return
    if (result.page) {
      setItems(result.page.rows)
      setTotal(result.page.total)
      setError(null)
    } else {
      setError(result.error)
    }
    setLoading(false)
    setRefreshing(false)
  }, [])

  // Initial load and every new search; earlier results stay visible until the new ones arrive
  useEffect(() => {
    fetchFirstPage().then(applyFirstPage)
  }, [fetchFirstPage, applyFirstPage])

  const refresh = useCallback(async () => {
    setRefreshing(true)
    applyFirstPage(await fetchFirstPage())
  }, [fetchFirstPage, applyFirstPage])

  const loadMore = useCallback(() => {
    if (loading || loadingMore || refreshing || items.length >= total) return
    const id = requestId.current
    setLoadingMore(true)
    fetchPage(items.length)
      .then((page) => {
        if (id !== requestId.current) return
        setItems((current) => [...current, ...page.rows])
        setTotal(page.total)
      })
      .catch(() => {
        // Keep what is already on screen; pull-to-refresh retries
      })
      .finally(() => setLoadingMore(false))
  }, [fetchPage, items.length, loading, loadingMore, refreshing, total])

  return { items, total, loading, refreshing, loadingMore, error, search, setSearch, refresh, loadMore }
}
