import {defineConfig,type Plugin} from "vite";
import react from "@vitejs/plugin-react";
import type {IncomingMessage,ServerResponse} from "node:http";
function staticAbout():Plugin {
 const middleware=(req:IncomingMessage,_res:ServerResponse,next:()=>void)=>{
  const [path,query]= (req.url||"/").split("?");
  if(path==="/about/"||path==="/hr/about/")req.url=path+"index.html"+(query?"?"+query:"");
  next();
 };
 return {name:"static-about-directory-index",configureServer(server){server.middlewares.use(middleware);},configurePreviewServer(server){server.middlewares.use(middleware);}};
}
export default defineConfig({plugins:[staticAbout(),react()],server:{proxy:{"/api":"http://127.0.0.1:2025","/threads":"http://127.0.0.1:2025"}},preview:{host:"127.0.0.1",port:5175,proxy:{"/api":"http://127.0.0.1:2025","/threads":"http://127.0.0.1:2025"}}});
