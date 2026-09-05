"""
Curated skill taxonomy for AI/ML job postings.

This is the zero-dependency deterministic baseline: a deliberately narrow set
of AI, data and software skill terms grouped by category, each with common
surface-form variants. It is the taxonomy consumed by the default rule-based
extractor. The separately bundled ESCO artefact is a reference/lookup
vocabulary and does not replace this active extraction path.

When optional provider mode is explicitly enabled and a provider key is
available, validated provider results can supplement these deterministic
matches (see extractor.py and provider_config.py).
"""

SKILL_TAXONOMY: dict[str, dict[str, list[str]]] = {
    "Programming": {
        "Python": ["python"],
        "SQL": ["sql", "postgresql", "mysql", "t-sql"],
        "R": [" r ", "r programming", "r language"],
        "Java": ["java "],
        "JavaScript/TypeScript": ["javascript", "typescript", "js/ts", "node.js"],
        "C++": ["c++"],
    },
    "ML/DL Frameworks": {
        "PyTorch": ["pytorch", "torch"],
        "TensorFlow": ["tensorflow", "tf.keras"],
        "scikit-learn": ["scikit-learn", "sklearn"],
        "Keras": ["keras"],
        "Hugging Face": ["hugging face", "huggingface", "transformers library"],
        "XGBoost": ["xgboost"],
    },
    "LLM / GenAI": {
        "LLM APIs": ["openai api", "anthropic api", "claude api", "gpt-4", "llm api"],
        "RAG": ["rag", "retrieval augmented generation", "retrieval-augmented"],
        "Prompt Engineering": ["prompt engineering", "prompt design"],
        "Vector Databases": ["vector database", "pinecone", "weaviate", "chroma", "pgvector", "faiss"],
        "Fine-tuning": ["fine-tuning", "fine tuning", "lora", "peft"],
        "Agents": ["agentic", "ai agents", "multi-agent", "langchain", "llamaindex"],
    },
    "Data Engineering": {
        "Pandas": ["pandas"],
        "Spark": ["spark", "pyspark"],
        "Airflow": ["airflow"],
        "ETL": ["etl", "elt pipeline", "data pipeline"],
        "dbt": ["dbt "],
        "Data Warehousing": ["data warehouse", "snowflake", "bigquery", "redshift"],
    },
    "MLOps / Infra": {
        "Docker": ["docker"],
        "Kubernetes": ["kubernetes", "k8s"],
        "CI/CD": ["ci/cd", "continuous integration"],
        "Cloud (AWS)": ["aws", "amazon web services", "sagemaker"],
        "Cloud (GCP)": ["gcp", "google cloud", "vertex ai"],
        "Cloud (Azure)": ["azure", "azure ml"],
        "Model Monitoring": ["model monitoring", "ml observability"],
        "Experiment Tracking": ["mlflow", "weights & biases", "wandb"],
    },
    "Core ML Skills": {
        "Statistics": ["statistics", "statistical modeling", "hypothesis testing"],
        "A/B Testing": ["a/b testing", "experimentation"],
        "NLP": ["nlp", "natural language processing"],
        "Computer Vision": ["computer vision"],
        "Deep Learning": ["deep learning", "neural network"],
        "Model Evaluation": ["model evaluation", "cross-validation"],
        "Feature Engineering": ["feature engineering"],
    },
    "Collaboration / Product": {
        "Data Visualization": ["data visualization", "tableau", "power bi", "dashboards"],
        "Stakeholder Communication": ["stakeholder", "cross-functional"],
        "Version Control": ["git ", "github", "version control"],
        "Agile": ["agile", "scrum"],
    },
}


def all_skills() -> list[str]:
    return [skill for category in SKILL_TAXONOMY.values() for skill in category]


def skill_category(skill: str) -> str | None:
    for category, skills in SKILL_TAXONOMY.items():
        if skill in skills:
            return category
    return None
