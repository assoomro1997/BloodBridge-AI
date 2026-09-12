# BloodBridge AI

Right blood. Right place. Right time.

Finding a blood donor in an emergency takes hours of phone calls. BloodBridge AI reads
a request in plain language, checks medical compatibility, filters donors who are
available and eligible, ranks them by distance and urgency, and writes the message
that goes to the donor.

## How to run it

```bash
git clone <repo-url>
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
python tests/test_matching.py      # 36 backend and geography checks
python tests/test_ai.py            # 10 AI checks
python tests/test_integration.py   # 5 full scenarios
```

## Coverage

47 cities across Punjab, Sindh, Khyber Pakhtunkhwa, Balochistan, Islamabad,
Azad Kashmir and Gilgit-Baltistan. Distance is calculated from real coordinates
with the haversine formula, then capped at a 150 km search radius for donors and
400 km for blood banks and hospitals.

## Folder map

| Folder | Owner | Holds |
|---|---|---|
| `data/` | Laiba | donors.csv, blood_banks.csv, hospitals.csv |
| `backend/` | Laiba | matching engine, compatibility, scoring |
| `ai/` | Fizza | request reader, SMS writer, match explainer |
| `frontend/` | Iqra | every Streamlit screen piece |
| `services/` | Anees | data loader, blood bank and hospital lookup |
| `tests/` | all | backend, AI and end to end tests |
| `geo.py` | Anees | city coordinates and distance calculation |
| `docs/` | Mehwish | PRD, architecture, flow, demo scenarios |
| `app.py` | Anees | connects all modules |

## Live app

Deployed free on Streamlit Community Cloud. The app pulls straight from this
repository, so every push updates the live version.

## Safety note

Demo data only. A qualified blood bank must confirm every donor before any donation.
The AI never decides medical compatibility. That is fixed rule based logic in `backend/matching.py`.

## Free tools used

Streamlit, Streamlit Community Cloud, Groq free tier, Hugging Face Inference API, Python, CSV.
