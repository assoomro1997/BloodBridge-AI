# BloodBridge AI - Demo Scenarios

Run these five in front of the judges, in this order. Total: about two minutes.

## 1. The normal emergency

Tab: Quick request. City Nawabshah, B+, high urgency.

Shows: Ali Raza first at 2.5 km with score 91.0. Then Shahid Sial (O+, 1.5 km, 84.0)
and Faisal Detho (B-, 2.8 km, 81.4).

The line to say: Shahid Sial is closer, but Ali Raza is an exact group match, so he
wins. Also point out Bilal Shaikh at 1.2 km, nearer than everyone, correctly dropped
because he is marked unavailable.

## 2. Urgency changes the answer

Same request, urgency switched to low.

Shows: the third place changes and the scores move. Shahid Sial drops from 84.0 to 77.8.

The line to say: urgency does not add points to everyone. It changes what the system
cares about. High urgency weights distance at 50 percent. Low urgency weights the
group match at 50 percent.

## 3. It works anywhere in Pakistan

Tab: Quick request. Change the city to Lahore, same B+ high.

Shows: a completely different donor list, all Lahore based, with Lahore blood banks
and hospitals.

The line to say: 47 cities across all four provinces, Islamabad, Azad Kashmir and
Gilgit-Baltistan. Distance is calculated from real coordinates, not stored in a file.

## 4. Roman Urdu and a rare group

Tab: AI request. Type: Accident, AB negative khoon foran chahiye Peshawar mein

Shows: the AI reads AB-, high, Peshawar. AB- is rare, so the system correctly offers
compatible A-, B- and O- donors instead of failing.

The line to say: mixed language works, and the AI only read the sentence. The
compatibility decision came from fixed code.

## 5. Nobody is available

Tab: AI request. Type: Urgent B+ blood required at Gilgit

Shows: no donor inside the search radius. Instead the app lists DHQ Blood Bank Gilgit
with usable stock, and the nearest emergency hospitals with free beds.

The line to say: the app never shows an empty screen. A patient always leaves with
somewhere to go.

## The closing line

The AI reads the request and writes the message. The medical decision is fixed
rule based code, because a language model should never decide who can receive blood.
