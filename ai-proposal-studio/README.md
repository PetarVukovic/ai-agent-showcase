# AI Proposal Studio

Local MVP: a project brief becomes a source-backed requirement review, editable scope and downloadable proposal draft.

## Start

Two terminals, from this folder:

```sh
./start-backend.sh
./start-frontend.sh
```

- React / TypeScript: http://127.0.0.1:5175/
- LangGraph Agent Server: http://127.0.0.1:2025
- API docs: http://127.0.0.1:2025/docs
- English static description: http://127.0.0.1:5175/about/
- Croatian static description: http://127.0.0.1:5175/hr/about/

Initial installation: `uv venv .venv --python 3.12`, `uv pip install --python .venv/bin/python -r requirements.txt -e .`, then `npm ci` inside frontend. `.env.example` documents configuration. Keys remain backend-only; never put them in VITE variables. Optionally set `PROVIDER_ENV_FILE=/absolute/path/to/provider.env`; only GOOGLE_API_KEY is read from that file. Keep this setting local and gitignored. Gemini uses official google-genai SDK. OpenAI support uses langchain-openai.

Default UI selects Gemini if configured. Guided demo is explicitly rule-based and never invokes a model. OpenAI is selectable when OPENAI_API_KEY is set. Model errors are shown; they never silently switch to demo. Uploaded document text is sent to the selected provider only when analysis is requested. No Qdrant service is required for this small, bounded document review.

## What works

- Two synthetic project briefs, Northstar and Harbor; matching PDF/TXT files in frontend/public/samples.
- PDF/TXT upload: 5 MB, 30 PDF pages, 60,000 extracted characters. PyMuPDF extracts existing text. OCR is not implemented; image-only/encrypted/malformed PDFs receive a useful error.
- Real LangGraph nodes: load_document -> analyze_requirements -> verify_evidence -> price_scope -> build_proposal. The UI displays completed nodes from actual Agent Server SSE updates.
- Up to 12 selected requirements requested from AI (schema hard cap 15); not exhaustive compliance assessment. Every displayed quote must be an exact substring of its claimed page. Unverifiable rows are removed and reported.
- Catalogue prices and effort are calculated by code; no model-generated prices. Sample prices are not a real commercial offer; VAT is not calculated. Effort in person-days is not a calendar deadline.
- Scope-only revisions reuse verified requirements, skip the model call, revalidate evidence, and reprice. Excluded services are visibly marked; stale draft export is blocked until update.
- Markdown export; no external sending or actual project commitment.
- SQLite stores uploaded documents and finished proposal drafts. Agent Server manages execution checkpointing. This is a local development server, not production persistence/auth.
- React OpenUI typed RequirementCard/QuestionCard library and Renderer. Structured model output is verified then serialized into a fixed, domain-specific OpenUI layout; arbitrary AI-generated page layouts are not claimed. The source-view action is typed and updates the exact source highlight.
- Responsive English/Croatian UI. Model output language follows the language at analysis time; rerun analysis to translate model-written content.
- Static HTML /about/ and /hr/about/ with real content, FAQ, accurate SoftwareApplication schema and author. No canonical URL/sitemap is invented before a public deployment target exists. No ranking or GEO appearance is promised.

## Snimanje, 45–60 sekundi

1. Otvori http://127.0.0.1:5175/?lang=hr i ostavi Northstar odabran.
2. Klikni **Analiziraj projektni zahtjev** u Gemini načinu. Kratko prikaži stvarnu analizu.
3. Klikni izvor uz prvi zahtjev. Desno se označi točan odlomak.
4. Otvori **Pitanja** pa pokaži zahtjev izvan kataloga (24/7 i 99,99%).
5. U **Oblikujte opseg** isključi API integraciju. Pokaži da ogledni iznos pada za 1.800 €.
6. Klikni **Ažuriraj ponudu**, zatim **Nacrt ponude** i **Izvezi ponudu (.md)**.
7. Za novi pokušaj klikni kružnu strelicu u zaglavlju radnog prostora. Harbor je drugi gotovi scenarij.

If Gemini rate limits prevent recording, intentionally select the labelled guided demo; do not present it as a live model run.

## Checks

`frontend: npm run build` performs TypeScript and production Vite build. `./.venv/bin/pytest -q` checks graph evidence, source validity, scope prices and upload limits. Dependency snapshots: package-lock.json and requirements.lock.txt.

Verified on 2026-11-03: four backend tests passed; production frontend build passed; OpenUI parser passed EN/HR, partial streams and invalid-component checks. HTTP checks passed valid PDF/TXT and invalid type/size/corrupt/image-only PDF, scope-only model bypass, Markdown export. Real Gemini 3.5 Flash-Lite synthetic Northstar HR run returned 6 requirements, all source quotes verified, €10,450 catalogue total. `scripts/test_http.py` repeats HTTP + a paid Gemini request; use deliberately.
