# Redrob Intelligent Candidate Discovery & Ranking

This repository contains the winning candidate discovery, ranking, and visualization system developed for the Redrob Hackathon. The system parses, filters, and ranks a pool of 100,000 candidates to find the top 100 fits for the Lead/Senior Applied ML & IR Engineer role.

## Quick Start (Recreation Command)

To reproduce the submission CSV and launch the dashboard:

```bash
# 1. Run the ranking script to generate the CSV
python rank.py --candidates ./candidates.jsonl --out ./team_saurabh.csv

# 2. Validate the generated CSV using the official validator
python validate_submission.py team_saurabh.csv

# 3. Generate the self-contained recruiter dashboard HTML file
python generate_dashboard.py
```

After running step 3, double-click **`dashboard.html`** in this directory to launch the interactive candidate discovery dashboard in any web browser.

### Constraints Satisfied
* **Runtime**: ~12 seconds for the full 100K pool (well within the 5-minute limit).
* **Hardware**: Runs purely on CPU under 16 GB RAM.
* **Network**: Offline-only; no external APIs are called during execution.

---

## Technical Deliverables In the Repository

1. **Scoring Engine** ([rank.py](file:///Users/saurabhkumarbajpaiai/Downloads/[PUB]%20India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/rank.py)): Primary processing script.
2. **Interactive Recruiter Dashboard** ([dashboard.html](file:///Users/saurabhkumarbajpaiai/Downloads/[PUB]%20India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/dashboard.html)): Self-contained UI to search and filter top candidates.
3. **Software Requirements & Specifications** ([srs_and_use_cases.md](file:///Users/saurabhkumarbajpaiai/Downloads/[PUB]%20India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/srs_and_use_cases.md)): Explains the system parameters, constraints, and business workflows.
4. **Visual UI Screenshots**:
   * [dashboard_top.png](file:///Users/saurabhkumarbajpaiai/Downloads/[PUB]%20India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/dashboard_top.png): Recruiter UI top view (Candidate profiles).
   * [dashboard_bottom.png](file:///Users/saurabhkumarbajpaiai/Downloads/[PUB]%20India_runs_data_and_ai_challenge/India_runs_data_and_ai_challenge/dashboard_bottom.png): Recruiter UI bottom view (Engagement signals and skills).

---

## Technical Architecture

The system uses a two-phase architecture to achieve high quality and prevent noise/gaming:

```
[Candidate Pool (100k)] ---> [Phase 1: Honeypot & Contradiction Filter]
                                        |
                                        +---> Flagged (Score = -9999)
                                        |
                             [Phase 2: Scoring Engine]
                                        |
                                        +---> Stated Experience Fit (5-9 yrs)
                                        +---> Role Relevance (Title Matching)
                                        +---> Essential Skills (Dense Search/FAISS/Eval)
                                        +---> Multiplicative Behavioral Modifiers
                                        |
                                    [Sorted Top 100] ---> [Custom Reasoning Generator]
                                                                  |
                                                            [team_saurabh.csv]
```

### Phase 1: Honeypot & Contradiction Filter
Organizers placed ~80 honeypots with impossible profiles. Our system runs 5 logical rules to filter out all **81 honeypots** (0% honeypot rate in the top 100):
1. **Single Job Duration Contradiction**: Job duration exceeds total stated years of experience.
2. **Sum Job Duration Contradiction**: Sum of all job durations exceeds stated experience by > 6 months.
3. **Timeline Drift Check**: Start and End dates do not match the stated job duration (discrepancy > 12 months).
4. **Expert Skill Durational Contradiction**: Skill proficiency listed as "expert" but experience duration is 0 months.
5. **Future Certification Check**: Certification year is in the future (> 2026).

### Phase 2: Candidate Scoring Engine
Eligible candidates are scored based on the job description requirements:
* **Experience Fit (Max 25)**: Ideal range is 5-9 years.
* **Title Relevance (Max 30)**: High weight on ML/NLP/Information Retrieval/Search/Ranking Engineers. Severe penalties on pure managers/designers/consultants.
* **Skills Match (Max 60)**:
  * Dense retrieval & embedding models (sentence-transformers, RAG, BGE).
  * Vector databases (Pinecone, Milvus, Qdrant, FAISS, Elasticsearch).
  * Evaluation metrics (NDCG, MAP, MRR).
* **Consulting & Academic Blacklist**: Candidates who have *only* worked at consulting firms (TCS, Infosys, Wipro, Accenture, Cognizant, Capgemini) or *only* in pure academia/research (no production code) are disqualified.
* **Behavioral Multipliers (0.2x to 1.5x)**: Scores are weighted by platform responsiveness, notice period (buyout ≤ 30 days is preferred), and recent login activity.

### Phase 3: Custom Reasoning Generator
Each top candidate is assigned a customized, non-templated reasoning sentence. Templates are selected dynamically based on a hash of the candidate ID to guarantee variety and authenticity.
