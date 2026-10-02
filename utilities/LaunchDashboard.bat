@echo off
cd /d "C:\Path\To\ValveClaimsDashboard"
call .venv\Scripts\activate.bat
streamlit run Overview.py
pause