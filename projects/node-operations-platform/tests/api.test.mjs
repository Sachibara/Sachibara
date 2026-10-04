import test from 'node:test';import assert from 'node:assert/strict';import {mkdtemp,rm} from 'node:fs/promises';import {tmpdir} from 'node:os';import {join} from 'node:path';import {createServer} from '../src/server.mjs';import {openStore} from '../src/store.mjs';
test('account isolation, role checks, concurrency and durable audit trail',async()=>{
 const dir=await mkdtemp(join(tmpdir(),'operations-'));const store=await openStore({path:join(dir,'test.sqlite'),url:''});const {server}=await createServer({store,adminPassword:'test-admin-password-123'});await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));const base='http://127.0.0.1:'+server.address().port;
 async function call(path,method='GET',body,token='',version){const response=await fetch(base+'/api'+path,{method,headers:{'Content-Type':'application/json',Authorization:'Bearer '+token,...(version?{'If-Match':String(version)}:{})},body:body?JSON.stringify(body):undefined});return [response.status,await response.json()];}
 try{
  assert.equal((await call('/incidents'))[0],401);
  for(const email of ['alice@example.test','bob@example.test'])assert.equal((await call('/auth/register','POST',{email,password:'test-password-123'}))[0],201);
  assert.equal((await call('/auth/register','POST',{email:'ALICE@example.test',password:'test-password-123'}))[0],409);
  const alice=(await call('/auth/login','POST',{email:'alice@example.test',password:'test-password-123'}))[1].token;const bob=(await call('/auth/login','POST',{email:'bob@example.test',password:'test-password-123'}))[1].token;const admin=(await call('/auth/login','POST',{email:'admin@local.test',password:'test-admin-password-123'}))[1].token;
  const payload={title:'Uplink outage',priority:'High',status:'New'};const [code,row]=await call('/incidents','POST',payload,alice);assert.equal(code,201);
  assert.equal((await call('/incidents','GET',undefined,bob))[1].incidents.length,0);assert.equal((await call('/incidents/'+row.id,'PATCH',{...payload,status:'Resolved',version:1},bob))[0],404);
  assert.equal((await call('/incidents/'+row.id,'PATCH',{...payload,status:'Resolved',version:1},alice))[0],200);assert.equal((await call('/incidents/'+row.id,'PATCH',{...payload,version:1},alice))[0],409);
  assert.equal((await call('/audit','GET',undefined,alice))[0],403);assert.equal((await call('/audit','GET',undefined,admin))[1].events.length,2);
  assert.equal((await call('/incidents/'+row.id,'DELETE',undefined,alice,1))[0],409);assert.equal((await call('/incidents/'+row.id,'DELETE',undefined,alice,2))[0],200);
  await call('/auth/logout','POST',{},alice);assert.equal((await call('/incidents','GET',undefined,alice))[0],401);
 }finally{await new Promise(resolve=>server.close(resolve));await store.close();await rm(dir,{recursive:true,force:true});}
});
