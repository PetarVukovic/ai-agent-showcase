import assert from "node:assert/strict";
import {createParser,createStreamingParser} from "@openuidev/react-lang";
import {library,buildReviewProgram} from "./src/openui";
import type {Result} from "./src/types";
const data={requirements:[{title:'API "integration"',status:"supported",service_id:"integration",reason:"Verified catalogue match.",quote:'Exact source quote, with \"quotes\" and a newline\ninside.',page:1}],questions:["Who approves scope?"],excluded_services:[]} as unknown as Result;
const parser=createParser(library.toJSONSchema());
for(const lang of ["en","hr"] as const)for(const tab of ["requirements","questions"] as const){const code=buildReviewProgram(data,lang,tab);const result=parser.parse(code);assert.equal(result.meta.errors.length,0,JSON.stringify(result.meta.errors));const stream=createStreamingParser(library.toJSONSchema());for(let i=1;i<code.length;i+=17)stream.set(code.slice(0,i));assert.equal(stream.set(code,true).meta.errors.length,0);}
const malformed=parser.parse('root = UnsupportedCard("bad")');assert.ok(malformed.meta.errors.length>0);
const excluded=parser.parse(buildReviewProgram({...data,excluded_services:["integration"]},"en","requirements"));assert.equal(excluded.meta.errors.length,0);
console.log("OpenUI contract: EN/HR requirements/questions, partial streams, excluded scope and malformed output checks passed");
