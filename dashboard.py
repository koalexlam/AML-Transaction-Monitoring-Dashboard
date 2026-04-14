# ==================== AML Intelligent Monitoring Dashboard - Final Version ====================

import streamlit as st
import pandas as pd
import joblib
import shap
import matplotlib.pyplot as plt

st.set_page_config(page_title="AML Intelligent Monitor", layout="wide")

# ====================== 載入模型 ======================
@st.cache_resource
def load_assets():
    try:
        model = joblib.load('./xgboost_aml_model.pkl')
        explainer = shap.TreeExplainer(model)
        return model, explainer
    except Exception as e:
        st.error(f"❌ 模型載入失敗: {e}")
        st.stop()

model, explainer = load_assets()

# ====================== 特徵工程 ======================
def feature_engineering(df):
    df = df.copy()
    df['hour'] = df['step'] % 24
    df['day'] = df['step'] // 24
    df['amount_ratio'] = df['amount'] / (df['oldbalanceOrg'] + 1e-9)
    df['balance_change_orig'] = df['newbalanceOrig'] - df['oldbalanceOrg']
    df['balance_change_dest'] = df['newbalanceDest'] - df['oldbalanceDest']
    
    df['orig_tx_count'] = df.groupby('nameOrig')['nameOrig'].transform('count')
    df['dest_tx_count'] = df.groupby('nameDest')['nameDest'].transform('count')
    
    type_map = {'CASH_IN': 0, 'CASH_OUT': 1, 'DEBIT': 2, 'PAYMENT': 3, 'TRANSFER': 4}
    df['type_num'] = df['type'].map(type_map).fillna(4)
    return df

# ====================== 主介面 ======================
st.title("🛡️ AML Intelligent Transaction Monitoring Dashboard")
st.markdown("**XGBoost + SHAP 可解釋 AI** | PaySim 資料集示範")

uploaded_file = st.file_uploader("上傳交易資料 (PaySim 格式 CSV)", type=["csv"])

if uploaded_file:
    df_raw = pd.read_csv(uploaded_file)
    
    with st.spinner("正在進行深度分析..."):
        df = feature_engineering(df_raw)
        feature_cols = ['amount', 'oldbalanceOrg', 'newbalanceOrig', 'oldbalanceDest', 
                        'newbalanceDest', 'hour', 'day', 'amount_ratio', 
                        'balance_change_orig', 'balance_change_dest', 
                        'orig_tx_count', 'dest_tx_count', 'type_num']
        
        X = df[feature_cols]
        proba = model.predict_proba(X)[:, 1]
        df['risk_score'] = (proba * 100).round(2)
        df['is_fraud_pred'] = (proba >= 0.5).astype(int)

    # KPI
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("總交易筆數", f"{len(df):,}")
    c2.metric("高風險警報", f"{df['is_fraud_pred'].sum():,}", delta_color="inverse")
    c3.metric("警報率", f"{df['is_fraud_pred'].mean()*100:.2f}%")
    c4.metric("平均風險分數", f"{df['risk_score'].mean():.1f}")

    # 高風險警報
    st.subheader("🚨 高風險警報清單 (Top 30)")
    alerts = df[df['is_fraud_pred'] == 1].sort_values('risk_score', ascending=False).head(30)
    
    st.dataframe(
        alerts[['step', 'type', 'amount', 'nameOrig', 'nameDest', 'risk_score']].reset_index(drop=True),
        use_container_width=True,
        hide_index=True
    )

    # 下載按鈕
    if not alerts.empty:
        csv = alerts.to_csv(index=False).encode('utf-8')
        st.download_button("📥 下載高風險警報清單", csv, "AML_High_Risk_Alerts.csv", "text/csv")

    # 圖表分析
    st.subheader("📊 分析圖表")
    tab1, tab2, tab3 = st.tabs(["時間風險分佈", "交易類型風險", "風險分數分佈"])

    with tab1:
        hour_risk = df.groupby('hour')['risk_score'].mean()
        st.line_chart(hour_risk, x_label="Hour of Day", y_label="Average Risk Score")
        st.caption("凌晨時段風險明顯升高，為典型洗錢行為特徵")

    with tab2:
        type_risk = df.groupby('type')['risk_score'].mean()
        st.bar_chart(type_risk, x_label="Transaction Type", y_label="Average Risk Score")

    with tab3:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.hist(df['risk_score'], bins=50, color='#1f77b4', edgecolor='black', alpha=0.8)
        ax.set_xlabel("Risk Score (0-100)")
        ax.set_ylabel("Number of Transactions")
        ax.set_title("Risk Score Distribution")
        ax.set_yscale('log')
        st.pyplot(fig)
        plt.close(fig)
        st.caption("大多數交易風險接近 0，只有少數交易被判定為高風險")

    # SHAP 分析
    st.subheader("🔍 SHAP 可解釋性分析")
    fraud_cases = df[df['is_fraud_pred'] == 1].reset_index(drop=True)
    if not fraud_cases.empty:
        idx = st.selectbox("選擇一筆高風險交易進行解釋", fraud_cases.index,
                           format_func=lambda i: f"Risk Score: {fraud_cases.iloc[i]['risk_score']:.1f} | Type: {fraud_cases.iloc[i]['type']}")
        
        if st.button("產生 SHAP 解釋"):
            with st.spinner("正在計算 SHAP 值..."):
                row = fraud_cases.iloc[[idx]]
                X_row = row[feature_cols]
                shap_values = explainer.shap_values(X_row)
                
                fig = plt.figure(figsize=(12, 8))
                shap.plots.waterfall(shap.Explanation(
                    values=shap_values[0],
                    base_values=explainer.expected_value,
                    data=X_row.iloc[0],
                    feature_names=feature_cols
                ), max_display=12, show=False)
                st.pyplot(fig)
                plt.close(fig)
    else:
        st.info("目前無高風險交易可供 SHAP 分析。")

else:
    st.info("👈 請在上方上傳 PaySim 格式的交易 CSV 檔案開始分析")