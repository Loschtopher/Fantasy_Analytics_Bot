@echo off
chcp 65001 >nul
title Restarting Fantasy Football Bot
echo ============================================================
echo   Restarting Fantasy Football Bot
echo ============================================================
echo.
echo Stopping any running Python processes for the bot...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq Fantasy Football Bot*" 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting bot with latest code...
echo.
python final_working_bot.py
echo.
echo Bot stopped.
pause

