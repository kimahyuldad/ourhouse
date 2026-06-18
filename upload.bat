@echo off
chcp 949 > nul
echo =======================================================
echo     AssetFlow (아율이네 자산 관리) GitHub 업로드 도우미
echo =======================================================
echo.
echo 깃허브 저장소(https://github.com/kimahyuldad/ourhouse.git)로 
echo 업데이트 및 업로드를 시작합니다.
echo.
echo [1/2] 모든 변경 사항을 준비하고 기록합니다...
git add -A
git commit -m "Update AssetFlow" > nul 2>&1

echo [2/2] 깃허브로 업로드(Push) 중입니다...
echo (이미 로그인되어 있다면 바로 완료됩니다)
echo.
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo [오류] 업데이트 업로드에 실패했습니다.
    echo 인터넷 연결을 확인해 주세요.
) else (
    echo.
    echo [성공] 업데이트가 완료되었습니다!
    echo 약 1분 후 모바일 웹사이트(https://kimahyuldad.github.io/ourhouse/)에 자동으로 반영됩니다.
)
echo.
pause
