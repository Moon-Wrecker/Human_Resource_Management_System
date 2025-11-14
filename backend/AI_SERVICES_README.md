# AI Services - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements_ai.txt
```

### 2. Get API Key

Visit: https://makersuite.google.com/app/apikey

### 3. Create .env File

Create `.env` in **project root** (not backend folder):

```bash
# Required
GOOGLE_API_KEY=your_api_key_here

# Optional (defaults work well)
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_TEMPERATURE=0.2
```

### 4. Start Backend

```bash
cd backend
python main.py
```

✅ Look for: `AI routes registered: Policy RAG, Resume Screener, JD Generator`

## 📚 Features

### 1. Policy RAG (Q&A)
- **Endpoint**: `/api/v1/ai/policy-rag/ask`
- **Access**: All users
- **Auto-indexes**: Policies indexed automatically on upload

```bash
curl -X POST http://localhost:8000/api/v1/ai/policy-rag/ask \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"question": "How many leaves do I get?"}'
```

### 2. Resume Screener
- **Endpoint**: `/api/v1/ai/resume-screener/screen`
- **Access**: HR only
- **Streaming**: `/screen/stream` for progress updates

```bash
curl -X POST http://localhost:8000/api/v1/ai/resume-screener/screen \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"job_id": 1}'
```

### 3. Job Description Generator
- **Endpoint**: `/api/v1/ai/job-description/generate`
- **Access**: HR only
- **Dual Mode**: Preview or Save as Draft

```bash
curl -X POST http://localhost:8000/api/v1/ai/job-description/generate \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{
    "job_title": "Python Developer",
    "job_level": "mid",
    "department": "Engineering",
    "location": "Remote",
    "responsibilities": ["Develop APIs", "Write tests"],
    "requirements": [{"requirement": "3+ years Python", "is_required": true}],
    "save_as_draft": false
  }'
```

## 🧪 Test AI Services

```bash
# Test Policy RAG
curl http://localhost:8000/api/v1/ai/policy-rag/status

# Test Resume Screener (after uploading resumes)
curl http://localhost:8000/api/v1/ai/resume-screener/history \
  -H "Authorization: Bearer YOUR_TOKEN"

# Test JD Generator
curl http://localhost:8000/api/v1/ai/job-description/status \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📖 Full Documentation

See: `docs/AI_SERVICES_COMPLETE_GUIDE.md`

## 🐛 Troubleshooting

**Error: "AI service unavailable"**
```bash
# Check dependencies
pip list | grep langchain

# Verify API key
python -c "import os; print(os.getenv('GOOGLE_API_KEY'))"
```

**Error: "No policies indexed"**
```bash
# Upload a policy first, then:
curl -X POST http://localhost:8000/api/v1/ai/policy-rag/index/rebuild \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 📁 File Structure

```
backend/
├── ai_services/
│   ├── __init__.py
│   ├── policy_rag_service.py           # Policy Q&A logic
│   ├── resume_screener_service.py      # Resume analysis logic
│   └── job_description_generator_service.py
├── routes/
│   ├── ai_policy_rag.py                # Policy RAG endpoints
│   ├── ai_resume_screener.py           # Resume screener endpoints
│   └── ai_job_description.py           # JD generator endpoints
├── schemas/
│   └── ai_schemas.py                   # Pydantic schemas
├── ai_data/                            # Auto-created on startup
│   ├── policy_index/                   # FAISS index
│   └── resume_analysis/                # Stored analyses
├── requirements_ai.txt                 # AI dependencies
└── AI_SERVICES_README.md              # This file
```

## 🎯 Frontend Services

```typescript
// Policy RAG
import * as PolicyRAG from '@/services/aiPolicyRagService';

// Resume Screener  
import * as ResumeScreener from '@/services/aiResumeScreenerService';

// JD Generator
import * as JDGenerator from '@/services/aiJobDescriptionService';
```

## ✅ Production Checklist

- [ ] API key configured
- [ ] Dependencies installed
- [ ] Backend shows "AI routes registered"
- [ ] Test with sample data
- [ ] Monitor API usage/costs
- [ ] Configure rate limiting

## 💡 Tips

1. **Policy RAG**: Upload policies via `/api/v1/policies/{id}/upload` - auto-indexes
2. **Resume Screener**: Use streaming endpoint for better UX
3. **JD Generator**: Use preview mode first, then save as draft
4. **Cost**: Gemini Flash model is very cost-effective
5. **Performance**: Results are cached/stored permanently

## 🔗 Links

- **API Docs**: http://localhost:8000/api/docs
- **Full Guide**: `docs/AI_SERVICES_COMPLETE_GUIDE.md`
- **Google AI**: https://makersuite.google.com

---

**Status**: ✅ Production Ready
**Version**: 1.0.0
**Last Updated**: November 14, 2025

