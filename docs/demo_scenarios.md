# BloodBridge AI - Demo Scenarios

Run these four in front of the judges, in this order.

## 1. The normal emergency

Type: `My brother urgently needs B+ blood near Nawabshah`

Shows: AI reads B+, high, Nawabshah. Ali Raza comes first at 2.5 km with score 91.
Point out that Bilal Shaikh is closer at 1.2 km but was correctly dropped, because
he is marked unavailable.

## 2. Urgency changes the answer

Switch the same request to low urgency.

Shows: the ranking moves. Low urgency prefers the exact group match. High urgency
prefers the nearest donor. The urgency slider is not decoration.

## 3. The hard case

Type: `Accident, AB negative khoon foran chahiye Daur mein`

Shows: Roman Urdu works. AB- is rare, so the system correctly offers A-, B- and O-
donors instead of failing.

## 4. Nobody is available

Search for a group with no eligible donor nearby.

Shows: instead of an empty screen, the app lists blood banks holding usable stock
and emergency hospitals with free beds.

## The line to say

"The AI reads the request and writes the message. The medical decision is fixed
rule based code, because a language model should never decide who can receive blood."
