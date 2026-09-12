# BloodBridge AI - Architecture

## The four layers

```
          USER
            |
      [ frontend/ ]        Streamlit screens        Iqra
            |
      [ ai/ ]              reads the sentence       Fizza
            |
      [ backend/ ]         decides the matches      Laiba
            |
      [ data/ ]            donors, banks, hospitals Laiba
            |
        RESULTS
```

`app.py` sits on top and calls each layer in order. Anees owns that file.

`utils/geo.py` holds the coordinates of 47 Pakistani cities. The service layer uses
it to turn a donor local distance into a real distance from the patient, then drops
anyone outside the 150 km search radius. The matching engine never changes: it still
just reads distance_km.

## Request journey

1. User types a request, by form or in plain words.
2. AI pulls out blood group, urgency and city. If the AI is offline, keyword rules do the same job.
3. Backend removes every donor who is incompatible, unavailable or not eligible.
4. Backend scores the remaining donors and sorts them.
5. Services look up blood banks and emergency hospitals as a backup.
6. AI writes the donor message.
7. Frontend shows the ranked cards.

## The rule that matters

The AI never decides who can donate to whom. Blood compatibility is a fixed
medical table in `backend/matching.py`. The AI only reads language and writes language.

## Scoring

Score is out of 100 and has three parts:

| Part | What it measures |
|---|---|
| Match | same blood group beats merely compatible |
| Distance | 0 km is 100 points, 25 km or more is 0 |
| Readiness | how long since the donor last gave blood |

Urgency changes the weight of each part:

| Urgency | Match | Distance | Readiness |
|---|---|---|---|
| High | 30% | 50% | 20% |
| Medium | 40% | 35% | 25% |
| Low | 50% | 20% | 30% |

A high urgency case pushes nearby donors to the top. A low urgency case prefers
the best group match even if that donor is further away.
