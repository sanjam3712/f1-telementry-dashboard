# 🏎️ F1 Telemetry Dashboard with AI Predictions

An interactive **Formula 1 telemetry dashboard** built with Python that visualizes race data and uses **machine learning to predict lap performance**.

This project fetches real telemetry data and displays interactive charts to analyze driver performance, race pace, and tyre strategies.

---

# ✨ Features

📊 **Telemetry Visualization**

* Speed trace across the track
* Lap time comparisons
* Tyre strategy analysis

🧠 **AI Lap Time Prediction**

* Machine learning model predicts lap performance using telemetry data
* Uses features such as speed, throttle, and brake usage

🏁 **Driver Performance Analysis**

* Compare drivers across laps
* Analyze race pace trends

🗄️ **Telemetry Data Storage**

* Data stored in a local SQLite database

📈 **Interactive Charts**

* Built using Python visualization libraries

---

# 🧰 Tech Stack

Python
FastF1 API
Pandas
Scikit-learn
SQLite
Plotly / Dash
Flask

---

# 📂 Project Structure

f1-telemetry-dashboard
│
├── charts
│   ├── lap_times.py
│   ├── speed_trace.py
│   └── tyre_strategy.py
│
├── data
│   └── f1_telemetry.db
│
├── sql
│   └── database.py
│
├── utils
│   └── fetcher.py
│
├── ai_model.py
├── main.py
├── requirements.txt
└── README.md

---

# 🧠 Machine Learning Model

This project includes a **Random Forest regression model** that predicts lap time using telemetry data.

Features used by the model:

* Average Speed
* Maximum Speed
* Throttle Usage
* Brake Usage

The model is trained using historical telemetry extracted from race sessions.

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/sanjam3712/f1-telementry-dashboard.git
cd f1-telementry-dashboard
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the dashboard

```bash
python main.py
```

---

# 📊 Example Dashboard Insights

The dashboard allows users to explore:

• Driver lap time comparisons
• Speed traces throughout the circuit
• Tyre degradation and strategy insights
• AI-predicted lap performance

---

# 🔮 Future Improvements

Real-time race telemetry integration

Overtake probability prediction

Driver performance ranking using machine learning

Race strategy simulator

Live race analytics dashboard

---

# 👨‍💻 Author

**Sanjam Bedi**

Engineering Student
Electronics and Computer Engineering
Motorsport Analytics Enthusiast

---

