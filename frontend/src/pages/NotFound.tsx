import {Link} from 'react-router-dom'; export function NotFound(){return <div className="grid min-h-screen place-items-center p-6 text-center"><div><p className="text-6xl font-bold text-blue-600">404</p><h1 className="mt-4 text-2xl font-bold">Page not found</h1><Link className="btn-primary mt-6 inline-block" to="/dashboard">Return to dashboard</Link></div></div>}

