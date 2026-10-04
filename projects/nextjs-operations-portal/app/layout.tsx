import type {Metadata} from 'next';import './style.css';
export const metadata:Metadata={title:'Operations Portal · Sachibara',description:'Server-rendered incident operations portal.'};
export default function Layout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>;}
