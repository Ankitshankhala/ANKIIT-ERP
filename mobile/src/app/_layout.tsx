import { SplashScreen, Stack } from 'expo-router'
import { StatusBar } from 'expo-status-bar'
import { SafeAreaProvider } from 'react-native-safe-area-context'

import { AuthProvider, useAuth } from '@/lib/auth'
import { colors } from '@/theme'

// Keep the native splash screen up until the saved session has been checked
SplashScreen.preventAutoHideAsync()

export default function RootLayout() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <SplashScreenController />
        <RootNavigator />
      </AuthProvider>
      <StatusBar style="dark" />
    </SafeAreaProvider>
  )
}

function SplashScreenController() {
  const { isRestoring } = useAuth()
  if (!isRestoring) SplashScreen.hide()
  return null
}

function RootNavigator() {
  const { user, isRestoring } = useAuth()
  const signedIn = !!user

  // Mounting the guards before the saved session is known would bounce a deep link
  // (or a web refresh on /crm) to the login screen and lose it; the splash covers this
  if (isRestoring) return null

  return (
    <Stack
      screenOptions={{
        headerShown: false,
        contentStyle: { backgroundColor: colors.background },
        headerTintColor: colors.primary,
      }}
    >
      <Stack.Protected guard={signedIn}>
        <Stack.Screen name="(tabs)" />
        <Stack.Screen
          name="customers/new"
          options={{ presentation: 'modal', headerShown: true, title: 'New customer' }}
        />
      </Stack.Protected>
      <Stack.Protected guard={!signedIn}>
        <Stack.Screen name="login" />
      </Stack.Protected>
    </Stack>
  )
}
