import os
from fastapi import FastAPI
from ops.graph import catalog, google_key
app=FastAPI(title='AI Operations Desk demo')
@app.get('/ops/config')
def config():
 return {'openai_available':bool(os.getenv('OPENAI_API_KEY')),'model':os.getenv('OPENAI_MODEL','gpt-4.1-mini'),'gemini_available':bool(google_key()),'gemini_model':os.getenv('GEMINI_MODEL','gemini-3.5-flash-lite'),'demo_data':True}
@app.get('/ops/catalog')
def products(): return catalog()
