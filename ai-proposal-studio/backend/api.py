import os
import pymupdf
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from backend.catalog import SERVICES, SAMPLES
from backend.store import put, get
from backend.provider import google_key
app=FastAPI(title="AI Proposal Studio")
@app.get("/api/config")
def config():
 return {"gemini_configured":bool(google_key()),"gemini_model":os.getenv("GEMINI_MODEL","gemini-3.5-flash-lite"),"openai_configured":bool(os.getenv("OPENAI_API_KEY")),"model":os.getenv("OPENAI_MODEL","gpt-4.1-mini"),"services":SERVICES,"samples":SAMPLES}
@app.post("/api/documents")
async def upload(file: UploadFile=File(...)):
 raw=await file.read(5*1024*1024+1)
 if len(raw)>5*1024*1024: raise HTTPException(413,"Maximum file size is 5 MB")
 name=(file.filename or "document").replace("/","_").replace("\\","_")[:120]
 try:
  if name.lower().endswith(".pdf"):
   with pymupdf.open(stream=raw,filetype="pdf") as pdf:
    if pdf.needs_pass: raise ValueError("Encrypted PDFs are not supported")
    if len(pdf)>30: raise ValueError("Maximum 30 pages")
    pages=[{"page":i+1,"text":page.get_text()} for i,page in enumerate(pdf)]
  elif name.lower().endswith(".txt"):
   pages=[{"page":1,"text":raw.decode("utf-8")}]
  else: raise ValueError("Upload a PDF or UTF-8 TXT file")
  size=sum(len(p["text"]) for p in pages)
  if size<10: raise ValueError("No extractable text. This MVP does not run OCR; upload a text PDF or TXT.")
  if size>60000: raise ValueError("Maximum 60,000 extracted characters")
 except Exception as e:
  if isinstance(e,ValueError): raise HTTPException(422,str(e))
  raise HTTPException(422,"Could not read document. Upload an unencrypted text PDF or UTF-8 TXT.")
 doc={"title":name,"title_hr":name,"pages":pages,"extraction":"PyMuPDF text extraction" if name.lower().endswith(".pdf") else "UTF-8 text"}
 ident=put("documents",doc)
 return {"document_id":ident,"document":doc}
@app.get("/api/proposals/{ident}/export")
def export(ident: str):
 item=get("proposals",ident)
 if not item: raise HTTPException(404,"Proposal not found")
 return PlainTextResponse(item["markdown"],media_type="text/markdown",headers={"Content-Disposition":'attachment; filename="project-proposal.md"'})
