#!/bin/bash
# Clear Vite Cache Script
# Run this when you have module resolution issues

echo "🧹 Clearing Vite cache and restarting..."

# Remove Vite cache directories
rm -rf node_modules/.vite
rm -rf .vite
rm -rf dist

echo "✅ Cache cleared!"
echo "🚀 Now run: npm run dev"



