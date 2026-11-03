# AI Operations Desk

Local MVP by Petar Vuković: AI quote automation with a real LangGraph approval pause, React/TypeScript, typed OpenUI components, direct Gemini/OpenAI inference and a synthetic SQLite product catalog.

## Run

Backend (Python 3.11+):
```sh
cd backend
uv sync --frozen
cp .env.example .env
# Add your own OPENAI_API_KEY to backend/.env. Never put it in frontend env.
.venv/bin/langgraph dev --host 127.0.0.1 --port 2024 --no-browser --allow-blocking
```
Frontend:
```sh
cd frontend
npm ci
npm run dev
```
Open http://127.0.0.1:5174. Backend API http://127.0.0.1:2024/docs.

The labelled **Demo mode** makes no model calls and is labeled as deterministic. OpenAI mode calls the configured `OPENAI_MODEL` directly; errors are surfaced, never silently replaced with demo output. Both modes use the same calculation/policy graph. OpenAI generates OpenUI brief content; the library and generated system prompt share one typed contract (`src/openui.tsx`, generated `backend/ops/openui-prompt.txt`). Run `npm run generate:ui` after changing the library.

Agent Server owns thread checkpointing in `.langgraph_api`; SQLite holds only business records. Reloading the UI restores the last thread from the local server. This is local development, not a production deployment. No email is sent and no stock is reserved. Approved/declined decisions apply to the exact quote digest. Changing terms requires recalculation. Prices exclude VAT and are synthetic.

## Checks
`cd backend && .venv/bin/python -m unittest test_workflow -v`
`cd frontend && npm run build`

## SEO / GEO
Static, crawlable English `/about/` and Croatian `/hr/about/` explain the actual workflow with visible FAQ and SoftwareApplication schema. Target phrases: AI sales operations demo, AI quote automation, AI izrada ponuda, automatizacija prodajnih upita. The local demo is noindex; there is no invented public canonical. Before publishing, set the real production domain, canonical/hreflang/sitemap and public robots policy, verify indexing and link from the main portfolio. No ranking or conversion claims are made.

## Gemini
The optional provider-file setup reads only `GOOGLE_API_KEY` from the configured `PROVIDER_ENV_FILE=/absolute/path/to/provider.env`, without loading unrelated application variables or copying the key. `GEMINI_MODEL` defaults to gemini-3.5-flash-lite. The UI selects Gemini when available. Errors are visible; there is no silent demo fallback.

## Snimanje (45–60 s)
1. Otvori aplikaciju, odaberi HR i klikni Kreni ispočetka.
2. Prvi scenarij: 40 stolaca, 12% popusta. Klikni Pripremi moju ponudu.
3. Pokaži izračun i izvore; zatim odobri popust i pokaži nacrt odgovora.
4. Odaberi izazov sa zalihama i ponovno izračunaj: agent blokira ponudu.
5. Odaberi dostupnu alternativu Form i ponovno izračunaj.
6. Izvezi demo ponudu. Jasno pokaži oznaku sintetičkih podataka.

Start scripts: `sh start-backend.sh` and `sh start-frontend.sh`.
