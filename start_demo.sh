#!/bin/bash

echo "========================================"
echo "    GenMentor MVP Demo"
echo "========================================"
echo ""
echo "Starting services..."
echo ""

echo "1. Backend API is running on: http://localhost:5000"
echo "2. Opening demo page..."
echo ""

# Open URLs in default browser
if command -v xdg-open > /dev/null; then
    xdg-open http://localhost:5000/docs
    xdg-open frontend/simple_demo.html
elif command -v open > /dev/null; then
    open http://localhost:5000/docs
    open frontend/simple_demo.html
else
    echo "Please open these URLs manually:"
    echo "- http://localhost:5000/docs"
    echo "- frontend/simple_demo.html"
fi

echo ""
echo "Demo is ready!"
echo ""
echo "Available URLs:"
echo "- Backend API: http://localhost:5000"
echo "- API Documentation: http://localhost:5000/docs"
echo "- Demo Interface: frontend/simple_demo.html"
echo "- Onboarding Mockups: frontend/mockups/onboarding/"
echo ""
echo "Press Enter to exit..."
read