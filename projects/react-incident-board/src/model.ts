export type Status = 'New' | 'Investigating' | 'Resolved';
export type Priority = 'High' | 'Medium' | 'Low';
export interface Incident { id:string; title:string; priority:Priority; status:Status; created:string }
export const statuses:Status[] = ['New','Investigating','Resolved'];
export function validIncident(x:unknown):x is Incident {
  if (!x || typeof x !== 'object') return false;
  const v=x as Record<string,unknown>;
  return typeof v.id==='string' && v.id.length>0 && typeof v.title==='string' && v.title.trim().length>0 && v.title.length<=120 &&
    ['High','Medium','Low'].includes(String(v.priority)) && statuses.includes(v.status as Status) && typeof v.created==='string' && !Number.isNaN(Date.parse(v.created));
}
export function parseIncidents(raw:string):Incident[] {
  const values:unknown=JSON.parse(raw);
  if (!Array.isArray(values) || values.length>500 || !values.every(validIncident) || new Set(values.map(v=>v.id)).size!==values.length) throw new Error('Import must contain up to 500 valid incidents with unique IDs.');
  return values;
}
export function transition(items:Incident[],id:string,status:Status):Incident[] {
  if (!statuses.includes(status)) throw new Error('Invalid status');
  return items.map(item=>item.id===id ? {...item,status} : item);
}
