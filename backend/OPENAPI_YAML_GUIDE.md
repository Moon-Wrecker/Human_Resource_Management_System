# OpenAPI YAML Access Guide

## 🚀 How to Access OpenAPI YAML

### Method 1: Download via Browser (Recommended)

**URL:** `http://localhost:8000/api/openapi.yaml`

1. Start your backend server:
   ```bash
   cd backend
   python main.py
   ```

2. Open in your browser:
   ```
   http://localhost:8000/api/openapi.yaml
   ```

3. The YAML file will be **automatically downloaded** to your Downloads folder

---

### Method 2: View in Browser

To **view** the YAML content in your browser instead of downloading:

**URL:** `http://localhost:8000/api/openapi.json`

Then convert it to YAML, or use Swagger UI to explore interactively.

---

### Method 3: Download via cURL

```bash
curl http://localhost:8000/api/openapi.yaml -o openapi.yaml
```

This will save the YAML file to your current directory.

---

### Method 4: Generate Locally (Alternative)

If the server is not running, you can generate the YAML file locally:

```bash
cd backend
python generate_openapi_yaml.py
```

Output: `backend/openapi.yaml`

---

## 📋 Available Documentation Endpoints

| Endpoint | Format | Description |
|----------|--------|-------------|
| `/api/docs` | HTML | Interactive Swagger UI (best for testing) |
| `/api/redoc` | HTML | ReDoc documentation (best for reading) |
| `/api/openapi.json` | JSON | OpenAPI specification in JSON format |
| `/api/openapi.yaml` | YAML | OpenAPI specification in YAML format (downloadable) |

---

## ✅ Verify It's Working

1. Start the server:
   ```bash
   cd backend
   python main.py
   ```

2. Check the server logs - you should see:
   ```
   AI services routes loaded successfully
   AI routes registered: Policy RAG, Resume Screener, JD Generator
   ```

3. Access any of these URLs in your browser:
   - `http://localhost:8000/api/docs` - Swagger UI
   - `http://localhost:8000/api/openapi.yaml` - Download YAML
   - `http://localhost:8000/api/v1` - API info (includes all endpoints)

---

## 🎯 For Milestone 4 Submission

You can use either:

1. **Generated YAML file** (already created): `backend/openapi.yaml`
   - Generated using: `python generate_openapi_yaml.py`
   - Contains all 137 endpoints

2. **Live YAML endpoint**: `http://localhost:8000/api/openapi.yaml`
   - Downloads the same content
   - Always up-to-date with current API state

Both methods produce identical YAML content!

---

## 🔧 Troubleshooting

### Issue: "Cannot access http://localhost:8000"
**Solution:** Make sure the backend server is running:
```bash
cd backend
python main.py
```

### Issue: "YAML file is empty or corrupted"
**Solution:** Regenerate the YAML file:
```bash
cd backend
python generate_openapi_yaml.py
```

### Issue: "Import error: No module named 'yaml'"
**Solution:** Install PyYAML:
```bash
pip install PyYAML
```
(Note: It's already in requirements.txt, so this shouldn't happen)

---

## 📊 What's in the YAML?

The OpenAPI YAML file contains:

- ✅ All 137 API endpoints
- ✅ Request/response schemas
- ✅ Authentication specifications
- ✅ Error response definitions
- ✅ Example requests and responses
- ✅ User story mappings (in descriptions)
- ✅ API categories/tags (24 categories)

---

## 🎉 Quick Test

To verify everything works:

```bash
# 1. Start server
cd backend
python main.py

# 2. In another terminal, download the YAML
curl http://localhost:8000/api/openapi.yaml -o test_openapi.yaml

# 3. Check the file
cat test_openapi.yaml | head -20
```

You should see the OpenAPI YAML content with your API documentation!


