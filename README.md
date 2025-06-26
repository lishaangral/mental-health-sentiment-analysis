# Mental Health Sentiment Analysis Project

A privacy-focused, real-time screen sentiment monitoring tool that uses **OCR + RoBERTa Transformer** to detect emotional signals from your screen and helps you reflect, react and improve your mental well-being.

![Mental Health Sentiment Monitor](https://user-images.githubusercontent.com/your-image-link.png)

---

## 📑 Index

- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [How to Use](#-how-to-use)
  - [Use on Local Machine](#use-on-local-machine)
  - [Use on Deployed App](#use-on-deployed-app)
- [Dashboard Preview](#-dashboard-preview)
- [Future Endeavors](#-future-endeavors)
- [Datasets & Resources Used](#-datasets--resources-used)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [License](#-license)

---

## Features

- **Screen-based OCR Monitoring** – captures screen content, runs it through `pytesseract`, and analyzes emotions using a fine-tuned RoBERTa model.
- **Thought Text Check-in** – users can manually enter their thoughts and receive sentiment analysis feedback.
- **Interactive Dashboard** – view emotion trends, app usage, and scores over time.
- **Customizable Notifications** – get notified when distress is detected or during daily check-ins.
- **Sentiment Control Exercises** – calming tools like breathing timers, music, videos, and mindfulness activities.
- **User Preferences** – change monitored apps, enable/disable features, and set log retention period.
- **Log Cleanup** – auto-delete older logs based on retention settings.

---

## Tech Stack

| Layer         | Tech                                                            |
|---------------|-----------------------------------------------------------------|
| Frontend      | Streamlit                                                       |
| NLP Model     | HuggingFace Transformers (RoBERTa-base fine-tuned)              |
| OCR           | pytesseract + PIL                                               |
| Data Logging  | JSONL Logs + Local File Storage                                 |
| Background    | Python threading, pygetwindow, ImageGrab                        |
| Notifications | plyer (desktop-based), customizable triggers                    |
| Deployment    | Streamlit Cloud (for web-based features only)                   |

---

## How to Use

### Use on Local Machine

> 🔒 Recommended if you want **real-time screen monitoring**.

1. **Clone the repository**
```bash
git clone https://github.com/your-username/mental-health-sentiment-analysis.git
cd mental-health-sentiment-analysis
````

2. **Create & activate virtual environment (optional but recommended)**

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the app**

```bash
cd app
streamlit run streamlit_app.py
```

### 🌐 Use on Deployed App (Streamlit Cloud)

> Works for Thought Input, Dashboard, and Sentiment Tools
> Screen monitoring & desktop notifications **do not** work here

1. Visit the hosted URL (e.g. [Streamlit Link](https://mental-health-sentiment-analysis.streamlit.app/))

2. Try features like:

   * Thought input
   * Dashboard
   * Sentiment Control page
   * Preferences

3. **Note:** To use the full monitoring system, run locally (see above).

---

## Dashboard Preview

Features:

* Emotion variation over 24 hours
* App-wise sentiment logs
* Daily insights and key takeaways
* Emotion score charts
* Smart warning messages with coping suggestions

---

## Future Endeavors

* Android/iOS app for passive mood tracking
* Emotion comparison across weeks/months
* More fine-tuning with psychology and mental health texts
* Gamification of mental health check-ins
* Plugin support for browser/emails to extend monitoring

---

## Datasets & Resources Used

Fine-tuned on:

* [The Diagnostic and Statistical Manual of Mental Disorders (DSM-5)](https://psychiatryonline.org/doi/book/10.1176/appi.books.9780890425787)
* [Kaggle: Sentiment Analysis for Mental Health](https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health)

These sources provided diverse and labeled emotional data (stress, suicidal ideation, support-seeking, etc.) for supervised training.

---

## 🧾 License

MIT License © 2025 \[Lisha Angral]

```

