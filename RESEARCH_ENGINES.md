# Research Engines

This catalog maps the implemented research/intelligence engines in the repository to their purpose and outputs.

## 1) Prompt Strategy Engine

- File: `prompt_engine.py`
- Purpose: Generates domain-aware collection prompts, URL strategies, and smart filters.
- Output artifacts:
  - collection strategies
  - normalized prompt payloads
  - filter recommendations

## 2) Browser Collection Engine

- File: `browser_automation.py`
- Purpose: Collects data from JS-heavy or login-gated sources.
- Output artifacts:
  - structured records from browser sessions
  - metadata on collection sessions

## 3) Threat Analysis Engine

- File: `threat_analysis_engine.py`
- Purpose: Performs categorization, severity analysis, and risk scoring for cybersecurity data.
- Output artifacts:
  - threat scoring outputs
  - categorized risk records

## 4) Cross-Domain Intelligence Engine

- File: `cross_domain_intelligence.py`
- Purpose: Correlates findings across domains for broader situational insight.
- Output artifacts:
  - cross-domain correlation summaries
  - composite intelligence views

## 5) AI Insights Engine

- File: `ai_insights_engine.py`
- Purpose: Produces trend/anomaly insights and recommendation narratives.
- Output artifacts:
  - analytical insight summaries
  - recommendation-ready intelligence notes

## 6) Report Generation Engine

- File: `report_generator.py`
- Purpose: Converts intelligence outputs into operational and executive consumables.
- Output artifacts:
  - Markdown/JSON/CSV reporting outputs
  - executive-facing summaries
