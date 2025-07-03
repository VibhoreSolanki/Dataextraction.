import streamlit as st
import yfinance as yf
import pandas as pd
import openpyxl
from openpyxl.utils import get_column_letter
from io import BytesIO

st.set_page_config(layout="wide", page_title="Stock Data Downloader")

st.title("📉 Yahoo Finance Stock Data Downloader")

# Dummy ticker list (shortened for brevity — replace with full)
tickers_list = [
    "ASIANPAINT.NS", "TATAMOTORS.NS", "RELIANCE.NS", "HDFCBANK.NS", "ITC.NS",
    "INFY.NS", "SBIN.NS", "ADANIENT.NS", "ULTRACEMCO.NS", "LT.NS"
]

# --- UI Controls ---
selected_tickers = st.multiselect("✅ Select Tickers", options=tickers_list)

col1, col2 = st.columns(2)
with col1:
    period = st.selectbox("⏱️ Select Period", [
        "1 day", "5 days", "1 month", "3 months", "6 months", "1 year", "2 years", "5 years", "10 years", "YTD", "Max"
    ])
with col2:
    interval = st.selectbox("📊 Select Interval", ["Daily", "Weekly", "Monthly"])

period_map = {"1 day": "1d", "5 days": "5d", "1 month": "1mo", "3 months": "3mo", "6 months": "6mo", "1 year": "1y", "2 years": "2y", "5 years": "5y", "10 years": "10y", "YTD": "ytd", "Max": "max"}
interval_map = {"Daily": "1d", "Weekly": "1wk", "Monthly": "1mo"}

yf_period = period_map[period]
yf_interval = interval_map[interval]

# --- Download Button ---
if st.button("📥 Download Data to Excel"):
    if not selected_tickers:
        st.warning("Please select at least one ticker.")
    else:
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine="openpyxl")

        for ticker in selected_tickers:
            try:
                df = yf.download(ticker, period=yf_period, interval=yf_interval, progress=False)
                if not df.empty:
                    df.to_excel(writer, sheet_name=ticker[:31])
            except Exception as e:
                st.error(f"Error fetching {ticker}: {e}")

        writer.close()

        # Auto-fit columns
        wb = openpyxl.load_workbook(output)
        for sheet in wb.sheetnames:
            ws = wb[sheet]
            for col in ws.columns:
                max_len = max((len(str(cell.value)) for cell in col if cell.value), default=0)
                ws.column_dimensions[get_column_letter(col[0].column)].width = max_len + 2
        new_output = BytesIO()
        wb.save(new_output)

        st.success("✅ Download complete!")

        st.download_button(
            label="📂 Click to Download Excel File",
            data=new_output.getvalue(),
            file_name="StockData.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
