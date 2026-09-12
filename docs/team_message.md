# Message to send in the team group

Copy this as it is.

---

Assalam o Alaikum team.

Core system ready hai aur chal raha hai. Ab har member ko apna module verify karna hai.
Repo clone karo, `pip install -r requirements.txt` chalao, phir `streamlit run app.py`.

**Laiba** - `backend/matching.py` aur `data/` tumhare hain.
Chalao: `python tests/test_matching.py`. 25 checks pass hone chahiye.
Tumhara kaam: donors.csv mein 25 se 40 donors karo, aur naye test cases add karo.
Urgency wali problem fix ho chuki hai. Ab high urgency distance ko 50% weight deti hai,
low urgency blood group match ko 50% deti hai. Code parh ke samajh lo, judges pooch sakte hain.

**Fizza** - `ai/ai_module.py` tumhara hai.
Chalao: `python tests/test_ai.py`. 10 checks pass hone chahiye.
Abhi offline rules chal rahe hain. Tum apni free Groq key `.env` mein daalo aur dobara test karo.
Key kisi ko mat bhejo, GitHub par mat daalo. Tumhara kaam: prompt ko behtar karo aur
5 aur Roman Urdu sentences test karo.

**Iqra** - `frontend/ui_components.py` tumhara hai.
App chala kar dekho. Har screen ek chhota function hai. Tumhara kaam: colors, spacing,
aur donor card ka design behtar karo. Matching logic ko haath mat lagana, sirf display.
Screenshot bhej dena `assets/screenshots/` ke liye.

**Mehwish** - `docs/` tumhara hai.
`architecture.md` aur `demo_scenarios.md` parh lo, sab kuch wahan likha hai.
Tumhara kaam: problem statement mein Pakistan ke real numbers add karo, aur pitch deck
ko workflow slides ke upar banao.

**Eman** - daily status collect karna hai. Har member se sirf yeh 5 lines:
DONE / FILES / TESTED / BLOCKER / NEED FROM.

**Rule** - apne folder ke bahar kuch mat badlo. Kisi aur ki file change karni ho to
pehle mujhse poocho. Is se merge conflict nahi hoga.

Abhi koi naya feature start nahi karna. Pehle sab apna module verify karo, phir
Hugging Face Spaces par deploy karenge.
