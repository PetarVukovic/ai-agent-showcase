import {writeFileSync} from 'node:fs';
import {generateSystemPrompt} from '@openuidev/lang-core';
import {library} from './src/openui';
const schema=library.toJSONSchema();
const spec={schema,root:'BriefPanel'};
writeFileSync('src/openui.spec.json',JSON.stringify(spec,null,2));
writeFileSync('../backend/ops/openui-prompt.txt',generateSystemPrompt(library.toSpec()));
console.log('Generated prompt from the actual typed OpenUI component catalog');
