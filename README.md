llm-semantic-cache/
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application factory & middleware
│   ├── config.py            # Centralized configuration & environment vars
│   ├── routers/
│   │   ├── __init__.py
│   │   └── proxy.py         # API route controllers (/generate, /metrics)
│   ├── services/
│   │   ├── __init__.py
│   │   └── cache_service.py # Vector embeddings & cosine similarity core engine
│   └── schemas/
│       ├── __init__.py
│       └── payload.py       # Pydantic data validation contracts
├── static/                  # S-Tier Web Dashboard UI
│   └── index.html           # Interactive frontend for real-time testing & latency tracking
└── tests/
    └── test_proxy.py        # Automated unit & integration tests