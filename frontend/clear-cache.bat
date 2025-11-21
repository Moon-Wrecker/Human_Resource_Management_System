@echo off
REM Clear Vite Cache Script for Windows
REM Run this when you have module resolution issues

echo 🧹 Clearing Vite cache and restarting...

REM Remove Vite cache directories
if exist node_modules\.vite rmdir /s /q node_modules\.vite
if exist .vite rmdir /s /q .vite
if exist dist rmdir /s /q dist

echo ✅ Cache cleared!
echo 🚀 Now run: npm run dev
pause



