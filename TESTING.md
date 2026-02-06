# 🧪 Testing Guide

Comprehensive testing instructions to ensure everything works correctly.

## Pre-Testing Checklist

Before running tests, verify:

- [ ] PostgreSQL is running: `brew services list`
- [ ] Backend server is running on port 8000
- [ ] Frontend server is running on port 3000
- [ ] `.env` file is configured correctly
- [ ] Database is initialized

## 1. Backend API Testing

### Test 1: Health Check

```bash
# Should return API info
curl http://localhost:8000

# Expected output:
# {
#   "message": "Wiki Quiz API is running!",
#   "version": "1.0.0",
#   "endpoints": { ... }
# }
```

✅ **Pass**: JSON response with "Wiki Quiz API is running!"  
❌ **Fail**: Connection refused or error

### Test 2: Generate Quiz (Alan Turing)

```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'
```

**Expected:**
- Status: 200 OK
- Response time: 20-40 seconds (first time)
- JSON with: id, title, summary, quiz array, related_topics

✅ **Pass**: Complete quiz returned with 5-10 questions  
❌ **Fail**: Error message or timeout

### Test 3: Caching (Duplicate URL)

```bash
# Run the same request again
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Alan_Turing"}'
```

**Expected:**
- Status: 200 OK
- Response time: < 1 second (cached)
- Same quiz data as before

✅ **Pass**: Instant response from cache  
❌ **Fail**: Takes 20+ seconds again

### Test 4: Invalid URL

```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://google.com"}'
```

**Expected:**
- Status: 400 Bad Request
- Error message about invalid URL

✅ **Pass**: Clear error message  
❌ **Fail**: Server crashes or unclear error

### Test 5: Get History

```bash
curl http://localhost:8000/api/quiz/history
```

**Expected:**
- Status: 200 OK
- Array of quiz objects with id, url, title, created_at

✅ **Pass**: Returns array with at least 1 quiz  
❌ **Fail**: Empty array or error

### Test 6: Get Quiz by ID

```bash
# Replace {id} with actual ID from history
curl http://localhost:8000/api/quiz/1
```

**Expected:**
- Status: 200 OK
- Full quiz details

✅ **Pass**: Complete quiz data  
❌ **Fail**: 404 Not Found

## 2. Frontend Testing

### Test 1: Page Load

1. Open http://localhost:3000
2. Check:
   - [ ] Page loads without errors
   - [ ] "Wiki Quiz Generator" header visible
   - [ ] Two tabs: "Generate Quiz" and "Quiz History"
   - [ ] Input field has default URL
   - [ ] "Generate Quiz" button is clickable

### Test 2: Generate Quiz via UI

1. Keep default URL (Alan Turing)
2. Click "Generate Quiz"
3. Check:
   - [ ] Button becomes disabled
   - [ ] Loading spinner appears
   - [ ] "Scraping and generating..." message shows
   - [ ] After 20-30 seconds, quiz displays
   - [ ] Quiz has:
     - [ ] Article title and summary
     - [ ] Info cards (sections, people, orgs, locations)
     - [ ] 5-10 quiz questions
     - [ ] Each question has difficulty badge
     - [ ] Each question has 4 options
     - [ ] Correct answer is highlighted in green
     - [ ] Explanation is shown
     - [ ] Related topics are displayed

### Test 3: History Tab

1. Click "Quiz History" tab
2. Check:
   - [ ] Tab switches successfully
   - [ ] Table displays with columns: ID, Title, URL, Created, Actions
   - [ ] At least one quiz is listed (Alan Turing)
   - [ ] "View Details" button is present

### Test 4: Quiz Details Modal

1. Click "View Details" on any quiz
2. Check:
   - [ ] Modal opens
   - [ ] Full quiz is displayed
   - [ ] Close button (×) works
   - [ ] Clicking outside modal closes it
   - [ ] Content is same as generation view

### Test 5: Error Handling

1. Enter invalid URL: `https://google.com`
2. Click "Generate Quiz"
3. Check:
   - [ ] Error message appears
   - [ ] Message is clear and helpful
   - [ ] Button becomes enabled again
   - [ ] No crash or freeze

## 3. Database Testing

### Test 1: Check Database Connection

```bash
psql -U quiz_user -d wiki_quiz_db -h localhost

# In psql:
\dt  # Should show wiki_quizzes table
```

### Test 2: Verify Data Storage

```sql
-- Count quizzes
SELECT COUNT(*) FROM wiki_quizzes;

-- View latest quiz
SELECT id, title, url, created_at 
FROM wiki_quizzes 
ORDER BY created_at DESC 
LIMIT 1;

-- Check quiz data structure
SELECT 
  id, 
  title,
  jsonb_array_length(quiz) as num_questions
FROM wiki_quizzes;
```

### Test 3: Data Integrity

```sql
-- Check for NULL values where there shouldn't be
SELECT * FROM wiki_quizzes 
WHERE title IS NULL 
   OR url IS NULL 
   OR quiz IS NULL;
   
-- Should return 0 rows
```

## 4. Integration Testing

### Test Multiple Wikipedia Articles

Test with different types of articles:

#### 1. Historical Figure
```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Marie_Curie"}'
```

Check:
- [ ] Questions about Nobel Prizes
- [ ] Questions about radioactivity
- [ ] Biographical questions

#### 2. Scientific Concept
```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Quantum_mechanics"}'
```

Check:
- [ ] Questions about principles
- [ ] Historical questions
- [ ] Difficulty varies

#### 3. Geographic Location
```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Paris"}'
```

Check:
- [ ] Questions about landmarks
- [ ] Historical questions
- [ ] Cultural questions

#### 4. Technology
```bash
curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Python_(programming_language)"}'
```

Check:
- [ ] Questions about features
- [ ] Historical questions
- [ ] Usage questions

## 5. Quiz Quality Testing

### Evaluate Generated Questions

For each quiz, verify:

#### Content Quality
- [ ] Questions are factually correct
- [ ] Questions reference article content
- [ ] No hallucinated information
- [ ] Explanations cite article sections

#### Question Structure
- [ ] Each question has exactly 4 options
- [ ] Only one correct answer per question
- [ ] Options are plausible but distinct
- [ ] Correct answer varies (not always option B)

#### Difficulty Distribution
- [ ] Mix of easy, medium, hard questions
- [ ] Easy questions test basic facts
- [ ] Medium questions test understanding
- [ ] Hard questions test deeper analysis

#### Diversity
- [ ] Questions cover different article sections
- [ ] Different question types (who, what, where, when, why)
- [ ] Not all questions are dates/names

## 6. Performance Testing

### Response Time Test

```bash
# Measure response time
time curl -X POST http://localhost:8000/api/quiz/generate \
  -H "Content-Type: application/json" \
  -d '{"url": "https://en.wikipedia.org/wiki/Short_Article"}'
```

**Expected:**
- First request: 15-40 seconds
- Cached request: < 1 second

### Load Test (Optional)

```bash
# Install apache bench
brew install httpd

# Test 10 concurrent requests
ab -n 10 -c 2 -p quiz_request.json -T application/json \
  http://localhost:8000/api/quiz/generate
```

## 7. Error Handling Testing

### Test 1: Missing API Key

1. Remove `GOOGLE_API_KEY` from `.env`
2. Restart backend
3. Try generating quiz

**Expected:** Clear error about missing API key

### Test 2: Database Connection Error

1. Stop PostgreSQL: `brew services stop postgresql@15`
2. Try accessing history

**Expected:** Error message about database connection

### Test 3: Invalid Wikipedia URL

Test these URLs:
- `https://wikipedia.org` (no article)
- `https://en.wikipedia.org/wiki/Special:Random` (special page)
- `https://example.com` (not Wikipedia)

**Expected:** Appropriate error messages

## 8. Browser Compatibility Testing

Test on:
- [ ] Chrome
- [ ] Safari
- [ ] Firefox
- [ ] Edge

Check:
- [ ] Layout is responsive
- [ ] Buttons work
- [ ] Modals open/close
- [ ] No console errors

## 9. Mobile Responsiveness

Test on mobile screen sizes:

1. Open browser DevTools (F12)
2. Toggle device toolbar
3. Test iPhone, iPad sizes
4. Check:
   - [ ] Layout adjusts properly
   - [ ] Text is readable
   - [ ] Buttons are tappable
   - [ ] No horizontal scrolling

## Test Results Checklist

After completing all tests:

### Backend ✅
- [ ] Health check works
- [ ] Quiz generation works
- [ ] Caching works
- [ ] History retrieval works
- [ ] Error handling works

### Frontend ✅
- [ ] Page loads correctly
- [ ] Quiz generation UI works
- [ ] History tab works
- [ ] Modal works
- [ ] Error messages display

### Database ✅
- [ ] Connection works
- [ ] Data is stored correctly
- [ ] Queries are efficient
- [ ] No orphaned data

### Integration ✅
- [ ] Different article types work
- [ ] Questions are high quality
- [ ] Related topics are relevant
- [ ] Entity extraction works

### Performance ✅
- [ ] Response times acceptable
- [ ] Caching improves speed
- [ ] No memory leaks
- [ ] Browser performance good

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| Timeout during quiz generation | Increase timeout, check Gemini API quota |
| Questions seem hallucinated | Review prompt in quiz_generator.py |
| Database errors | Check PostgreSQL is running |
| CORS errors | Verify CORS settings in main.py |
| Slow performance | Check article length, consider text truncation |

## Reporting Issues

If tests fail, collect:

1. Error messages from terminal
2. Browser console errors (F12)
3. Network tab requests/responses
4. Environment details:
   - Python version
   - PostgreSQL version
   - macOS version

## Success Criteria

All tests should pass with:
- ✅ No server crashes
- ✅ No database errors
- ✅ No frontend errors
- ✅ Quiz quality meets requirements
- ✅ Performance within acceptable ranges

---

**Testing Complete! 🎉**

If all tests pass, your Wiki Quiz App is production-ready!
