import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
export default defineConfig({plugins:[{name:'static-about-pages',configureServer(server){server.middlewares.use((req,_res,next)=>{if(req.url==='/about/'||req.url==='/hr/about/')req.url+='index.html';next()})}},react()],server:{proxy:{'/api':{target:'http://127.0.0.1:2024',changeOrigin:true,rewrite:p=>p.replace(/^\/api/,'')}}}});
