# ANKIIT ERP Mobile

The Android and iOS app for ANKIIT ERP, built with Expo (SDK 58, React Native, TypeScript,
Expo Router). It talks to the same FastAPI backend as the web app, so the same users,
organizations and permissions apply.

## What it does

| Tab | Shows |
| --- | --- |
| Home | Cash, net income, receivables and payables, record counts and the latest invoices |
| Customers | Searchable customer list with pull-to-refresh and infinite scroll; **+** adds a customer |
| Products | Searchable product list with SKU, category and price |
| Employees | Searchable employee list with title, department and status |
| Profile | Signed-in user, role, organization and server; sign out |

- Tokens are stored in the iOS Keychain / Android Keystore (`expo-secure-store`), and the
  access token is refreshed automatically when it expires.
- Every screen respects the backend's permissions: a module the user's role can't open
  shows "No access" instead of an error, and the **+** button only appears for users who
  can create customers.
- Data is always the signed-in user's organization (the backend enforces this).

## Run it on your phone

1. Install **Expo Go** from the App Store or Google Play.
2. Start the backend so other devices on your network can reach it (from `backend/`):

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

   On Windows, allow Python through the firewall for private networks when asked.
3. Start the app (from `mobile/`):

   ```bash
   npm install
   npx expo start
   ```

4. Scan the QR code with the camera (iOS) or Expo Go (Android). The phone must be on the
   same Wi-Fi as your computer.
5. Sign in with a web-app account, e.g. the dev admin from `config.env.example`.

The app guesses the server from the address the phone loaded the app from
(`http://<your-computer-ip>:8000`). If that's wrong, tap **Server** on the sign-in screen
and enter the address, or set `EXPO_PUBLIC_API_URL` before `npx expo start`:

```bash
EXPO_PUBLIC_API_URL=http://192.168.1.20:8000 npx expo start
```

## Preview in a browser

```bash
npx expo start --web
```

Opens on http://localhost:8081 and uses the API at http://localhost:8000. That origin is
already in `ALLOWED_ORIGINS` in `config.env.example`; restart the backend after changing
`.env`. In the browser preview, tokens are kept in `localStorage` because SecureStore is
native-only.

## Checks

```bash
npm run type-check   # tsc --noEmit
npm run lint         # expo lint
npx expo-doctor      # dependency and config health
npx expo export --platform android --platform ios   # production bundles
```

## Building store apps

Use EAS Build (`npx eas-cli@latest build`); no local Xcode or Android Studio is needed.
The app IDs are `com.ankiit.erp` on both platforms (`app.json`). Release builds should talk
to an **HTTPS** API: plain `http://` works in Expo Go for development, but iOS and Android
block cleartext traffic in release builds by default.

## Project layout

```
src/
  app/                  Screens (Expo Router: every file is a route)
    _layout.tsx         Auth gate: tabs when signed in, login otherwise
    login.tsx
    (tabs)/             Home, Customers, Products, Employees, Profile
    customers/new.tsx   New customer form (modal)
  components/           Buttons, fields, list rows, list screen, status views
  lib/
    api.ts              fetch client: bearer token, refresh on 401, readable errors
    auth.tsx            Session restore, sign in/out, permission check
    server.ts           Default server address and URL normalization
    storage.ts          SecureStore with a localStorage fallback on web
    usePagedList.ts     Search + paging for the API's list endpoints
  theme.ts              Colors and spacing (matches the web app)
```
