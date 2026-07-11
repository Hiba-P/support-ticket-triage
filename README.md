# Support Ticket Triage Intelligence

Predicts SLA-breach risk for incoming consumer complaints using machine learning and NLP — built on 878,515 real complaints from the CFPB (US Consumer Financial Protection Bureau).

**Live app:** https://support-ticket-triage-ep3gdvp9uahzuxpdaxjlnp.streamlit.app
**API docs:** https://support-ticket-triage.onrender.com/docs

## The Problem

Support teams typically process complaints in the order they arrive, not the order they matter. This project predicts which incoming complaints are at risk of missing their response deadline (SLA), so high-risk tickets can be prioritized.

## Key Findings

- **Data quality discovery:** 16.9% of complaint narratives were near-duplicate templates (likely from credit-repair services), not organic writing — discovered via BERTopic clustering and removed before training to prevent train/test leakage.
- **Rare-event handling:** Only 2.1% of complaints were actually late. Used time-based validation (not random splits) to reflect real-world deployment conditions, and detected an ~80% relative increase in late-response rate across the study window.
- **Model comparison:** Logistic Regression, LightGBM, and tuned LightGBM (via RandomizedSearchCV with PR-AUC scoring) converged to similar performance — evidence the bottleneck was feature information content, not model capacity.
- **NLP layer:** Sentence-transformer embeddings achieved 93% accuracy on Product classification and meaningful results on 16-class Issue classification, with an interpretable confusion pattern reflecting real complaint semantics.

## Architecture

Raw Complaints -> Clean & Engineer -> Train Models (structured + NLP) -> FastAPI -> Streamlit

- **Data:** CFPB Consumer Complaint Database, 2023-2026, Debt Collection + Credit Card categories
- **Structured modeling:** scikit-learn, LightGBM
- **NLP:** sentence-transformers, BERTopic
- **Backend:** FastAPI, deployed on Render
- **Frontend:** Streamlit, deployed on Streamlit Community Cloud
- **Fully free-tier infrastructure** — no paid APIs or cloud services

## Repository Structure

- `api/` — FastAPI backend
- `app/` — Streamlit frontend
- `src/` — Shared feature engineering
- `notebooks/` — EDA, modeling, and experimentation
- `data/` — Trained models (raw data excluded, see .gitignore)

## Limitations

- Precision on the rare "late" class is low (~5%) given a 45:1 class imbalance — the model is tuned for high recall (catches ~82% of true late cases) at the cost of false positives, appropriate for a triage/review workflow rather than an autonomous decision system.
- NLP models were trained on a 30,000-complaint stratified sample due to local compute constraints, not the full narrative-available subset (~321K).
- Template-generated complaint text behaves differently from organic writing — a limitation of the underlying data, addressed via deduplication but not fully eliminated.

## Author

Hiba P. — [LinkedIn](https://www.linkedin.com/in/hiba-puthiyedath) | [GitHub](https://github.com/Hiba-P)
