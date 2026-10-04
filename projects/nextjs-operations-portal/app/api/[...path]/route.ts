import {NextRequest,NextResponse} from 'next/server';import {cookies} from 'next/headers';import {backend} from '../../../lib/api';
export const runtime='nodejs';
export async function POST(request:NextRequest,{params}:{params:Promise<{path:string[]}>}){
 const path='/'+(await params).path.join('/');const allowed=['/auth/login','/auth/register','/auth/logout','/incidents'];if(!allowed.includes(path))return NextResponse.json({error:'Unknown route'},{status:404});
 const origin=process.env.PORTAL_ORIGIN||'http://localhost:3000';if(request.headers.get('origin')!==origin)return NextResponse.json({error:'Origin not allowed. Configure PORTAL_ORIGIN to match the browser URL.'},{status:403});
 if(request.headers.get('content-type')?.split(';')[0]!=='application/json')return NextResponse.json({error:'Use JSON'},{status:415});
 if(Number(request.headers.get('content-length')||0)>65536)return NextResponse.json({error:'Payload too large'},{status:413});
 const body=await request.text();if(Buffer.byteLength(body)>65536)return NextResponse.json({error:'Payload too large'},{status:413});
 try{JSON.parse(body||'{}');}catch{return NextResponse.json({error:'Invalid JSON'},{status:400});}
 try{const token=(await cookies()).get('ops_session')?.value;const result=await backend(path,token,'POST',body);const data=await result.json();const response=NextResponse.json(path==='/auth/login'&&result.ok?{user:data.user}:data,{status:result.status});if(path==='/auth/login'&&result.ok)response.cookies.set('ops_session',data.token,{httpOnly:true,sameSite:'strict',secure:process.env.NODE_ENV==='production',path:'/',maxAge:43200});if(path==='/auth/logout')response.cookies.delete('ops_session');return response;}catch{return NextResponse.json({error:'Operations API unavailable'},{status:502});}
}
