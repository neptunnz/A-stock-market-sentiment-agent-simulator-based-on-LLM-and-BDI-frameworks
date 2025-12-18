@echo off
chcp 65001 >nul
echo 正在启动股票市场情绪智能体模拟器...
echo.
cd /d %~dp0
py -m streamlit run app.py
pause

