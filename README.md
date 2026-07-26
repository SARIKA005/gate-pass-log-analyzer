# Gate-Pass-Log-Analyzer
An AI-powered web application for analyzing  gate pass logs. It provides interactive dashboards, generates security insights, and detects anomalous entry/exit patterns , purpose of visiting , peak traffic hours on each gate using machine learning.

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
 ## 📂 Project Structure
 ```
Gate-Pass-Log-Analyzer/
│
├── Frontend/
│   ├── assets/
│   │   └── bsp_logo.jpg
│   │
│   ├── components/
│   │   └── sidebar.py
│   │
│   ├── views/
│   │   ├── ai_purpose.py
│   │   ├── anomaly.py
│   │   ├── dashboard.py
│   │   ├── entry_exit.py
│   │   ├── gate_analysis.py
│   │   ├── login.py
│   │   ├── peak_traffic.py
│   │   ├── report.py
│   │   └── upload.py
│   │
│   ├── app.py
│   ├── requirements.txt
│   └── style.py
│
├── utils/                     # Backend utilities 
│   ├── __init__.py
│   ├── load_data.py
│   ├── data_cleaning.py
│   ├── preprocess.py
│   ├── report_generator.py
│   └── helper.py
│
├── models/                    # AI / Analysis 
│   ├── __init__.py
│   ├── purpose_classifier.py
│   ├── anomaly_detector.py
│   └── traffic_analysis.py
│
└── notebooks/                 # For experimentation only
    └── data_analysis.ipynb
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
## 🔍 Machine Learning

The project applies an unsupervised anomaly detection algorithm to identify unusual visitor activities such as:

- Peak traffic hours at each gate
- Unusual entry timings
- Abnormal visitor frequency
- Suspicious movement patterns

These observations can assist security teams in prioritizing records for further review.


## 📈 Future Enhancements

- Face Recognition-based Entry
- Email Alerts
- SMS Notifications
- Real-time Monitoring
- Predictive Visitor Forecasting


---

## 💡 Use Cases

- Manufacturing Plants
- Corporate Offices
- Government Organizations
- Educational Institutions
- Industrial Facilities
- Research Campuses

⭐ If you find this project useful, consider giving it a star.



