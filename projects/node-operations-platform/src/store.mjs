import {DatabaseSync} from 'node:sqlite';
import {mkdirSync} from 'node:fs';import {dirname} from 'node:path';
const schema=`CREATE TABLE IF NOT EXISTS users(id TEXT PRIMARY KEY,email TEXT UNIQUE NOT NULL,password TEXT NOT NULL,role TEXT NOT NULL CHECK(role IN ('admin','operator')));
CREATE TABLE IF NOT EXISTS sessions(token TEXT PRIMARY KEY,user_id TEXT NOT NULL REFERENCES users(id),expires TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS incidents(id TEXT PRIMARY KEY,owner_id TEXT NOT NULL REFERENCES users(id),title TEXT NOT NULL,priority TEXT NOT NULL,status TEXT NOT NULL,version INTEGER NOT NULL DEFAULT 1,created TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS audit(id TEXT PRIMARY KEY,user_id TEXT NOT NULL,action TEXT NOT NULL,target TEXT NOT NULL,created TEXT NOT NULL);`;
export async function openStore({path='data/operations.sqlite',url=process.env.DATABASE_URL}={}){
 if(url){
  const {Pool}=await import('pg');const pool=new Pool({connectionString:url});await pool.query(schema);
  const sql=(text)=>{let i=0;return text.replace(/\?/g,()=>'$'+(++i));};
  return {kind:'PostgreSQL',async query(text,args=[]){return (await pool.query(sql(text),args)).rows;},async mutate(text,args,audit){const c=await pool.connect();try{await c.query('BEGIN');const rows=(await c.query(sql(text),args)).rows;if(rows.length)await c.query('INSERT INTO audit VALUES ($1,$2,$3,$4,$5)',audit);await c.query('COMMIT');return rows;}catch(e){await c.query('ROLLBACK');throw e;}finally{c.release();}},async close(){await pool.end();}};
 }
 mkdirSync(dirname(path),{recursive:true});const db=new DatabaseSync(path);db.exec('PRAGMA foreign_keys=ON; PRAGMA journal_mode=WAL; PRAGMA busy_timeout=5000;'+schema);
 return {kind:'SQLite',async query(text,args=[]){return db.prepare(text).all(...args);},async mutate(text,args,audit){db.exec('BEGIN IMMEDIATE');try{const rows=db.prepare(text).all(...args);if(rows.length)db.prepare('INSERT INTO audit VALUES (?,?,?,?,?)').run(...audit);db.exec('COMMIT');return rows;}catch(e){db.exec('ROLLBACK');throw e;}},async close(){db.close();}};
}
