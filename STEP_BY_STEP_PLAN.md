# Step-by-Step Frontend Transformation Plan
## Medical Simulation → College Class Finding Website

**Goal:** Transform the frontend while keeping chat functionality, voice features, and your existing backend.

---

## 🎯 **STEP 1: UPDATE HOMEPAGE CONTENT**
**File:** `templates/index.html`

### What to Change:
1. **Page Title:** "Courseium - Medical Case Simulations" → "Courseium - Smart Class Finder"
2. **Hero Headline:** "Learn to Think Like a Doctor" → "Find Your Perfect Classes with AI"
3. **Hero Subtext:** Replace medical description with class-finding description
4. **Call-to-Action Button:** "Start Simulation" → "Find Classes"

### Specific Text Replacements:
```html
<!-- OLD -->
<h1>Learn to Think Like a Doctor</h1>
<p>Practice clinical reasoning with interactive patient case simulations.</p>

<!-- NEW -->
<h1>Find Your Perfect Classes with AI</h1>
<p>Get personalized course recommendations through voice or text. Discover classes that match your interests and schedule.</p>
```

**✅ Completion Criteria:** Homepage shows class-finding content instead of medical content.

---

## 🎯 **STEP 2: UPDATE NAVIGATION & FEATURE CARDS**
**File:** `templates/index.html`

### Navigation Changes:
- "Cases" → "Find Classes"
- Keep "Home" and "About"

### Feature Cards Section:
Replace the 3 "How It Works" cards:

**OLD Cards:**
1. "Interview the Patient"
2. "Analyze and Diagnose" 
3. "Review Performance"

**NEW Cards:**
1. **"Voice Search"** - "Ask about classes using natural language"
2. **"Smart Matching"** - "Get personalized course recommendations" 
3. **"Schedule Planning"** - "Find classes that fit your timetable"

**✅ Completion Criteria:** Feature cards describe class-finding instead of medical diagnosis.

---

## 🎯 **STEP 3: UPDATE TESTIMONIALS SECTION**
**File:** `templates/index.html`

### Replace Medical Student Testimonials:
```html
<!-- OLD -->
<p>"Courseium helped me develop my clinical reasoning skills..."</p>
<div class="testimonial-author">- Medical Student, Year 2</div>

<!-- NEW -->
<p>"Courseium helped me find the perfect classes for my major and schedule!"</p>
<div class="testimonial-author">- College Student, Sophomore</div>
```

**✅ Completion Criteria:** Testimonials are from college students about class finding.

---

## 🎯 **STEP 4: RENAME AND UPDATE CASES PAGE**
**Files:** `templates/cases.html` → `templates/courses.html`

### Actions:
1. **Rename file:** `cases.html` → `courses.html`
2. **Update page title:** "Medical Cases" → "Find Courses"
3. **Update filter labels:**
   - "Condition" → "Department"
   - "Age" → "Credits"
   - "Gender" → "Semester"
4. **Update search placeholder:** "Search cases..." → "Search courses..."

**✅ Completion Criteria:** Courses page has academic filters instead of medical ones.

---

## 🎯 **STEP 5: UPDATE MAIN CHAT INTERFACE**
**Files:** `templates/simulation.html` → `templates/class_finder.html`

### Major Changes:
1. **Rename file:** `simulation.html` → `class_finder.html`
2. **Update page title:** "Case Simulation" → "Class Finder"
3. **Replace patient profile section** with course search filters
4. **Update phase indicators:**
   - "Patient Assessment" → "Course Search"
   - "Differential Diagnosis" → "Schedule Building"

### Remove Patient-Specific Elements:
- Patient image section
- Medical history details
- Vital signs
- Physical exam details

**✅ Completion Criteria:** Main interface focuses on course finding instead of patient diagnosis.

---

## 🎯 **STEP 6: UPDATE BACKEND ROUTES**
**File:** `app.py`

### Route Updates:
```python
# OLD
@app.route('/cases')
def cases():

# NEW  
@app.route('/courses')
def courses():

# OLD
@app.route('/simulation/<case_id>')
def simulation(case_id):

# NEW
@app.route('/find-classes')
def find_classes():
```

### Chat Prompt Updates:
Replace medical AI prompts with academic assistance prompts in the `/api/chat` route.

**✅ Completion Criteria:** Routes use academic terminology and URLs.

---

## 🎯 **STEP 7: UPDATE JAVASCRIPT FUNCTIONALITY**
**File:** `static/js/main.js`

### Function Updates:
1. **Replace medical voice prompts** with academic ones
2. **Update placeholder text** in voice input functions
3. **Change filter logic** from medical terms to academic terms

### Example Voice Prompt Changes:
```javascript
// OLD
textArea.value = 'Can you tell me more about your pain? When did it start?';

// NEW  
textArea.value = 'What type of classes are you looking for this semester?';
```

**✅ Completion Criteria:** Voice inputs generate academic questions instead of medical ones.

---

## 🎯 **STEP 8: REPLACE HERO IMAGE**
**File:** `static/images/`

### Image Updates:
1. **Replace:** `doctor-patient.svg` → `student-studying.svg` or similar academic image
2. **Update alt text** in `templates/index.html`
3. **Consider updating:** Medical icons → Academic icons (books, graduation cap, etc.)

**✅ Completion Criteria:** Homepage image shows academic/student theme instead of medical.

---

## 🎯 **STEP 9: UPDATE CSS STYLING (OPTIONAL)**
**File:** `static/css/styles.css`

### Color Scheme Changes:
- Consider changing from medical whites/blues to academic colors
- Update any medical-specific styling
- Ensure course cards look different from patient cards

**✅ Completion Criteria:** Visual theme feels academic rather than medical.

---

## 🎯 **STEP 10: INTEGRATE RHYME VOICE MODEL**
**Files:** `app.py` and `static/js/main.js`

### Backend Changes:
```python
# Replace OpenAI voice endpoints with Rhyme
@app.route('/api/transcribe-rhyme', methods=['POST'])
def transcribe_with_rhyme():
    # Your Rhyme STT integration
    pass

@app.route('/api/speak-rhyme', methods=['POST'])  
def speak_with_rhyme():
    # Your Rhyme TTS integration
    pass
```

### Frontend Changes:
Update JavaScript to call new Rhyme endpoints instead of OpenAI endpoints.

**✅ Completion Criteria:** Voice input/output uses Rhyme instead of current voice model.

---

## 📋 **COMPLETION CHECKLIST**

**Phase 1 - Content Updates:**
- [ ] Step 1: Homepage content updated
- [ ] Step 2: Navigation and feature cards updated  
- [ ] Step 3: Testimonials updated
- [ ] Step 4: Cases page renamed and updated

**Phase 2 - Interface Updates:**
- [ ] Step 5: Main chat interface updated
- [ ] Step 6: Backend routes updated
- [ ] Step 7: JavaScript functionality updated

**Phase 3 - Assets & Integration:**
- [ ] Step 8: Images replaced
- [ ] Step 9: CSS styling updated (optional)
- [ ] Step 10: Rhyme voice model integrated

---

## 🚀 **SUGGESTED ORDER**

**Start Here (Easy Wins):**
1. Step 1 → Step 2 → Step 3 (Homepage transformation)
2. Step 8 (Image replacement)  
3. Step 4 (Courses page)

**Then Continue:**
4. Step 5 (Main interface)
5. Step 6 & 7 (Backend/JavaScript)

**Finish With:**
6. Step 10 (Rhyme integration)
7. Step 9 (CSS polish)

---

**Each step is independent and can be completed one at a time. Start with Step 1 when ready! 🎓** 