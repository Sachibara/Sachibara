# Next.js Operations Portal

Next.js App Router / TypeScript companion to the Node Operations API. Server components fetch incident data with caching disabled, the client handles forms, and a same-origin route handler stores the API session in an HttpOnly cookie. Includes account creation, login, incident creation/listing, logout and an error boundary.

## Run
Start `../node-operations-platform` first. Install Node 22.18+:
```sh
npm install
npm run dev
```
Open **http://localhost:3000**. `NODE_API_URL` defaults to `http://127.0.0.1:5081`; it is server-only. `PORTAL_ORIGIN` defaults to `http://localhost:3000` and must exactly match the browser origin (including port). If you use `127.0.0.1:3000`, set it accordingly. `npm run build` checks the Next.js application. Production cookie transport requires HTTPS.

This companion focuses on Next.js server/client boundaries; the React Vite application supplies incident editing/deletion and administrator audit views. Both use the same API and database. No hosted deployment is implied.
