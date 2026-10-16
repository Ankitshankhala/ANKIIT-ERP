import Ionicons from '@expo/vector-icons/Ionicons'
import { Tabs, type BottomTabNavigationOptions } from 'expo-router/js-tabs'
import type { ComponentProps } from 'react'

import { colors } from '@/theme'

type IconName = ComponentProps<typeof Ionicons>['name']

type TabBarIconProps = Parameters<NonNullable<BottomTabNavigationOptions['tabBarIcon']>>[0]

function tabIcon(name: IconName): BottomTabNavigationOptions['tabBarIcon'] {
  function TabBarIcon({ color, size }: TabBarIconProps) {
    // The tab bar passes our string tint colors; Ionicons can't take a processed (numeric) color
    return <Ionicons name={name} color={typeof color === 'number' || color == null ? undefined : color} size={size} />
  }
  return TabBarIcon
}

export default function TabsLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.textMuted,
        headerTitleStyle: { color: colors.text, fontWeight: '600' },
        sceneStyle: { backgroundColor: colors.background },
      }}
    >
      <Tabs.Screen name="index" options={{ title: 'Home', tabBarIcon: tabIcon('home-outline') }} />
      <Tabs.Screen name="crm" options={{ title: 'Customers', tabBarIcon: tabIcon('people-outline') }} />
      <Tabs.Screen name="inventory" options={{ title: 'Products', tabBarIcon: tabIcon('cube-outline') }} />
      <Tabs.Screen name="hr" options={{ title: 'Employees', tabBarIcon: tabIcon('id-card-outline') }} />
      <Tabs.Screen name="profile" options={{ title: 'Profile', tabBarIcon: tabIcon('person-circle-outline') }} />
    </Tabs>
  )
}
