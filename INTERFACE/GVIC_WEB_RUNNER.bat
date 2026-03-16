@echo off
title GVIC WEB APP RUNNER v1.2 - FORCE-PROVISIONING
chcp 65001 > nul

set "GVIC_WEB_PATH=C:\GVIC\INTERFACE"
cd /d "%GVIC_WEB_PATH%"

cls
echo =====================================================================
echo    🛡️ GVIC WEB APP COMMAND CENTER - EMERGENCY RESTORE
echo =====================================================================

:: 1. 엔진 보급 확인 및 강제 설치
echo [보고] 신경망 엔진(Streamlit) 상태를 정밀 점검합니다...
python -c "import streamlit" >nul 2>&1
if %errorlevel% neq 0 (
    echo [경고] 엔진이 없습니다! 즉시 본진으로부터 보급을 강행합니다...
    python -m pip install --upgrade pip
    python -m pip install streamlit pandas streamlit-bootstrap-components dash-bootstrap-components
    if %errorlevel% neq 0 (
        echo [치명] 보급망 차단! 인터넷 연결을 확인하십시오.
        pause
        exit
    )
    echo [보고] 보급 완료. 엔진이 장착되었습니다.
)

:: 2. 기존 포트 정화 (유령 프로세스 소탕)
echo [보고] 통신망(8501)을 정화합니다...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8501') do taskkill /f /pid %%a >nul 2>&1

:: 3. 전술 사령부 점화
echo 🚀 전술 사령부(gvic_web_app.py) 엔진 점화 중...
:: Headless 모드로 백그라운드 가동
start /b python -m streamlit run "gvic_web_app.py" --server.port 8501 --server.headless true

:: 4. 게이트웨이 개방 대기 (충분한 예열 시간 부여)
echo [보고] 엔진 예열 중... (10초 대기)
timeout /t 10 > nul
echo [보고] 통신 게이트웨이 접속: http://localhost:8501
start http://localhost:8501

echo =====================================================================
echo [완료] 지휘소가 정상 복구되었습니다.
pause