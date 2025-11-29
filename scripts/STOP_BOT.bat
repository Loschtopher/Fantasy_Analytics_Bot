@echo off
title Stop Bot
echo ============================================================
echo   Stopping Fantasy Football Bot
echo ============================================================
echo.
echo Stopping all Python processes...
taskkill /F /IM python.exe 2>nul
echo.
echo Done! All Python processes stopped.
echo.
pause

