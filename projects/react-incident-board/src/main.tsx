import React, {useEffect,useState} from 'react';
import {createRoot} from 'react-dom/client';
import {parseIncidents,statuses,transition,type Incident,type Priority} from './model.ts';
import './style.css';
const key='sachibara-incidents-v1';
const seed:Incident[]=[{id:'demo-1',title:'Branch switch uplink intermittent',priority:'High',status:'New',created:new Date().toISOString()},{id:'demo-2',title:'Review endpoint patch compliance',priority:'Medium',status:'Investigating',created:new Date().toISOString()}];
function App(){
  const [items,setItems]=useState<Incident[]>(()=>{try {const raw=localStorage.getItem(key);return raw?parseIncidents(raw):seed;}catch{return seed;}});
  const [title,setTitle]=useState(''),[priority,setPriority]=useState<Priority>('Medium'),[query,setQuery]=useState(''),[error,setError]=useState('');
  useEffect(()=>{try{localStorage.setItem(key,JSON.stringify(items));}catch{setError('Storage unavailable. Export your incidents before closing this tab.');}},[items]);
  function add(e:React.FormEvent){e.preventDefault();if(!title.trim())return;if(items.length>=500){setError('The board is limited to 500 incidents.');return;}setItems([...items,{id:crypto.randomUUID(),title:title.trim(),priority,status:'New',created:new Date().toISOString()}]);setTitle('');}
  function download(){const url=URL.createObjectURL(new Blob([JSON.stringify(items,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='incidents.json';a.click();URL.revokeObjectURL(url);}
  async function upload(file?:File){if(!file)return;try{if(file.size>1024*1024)throw new Error('Import must be smaller than 1 MB.');const next=parseIncidents(await file.text());if(confirm('Replace the current board with this import?'))setItems(next);setError('');}catch(e){setError(e instanceof Error?e.message:'Import failed.');}}
  return <main><header><div><span className="eyebrow">Sachibara / Frontend lab</span><h1>Incident command board</h1><p className="muted">Triage, investigate, resolve. Your board stays on this device.</p></div><button onClick={download}>Export JSON</button></header>
  {error&&<p className="error" role="alert">{error}</p>}
  <section className="grid" aria-label="Incident totals">{statuses.map(s=><div className="card" key={s}><span className="muted">{s}</span><div className="stat">{items.filter(i=>i.status===s).length}</div></div>)}</section>
  <form className="inline" onSubmit={add}><label>Incident title<br/><input required maxLength={120} value={title} onChange={e=>setTitle(e.target.value)} placeholder="Describe the issue"/></label><label>Priority<br/><select value={priority} onChange={e=>setPriority(e.target.value as Priority)}>{['High','Medium','Low'].map(p=><option key={p}>{p}</option>)}</select></label><button>Add incident</button></form>
  <div className="toolbar"><label>Search<br/><input value={query} onChange={e=>setQuery(e.target.value)} placeholder="Filter incidents"/></label><label>Import backup<br/><input type="file" accept=".json,application/json" onChange={e=>{void upload(e.target.files?.[0]);e.target.value='';}}/></label></div>
  <section className="grid">{statuses.map(status=><section key={status} aria-label={status}><h2>{status}</h2><div className="stack">{items.filter(i=>i.status===status&&i.title.toLowerCase().includes(query.toLowerCase())).map(i=><article className="card" key={i.id}><span className="badge">{i.priority}</span><h3>{i.title}</h3><p className="muted">{new Date(i.created).toLocaleDateString()}</p><label>Move incident<br/><select value={i.status} onChange={e=>setItems(transition(items,i.id,e.target.value as Incident['status']))}>{statuses.map(s=><option key={s}>{s}</option>)}</select></label><p><button className="danger" onClick={()=>{if(confirm('Delete this incident?'))setItems(items.filter(x=>x.id!==i.id));}}>Delete</button></p></article>)}{!items.some(i=>i.status===status&&i.title.toLowerCase().includes(query.toLowerCase()))&&<p className="muted">No matching incidents.</p>}</div></section>)}</section>
  <footer>Local portfolio demo · React + TypeScript · No account or cloud sync</footer></main>;
}
createRoot(document.getElementById('root')!).render(<React.StrictMode><App/></React.StrictMode>);
