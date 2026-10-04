import {randomBytes,scrypt,timingSafeEqual,createHash} from 'node:crypto';
import {promisify} from 'node:util';
const derive=promisify(scrypt);
export async function hashPassword(password){const salt=randomBytes(16).toString('hex');const key=await derive(password,salt,64);return salt+':'+key.toString('hex');}
export async function verifyPassword(password,stored){const [salt,encoded]=stored.split(':');const expected=Buffer.from(encoded,'hex');const actual=await derive(password,salt,64);return actual.length===expected.length&&timingSafeEqual(actual,expected);}
export const hashToken=token=>createHash('sha256').update(token).digest('hex');
export function credentials(body){if(typeof body.email!=='string'||typeof body.password!=='string')throw Error('Email and password required.');const email=body.email.trim().toLowerCase();if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)||email.length>254||body.password.length<12||body.password.length>128)throw Error('Use a valid email and a password of 12–128 characters.');return {email,password:body.password};}
export function incident(body){if(typeof body.title!=='string'||!body.title.trim()||body.title.trim().length>120)throw Error('Title must contain 1–120 characters.');if(!['High','Medium','Low'].includes(body.priority)||!['New','Investigating','Resolved'].includes(body.status))throw Error('Invalid priority or status.');return {title:body.title.trim(),priority:body.priority,status:body.status};}
