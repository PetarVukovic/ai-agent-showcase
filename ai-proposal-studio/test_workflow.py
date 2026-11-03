import pytest
from backend.graph import graph, verify_evidence, load_document, price_scope
from backend.catalog import SAMPLES
from fastapi.testclient import TestClient
from backend.api import app

def test_catalog_price_and_source_integrity():
 r=graph.invoke({"mode":"demo","sample_id":"knowledge","language":"en","scope_only":False,"excluded_services":[]})
 assert r["total"]==10450
 assert r["total"]==sum(s["price"] for s in r["selected_services"])
 pages={p["page"]:p["text"] for p in r["document"]["pages"]}
 assert all(x["quote"] in pages[x["page"]] for x in r["requirements"])
 assert any(x["status"]=="missing" and "24/7" in x["quote"] for x in r["requirements"])
 revised=graph.invoke({**r,"scope_only":True,"excluded_services":["integration"]})
 assert revised["total"]==8650
 assert revised["requirements"]==r["requirements"]
 assert "One documented API integration:" not in revised["proposal_markdown"]

def test_reject_fabricated_evidence_and_unknown_service():
 state={"document":{"pages":[{"page":1,"text":"Exact source passage."}]},"requirements":[{"quote":"Exact source passage.","page":1,"service_id":"invented","status":"supported"},{"quote":"Fabricated passage.","page":1,"service_id":"knowledge","status":"supported"},{"quote":"Exact source passage.","page":2,"service_id":"knowledge","status":"supported"}]}
 checked=verify_evidence(state)
 assert len(checked["requirements"])==1
 assert checked["requirements"][0]["status"]=="missing"
 assert checked["requirements"][0]["service_id"] is None
 assert checked["evidence_rejected"]==2
 with pytest.raises(ValueError): verify_evidence({"document":state["document"],"requirements":[{"quote":"fake","page":1}]})

def test_scope_input_validation():
 with pytest.raises(ValueError): load_document({"sample_id":"knowledge","mode":"demo","excluded_services":["invented"]})
 with pytest.raises(ValueError): load_document({"scope_only":True})
 with pytest.raises(ValueError): load_document({"sample_id":"unknown"})
 with pytest.raises(ValueError): load_document({"mode":"pretend"})

def test_upload_contract():
 client=TestClient(app)
 assert client.post("/api/documents",files={"file":("bad.exe",b"bad","application/octet-stream")}).status_code==422
 assert client.post("/api/documents",files={"file":("bad.pdf",b"bad","application/pdf")}).status_code==422
 valid=client.post("/api/documents",files={"file":("brief.txt",b"We need a bilingual web interface.","text/plain")})
 assert valid.status_code==200
 assert valid.json()["document"]["pages"][0]["text"]=="We need a bilingual web interface."
 assert client.get("/api/proposals/unknown/export").status_code==404
