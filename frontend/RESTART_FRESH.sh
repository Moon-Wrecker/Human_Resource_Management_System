#!/bin/bash
# Complete Frontend Restart Script
# This will fix all module export issues

echo "🛑 Stopping any running Vite processes..."
pkill -f "vite" 2>/dev/null || true

echo "🧹 Clearing ALL caches..."
rm -rf node_modules/.vite
rm -rf .vite
rm -rf dist
rm -rf node_modules/.tmp

echo "✅ Caches cleared!"
echo ""
echo "🚀 Starting dev server..."
echo "   Open: http://localhost:5173"
echo "   Press Ctrl+C to stop"
echo ""

npm run dev


