export type Language="en"|"hr";
export type Service={id:string;name:string;name_hr:string;price:number;days:number};
export type Doc={title:string;title_hr?:string;pages:{page:number;text:string}[];extraction?:string};
export type Requirement={title:string;quote:string;page:number;service_id:string|null;status:"supported"|"partial"|"missing";reason:string};
export type Result={document:Doc;requirements:Requirement[];questions:string[];selected_services:Service[];total:number;days:number;summary:string;proposal_markdown:string;proposal_id:string;evidence_rejected:number;mode:"demo"|"openai"|"gemini";excluded_services?:string[]};
export type Config={gemini_configured:boolean;gemini_model:string;openai_configured:boolean;model:string;services:Service[];samples:Record<string,Doc>};
