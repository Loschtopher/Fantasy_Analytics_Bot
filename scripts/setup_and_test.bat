@echo off
echo ========================================
echo Fantasy Football Bot - Quick Setup
echo ========================================
echo.

echo Step 1: Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo.

echo Step 2: Setting up credentials...
echo (This will open an interactive setup)
python easy_setup.py
echo.

echo Step 3: Testing your setup...
python test_setup.py
echo.

echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start your bot, run:
echo   python run_bot.py
echo.
echo Or double-click: start_bot.bat
echo.
pause








