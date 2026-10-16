import { apiBaseUrl, defaultServerUrl } from './server'
import type { TokenResponse } from './types'

export class ApiError extends Error {
  /** HTTP status, or 0 when the server could not be reached */
  readonly status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
  }

  get isForbidden() {
    return this.status === 403
  }
}

type Query = Record<string, string | number | boolean | undefined | null>

interface RequestOptions {
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  body?: unknown
  query?: Query
  /** Send the bearer token and retry once after refreshing it (default true) */
  auth?: boolean
}

interface Session {
  server: string
  accessToken: string | null
  refreshToken: string | null
}

async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body = await response.json()
    const detail = body?.detail
    if (typeof detail === 'string') return detail
    // FastAPI validation errors: [{ loc, msg, ... }]
    if (Array.isArray(detail) && detail[0]?.msg) return detail.map((d: { msg: string }) => d.msg).join('\n')
  } catch {
    // Not JSON
  }
  return `Request failed (${response.status})`
}

function buildUrl(server: string, path: string, query?: Query): string {
  const url = `${apiBaseUrl(server)}${path}`
  const params = Object.entries(query ?? {})
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .map(([key, value]) => `${encodeURIComponent(key)}=${encodeURIComponent(String(value))}`)
  return params.length ? `${url}?${params.join('&')}` : url
}

class ApiClient {
  private session: Session = { server: defaultServerUrl(), accessToken: null, refreshToken: null }
  private refreshInFlight: Promise<boolean> | null = null

  /** Called after a token refresh so the new access token can be persisted */
  onTokensChanged?: (accessToken: string) => void
  /** Called when the session can no longer be used (refresh failed) */
  onSessionExpired?: () => void

  get server() {
    return this.session.server
  }

  configure(session: Partial<Session>) {
    this.session = { ...this.session, ...session }
  }

  async request<T>(path: string, options: RequestOptions = {}): Promise<T> {
    const { auth = true } = options
    let response = await this.send(path, options)

    if (response.status === 401 && auth && this.session.refreshToken) {
      if (await this.refreshAccessToken()) {
        response = await this.send(path, options)
      }
    }
    if (response.status === 401 && auth) {
      this.onSessionExpired?.()
    }
    if (!response.ok) {
      throw new ApiError(response.status, await readErrorMessage(response))
    }
    if (response.status === 204) return undefined as T
    return (await response.json()) as T
  }

  get<T>(path: string, query?: Query) {
    return this.request<T>(path, { query })
  }

  post<T>(path: string, body?: unknown, options: Omit<RequestOptions, 'method' | 'body'> = {}) {
    return this.request<T>(path, { ...options, method: 'POST', body })
  }

  private async send(path: string, { method = 'GET', body, query, auth = true }: RequestOptions) {
    const headers: Record<string, string> = { Accept: 'application/json' }
    if (body !== undefined) headers['Content-Type'] = 'application/json'
    if (auth && this.session.accessToken) headers.Authorization = `Bearer ${this.session.accessToken}`

    try {
      return await fetch(buildUrl(this.session.server, path, query), {
        method,
        headers,
        body: body === undefined ? undefined : JSON.stringify(body),
      })
    } catch {
      throw new ApiError(0, `Can't reach the server at ${this.session.server}`)
    }
  }

  /** One refresh at a time; concurrent 401s wait for the same attempt */
  private refreshAccessToken(): Promise<boolean> {
    if (!this.refreshInFlight) {
      this.refreshInFlight = (async () => {
        try {
          const tokens = await this.request<TokenResponse>(
            '/auth/refresh',
            { method: 'POST', body: { refresh_token: this.session.refreshToken }, auth: false },
          )
          this.session.accessToken = tokens.access_token
          this.onTokensChanged?.(tokens.access_token)
          return true
        } catch {
          return false
        } finally {
          this.refreshInFlight = null
        }
      })()
    }
    return this.refreshInFlight
  }
}

export const api = new ApiClient()
