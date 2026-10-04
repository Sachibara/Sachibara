import http from 'node:http';import {randomUUID,randomBytes} from 'node:crypto';import {readFileSync} from 'node:fs';import {fileURLToPath} from 'node:url';
import {openStore} from './store.mjs';import {hashPassword,verifyPassword,hashToken,credentials,incident} from './auth.mjs';
export async function createServer({store,adminEmail='admin@local.test',adminPassword}={}){
 store=store||await openStore();let bootstrap=null;
 if(!(await store.query("SELECT id FROM users WHERE role='admin' LIMIT 1")).length){const password=adminPassword||randomBytes(24).toString('base64url');const c=credentials({email:adminEmail,password});await store.query('INSERT INTO users VALUES (?,?,?,?)',[randomUUID(),c.email,await hashPassword(c.password),'admin']);bootstrap={email:c.email,password};}
 const attempts=new Map();
 const server=http.createServer(async(req,res)=>{
  const send=(code,body)=>{res.writeHead(code,{'Content-Type':'application/json','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});res.end(JSON.stringify(body));};
  const url=new URL(req.url,'http://localhost'),path=url.pathname;
  if(req.method==='GET'&&path==='/api/health')return send(200,{status:'ok',database:store.kind});
  if(req.method==='GET'&&path==='/'){res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Content-Security-Policy':"default-src 'none'; style-src 'unsafe-inline'; base-uri 'none'; frame-ancestors 'none'"});return res.end(readFileSync(new URL('../public/index.html',import.meta.url)));}
  try{
   let body={};if(['POST','PATCH'].includes(req.method)){
    if(req.headers['content-type']?.split(';')[0]!=='application/json')return send(415,{error:'Use application/json.'});
    let text='';for await(const chunk of req){text+=chunk;if(Buffer.byteLength(text)>65536)return send(413,{error:'Payload too large.'});}
    try{body=JSON.parse(text||'{}');}catch{return send(400,{error:'Invalid JSON.'});}
    if(!body||typeof body!=='object'||Array.isArray(body))return send(400,{error:'JSON object required.'});
   }
   if(req.method==='POST'&&['/api/auth/login','/api/auth/register'].includes(path)){
    const ip=req.socket.remoteAddress;const now=Date.now();let rate=attempts.get(ip);if(!rate||now-rate.start>900000){if(attempts.size>1024)attempts.clear();rate={start:now,count:0};attempts.set(ip,rate);}if(++rate.count>20)return send(429,{error:'Too many authentication attempts. Try again in 15 minutes.'});
    let c;try{c=credentials(body);}catch(e){return send(400,{error:e.message});}
    if(path.endsWith('register')){try{await store.query('INSERT INTO users VALUES (?,?,?,?)',[randomUUID(),c.email,await hashPassword(c.password),'operator']);return send(201,{message:'Account created. Sign in.'});}catch(e){if(e.code==='23505'||e.message?.includes('UNIQUE'))return send(409,{error:'Email is already registered.'});throw e;}}
    const user=(await store.query('SELECT * FROM users WHERE email=?',[c.email]))[0];if(!user||!await verifyPassword(c.password,user.password))return send(401,{error:'Invalid credentials.'});
    const token=randomBytes(32).toString('base64url');await store.query('DELETE FROM sessions WHERE expires<=?',[new Date().toISOString()]);await store.query('INSERT INTO sessions VALUES (?,?,?)',[hashToken(token),user.id,new Date(Date.now()+43200000).toISOString()]);return send(200,{token,user:{id:user.id,email:user.email,role:user.role}});
   }
   const token=req.headers.authorization?.startsWith('Bearer ')?req.headers.authorization.slice(7):'';
   const user=(await store.query('SELECT users.id,email,role FROM sessions JOIN users ON users.id=sessions.user_id WHERE token=? AND expires>?',[hashToken(token),new Date().toISOString()]))[0];if(!user)return send(401,{error:'Sign in required.'});
   if(req.method==='POST'&&path==='/api/auth/logout'){await store.query('DELETE FROM sessions WHERE token=?',[hashToken(token)]);return send(200,{ok:true});}
   if(req.method==='GET'&&path==='/api/auth/me')return send(200,{user});
   if(req.method==='GET'&&path==='/api/audit'){if(user.role!=='admin')return send(403,{error:'Administrator role required.'});return send(200,{events:await store.query('SELECT action,target,created,email FROM audit JOIN users ON users.id=audit.user_id ORDER BY created DESC LIMIT 200')});}
   if(req.method==='GET'&&path==='/api/incidents'){return send(200,{incidents:await store.query('SELECT * FROM incidents'+(user.role==='admin'?'':' WHERE owner_id=?')+' ORDER BY created DESC LIMIT 500',user.role==='admin'?[]:[user.id])});}
   if(req.method==='POST'&&path==='/api/incidents'){
    let input;try{input=incident(body);}catch(e){return send(400,{error:e.message});}
    const id=randomUUID(),now=new Date().toISOString();const rows=await store.mutate('INSERT INTO incidents(id,owner_id,title,priority,status,created) VALUES (?,?,?,?,?,?) RETURNING *',[id,user.id,input.title,input.priority,input.status,now],[randomUUID(),user.id,'incident.created',id,now]);return send(201,rows[0]);
   }
   const match=path.match(/^\/api\/incidents\/([a-f0-9-]{36})$/);
   if(match&&['PATCH','DELETE'].includes(req.method)){
    const existing=(await store.query('SELECT * FROM incidents WHERE id=?',[match[1]]))[0];if(!existing||(user.role!=='admin'&&existing.owner_id!==user.id))return send(404,{error:'Incident not found.'});
    const version=req.method==='DELETE'?Number(req.headers['if-match']):body.version;if(!Number.isInteger(version)||version<1)return send(400,{error:'Current record version is required.'});
    let query,args,action;
    if(req.method==='PATCH'){let input;try{input=incident(body);}catch(e){return send(400,{error:e.message});}query='UPDATE incidents SET title=?,priority=?,status=?,version=version+1 WHERE id=? AND version=? RETURNING *';args=[input.title,input.priority,input.status,existing.id,version];action='incident.updated';}
    else{query='DELETE FROM incidents WHERE id=? AND version=? RETURNING *';args=[existing.id,version];action='incident.deleted';}
    const rows=await store.mutate(query,args,[randomUUID(),user.id,action,existing.id,new Date().toISOString()]);return rows.length?send(200,req.method==='DELETE'?{ok:true}:rows[0]):send(409,{error:'Record changed. Refresh before retrying.'});
   }
   return send(404,{error:'Unknown route.'});
  }catch(e){console.error('Request failed:',e.code||e.name);if(!res.headersSent)send(500,{error:'Internal server error.'});}
 });return {server,store,bootstrap};
}
if(process.argv[1]===fileURLToPath(import.meta.url)){
 const {server,bootstrap}=await createServer({adminEmail:process.env.ADMIN_EMAIL||'admin@local.test',adminPassword:process.env.ADMIN_PASSWORD});
 server.listen(Number(process.env.PORT||5081),process.env.HOST||'127.0.0.1',()=>{console.log('Operations API ready on port '+(process.env.PORT||5081));if(bootstrap)console.log('Initial administrator:',bootstrap);});
}
