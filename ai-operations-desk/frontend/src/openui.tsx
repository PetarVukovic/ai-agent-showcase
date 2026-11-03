import {createLibrary, defineComponent} from '@openuidev/react-lang';
import {z} from 'zod';
const Brief=defineComponent({name:'Brief',description:'A short factual business summary of the current quote. No invented facts.',props:z.object({title:z.string(),body:z.string()}),component:({props})=><div className="ai-brief"><h3>{props.title}</h3><p>{props.body}</p></div>});
const Notice=defineComponent({name:'Notice',description:'A brief constraint or next step. Use neutral for demo disclosure, warning for a real policy issue.',props:z.object({text:z.string(),tone:z.enum(['neutral','warning'])}),component:({props})=><div className={'ai-notice '+props.tone}><span aria-hidden="true">{props.tone==='warning'?'!':'i'}</span><p>{props.text}</p></div>});
const BriefPanel=defineComponent({name:'BriefPanel',description:'Root container for a quote explanation.',props:z.object({children:z.array(z.union([Brief.ref,Notice.ref]))}),component:({props,renderNode})=><div>{renderNode(props.children)}</div>});
export const library=createLibrary({id:'operations-desk',root:'BriefPanel',components:[BriefPanel,Brief,Notice]});
