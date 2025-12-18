@echo off
echo 启动股票市场情绪智能体模拟器...
echo.
echo 正在检查依赖...
pip install -r requirements.txt
echo.
echo 启动Streamlit应用...
streamlit run app.py
pause

