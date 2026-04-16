
EvalGenAI/
│
├── agent/                          # 🧠 Intelligence Layer
│   ├── classifier.py               # task detection (answer / predict)
│   ├── router.py                   # routes query to correct pipeline
│
├── RAG/                            # 🔍 RAG SYSTEMS
│   │
│   ├── answer_rag/                 # 🟢 Answer Generation RAG
│   │   ├── ingest_kb.py            # ingest notes + diagrams
│   │   ├── retrieve.py             # retrieve notes + diagrams
│   │   ├── generate.py             # generate final answer
│   │
│   ├── qp_rag/                     # 🔥 Question Prediction RAG
│   │   ├── ingest_qp.py            # ingest assignments + IA + PYQ
│   │   ├── retrieve_qp.py          # predict questions
│
│
├── data/                           # 📦 KNOWLEDGE BASE
│   └── iot/
│       │
│       ├── mod1/
│       │   ├── notes/
│       │   │   └── IOT_mod1.json
│       │   │
│       │   ├── diagrams/
│       │   │   ├── diagrams.json
│       │   │   └── images/
│       │   │       ├── iot_framework.png
│       │   │       ├── ge_iot_framework.png
│       │   │       ├── ptc_framework.png
│       │   │       └── industry_examples.png
│       │
│       ├── mod2/
│       │   ├── notes/
│       │   │   └── IOT_mod2.json
│       │   │
│       │   ├── diagrams/
│       │   │   ├── diagrams.json
│       │   │   └── images/
│       │       ├── osi_model_layers.png
│       │       ├── range_vs_power.png
│       │       ├── range_vs_data_rate.png
│       │       ├── application_layer.png
│       │       └── connection_security.png
│       │
│       ├── mod3/
│       │   ├── notes/
│       │   ├── diagrams/
│       │
│       ├── mod4/
│       │   ├── notes/
│       │   ├── diagrams/
│       │
│       ├── mod5/
│       │   ├── notes/
│       │   ├── diagrams/
│       │
│       ├── assignments/            # 🔥 MOST IMPORTANT FOR PREDICTION
│       │   ├── module1.json
│       │   ├── module2.json
│       │   ├── module3.json
│       │   ├── module4.json
│       │   ├── module5.json
│       │
│       ├── ia/                     # 📝 Internal Assessment Papers
│       │   ├── ia1.json
│       │   ├── ia2.json
│       │   ├── ia3.json
│       │
│       ├── pyq/                    # 📜 Previous Year Questions
│       │   └── pyq_all.json
│       │
│       └── eval/                   # 📊 Evaluation Scheme
│           └── eval.json
│
│
├── chroma_db/                      # ⚡ AUTO-GENERATED (DO NOT PUSH)
│
├── utils/                          # 🔧 Helpers (optional but useful)
│   ├── loader.py
│   ├── embeddings.py
│
├── configs/                        # ⚙️ Configurations
│   └── config.yaml
│
├── main.py                         # 🚀 MAIN ENTRY POINT
├── requirements.txt
└── .gitignore
