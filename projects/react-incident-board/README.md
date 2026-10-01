# Incident Command Board

React / ReactJS + TypeScript frontend: create incidents, prioritize, search, move between three workflow states, delete with confirmation, and import/export validated JSON backups. Browser localStorage persists the board. Responsive layout and labelled keyboard-accessible controls.

## Run
Node.js 22.18+ (or 24) and npm:
```sh
npm install
npm run dev
```
Open the URL printed by Vite. `npm run build` checks TypeScript and creates `dist/`; `npm test` checks import validation and immutable transitions using Node's native TypeScript support.

## Showcase
Add a high-priority network incident, move it to Investigating, refresh, export, delete, and re-import. Show a rejected malformed backup. This is a personal local board; records are not shared between devices. Import replaces the board only after confirmation. Maximum 500 incidents, 1 MB import. No backend or authentication is implied.
