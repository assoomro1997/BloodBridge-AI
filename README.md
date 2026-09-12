---
title: BloodBridge AI
emoji: 🩸
colorFrom: red
colorTo: gray
sdk: streamlit
sdk_version: 1.37.0
app_file: app.py
pinned: false
---

# BloodBridge AI

Right blood. Right place. Right time.

Finding a blood donor in an emergency takes hours of phone calls. BloodBridge AI reads
a request in plain language, checks medical compatibility, filters donors who are
available and eligible, ranks them by distance and urgency, and writes the message
that goes to the donor.

## How to run it

```bash
git clone https://github.com/assoomro1997/BloodBridge-AI
cd BloodBridge-AI
pip install -r requirements.txt
streamlit run app.py
```

The app works with no API key. It uses a rule based reader when no key is set,
so the demo never fails.

To turn on the LLM, copy `.env.example` to `.env` and add a free key:

```
GROQ_API_KEY=your_key_here
```

or a free Hugging Face token:

```
HF_TOKEN=your_token_here
```

## Run the tests

```bash
python tests/test_matching.py      # 25 backend checks
python tests/test_ai.py            # 10 AI checks
python tests/test_integration.py   # 4 full scenarios
```

## Folder map

| Folder | Owner | Holds |
|---|---|---|
| `data/` | Laiba | donors.csv, blood_banks.csv, hospitals.csv |
| `backend/` | Laiba | matching engine, compatibility, scoring |
| `ai/` | Fizza | request reader, SMS writer, match explainer |
| `frontend/` | Iqra | every Streamlit screen piece |
| `services/` | Anees | data loader, blood bank and hospital lookup |
| `tests/` | all | backend, AI and end to end tests |
| `docs/` | Mehwish | PRD, architecture, flow, demo scenarios |
| `app.py` | Anees | connects all modules |

## Safety note

Demo data only. A qualified blood bank must confirm every donor before any donation.
The AI never decides medical compatibility. That is fixed rule based logic in `backend/matching.py`.

## Free tools used

Streamlit, Hugging Face Spaces, Hugging Face Inference API, Groq free tier, Python, CSV.
