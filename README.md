<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:1B4F8A,100:2E75B6&height=180&section=header&text=K%20Nagashivashankar&fontSize=46&fontColor=ffffff&fontAlignY=40&animation=fadeIn" width="100%" alt="K Nagashivashankar" />
</p>

<p align="right">
  <a href="https://linkedin.com/in/knagashivashankar"><img src="https://skillicons.dev/icons?i=linkedin" height="28" alt="LinkedIn" /></a>
  <a href="mailto:nagashivashankar0410@gmail.com"><img src="https://skillicons.dev/icons?i=gmail" height="28" alt="Email" /></a>
</p>

<p align="center">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=500&size=20&duration=3000&pause=1000&color=2E75B6&center=true&vCenter=true&width=650&lines=Building+AI+that+knows+when+not+to+answer;Lead+developer+of+PHOENIX+%C2%B7+IEEE+TDSC+(under+review);AI+agents+%C2%B7+Retrieval+%C2%B7+Backend+systems;Open+to+2027+internships" alt="Typing animation" />
</p>

## About me

- CS undergrad at **KMIT, Hyderabad**
- I build AI that checks its own work, and says *"I don't know"* when it can't
- Lead developer and corresponding author of **PHOENIX**, a verify-or-abstain system for financial QA *(under review, IEEE TDSC)*
- Led the team behind **Precedent**, an accounts-payable agent that learns from every invoice it resolves
- Lead Organizer, **GDG on Campus KMIT**

## Projects

### Precedent
*The accounts-payable agent that learns from every invoice exception it resolves*

<img src="assets/precedent.svg" width="100%" alt="Precedent: an invoice is matched, checked against hard controls, compared with past cases and approved" />

Finance teams resolve the same invoice problems again and again, and the know-how sits in a few clerks' heads. Precedent checks each invoice against its purchase order and goods receipt, recalls how the team handled similar cases, and recommends a decision with those past cases as proof. Duplicate invoices, bank-detail changes, GSTIN, e-invoice IRN, new vendors and approval limits are enforced in code the AI can never override, and it only acts on its own once it has statistically earned that autonomy.

**Results:** 98% match with the clerk's decision with memory vs. 50% without · 0 wrong payments in a 26-week replay · $17 per 1,000 cases, 2.7 s median<br>
**Built with:** Python · FastAPI · Hindsight · Gemini · scikit-learn · React · Docker<br>
**Role:** Team leader · backend, AI and memory (4-member team)

[Live demo](https://precedent-ap.onrender.com) · [Code](https://github.com/Eldorado5002/Claude_Coders4)

<br>

### IUPMS: Smart Parking System
*Real-time parking management with computer vision and IoT*

<img src="assets/iupms.svg" width="100%" alt="IUPMS: cars are detected at the gate, the ESP32 opens it, and slots update as cars park and leave" />

A camera running YOLOv8 and DeepSORT detects and tracks each arriving vehicle, and PaddleOCR reads its number plate. The decision goes over MQTT to an ESP32 that opens the gate, while IR sensors track every slot and a React/Node portal shows live availability and reservations.

**Results:** 30 FPS detection · under 500 ms gate response · 6-slot hardware prototype<br>
**Built with:** Python · YOLOv8 · DeepSORT · PaddleOCR · ESP32 (MicroPython) · MQTT · MongoDB · React · Node.js

[Live demo](https://team99parking.onrender.com/) · [Code](https://github.com/Eldorado5002/Team99) · [Video](https://www.youtube.com/watch?v=3aC8Mt1YaYg)

<br>

### PHOENIX
*Evidence-grounded verify-or-abstain for financial question answering*

<img src="assets/phoenix.svg" width="100%" alt="PHOENIX: answers only when every figure is sourced and the math checks out, otherwise abstains" />

Language models answering questions on financial filings often return confident wrong numbers. PHOENIX answers only when every figure is tied to a quoted source in the filing and the arithmetic is recomputed exactly; otherwise it abstains instead of guessing. I also built PHOENIX-IN, a 142-question benchmark on 24 Indian annual reports.

**Results:** silent wrong answers 16.8% → 5.0% on DocFinQA (open-weight model) · caught 359 of 360 injected unsupported figures · tested on 4 benchmarks and 2 model families<br>
**Built with:** Python · LangGraph · Qdrant · BGE-M3 · Gemini · Nemotron<br>
**Status:** paper under review at IEEE TDSC · code private

## Tech stack

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,java,c,cpp,js,ts,fastapi,flask,redis,postgres,mysql,mongodb,docker,gcp,aws,git,linux,sklearn&perline=9" alt="Tech stack" />
</p>

<p align="center"><sub><b>AI &amp; retrieval:</b> RAG · hybrid search · cross-encoder reranking · LangGraph · Qdrant · BGE-M3 · Gemini · Vertex AI</sub></p>

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/Eldorado5002/Eldorado5002/output/github-snake-dark.svg" />
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/Eldorado5002/Eldorado5002/output/github-snake.svg" />
    <img alt="Contribution snake animation" src="https://raw.githubusercontent.com/Eldorado5002/Eldorado5002/output/github-snake.svg" />
  </picture>
</p>

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2E75B6,100:1B4F8A&height=120&section=footer" width="100%" alt="" />
</p>
