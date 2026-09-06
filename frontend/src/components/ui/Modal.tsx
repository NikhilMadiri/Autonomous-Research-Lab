import type {ReactNode} from 'react';
export function Modal({open,onClose,title,children}:{open:boolean;onClose:()=>void;title:string;children:ReactNode}){if(!open)return null;return <div className="fixed inset-0 z-50 grid place-items-center bg-slate-950/50 p-4"><div className="card w-full max-w-lg"><div className="mb-5 flex items-center justify-between"><h2 className="text-lg font-bold">{title}</h2><button onClick={onClose} className="text-slate-400">✕</button></div>{children}</div></div>}

