@echo off
chcp 65001 >nul
title Quick Restart Bot
echo ============================================================
echo   Quick Restart Fantasy Football Bot
echo ============================================================
echo.
echo Step 1: Stopping old bot...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Step 2: Starting fresh bot with latest code...
echo.
python final_working_bot.py
echo.
echo Bot stopped.
pause

