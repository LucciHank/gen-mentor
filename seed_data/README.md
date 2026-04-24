# GenMentor Seed Data

Bộ seed data hoàn chỉnh cho GenMentor MVP demo.

## Cấu trúc

```
seed_data/
├── raw/                    # File gốc mẫu
│   ├── AI/                # AI/ML learning materials
│   ├── ERP_SOP/           # ERP Standard Operating Procedures
│   ├── Software_Process/  # Software development processes
│   └── Assessment/        # Assessment templates
├── taxonomy/              # Taxonomy definitions
├── normalized_examples/   # Processed data examples
├── database/             # Database schema và migration
└── manifests/            # Ingestion manifests
```

## Cách sử dụng

1. **Setup Database**: Chạy `database/minimal_schema.sql`
2. **Seed Taxonomy**: Import `taxonomy/*.json` vào database
3. **Upload Documents**: Copy `raw/` vào storage
4. **Register Documents**: Import `manifests/document_registry.csv`
5. **Process Documents**: Sử dụng `manifests/knowledge_manifest.json`

## Quick Start

```bash
# Backend setup
cd backend
python -m pip install -r requirements.txt
python scripts/setup_database.py
python scripts/seed_taxonomy.py
python scripts/ingest_documents.py

# Frontend setup
cd frontend
python -m pip install -r requirements.txt
streamlit run main.py
```