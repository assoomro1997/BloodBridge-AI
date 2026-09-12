# Product Requirements Document

## BloodBridge AI

Right blood. Right place. Right time.

| Field | Value |
|---|---|
| Product name | BloodBridge AI |
| Version | 1.0 (Hackathon MVP) |
| Date | 12 September 2026 |
| Event | PakAngels GenAI and Agentic AI Training, Cohort 11, Mid-Term Hackathon |
| Team Lead and Technical Lead | Anees Ahmed |
| Co-Lead and Submission Coordinator | Eman Fatima |
| Document owner | Anees Ahmed |
| Status | MVP built, tested and deployed live. |

---

## 1. Problem statement

When a patient needs blood in an emergency, the search starts with phone calls.
Family members call relatives. Someone posts in a WhatsApp group. Someone else calls
blood banks one at a time. Hours pass before a suitable donor is confirmed.

Three things make this slow:

1. Donor information is scattered. There is no single place to search.
2. Matching is done by hand. A person under stress has to remember which blood
   groups are compatible with which.
3. Nobody knows who is actually free and medically fit to donate today. A phone
   number in a list is not the same as an available donor.

The information needed to solve this already exists. It is simply not organised,
not filtered, and not ranked.

*Note for Mehwish: add one cited statistic from a Pakistani source here before submission.*

---

## 2. Goals

| ID | Goal | How we measure it |
|---|---|---|
| G1 | Turn a blood request into a ranked donor list in under one second | Time from search click to results |
| G2 | Never return a medically wrong match | Every compatibility rule covered by an automated test |
| G3 | Accept a request in plain language, English or Roman Urdu | Test sentences in both languages return correct fields |
| G4 | Work in any major Pakistani city | 47 cities across all provinces and territories |
| G5 | Never show an empty screen | Blood bank and hospital fallback always appears |
| G6 | Run on free tools only | No paid service anywhere in the stack |

## 3. Non-goals

These are deliberately excluded from version 1.0:

- We do not register real donors or store real personal data.
- We do not send real SMS or WhatsApp messages. We generate the message text only.
- We do not replace a blood bank. Final medical clearance stays with a qualified
  blood bank in every case.
- We do not diagnose, advise on treatment, or estimate how many units a patient needs.
- We do not handle payment, appointments, or transport.

---

## 4. Target users

| User | What they need | How BloodBridge AI helps |
|---|---|---|
| Patient attendant | A donor, fast, while standing in a hospital corridor | One sentence in, ranked donors out |
| Hospital staff | To know where usable stock exists right now | Blood bank list with usable groups and unit counts |
| Blood bank | To see which requests are unmet nearby | Structured request data instead of phone calls |
| Donor | A clear, polite request with enough detail to decide | A generated message with group, urgency and place |

---

## 5. User stories

| ID | Story |
|---|---|
| US1 | As a patient attendant, I want to type my emergency in normal words, so that I do not have to fill a form during a crisis. |
| US2 | As a patient attendant, I want the nearest suitable donor at the top, so that I call the right person first. |
| US3 | As a patient attendant, I want to see why a donor was ranked first, so that I trust the result. |
| US4 | As a patient attendant, I want blood bank options when no donor is free, so that I still have somewhere to go. |
| US5 | As a hospital staff member, I want to know which emergency units have free beds, so that I can refer the patient correctly. |
| US6 | As a donor, I want a clear message telling me the blood group, urgency and location, so that I can decide quickly. |

---

## 6. Functional requirements

Priority: P0 is required for the MVP. P1 is built if time allows. P2 is future work.

### 6.1 Request input

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR1.1 | The system accepts a structured request: blood group, urgency, city, hospital, units | P0 | Done |
| FR1.2 | The system accepts a free text request in English | P0 | Done |
| FR1.3 | The system accepts a free text request in Roman Urdu | P0 | Done |
| FR1.4 | The system extracts blood group, urgency and location from free text | P0 | Done |
| FR1.5 | If the blood group cannot be found, the system asks the user to state it clearly | P0 | Done |

### 6.2 Matching

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR2.1 | The system applies the standard blood compatibility table for all eight groups | P0 | Done |
| FR2.2 | The system removes donors marked unavailable | P0 | Done |
| FR2.3 | The system removes donors marked ineligible | P0 | Done |
| FR2.4 | The system removes donors who donated less than 90 days ago | P0 | Done |
| FR2.4b | The system removes donors beyond the 150 km search radius | P0 | Done |
| FR2.5 | The system scores every remaining donor out of 100 | P0 | Done |
| FR2.6 | Urgency changes the weight of blood group match, distance and readiness | P0 | Done |
| FR2.7 | The system returns the top five donors, highest score first | P0 | Done |
| FR2.8 | The system gives a short plain text reason for each ranked donor | P0 | Done |

### 6.3 Fallback layer

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR3.1 | The system lists blood banks holding a group the patient can receive | P0 | Done |
| FR3.2 | Blood banks in the patient city appear first, then by unit count | P0 | Done |
| FR3.3 | The system lists hospitals with an open emergency unit and free beds | P0 | Done |
| FR3.4 | The fallback appears whether or not donors were found | P0 | Done |

### 6.4 Donor message

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR4.1 | The system generates a short message for the top ranked donor | P0 | Done |
| FR4.2 | The message states blood group, urgency and location | P0 | Done |
| FR4.3 | The message is shown on screen so it can be copied | P0 | Done |
| FR4.4 | The message is sent automatically by SMS or WhatsApp | P2 | Future |

### 6.5 Interface

| ID | Requirement | Priority | Status |
|---|---|---|---|
| FR5.1 | The app runs in a browser with no install | P0 | Done |
| FR5.2 | Results show name, group, distance, score and reason | P0 | Done |
| FR5.3 | Donor phone numbers stay hidden until the donor accepts | P0 | Done |
| FR5.4 | A sidebar shows database counts and which AI provider is active | P1 | Done |
| FR5.5 | Donors are shown on a map | P2 | Future |

---

## 7. Non-functional requirements

| ID | Requirement | Target |
|---|---|---|
| NFR1 | Search response time | Under 1 second for the matching engine |
| NFR2 | Availability during demo | The app must work with no API key and no internet for the AI step |
| NFR3 | Test coverage of matching rules | Every compatibility and filter rule has an automated test |
| NFR4 | Cost | Zero. Free tiers only |
| NFR5 | Readability | Any team member can read and explain their own module |
| NFR6 | Portability | Swapping CSV files for a real database must not change the matching engine |

---

## 8. System architecture

```
                    USER
                      |
              [ frontend/ ]      Streamlit screens
                      |
              [ ai/ ]            Reads the request, writes the message
                      |
              [ backend/ ]       Compatibility, filters, scoring
                      |
              [ data/ ]          Donors, blood banks, hospitals
                      |
                   RESULTS
```

`app.py` sits above these four layers and calls them in order. No layer calls
the layer above it. This keeps each module testable on its own.

### Request journey

1. User submits a request, by form or in plain words.
2. The AI layer extracts blood group, urgency and city.
3. The backend removes incompatible, unavailable and ineligible donors.
4. The backend scores and sorts the remaining donors.
5. The service layer looks up blood banks and emergency hospitals.
6. The AI layer writes the donor message.
7. The frontend displays the ranked list, the message and the fallback options.

---

## 9. Data model

### donors.csv

| Field | Type | Purpose |
|---|---|---|
| donor_id | text | Unique reference |
| name | text | Display name |
| blood_group | text | One of the eight groups |
| available | true or false | Donor is free right now |
| eligible | true or false | Donor has no known bar to donating |
| distance_km | number | Distance from the request location |
| city | text | Donor city |
| contact | text | Phone number, hidden until the donor accepts |
| last_donation_days | number | Days since the last donation |

### blood_banks.csv

| Field | Type | Purpose |
|---|---|---|
| bank_id | text | Unique reference |
| name | text | Blood bank name |
| blood_groups_available | list | Groups currently in stock |
| location | text | City |
| available_units | number | Units held |
| contact | text | Phone number |
| open_24h | true or false | Round the clock service |

### hospitals.csv

| Field | Type | Purpose |
|---|---|---|
| hospital_id | text | Unique reference |
| name | text | Hospital name |
| location | text | City |
| contact | text | Phone number |
| emergency_available | true or false | Emergency unit is open |
| beds_free | number | Emergency beds free |

All data in version 1.0 is demo data. No real person is listed.

---

## 10. Matching logic specification

### 10.1 Compatibility

The system uses the standard recipient to donor table. This is fixed code, not
a model output.

| Patient group | Can receive from |
|---|---|
| A+ | A+, A-, O+, O- |
| A- | A-, O- |
| B+ | B+, B-, O+, O- |
| B- | B-, O- |
| AB+ | all eight groups |
| AB- | A-, B-, AB-, O- |
| O+ | O+, O- |
| O- | O- |

### 10.2 Filters

A donor must pass all five checks to be scored:

1. Blood group is compatible with the patient.
2. Donor is marked available.
3. Donor is marked eligible.
4. At least 90 days have passed since the donor last gave blood.
5. The donor is within the 150 km search radius of the patient city.

### 10.2b Geography

`geo.py` holds the coordinates of 47 Pakistani cities covering all four
provinces, Islamabad, Azad Kashmir and Gilgit-Baltistan. Distance between two
cities is calculated with the haversine formula at run time.

A donor record stores only the local distance inside their own city. The service
layer adds the city to city distance on top, so the same donor file works for a
patient searching from any city. The matching engine is unchanged: it still reads
one `distance_km` value.

Donors past 150 km are dropped, because someone that far away cannot help in an
emergency. Blood banks and hospitals use a wider 400 km radius, because a hospital
will send a vehicle for units when no donor is available.

### 10.3 Scoring

Each donor receives a score out of 100 built from three parts.

| Part | Range | Rule |
|---|---|---|
| Match | 70 to 100 | Same group scores 100. Compatible but different group scores 70 |
| Distance | 0 to 100 | 0 km scores 100. 25 km or more scores 0. Linear in between |
| Readiness | 40 to 100 | 365 days or more since last donation scores 100. Under 120 days scores 40 |

### 10.4 Urgency weights

Urgency does not add points. It changes how much each part counts.

| Urgency | Match | Distance | Readiness | Effect |
|---|---|---|---|---|
| High | 30% | 50% | 20% | The nearest safe donor rises to the top |
| Medium | 40% | 35% | 25% | Balanced |
| Low | 50% | 20% | 30% | The best group match wins even if further away |

This was a deliberate design decision. An earlier version added flat urgency
points to every donor, which meant urgency changed nothing about the order.
The weighted version makes urgency actually affect the result.

---

## 11. AI component specification

### In scope for the AI

| Function | Input | Output |
|---|---|---|
| analyze_request | A sentence in English or Roman Urdu | Blood group, urgency, location |
| generate_donor_message | Donor name, group, urgency, place | A short polite request message |
| explain_match | A ranked donor record | One sentence explaining the ranking |

### Out of scope for the AI

The AI must never:

- Decide which blood group can be given to which patient.
- Judge whether a donor is medically fit.
- Change the ranking or the score.
- Replace the final check by a qualified blood bank.

Blood compatibility is a fixed table in `backend/matching.py`. A language model
can produce a wrong answer that sounds confident. A fixed table cannot. In a
medical application this separation is the most important design rule in the
product.

### Provider strategy

The system tries three options in order:

1. Groq Llama 3.1, if a Groq key is present.
2. Hugging Face Inference API, if a Hugging Face token is present.
3. Rule based keyword extraction, if neither is available.

The third option means the product works with no API key, no quota and no
internet for the AI step. The search still returns correct results. This was
built on purpose so that a network failure during judging does not break the demo.

---

## 12. Safety, privacy and ethics

| Area | Decision |
|---|---|
| Medical decisions | Compatibility is fixed code. The AI never decides it |
| Final clearance | Every screen states that a blood bank must confirm the donor |
| Personal data | Demo data only. No real donor is listed in version 1.0 |
| Contact details | Donor phone numbers stay hidden until the donor accepts |
| Secrets | API keys live in a local `.env` file, never in the repository |
| Scope | The product never gives medical advice or dosage information |

---

## 13. Technology stack

| Layer | Tool | Cost |
|---|---|---|
| Interface | Streamlit | Free |
| Hosting | Streamlit Community Cloud | Free |
| Language model, first choice | Groq Llama 3.1 | Free tier |
| Language model, second choice | Hugging Face Inference API | Free tier |
| Matching engine | Python | Free |
| Data layer | CSV files and city coordinates | Free |
| Version control | GitHub | Free |

---

## 14. Success metrics

| Metric | Target | Result |
|---|---|---|
| Matching engine and geography tests passing | All | 36 of 36 |
| AI module tests passing | All | 10 of 10 |
| End to end demo scenarios completing | All | 5 of 5 |
| Search response time | Under 1 second | Met |
| Works with no API key | Yes | Yes |
| Cost of the stack | Zero | Zero |

---

## 15. Out of scope for version 1.0

Planned for later releases:

| Feature | Release |
|---|---|
| Real SMS and WhatsApp delivery | v1.1 |
| Live donor map with routes | v1.1 |
| Real database in place of CSV files | v1.2 |
| Donor self registration and consent flow | v1.2 |
| Blood bank stock prediction | v2.0 |
| Donor reward and recognition system | v2.0 |
| Voice request in Urdu | v2.0 |

---

## 16. Team and ownership

### Leadership

| Role | Member | Scope |
|---|---|---|
| Team Lead and Technical Lead | Anees Ahmed | Owns the project and the technical side. Architecture, module contracts, integration, end to end testing, deployment, technical readiness and the final submission. Registered team leader for the hackathon |
| Co-Lead and Submission Coordinator | Eman Fatima | Team coordination and progress tracking. Verifies member details, collects daily status from every member, and checks the final submission alongside the Team Lead |

### Development team

| Role | Member | Owns | Deliverable |
|---|---|---|---|
| Backend and Data Developer | Laiba | `backend/`, `data/` | `matching.py` and the three datasets |
| AI and LLM Developer | Fizza Fatima | `ai/` | `ai_module.py`, prompts, provider fallback |
| Frontend Developer | Iqra Batool | `frontend/` | `ui_components.py`, every Streamlit screen |
| Project Manager and Pitch Lead | Mehwish | `docs/`, submission material | Research, this document, slides, demo video |

### Working rule

One person, one primary folder. A member who needs to change a file outside their
own folder asks the owner first. This kept six first time collaborators working
in parallel without merge conflicts.

---

## 17. Risks

| Risk | Impact | Action taken |
|---|---|---|
| API quota runs out or internet fails during judging | Demo breaks | Rule based fallback built in. The app runs with no key |
| A language model gives a wrong compatibility answer | Patient safety | Compatibility moved out of the AI into fixed code |
| Six beginners editing the same files | Merge conflicts, lost work | One owner per folder, agreed before any code was written |
| Members blocked waiting for each other | Lost hours | Each module built against a fixed contract, testable alone |
| Scope creep into maps, SMS and chatbots | MVP never finishes | Extra features frozen until the core worked end to end |
| Demo data mistaken for real donor data | Trust and privacy | Stated on the interface, in the README and in this document |

---

## 18. Milestones

| Step | Work | Status |
|---|---|---|
| 1 | Repository structure and demo datasets | Done |
| 2 | Matching engine with tests | Done |
| 3 | AI request reader with fallback | Done |
| 4 | Streamlit interface | Done |
| 5 | Full integration in `app.py` | Done |
| 6 | Blood bank and hospital fallback, nationwide coverage | Done |
| 7 | Automated tests, 51 checks passing | Done |
| 8 | Deploy to Streamlit Community Cloud | Done |
| 9 | Slides, PRD and demo video | In progress |
| 10 | Final submission | 13 September 2026, 11:59 PM PKT |

---

## 19. Submission links

| Item | Link |
|---|---|
| Live app | https://bloodbridge-ai-pk.streamlit.app/ |
| Code repository | see the hackathon registration form |
| Presentation slides | see the hackathon registration form |
| This document | see the hackathon registration form |
| Presentation video | see the hackathon registration form |

---

*BloodBridge AI is a hackathon prototype. It uses demo data. A qualified blood
bank must confirm every donor before any donation takes place.*
