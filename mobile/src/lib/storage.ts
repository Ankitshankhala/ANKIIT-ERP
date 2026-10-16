import { Platform } from 'react-native'
import * as SecureStore from 'expo-secure-store'

// Tokens live in the iOS Keychain / Android Keystore via SecureStore. SecureStore has
// no web implementation, so the browser preview falls back to localStorage.
const isWeb = Platform.OS === 'web'

export async function getItem(key: string): Promise<string | null> {
  if (isWeb) {
    try {
      return globalThis.localStorage?.getItem(key) ?? null
    } catch {
      return null
    }
  }
  return SecureStore.getItemAsync(key)
}

export async function setItem(key: string, value: string): Promise<void> {
  if (isWeb) {
    try {
      globalThis.localStorage?.setItem(key, value)
    } catch {
      // Private mode / blocked storage: the session just won't survive a reload
    }
    return
  }
  await SecureStore.setItemAsync(key, value)
}

export async function deleteItem(key: string): Promise<void> {
  if (isWeb) {
    try {
      globalThis.localStorage?.removeItem(key)
    } catch {
      // Nothing to remove
    }
    return
  }
  await SecureStore.deleteItemAsync(key)
}
