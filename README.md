# Gate-Pass-Log-Analyzer
An AI-powered web application for analyzing CISF gate pass logs. It provides interactive dashboards, generates security insights, and detects anomalous entry/exit patterns , purpose of visiting , peak traffic hours on each gate using machine learning.

# ✨ Features

- 📂 Upload gate pass logs in Excel format
- 📊 Interactive analytics dashboard
- 🚪 Gate-wise visitor analysis
- ⏰ Peak traffic hour detection on each gate
- 📅 Traffic trends
- 🏢 Department-wise visitor insights
- 🚗 Vehicle type distribution
- 🤖 AI-powered purpose categorization using NLP
- 🚨 Machine Learning-based anomaly detection
-📑 Export reports (Excel/PDF)

  ## 📊 Dashboard

The dashboard provides:

- Total Entries & Exits
- Visitor Statistics
- Gate-wise Analysis
- Department-wise Analysis
- Peak Traffic Hours
- Hourly Visitor Distribution
- Purpose Distribution
- Vehicle Analysis
- Anomaly Summary
- ## 📂 Project Structure

```text
Gate-Pass-Log-Analyzer/
│
├── app.py
├── requirements.txt
├── README.md
│
├── database/
│   ├── db.py
│   └── schema.sql
│
├── pages/
│   ├── Dashboard.py
│   ├── Traffic_Analysis.py
│   ├── Purpose_Analysis.py
│   ├── Anomaly_Detection.py
│   └── Reports.py
│
├── models/
│   ├── purpose_classifier.py
│   ├── anomaly_detector.py
│   └── clustering.py
│
├── utils/
│   ├── preprocess.py
│   ├── data_cleaning.py
│   ├── charts.py
│   └── report_generator.py
│
├── uploads/
├── outputs/
└── assets/
```

---

## ⚙️ Workflow

```text
           Excel Gate Pass Logs
                     │
                     ▼
              Data Cleaning
                     │
                     ▼
              MySQL Database
                     │
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
Dashboard Analytics      AI Purpose Categorization
         │                       │
         │              Sentence Embeddings
         │                       │
         ▼                       ▼
Traffic Insights      Semantic Clustering
         │                       │
         └───────────┬───────────┘
                     ▼
             Anomaly Detection
                     │
                     ▼
          Interactive Security Dashboard
```

---


## 📈 Future Enhancements

- QR Code Integration
- RFID Support
- Face Recognition-based Entry
- Email Alerts
- SMS Notifications
- Real-time Monitoring
- Predictive Visitor Forecasting
- LLM-powered Natural Language Search

---

## 💡 Use Cases

- Manufacturing Plants
- Corporate Offices
- Government Organizations
- Educational Institutions
- Industrial Facilities
- Research Campuses





