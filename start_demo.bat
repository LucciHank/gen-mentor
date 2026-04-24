@echo off
echo ========================================
echo    GenMentor MVP Demo
echo ========================================
echo.
echo Starting services...
echo.

echo 1. Backend API is running on: http://localhost:5000
echo 2. Opening demo page...
echo.

start http://localhost:5000/docs
start frontend\simple_demo.html

echo.
echo Demo is ready!
echo.
echo Available URLs:
echo - Backend API: http://localhost:5000
echo - API Documentation: http://localhost:5000/docs  
echo - Demo Interface: frontend\simple_demo.html
echo - Onboarding Mockups: frontend\mockups\onboarding\
echo.
echo Press any key to exit...
pause > nul