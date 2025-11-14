# GenAI HRMS - AI Services Complete Guide

## 📋 Table of Contents

1. [Overview](#overview)
2. [Setup & Installation](#setup--installation)
3. [Policy RAG (Q&A AI)](#policy-rag-qa-ai)
4. [Resume Screener AI](#resume-screener-ai)
5. [Job Description Generator](#job-description-generator)
6. [Frontend Integration](#frontend-integration)
7. [API Reference](#api-reference)
8. [Troubleshooting](#troubleshooting)

---

## Overview

The GenAI HRMS includes three powerful AI features powered by Google Gemini:

### 🤖 AI Features

| Feature | Description | Users | Status |
|---------|-------------|-------|--------|
| **Policy RAG** | AI-powered policy Q&A with auto-indexing | All Users | ✅ Production Ready |
| **Resume Screener** | Intelligent resume analysis & ranking | HR Only | ✅ Production Ready |
| **JD Generator** | AI-generated job descriptions | HR Only | ✅ Production Ready |

### 🌟 Key Capabilities

- **Natural Language Understanding**: Ask questions in plain English
- **Context-Aware Responses**: Maintains conversation history
- **Automatic Indexing**: Policies indexed automatically on upload
- **Real-time Progress**: Streaming updates for long operations
- **Persistent Storage**: All analysis results stored permanently
- **Dual Modes**: Generate only or save as draft options

---

## Setup & Installation

### 1. Prerequisites

```bash
# Python 3.9+
python --version

# Required packages
pip install -r backend/requirements_ai.txt
```

### 2. Get Google API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the key

### 3. Configure Environment

Create `.env` file in the **project root**:

```bash
# ==================== AI CONFIGURATION ====================
GOOGLE_API_KEY=your_actual_api_key_here

# AI Model Settings (optional - defaults are optimized)
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=models/embedding-001
GEMINI_TEMPERATURE=0.2

# Policy RAG Settings
POLICY_RAG_CHUNK_SIZE=1000
POLICY_RAG_CHUNK_OVERLAP=200
POLICY_RAG_RETRIEVAL_K=3
POLICY_RAG_INDEX_DIR=ai_data/policy_index

# Resume Screener Settings
RESUME_SCREENER_MAX_WORKERS=4
RESUME_SCREENER_STORAGE_DIR=ai_data/resume_analysis

# Job Description Generator
JD_GENERATOR_ENABLED=True
```

### 4. Verify Setup

```bash
cd backend
python -c "from ai_services.policy_rag_service import PolicyRAGService; print('✅ AI Services Ready')"
```

### 5. Start Backend

```bash
cd backend
python main.py
```

You should see:
```
INFO:     AI services routes loaded successfully
INFO:     AI routes registered: Policy RAG, Resume Screener, JD Generator
```

---

## Policy RAG (Q&A AI)

### Overview

AI-powered question answering about company policies using Retrieval-Augmented Generation (RAG).

**Features:**
- ✅ Auto-indexes policies on upload
- ✅ Natural language questions
- ✅ Context-aware conversations
- ✅ Source citations
- ✅ Suggested questions

### How It Works

```
1. Policy Upload → 2. Auto-Index → 3. Ask Questions → 4. Get AI Answers
```

### API Endpoints

#### 1. Ask Question

```bash
POST /api/v1/ai/policy-rag/ask
```

**Request:**
```json
{
  "question": "How many casual leaves am I allowed per year?",
  "chat_history": [
    {
      "role": "user",
      "content": "What is the leave policy?"
    },
    {
      "role": "assistant",
      "content": "The leave policy includes casual, sick, and earned leaves..."
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "answer": "Employees are entitled to 12 casual leaves per calendar year...",
  "sources": [
    {
      "policy_title": "Leave Policy 2025",
      "content": "Casual Leave: 12 days per calendar year..."
    }
  ],
  "question": "How many casual leaves am I allowed per year?"
}
```

#### 2. Get Suggestions

```bash
GET /api/v1/ai/policy-rag/suggestions
```

**Response:**
```json
{
  "suggestions": [
    "How many casual leaves am I allowed per year?",
    "What is the policy for sick leave?",
    "How do I enroll in the health insurance plan?",
    ...
  ]
}
```

#### 3. Check Index Status

```bash
GET /api/v1/ai/policy-rag/status
```

**Response:**
```json
{
  "indexed": true,
  "total_vectors": 1024,
  "index_location": "ai_data/policy_index",
  "model": "gemini-2.0-flash-exp",
  "embedding_model": "models/embedding-001"
}
```

#### 4. Rebuild Index (Admin)

```bash
POST /api/v1/ai/policy-rag/index/rebuild
```

### Frontend Integration

```typescript
import { 
  askPolicyQuestion, 
  getPolicySuggestions,
  getPolicyIndexStatus 
} from '@/services/aiPolicyRagService';

// Ask a question
const answer = await askPolicyQuestion({
  question: "What is the remote work policy?",
  chat_history: [] // Optional
});

// Get suggestions
const suggestions = await getPolicySuggestions();

// Check if ready
const status = await getPolicyIndexStatus();
if (status.indexed) {
  // Ready to use
}
```

### Best Practices

1. **First Use**: Check index status before allowing questions
2. **Conversational**: Pass chat history for context-aware answers
3. **Citations**: Always show source policies to users
4. **Suggestions**: Display suggested questions to guide users
5. **Feedback**: Allow users to rate answer quality

---

## Resume Screener AI

### Overview

AI-powered resume analysis that screens candidates against job descriptions with detailed scoring and insights.

**Features:**
- ✅ Intelligent skill matching
- ✅ Experience verification
- ✅ Education validation
- ✅ Strengths & gaps analysis
- ✅ Overall fit score (0-100)
- ✅ Permanent storage
- ✅ Real-time streaming progress

### Analysis Components

| Component | Description |
|-----------|-------------|
| **Overall Fit Score** | 0-100 score based on all factors |
| **Skill Matches** | Each skill with proficiency level (1-5) |
| **Experience Matches** | Years required vs. present with relevance |
| **Education Match** | Degree requirements verification |
| **Strengths** | Key positive points |
| **Gaps** | Areas for improvement |
| **Summary** | AI-generated hiring recommendation |

### API Endpoints

#### 1. Screen Resumes (Standard)

```bash
POST /api/v1/ai/resume-screener/screen
```

**Request:**
```json
{
  "job_id": 1,
  "job_description": "Optional - overrides job listing description",
  "resume_ids": [1, 2, 3] // Optional - screens specific applications
}
```

**Response:**
```json
{
  "success": true,
  "job_id": 1,
  "job_title": "Senior Python Developer",
  "results": [
    {
      "candidate_name": "John Doe",
      "application_id": 1,
      "overall_fit_score": 85,
      "skill_matches": [
        {
          "skill_name": "Python",
          "present_in_resume": true,
          "importance_level": 5,
          "proficiency_level": 4,
          "context": "5 years experience with Django"
        }
      ],
      "experience_matches": [
        {
          "area": "Backend Development",
          "years_required": 3,
          "years_present": 5,
          "relevance_score": 5,
          "context": "Led backend team at TechCorp"
        }
      ],
      "education_match": {
        "requirement": "Bachelor's in Computer Science",
        "has_match": true,
        "details": "B.Tech CS from IIT"
      },
      "strengths": [
        "Strong Python expertise",
        "Proven leadership",
        "Excellent problem-solving"
      ],
      "gaps": [
        "Limited AWS experience",
        "No CI/CD mention"
      ],
      "summary": "Excellent candidate with strong technical skills..."
    }
  ],
  "total_analyzed": 3,
  "average_score": 78.5,
  "top_candidate": "John Doe",
  "analysis_id": "abc123xyz456"
}
```

#### 2. Screen Resumes (With Progress Streaming)

```bash
POST /api/v1/ai/resume-screener/screen/stream
```

**Stream Events:**

```javascript
// Event: start
{
  "total": 10,
  "job_title": "Senior Developer"
}

// Event: result (per resume)
{
  "candidate": "John Doe",
  "score": 85,
  "progress": 30
}

// Event: complete
{
  "analysis_id": "abc123",
  "total_analyzed": 10,
  "average_score": 75.5,
  "top_candidate": "John Doe"
}

// Event: error
{
  "error": "Error message"
}
```

#### 3. Get Saved Results

```bash
GET /api/v1/ai/resume-screener/results/{analysis_id}
```

#### 4. Get Screening History

```bash
GET /api/v1/ai/resume-screener/history?job_id=1
```

**Response:**
```json
{
  "success": true,
  "total": 5,
  "history": [
    {
      "analysis_id": "abc123",
      "job_id": 1,
      "job_title": "Senior Developer",
      "timestamp": "2025-11-14T10:30:00",
      "total_analyzed": 10,
      "average_score": 75.5,
      "top_candidate": "John Doe"
    }
  ]
}
```

### Frontend Integration

```typescript
import { 
  screenResumes, 
  screenResumesWithProgress,
  getScreeningHistory 
} from '@/services/aiResumeScreenerService';

// Standard screening
const result = await screenResumes({
  job_id: 1,
  resume_ids: [1, 2, 3]
});

// With streaming progress
const eventSource = screenResumesWithProgress(
  { job_id: 1 },
  (progress) => {
    if (progress.type === 'result') {
      console.log(`${progress.data.candidate}: ${progress.data.score}%`);
    } else if (progress.type === 'complete') {
      console.log('Screening complete!', progress.data);
    }
  },
  (error) => console.error(error)
);

// View history
const history = await getScreeningHistory(1); // job_id
```

### Best Practices

1. **Use Streaming**: For better UX when screening multiple resumes
2. **Save Analysis ID**: Store for future reference
3. **Export Results**: Use CSV export utility for reports
4. **Score Interpretation**: 
   - 80-100: Excellent Fit (Green)
   - 60-79: Good Fit (Yellow)
   - 40-59: Fair Fit (Orange)
   - 0-39: Poor Fit (Red)
5. **Review Manually**: AI is a tool, not a replacement for human judgment

---

## Job Description Generator

### Overview

AI-powered job description generator that creates professional, ATS-friendly job postings.

**Features:**
- ✅ Two modes: Preview or Save as Draft
- ✅ Structured output (summary, responsibilities, qualifications)
- ✅ Benefits and application sections
- ✅ Improve existing JDs
- ✅ Extract SEO/ATS keywords
- ✅ Copy/download capabilities

### Generation Modes

| Mode | Description | Use Case |
|------|-------------|----------|
| **Preview Only** | Generate JD for review | Want to edit before saving |
| **Save as Draft** | Creates job listing draft | Ready to publish soon |

### API Endpoints

#### 1. Generate Job Description

```bash
POST /api/v1/ai/job-description/generate
```

**Request:**
```json
{
  "job_title": "Senior Python Developer",
  "job_level": "senior",
  "department": "Engineering",
  "location": "Remote/Bangalore",
  "employment_type": "full-time",
  "company_info": {
    "name": "TechCorp",
    "description": "Leading AI company",
    "industry": "Technology",
    "values": ["Innovation", "Excellence"]
  },
  "responsibilities": [
    "Design and develop scalable backend services",
    "Mentor junior developers",
    "Review code and ensure quality"
  ],
  "requirements": [
    {
      "requirement": "5+ years Python experience",
      "is_required": true
    },
    {
      "requirement": "AWS experience",
      "is_required": false
    }
  ],
  "salary_range": "$120,000 - $150,000",
  "benefits": [
    "Health insurance",
    "Remote work",
    "401(k) matching"
  ],
  "save_as_draft": false
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "title": "Senior Python Developer",
    "company_overview": "TechCorp is a leading AI company...",
    "job_summary": "We're seeking an experienced Senior Python Developer...",
    "key_responsibilities": [
      "Design, develop, and maintain scalable backend services...",
      "Provide technical mentorship to junior team members...",
      ...
    ],
    "required_qualifications": [
      "5+ years of professional Python development experience",
      "Strong understanding of RESTful APIs and microservices",
      ...
    ],
    "preferred_qualifications": [
      "Experience with AWS cloud services",
      "Familiarity with CI/CD pipelines",
      ...
    ],
    "benefits_section": "We offer comprehensive benefits including...",
    "how_to_apply": "To apply, please submit your resume...",
    "full_description": "Complete formatted job description..."
  },
  "job_listing_id": 123, // Only if save_as_draft=true
  "message": "Job description generated successfully"
}
```

#### 2. Improve Existing JD

```bash
POST /api/v1/ai/job-description/improve?job_listing_id=1
```

**Request (Query Params):**
```json
{
  "improvements": [
    "Make it more engaging",
    "Add remote work benefits",
    "Emphasize growth opportunities"
  ]
}
```

#### 3. Extract Keywords

```bash
POST /api/v1/ai/job-description/extract-keywords?job_description=...
```

**Response:**
```json
{
  "success": true,
  "keywords": [
    "Python", "Backend", "Django", "REST API", 
    "Microservices", "AWS", "Leadership", ...
  ],
  "total": 15
}
```

#### 4. Check Status

```bash
GET /api/v1/ai/job-description/status
```

### Frontend Integration

```typescript
import { 
  generateJobDescription,
  improveJobDescription,
  extractKeywords,
  formatJobDescription,
  copyToClipboard
} from '@/services/aiJobDescriptionService';

// Generate JD
const result = await generateJobDescription({
  job_title: "Senior Python Developer",
  job_level: "senior",
  department: "Engineering",
  location: "Remote",
  responsibilities: [...],
  requirements: [...],
  save_as_draft: false // Preview mode
});

if (result.success && result.data) {
  // Display generated JD
  const formatted = formatJobDescription(result.data);
  
  // Copy to clipboard
  await copyToClipboard(formatted);
  
  // Or download
  downloadAsTextFile(formatted, 'job-description.txt');
}

// Improve existing JD
await improveJobDescription(jobId, [
  "Add diversity statement",
  "Emphasize work-life balance"
]);

// Extract keywords for SEO
const keywords = await extractKeywords(jobDescription);
```

### Best Practices

1. **Be Specific**: Provide detailed responsibilities and requirements
2. **Use Preview Mode**: Review before saving as draft
3. **Iterate**: Use improve function for refinements
4. **SEO Optimize**: Use keyword extraction for better visibility
5. **Customize**: Always review and personalize AI-generated content
6. **Save Time**: Use for initial draft, then refine

---

## Frontend Integration

### Installation

All frontend services are ready to use. Import from `@/services/`:

```typescript
// Policy RAG
import * as PolicyRAG from '@/services/aiPolicyRagService';

// Resume Screener
import * as ResumeScreener from '@/services/aiResumeScreenerService';

// JD Generator
import * as JDGenerator from '@/services/aiJobDescriptionService';
```

### Example Components

#### 1. Policy Q&A Component

```typescript
import { useState, useEffect } from 'react';
import { askPolicyQuestion, getPolicySuggestions } from '@/services/aiPolicyRagService';

function PolicyQA() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState(null);
  const [suggestions, setSuggestions] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadSuggestions();
  }, []);

  const loadSuggestions = async () => {
    const sug = await getPolicySuggestions();
    setSuggestions(sug);
  };

  const handleAsk = async () => {
    setLoading(true);
    const result = await askPolicyQuestion({ question });
    setAnswer(result);
    setLoading(false);
  };

  return (
    <div>
      <input 
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask about policies..."
      />
      <button onClick={handleAsk} disabled={loading}>
        {loading ? 'Thinking...' : 'Ask'}
      </button>
      
      {answer?.success && (
        <div>
          <p>{answer.answer}</p>
          {answer.sources && (
            <div>
              <h4>Sources:</h4>
              {answer.sources.map((s, i) => (
                <p key={i}>{s.policy_title}</p>
              ))}
            </div>
          )}
        </div>
      )}

      <div>
        <h4>Suggested Questions:</h4>
        {suggestions.map((s, i) => (
          <button key={i} onClick={() => setQuestion(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}
```

#### 2. Resume Screener with Progress

```typescript
import { useState } from 'react';
import { screenResumesWithProgress } from '@/services/aiResumeScreenerService';

function ResumeScreener({ jobId }: { jobId: number }) {
  const [progress, setProgress] = useState(0);
  const [results, setResults] = useState([]);
  const [screening, setScreening] = useState(false);

  const startScreening = () => {
    setScreening(true);
    setProgress(0);
    setResults([]);

    const eventSource = screenResumesWithProgress(
      { job_id: jobId },
      (progressData) => {
        if (progressData.type === 'result') {
          setProgress(progressData.data.progress);
          setResults(prev => [...prev, progressData.data]);
        } else if (progressData.type === 'complete') {
          setScreening(false);
          console.log('Complete:', progressData.data);
        }
      },
      (error) => {
        console.error(error);
        setScreening(false);
      }
    );
  };

  return (
    <div>
      <button onClick={startScreening} disabled={screening}>
        {screening ? `Screening... ${progress}%` : 'Start Screening'}
      </button>

      {results.map((result, i) => (
        <div key={i}>
          <h3>{result.candidate}</h3>
          <p>Score: {result.score}%</p>
        </div>
      ))}
    </div>
  );
}
```

#### 3. JD Generator Component

```typescript
import { useState } from 'react';
import { generateJobDescription } from '@/services/aiJobDescriptionService';

function JDGenerator() {
  const [formData, setFormData] = useState({
    job_title: '',
    job_level: 'mid',
    department: '',
    location: '',
    responsibilities: [''],
    requirements: [{ requirement: '', is_required: true }],
    save_as_draft: false
  });
  const [generatedJD, setGeneratedJD] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerate = async () => {
    setLoading(true);
    const result = await generateJobDescription(formData);
    if (result.success) {
      setGeneratedJD(result.data);
    }
    setLoading(false);
  };

  return (
    <div>
      {/* Form inputs */}
      <button onClick={handleGenerate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate JD'}
      </button>

      {generatedJD && (
        <div>
          <h2>{generatedJD.title}</h2>
          <p>{generatedJD.job_summary}</p>
          {/* Display full JD */}
        </div>
      )}
    </div>
  );
}
```

---

## API Reference

### Authentication

All AI endpoints require authentication via JWT token:

```bash
Authorization: Bearer <your_jwt_token>
```

### Rate Limiting

- **Policy RAG**: 100 requests/minute
- **Resume Screener**: 10 screenings/hour (streaming recommended)
- **JD Generator**: 20 generations/hour

### Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid request data |
| 401 | Unauthorized (missing/invalid token) |
| 403 | Forbidden (insufficient permissions) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | AI service unavailable |

---

## Troubleshooting

### Issue: "AI service unavailable"

**Cause**: Missing dependencies or invalid API key

**Solution**:
```bash
# 1. Install dependencies
pip install -r backend/requirements_ai.txt

# 2. Check API key
echo $GOOGLE_API_KEY

# 3. Verify setup
python -c "import langchain_google_genai; print('OK')"
```

### Issue: "No policies indexed"

**Cause**: Policies not uploaded or indexing failed

**Solution**:
```bash
# 1. Upload a policy via UI or API
POST /api/v1/policies/{id}/upload

# 2. Rebuild index
POST /api/v1/ai/policy-rag/index/rebuild

# 3. Check status
GET /api/v1/ai/policy-rag/status
```

### Issue: "Resume screening very slow"

**Cause**: Large number of resumes without streaming

**Solution**:
- Use streaming endpoint: `/api/v1/ai/resume-screener/screen/stream`
- Process in smaller batches
- Increase `RESUME_SCREENER_MAX_WORKERS` in `.env`

### Issue: "Generated JD is generic"

**Cause**: Insufficient input details

**Solution**:
- Provide more specific responsibilities
- Add company culture information
- Include unique benefits
- Use improve endpoint for refinement

### Getting Help

- **Documentation**: Check this guide and API docs at `/api/docs`
- **Logs**: Check `backend/logs/` for detailed error messages
- **Support**: Contact development team

---

## Production Checklist

- [ ] Google API key configured in `.env`
- [ ] AI dependencies installed (`requirements_ai.txt`)
- [ ] Directories created (auto-created on startup)
- [ ] Backend logs show "AI routes registered"
- [ ] Test each feature with sample data
- [ ] Set up rate limiting in production
- [ ] Monitor API usage and costs
- [ ] Configure CORS for frontend domain
- [ ] Set up error monitoring (Sentry, etc.)
- [ ] Document custom configurations
- [ ] Train users on AI features

---

## Cost Optimization

### Google Gemini API

- **Model**: gemini-2.0-flash-exp (free tier available)
- **Embeddings**: ~$0.00001 per 1K tokens
- **Generation**: ~$0.0001 per 1K tokens

### Optimization Tips

1. **Cache Results**: Store screening/generation results
2. **Batch Operations**: Process multiple items together
3. **Appropriate Models**: Use flash model for speed
4. **Index Incrementally**: Only index new policies
5. **Monitor Usage**: Track API calls and costs

---

## Future Enhancements

- [ ] Multi-language support
- [ ] Custom fine-tuning options
- [ ] Feedback learning loop
- [ ] Advanced analytics dashboard
- [ ] Interview question generation
- [ ] Candidate skill gap training recommendations
- [ ] Automated policy compliance checks
- [ ] Integration with more LLM providers

---

**Last Updated**: November 14, 2025
**Version**: 1.0.0
**Status**: Production Ready ✅

