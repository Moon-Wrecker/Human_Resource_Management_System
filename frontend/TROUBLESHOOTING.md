# Frontend Troubleshooting Guide

## 🐛 Common Issues and Solutions

### Issue: "The requested module does not provide an export named..."

This error occurs when Vite's Hot Module Replacement (HMR) cache is out of sync with your code changes.

**Solution:**

#### **Option 1: Quick Fix (Try this first)**
```bash
# Stop the dev server (Ctrl+C or Cmd+C)

# Clear Vite cache
npm run clear-cache  # or use the scripts below

# Restart dev server
npm run dev
```

#### **Option 2: Use Clear Cache Scripts**

**On Linux/Mac:**
```bash
./clear-cache.sh
npm run dev
```

**On Windows:**
```cmd
clear-cache.bat
npm run dev
```

#### **Option 3: Manual Cache Clear**
```bash
# Stop dev server first!
rm -rf node_modules/.vite
rm -rf .vite
rm -rf dist
npm run dev
```

---

### Issue: Module Resolution Errors

If you see errors like "Cannot find module '@/services/...'"

**Check:**
1. Path aliases are configured in `vite.config.ts`:
   ```ts
   resolve: {
     alias: {
       "@": path.resolve(__dirname, "./src"),
     },
   }
   ```

2. TypeScript config has correct paths in `tsconfig.app.json`:
   ```json
   "paths": {
     "@/*": ["./src/*"]
   }
   ```

---

### Issue: API Connection Errors

**Symptoms:**
- Network errors in console
- "Failed to fetch" errors
- CORS errors

**Solution:**

1. **Check .env file exists:**
   ```bash
   # If .env doesn't exist, create it:
   cp env.template .env
   ```

2. **Verify .env content:**
   ```bash
   VITE_API_BASE_URL=http://localhost:8000
   VITE_ENV=development
   ```

3. **Check backend is running:**
   ```bash
   # In backend directory:
   uvicorn main:app --reload --port 8000
   ```

4. **Verify API URL in browser:**
   - Open: http://localhost:8000/api/docs
   - Should see Swagger documentation

---

### Issue: "Cannot import HRDashboardData" or similar type errors

**This is caused by Vite cache!**

**Solution:**
1. Stop dev server
2. Run: `rm -rf node_modules/.vite`
3. Run: `npm run dev`
4. Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

---

### Issue: Changes Not Reflecting in Browser

**Solutions:**

1. **Hard Refresh Browser:**
   - Windows/Linux: `Ctrl + Shift + R` or `Ctrl + F5`
   - Mac: `Cmd + Shift + R`

2. **Clear Browser Cache:**
   - Open DevTools (F12)
   - Right-click refresh button
   - Select "Empty Cache and Hard Reload"

3. **Restart Dev Server:**
   ```bash
   # Stop with Ctrl+C
   npm run dev
   ```

---

### Issue: TypeScript Errors in Editor

**Solutions:**

1. **Reload TypeScript Server (VS Code):**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type: "TypeScript: Restart TS Server"
   - Press Enter

2. **Reload Window:**
   - Press `Ctrl+Shift+P`
   - Type: "Developer: Reload Window"

3. **Clean TypeScript Build:**
   ```bash
   rm -rf node_modules/.tmp
   rm tsconfig.tsbuildinfo
   ```

---

### Issue: Port Already in Use

**Symptoms:**
```
Port 5173 is in use, trying another one...
```

**Solutions:**

1. **Kill the process using the port:**
   ```bash
   # Find process
   lsof -i :5173  # Mac/Linux
   netstat -ano | findstr :5173  # Windows
   
   # Kill process
   kill -9 <PID>  # Mac/Linux
   taskkill /F /PID <PID>  # Windows
   ```

2. **Use a different port:**
   ```bash
   npm run dev -- --port 3000
   ```

---

### Issue: Build Errors

**Solutions:**

1. **Clean install:**
   ```bash
   rm -rf node_modules
   rm package-lock.json
   npm install
   ```

2. **Clear all caches:**
   ```bash
   rm -rf node_modules/.vite
   rm -rf .vite
   rm -rf dist
   rm -rf node_modules/.tmp
   npm install
   npm run dev
   ```

---

## 🔍 Debugging Checklist

Before asking for help, verify:

- [ ] Backend is running on port 8000
- [ ] `.env` file exists and has correct API URL
- [ ] Vite cache is cleared
- [ ] Browser cache is cleared (hard refresh)
- [ ] No TypeScript errors in editor
- [ ] All imports use correct paths
- [ ] Node modules are installed
- [ ] Using correct Node version (16+)

---

## 📝 Quick Commands Reference

```bash
# Start dev server
npm run dev

# Clear Vite cache
rm -rf node_modules/.vite && rm -rf .vite && rm -rf dist

# Clear all caches and reinstall
rm -rf node_modules
rm -rf node_modules/.vite
rm -rf .vite
rm -rf dist
npm install
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type check
npm run type-check  # (if script exists)
```

---

## 🚀 Recommended Workflow

1. **Start backend first:**
   ```bash
   cd backend
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   uvicorn main:app --reload
   ```

2. **Start frontend in new terminal:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **If you make changes to:**
   - TypeScript types: Restart TS server in editor
   - Vite config: Restart dev server
   - Environment variables: Restart dev server
   - New dependencies: Run `npm install` first

---

## 💡 Pro Tips

1. **Use the clear-cache scripts** when you encounter module resolution issues
2. **Always hard refresh** after clearing cache
3. **Check browser console** for detailed error messages
4. **Check network tab** to verify API calls
5. **Keep backend and frontend terminals visible** to catch errors early

---

## 🆘 Still Having Issues?

1. Check backend logs for API errors
2. Check browser console for detailed errors
3. Verify all files are saved
4. Try restarting your editor
5. Check if any firewall is blocking connections

---

*Last Updated: November 13, 2025*


