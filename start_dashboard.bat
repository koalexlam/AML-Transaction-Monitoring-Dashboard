@echo off
title AML Anti-Money Laundering Dashboard
echo ================================================
echo    AML Transaction Monitoring Dashboard
echo    XGBoost + SHAP Explainable AI
echo ================================================
echo.
py -m streamlit run dashboard.py
pause