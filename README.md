# 🛡️ AML Intelligent Transaction Monitoring Dashboard

An **Anti-Money Laundering (AML)** transaction monitoring system built with **XGBoost + SHAP** using the PaySim synthetic dataset.

This project demonstrates a modern RegTech solution that combines high-performance fraud detection with **explainable AI**, effectively addressing the high false positive rate problem of traditional rule-based AML systems.

---

## ✨ Key Features

- **High-Performance Detection**: XGBoost model with PR-AUC of **0.9945**
- **Explainable AI**: SHAP values provide clear explanations for every high-risk alert
- **Significantly Lower False Positives**: Much higher Precision compared to traditional rules
- **Interactive Web Dashboard**: Built with Streamlit for easy testing and demonstration
- **Rich Visualizations**: Risk trends, transaction type analysis, and distribution charts
- **Export Functionality**: One-click download of high-risk alert lists

---

## 📊 Model Performance (PaySim Test Set)

| Metric               | Traditional Rule-based | XGBoost Model     |
|----------------------|------------------------|-------------------|
| Precision            | 0.0239                 | **0.95**          |
| Recall               | 0.9656                 | **0.98**          |
| F1-Score             | 0.0466                 | **0.96**          |
| PR-AUC               | -                      | **0.9945**        |

---

## 🚀 Dashboard Features

- Real-time risk scoring for uploaded transaction data
- High-risk alert list with one-click CSV download
- Interactive visualizations (24-hour risk pattern, transaction type risk, risk score distribution)
- SHAP explainability for individual high-risk transactions

---

## 🛠️ How to Run Locally

### Prerequisites
```bash
pip install streamlit pandas joblib shap matplotlib numpy scikit-learn xgboost
