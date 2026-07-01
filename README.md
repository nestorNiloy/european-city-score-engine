# 🏙️ European City Score Engine

> Which European city is the best fit for you — based on data, not gut feeling?

**🔴 Live Demo: [european-city-score-engine.streamlit.app](https://european-city-score-engine.streamlit.app)**

A data-driven web application that ranks top European tech cities using live job market data and multi-factor scoring. Users adjust priority weights interactively and watch the rankings update in real time.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red?logo=streamlit)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-lightblue?logo=plotly)
![Adzuna API](https://img.shields.io/badge/Adzuna-Live%20Jobs%20API-green)

---

## 🔍 What It Does

Most "best city to live in" rankings are static, opinionated, and impossible to personalize. This tool fixes that.

It pulls **live tech job listings** from the Adzuna API, combines them with cost of living, safety, and internet speed indices, and computes a **weighted score** for each city — with weights you control via sliders.

Change what matters to you → rankings update instantly.

---

## 📊 Factors & Data Sources

| Factor | Weight (default) | Source | Type |
|---|---|---|---|
| 💼 Tech Job Market | 35% | Adzuna API | Live |
| 💰 Cost of Living | 30% | Numbeo 2024 | Static |
| 🛡️ Safety Index | 20% | Numbeo 2024 | Static |
| 🌐 Internet Speed | 15% | Ookla Speedtest 2024 | Static |

**Cities compared:** Berlin · Munich · Amsterdam · Vienna · Zurich

---

## 🧠 How Scoring Works

Each factor is normalized to a 0–100 scale using min-max normalization:

- Higher job count → higher score
- Lower cost of living → higher score (inverted)
- Higher safety index → higher score
- Higher internet speed → higher score

Final score = weighted sum of all normalized factor scores.

---

## 🚀 Features

- **Live data** — job counts fetched in real time from Adzuna API
- **Interactive sliders** — adjust factor weights, rankings update instantly
- **Radar chart** — visualize each city's strengths and weaknesses at a glance
- **Bar chart** — compare final scores side by side
- **Raw data view** — full transparency on underlying numbers
- **Weight validation** — app enforces weights must sum to 100

---

## 🗂️ Project Structure

european-city-score-engine/
├── app.py                  # Streamlit app — UI, charts, layout
├── requirements.txt        # Dependencies
├── data/
│   ├── fetcher.py          # Adzuna API calls + static data
│   └── scorer.py           # Normalization + weighted scoring logic

---

## ⚙️ Run Locally

```bash
git clone https://github.com/nestorNiloy/european-city-score-engine
cd european-city-score-engine
pip install -r requirements.txt
streamlit run app.py
```

---

## 🔑 API Key Setup

This project uses the [Adzuna API](https://developer.adzuna.com) for live job data.

1. Register for a free key at developer.adzuna.com
2. Create a `.env` file in the root directory:
ADZUNA_APP_ID=your_app_id_here
ADZUNA_APP_KEY=your_app_key_here

---

## 📌 Potential Extensions

- Add more cities (Paris, Stockholm, Barcelona)
- Add weather/climate as a factor
- Pull cost of living data live via Numbeo API
- Add a "Your Profile" mode — student vs senior engineer vs family
- Deploy with Docker

---

*Built with Python · Streamlit · Plotly · Adzuna API*
