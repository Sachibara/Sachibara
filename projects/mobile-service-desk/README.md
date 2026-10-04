# Service Desk Mobile

React Native + Expo + TypeScript mobile client for `node-operations-platform`. Sign-in, native encrypted session storage, create incidents, refresh the list, advance/reopen status and revoke the session on sign-out. The API enforces ownership and optimistic version checks; mobile does not duplicate authorization logic.

## Run
Install Node 22+ and the dependencies:
```sh
npm install
npx expo install --fix
npm run check
npm start
```
Set `EXPO_PUBLIC_API_URL` before starting to your reachable API base URL, without `/api`. For an Android emulator using a host API, this is commonly `http://10.0.2.2:5081`; a physical phone requires a reachable server address. Use HTTPS for remote access. `127.0.0.1` on a phone means the phone itself. Configure the API bind address intentionally if testing on your LAN; default API binding is local-only.

SDK 54 is pinned as the target. Use a matching Expo Go/development build; current store Expo Go may target a newer SDK. This repository contains source, not a built APK/IPA. Create an account in the React web client first, then sign in on mobile. Native builds and device checks require Android/iOS tooling and are unverified in the authoring environment. SecureStore targets Android/iOS; a browser build is not the supported demo.

No offline mutation queue or push notifications are claimed. Network failures are shown and updates can be retried manually; stale versions require Refresh.
