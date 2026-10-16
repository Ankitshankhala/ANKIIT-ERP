import Constants from 'expo-constants'
import { Platform } from 'react-native'

const API_PATH = '/api/v1'

/**
 * Where the ANKIIT ERP backend is expected by default.
 *
 * EXPO_PUBLIC_API_URL wins when set. Otherwise, in development the phone loads the
 * JavaScript bundle from the dev machine (hostUri looks like "192.168.1.20:8081"), so
 * the API on that same machine is at port 8000. The browser preview uses localhost.
 */
export function defaultServerUrl(): string {
  const fromEnv = process.env.EXPO_PUBLIC_API_URL
  if (fromEnv) return normalizeServerUrl(fromEnv)

  const host = Constants.expoConfig?.hostUri?.split(':')[0]
  if (host && Platform.OS !== 'web') return `http://${host}:8000`
  return 'http://localhost:8000'
}

/** Accepts "192.168.1.20:8000", "https://erp.example.com/api/v1/" etc. and returns "scheme://host[:port]". */
export function normalizeServerUrl(input: string): string {
  let url = input.trim().replace(/\/+$/, '')
  if (!/^https?:\/\//i.test(url)) url = `http://${url}`
  if (url.toLowerCase().endsWith(API_PATH)) url = url.slice(0, -API_PATH.length)
  return url
}

export function apiBaseUrl(server: string): string {
  return `${server}${API_PATH}`
}
