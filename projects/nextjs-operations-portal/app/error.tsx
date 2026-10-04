'use client';
export default function ErrorPage({reset}:{reset:()=>void}){return <main><h1>Unable to load the portal</h1><p>Check the API connection and retry.</p><button onClick={reset}>Retry</button></main>;}
