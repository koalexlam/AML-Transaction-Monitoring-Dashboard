# 🛡️ AML Intelligent Transaction Monitoring Dashboard

**An Anti-Money Laundering (AML) transaction monitoring system built with XGBoost + SHAP using the PaySim synthetic dataset.**

This project demonstrates a modern RegTech solution that combines high-accuracy fraud detection with explainable AI, effectively solving the high false positive rate problem common in traditional rule-based AML systems.

## Key Features
- High-performance fraud detection with XGBoost (**PR-AUC: 0.9945**)
- Full explainability using SHAP values for every high-risk alert
- Significantly improved Precision compared to traditional rules
- Interactive Streamlit web dashboard for easy demonstration
- Rich visualizations and one-click alert export
- Clean, production-ready code structure

## Model Performance (PaySim Test Set)

| Metric       | Traditional Rule-based | XGBoost Model |
|--------------|------------------------|---------------|
| Precision    | 0.0239                 | **0.95**      |
| Recall       | 0.9656                 | **0.98**      |
| F1-Score     | 0.0466                 | **0.96**      |
| PR-AUC       | -                      | **0.9945**    |

## Dataset

This project uses the **PaySim** synthetic financial transaction dataset for training and evaluation.

- **Data Source**: PaySim simulator-generated synthetic mobile money transactions (modeled after real mobile money transaction behavior)
- **Dataset Characteristics**:
  - Approximately **6,000,000** transaction records
  - Simulates realistic money laundering behaviors
  - Includes key fields such as `step`, `type`, `amount`, `nameOrig`, `oldbalanceOrg`, `newbalanceOrig`, `nameDest`, `oldbalanceDest`, `newbalanceDest`, `isFraud`, and `isFlaggedFraud`
- **Why Synthetic Data?**  
  Real bank transaction data is rarely released publicly due to privacy and regulatory restrictions. PaySim is one of the most widely used public benchmark datasets in the AML research community.

> Original dataset and paper: [PaySim on Kaggle](https://www.kaggle.com/datasets/ealaxi/paysim1)

The model was trained on **80%** of the data, with the remaining **20%** used as the test set.

## Dashboard Features
- Real-time risk scoring after uploading transaction data
- High-risk alert list with one-click CSV download
- Multiple insightful visualizations (24-hour risk pattern, transaction type risk, risk score distribution)
- SHAP explainability analysis for individual transactions

## How to Run Locally

### Prerequisites
- Python 3.10 or 3.11

### Installation & Run

1. Clone the repository
   ```bash
   git clone https://github.com/koalexlam/AML-Transaction-Monitoring-Dashboard.git
   cd AML-Transaction-Monitoring-Dashboard Bash

2. Install dependenciesBash
   ```bash
   pip install -r requirements.txt

3. Run the dashboardBash
   ```bash
   python -m streamlit run dashboard.py

Or simply double-click start_dashboard.bat (Windows only)

## Project Structure

```text
AML-Transaction-Monitoring-Dashboard/
├── dashboard.py                    # Main Streamlit application
├── xgboost_aml_model.pkl           # Trained XGBoost model (large file)
├── requirements.txt                # List of required packages
├── start_dashboard.bat             # One-click launcher for Windows
├── README.md
└── images/                         # Screenshots (optional)
```

> Note: The model file `xgboost_aml_model.pkl` is quite large. You can also download it from Google Drive if needed.

## Project Highlights
1. Successfully applied Machine Learning to the financial compliance (RegTech) domain
2. Solved the high false positive issue in traditional AML systems
3. Implemented Explainable AI (XAI), which is crucial for regulatory acceptance
4. End-to-end development: data processing → feature engineering → modeling → visualization → interactive UI
