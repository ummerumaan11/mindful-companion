# Mindful Companion

A rule-based (not LLM-powered) mental wellness companion built with Streamlit: guided CBT-style coping techniques, a mood tracker, and a private journal — with a hard-coded crisis-safety layer that overrides everything else if it detects language suggesting the user may be in crisis.

⚠️ **This is a student/portfolio project.** It is not a licensed mental health service, cannot diagnose or treat anything, and its responses are entirely rule-based rather than clinical advice in any way. It's included here as a demonstration of building software responsibly in a sensitive domain, not as a real support tool.

## Why rule-based instead of an LLM

This was a deliberate design choice. An open-ended LLM chatbot can say unpredictable things in a domain where unpredictability carries real risk. Keeping this rule-based means:

- Every possible response is human-reviewed and known in advance — nothing is generated on the fly
- Crisis detection can be a **hard override**: a simple, auditable keyword check that runs before any other logic and always wins
- It's honest about its own limits, rather than simulating a level of understanding it doesn't have

## Safety design

- **`crisis_detection.py`** runs on every message, before anything else. If it matches, the app shows crisis hotline info and stops normal conversation — it does not try to keep chatting.
- Crisis resources (emergency number **112**) are **always visible** in the sidebar, not just shown reactively.
- A disclaimer banner is shown on every page load, not buried in a settings page.
- All coping techniques (grounding, box breathing, thought reframing) are standard, widely-published self-help psychoeducation — nothing clinical or prescriptive.

## Features

- **Chat**: keyword-triggered CBT-style coping suggestions for anxiety, stress, low mood, negative self-talk, and sleep trouble
- **Mood tracker**: daily mood check-ins (1–10) with an optional note, visualized as a trend line over time
- **Journal**: free-text private journal entries, saved locally

## Project structure

```
mental-health-companion/
├── app.py                  # Streamlit UI
├── crisis_detection.py      # hard safety override — checked first, always
├── responses.py              # CBT-style rule-based response flows
├── database.py                # SQLite storage for mood/journal entries
├── requirements.txt
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints (usually `http://localhost:8501`).

## What I'd want to explain about this project in an interview

- Why the crisis-detection check runs *before* any other logic, and why it's a separate, simple module rather than folded into the general chat logic
- The tradeoff between a rule-based system (predictable, auditable, safe) and an LLM-based one (more natural, harder to fully control) in a sensitive domain
- Why the keyword list is intentionally biased toward false positives rather than trying to be "smart" about detecting real risk

## Possible extensions

- Expand the topic/technique library
- Add authentication so mood/journal history is per-user instead of local-only
- If ever extending to an LLM backend, keep the crisis-detection module as a non-negotiable pre-filter regardless of what the LLM would otherwise generate

## License

MIT
