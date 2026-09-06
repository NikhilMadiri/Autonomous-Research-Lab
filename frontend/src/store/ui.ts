import {create} from 'zustand';
interface UIState{dark:boolean;toggle:()=>void}
export const useUIStore=create<UIState>((set)=>({dark:false,toggle:()=>set(s=>({dark:!s.dark}))}));

