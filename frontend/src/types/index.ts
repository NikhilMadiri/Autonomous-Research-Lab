export type ProjectStatus='draft'|'active'|'archived'; export type QuestionStatus='open'|'in_progress'|'answered'|'archived';
export interface Project {id:string; name:string; description?:string; status:ProjectStatus; owner_id?:string; created_at:string; updated_at:string}
export interface Question {id:string; project_id:string; title:string; description?:string; status:QuestionStatus; created_at:string; updated_at:string}
export interface Page<T>{items:T[];total:number;page:number;page_size:number}

