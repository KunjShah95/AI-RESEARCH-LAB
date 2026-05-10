# Autonomous Paper Analyzer

AI research assistant with multi-agent reasoning, source-grounded outputs, citation tracking, and citation graph analysis.

## Quick Start

```bash
# Install all dependencies
npm run install:all

# Run both frontend and backend
npm run dev
```

- Frontend: <http://localhost:5173>
- Backend API: <http://localhost:8001>

## Supported AI Providers

This project supports **7 LLM providers** with free and paid options:

### Free/Freemium Tier
- **Groq** - Fastest inference, free tier available
- **Google Gemini** - Free tier with 1.5 Flash model
- **OpenRouter** - 100+ models, some free options
- **NVIDIA NIM** - Free tier available

### Premium
- **OpenAI** - GPT-4o (industry standard)
- **Anthropic** - Claude 3.5 Sonnet (best reasoning)
- **Mistral** - Most cost-effective

**Setup**: Copy `.env.example` to `.env` and add your API keys. See [PROVIDERS.md](docs/PROVIDERS.md) for detailed setup instructions and cost comparison.

## Features

### Core Features

- **Paper Search**: Search across arXiv, Semantic Scholar, PubMed with semantic, hybrid, and vector search
- **Smart Summaries**: Multi-granularity summaries (one-sentence, abstract, structured) with confidence scores
- **Method Comparison**: Side-by-side analysis of datasets, metrics, and architectures
- **AI Debates**: Multi-agent debates with Proponent, Critic, and Methodologist roles
- **Insight Synthesis**: Identify research gaps and generate actionable recommendations
- **Paper Writing**: Generate literature reviews with source-grounded citations
- **Citation Clipboard**: Quick citation copying in APA, MLA, Chicago, IEEE formats

### Advanced Features

- **Citation Graph Analysis**: Build and analyze citation networks with PageRank, influence metrics
- **Related Paper Discovery**: Find similar papers using embeddings and citation patterns
- **Research Timeline**: Visualize research evolution over time
- **Collections & Projects**: Organize papers into collections and projects
- **Export**: BibTeX, RIS, JSON, CSV export formats

## Quick Start

```bash
# Install dependencies
cd ai-research-lab
pip install -r requirements.txt

# Set environment variables (optional for mock mode)
export DATABASE_URL="postgresql://localhost:5432/paper_analyzer"
export OPENAI_API_KEY="your-key"

# Start the backend server
uvicorn --app-dir . app.main:app --reload --port 8001

# In another terminal, start the frontend
cd frontend
npm install
npm run dev
```

The frontend runs at `http://localhost:5173` and connects to the backend at `http://localhost:8001`.

## Tech Stack

- **Frontend**: React, Vite, Framer Motion, React Router
- **Backend**: FastAPI, Pydantic
- **AI**: CrewAI (multi-agent), LangGraph (workflows)
- **Database**: PostgreSQL (production), SQLite (dev)
- **Vector Store**: FAISS (with mock fallback)

## API Endpoints

### Papers

- `POST /api/papers/search` - Search papers across sources
- `GET /api/papers/{id}` - Get paper details
- `POST /api/papers/summarize` - Generate structured summary
- `POST /api/papers/export/{format}` - Export citations (bibtex/ris/json/csv)

### Graph

- `POST /api/graph/build` - Build citation graph
- `GET /api/graph/metrics` - Get graph metrics
- `GET /api/graph/influential` - Get most influential papers
- `GET /api/graph/recommendations/{paper_id}` - Get paper recommendations
- `GET /api/graph/visualization/d3` - Get D3.js visualization data

### Other

- `POST /api/debate/start` - Start multi-agent debate
- `POST /api/synthesize` - Synthesize insights from papers
- `GET /api/projects/` - List projects
- `GET /api/collections/` - List collections

## Project Structure

```
ai-research-lab/
├── app/
│   ├── api/              # FastAPI routes (21+ endpoint files)
│   ├── agents/           # CrewAI agent definitions
│   ├── crews/            # Crew configurations
│   ├── clients/          # Paper source clients (arXiv, Semantic Scholar, PubMed)
│   ├── engines/          # Core engines
│   │   ├── citation_graph.py    # Citation network analysis (1100+ lines)
│   │   ├── advanced_search.py   # Semantic/hybrid/vector search
│   │   ├── synthesis.py          # Insight synthesis
│   │   └── ...
│   ├── graph/            # LangGraph workflows
│   ├── models/           # Pydantic data models
│   └── store/            # Database and vector store
├── frontend/
│   ├── src/
│   │   ├── App.jsx       # Main React app (24+ pages)
│   │   ├── services/     # API service layer
│   │   └── App.css       # "Academic Noir" design system
│   └── package.json
└── requirements.txt
```

## Frontend Pages

| Page | Description |
|------|-------------|
| `/` | Landing page with premium "Academic Noir" design |
| `/login`, `/signup` | Authentication pages |
| `/app` | Dashboard with sidebar navigation |
| `/app/search` | Paper search with filters |
| `/app/summarize/:id` | Structured paper summarization |
| `/app/compare` | Side-by-side paper comparison |
| `/app/qa` | Question answering over papers |
| `/app/discover` | Related paper discovery |
| `/app/debate` | Multi-agent debate system |
| `/app/synthesize` | Insight synthesis |
| `/app/graph` | Citation network visualization |
| `/app/timeline` | Research timeline |
| `/app/collections` | Paper collections |
| `/app/projects` | Research projects |
| `/app/export` | Citation export (BibTeX/RIS/JSON/CSV) |
| `/app/settings` | User settings |

## Design System: Academic Noir

The frontend uses a distinctive "Academic Noir" aesthetic:

- **Typography**: Cormorant Garamond (display), Outfit (body), Instrument Serif (accents)
- **Colors**: Deep charcoal backgrounds (#1a1a1a, #2d2d2d), warm gold accents (#d4a853)
- **Effects**: Subtle noise texture, radial gradients, glassmorphism

## License

MIT
