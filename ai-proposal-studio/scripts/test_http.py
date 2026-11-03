import io,json,time,httpx,pymupdf

base='http://127.0.0.1:2025'
client=httpx.Client(timeout=120)
cfg=client.get(base+'/api/config').json()
assert cfg['gemini_configured'] and not cfg['openai_configured']

def run(tid, inp):
    response=client.post(base+f'/threads/{tid}/runs/stream',json={'assistant_id':'proposal','input':inp,'stream_mode':['updates','values']})
    response.raise_for_status()
    final=None;nodes=[]
    for block in response.text.replace('\r\n','\n').split('\n\n'):
        event='';data=''
        for line in block.splitlines():
            if line.startswith('event:'):event=line[6:].strip()
            if line.startswith('data:'):data+=line[5:].strip()
        if not data:continue
        value=json.loads(data)
        assert event!='error',value
        if event=='updates':nodes+=list(value)
        if event=='values' and value.get('proposal_id'):final=value
    assert final,'No final proposal'
    return final,nodes

tid=client.post(base+'/threads',json={}).json()['thread_id']
r,nodes=run(tid,{'sample_id':'knowledge','mode':'demo','language':'en','scope_only':False,'excluded_services':[]})
assert r['total']==10450 and len(r['requirements'])==7
assert all(x in nodes for x in ['load_document','analyze_requirements','verify_evidence','price_scope','build_proposal'])
pages={p['page']:p['text'] for p in r['document']['pages']}
assert all(row['quote'] in pages[row['page']] for row in r['requirements'])
assert any(row['status']=='missing' and '24/7' in row['quote'] for row in r['requirements'])
r2,nodes=run(tid,{'scope_only':True,'excluded_services':['integration']})
assert r2['total']==8650 and 'analyze_requirements' not in nodes
assert 'integration' not in [s['id'] for s in r2['selected_services']]
export=client.get(base+f"/api/proposals/{r2['proposal_id']}/export")
assert export.status_code==200 and '€8,650' in export.text and 'One documented API integration:' not in export.text
assert client.get(base+'/api/proposals/unknown/export').status_code==404

upload=client.post(base+'/api/documents',files={'file':('brief.txt',b'We need a bilingual web interface.\nWe require a deployment guide.','text/plain')})
assert upload.status_code==200
assert client.post(base+'/api/documents',files={'file':('bad.exe',b'not allowed','application/octet-stream')}).status_code==422
assert client.post(base+'/api/documents',files={'file':('large.txt',b'x'*(5*1024*1024+1),'text/plain')}).status_code==413
assert client.post(base+'/api/documents',files={'file':('bad.pdf',b'not PDF','application/pdf')}).status_code==422
pdf=pymupdf.open();pdf.new_page()
assert client.post(base+'/api/documents',files={'file':('image-only.pdf',pdf.tobytes(),'application/pdf')}).status_code==422
pdf.close()
pdf=pymupdf.open();page=pdf.new_page();page.insert_text((50,50),'We need a bilingual web interface with human approval.')
valid=client.post(base+'/api/documents',files={'file':('valid.pdf',pdf.tobytes(),'application/pdf')})
assert valid.status_code==200 and 'bilingual' in valid.json()['document']['pages'][0]['text']
pdf.close()

tid=client.post(base+'/threads',json={}).json()['thread_id']
started=time.time()
ai,nodes=run(tid,{'sample_id':'knowledge','mode':'gemini','language':'hr','scope_only':False,'excluded_services':[]})
pages={p['page']:p['text'] for p in ai['document']['pages']}
assert ai['mode']=='gemini' and len(ai['requirements'])>0
assert all(row['quote'] in pages[row['page']] for row in ai['requirements'])
assert ai['total']==sum(s['price'] for s in ai['selected_services'])
assert all(s['id'] in {s['id'] for s in cfg['services']} for s in ai['selected_services'])
print(json.dumps({'http_checks':'passed','guided_requirements':len(r['requirements']),'guided_total':r['total'],'revised_total':r2['total'],'scope_skips_model':True,'upload_checks':'PDF/TXT valid + type/size/corrupt/image-only rejected','gemini_model':cfg['gemini_model'],'gemini_requirements':len(ai['requirements']),'gemini_source_rejections':ai['evidence_rejected'],'gemini_total':ai['total'],'gemini_seconds':round(time.time()-started,1)},ensure_ascii=False))
