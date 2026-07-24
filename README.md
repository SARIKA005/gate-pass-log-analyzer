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
Gate-Pass-Log-Analyzer/
│
├── app.py                     # Main Streamlit app 
├── requirements.txt
├── README.md
│
├── data/                      # Sample Excel files
│   └── GatePass_Log_100.xlsx
│
├── uploads/                   # Uploaded Excel files (optional)
│
├── outputs/                   # Generated reports
│   ├── report.pdf
│   └── report.csv
│
├── utils/                     # Backend utilities 
│   ├── __init__.py
│   ├── load_data.py
│   ├── data_cleaning.py
│   ├── preprocess.py
│   ├── report_generator.py
│   └── helper.py
│
├── models/                    # AI / Analysis (Your work)
│   ├── __init__.py
│   ├── purpose_classifier.py
│   ├── anomaly_detector.py
│   └── traffic_analysis.py
│
├── pages/                     # Streamlit pages 
│   ├── Dashboard.py
│   ├── Traffic_Analysis.py
│   ├── Purpose_Analysis.py
│   ├── Anomaly_Detection.py
│   └── Reports.py
│
├── assets/
│   ├── logo.png
│   └── style.css
│
└── notebooks/                 # For experimentation only
    └── data_analysis.ipynb

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





