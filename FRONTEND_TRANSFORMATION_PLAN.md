# Frontend Transformation Plan: Medical Simulation → College Class Finding

## 🎯 **PROJECT OVERVIEW**
Transform the existing medical case simulation website into a college class-finding platform while preserving the chat functionality and voice features.

**What We're Keeping:**
- ✅ Chat interface and functionality
- ✅ Voice input/output capabilities (replace voice model with Rhyme)
- ✅ Overall layout structure
- ✅ Flask backend architecture

**What We're Changing:**
- 🔄 All medical content → College/academic content
- 🔄 Patient cases → Course catalogs
- 🔄 Medical terminology → Academic terminology
- 🔄 Voice model (current → Rhyme)

---

## 📋 **PHASE 1: CONTENT & BRANDING TRANSFORMATION**

### 1.1 Website Identity & Branding
- **Current:** "Sutra - Medical Case Simulations"
- **New:** "Sutra - Smart Class Finder" or "Sutra - Course Discovery"
- **Logo/Branding:** Keep "Sutra" name, update tagline
- **Color Scheme:** Consider academic blues/greens vs medical whites

### 1.2 Homepage Content (`templates/index.html`)
**Current Sections to Replace:**
- "Learn to Think Like a Doctor" → "Find Your Perfect Classes"
- "Practice clinical reasoning" → "Discover courses with AI assistance"
- "Interactive patient case simulations" → "Smart course recommendations"

**New Hero Section:**
```
Headline: "Find Your Perfect Classes with AI"
Subtext: "Get personalized course recommendations through voice or text. 
          Discover classes that match your interests, schedule, and academic goals."
CTA: "Start Finding Classes"
```

**New Feature Cards:**
1. **Voice Search** - "Ask about classes using natural language"
2. **Smart Matching** - "Get personalized course recommendations"
3. **Schedule Planning** - "Find classes that fit your timetable"

### 1.3 Navigation & Pages
- **Home** - Class finder landing page
- **Find Classes** - Main search/chat interface (replaces "Cases")
- **My Schedule** - Student's selected courses (new feature)
- **About** - About the platform

---

## 📋 **PHASE 2: DATA STRUCTURE TRANSFORMATION**

### 2.1 Replace Medical Data with Course Data
**Current:** `data/patient_cases.json`
**New:** `data/course_catalog.json`

**Sample Course Data Structure:**
```json
{
  "id": "COURSE001",
  "course_code": "CS 101",
  "title": "Introduction to Computer Science",
  "department": "Computer Science",
  "credits": 3,
  "prerequisites": ["None"],
  "description": "Fundamental concepts in computer science...",
  "schedule": {
    "days": ["Mon", "Wed", "Fri"],
    "time": "10:00 AM - 11:00 AM",
    "semester": "Fall 2025"
  },
  "instructor": "Dr. Sarah Johnson",
  "enrollment": {"current": 45, "max": 60},
  "difficulty": "Beginner",
  "tags": ["Programming", "Logic", "Problem Solving"]
}
```

### 2.2 Sample Course Categories
- **STEM:** Computer Science, Mathematics, Engineering, Biology
- **Liberal Arts:** English, History, Philosophy, Art
- **Business:** Accounting, Marketing, Management
- **Social Sciences:** Psychology, Sociology, Political Science

---

## 📋 **PHASE 3: UI/UX TRANSFORMATION**

### 3.1 Main Chat Interface (`templates/simulation.html` → `templates/class_finder.html`)

**Current Patient Interface → New Course Finder Interface:**

**Replace:**
- Patient profile section → Course search filters
- Medical history → Student preferences
- Diagnosis phase → Course selection phase

**New Interface Layout:**
```
┌─────────────────────────────────────────────┐
│ 🎓 Sutra Class Finder                      │
├─────────────────────────────────────────────┤
│ Search Filters:                             │
│ [Department ▼] [Credits ▼] [Time ▼]         │
│ [Difficulty ▼] [Semester ▼]                 │
├─────────────────────────────────────────────┤
│ Chat Interface:                             │
│ 🤖: "Hi! What classes are you looking for?" │
│ 👤: [Voice Input 🎤] [Text Input ✍️]       │
│                                             │
│ Course Recommendations:                     │
│ [Course Card 1] [Course Card 2] [...]       │
└─────────────────────────────────────────────┘
```

### 3.2 Course Cards (Replace Patient Cases)
**New Course Card Design:**
```html
<div class="course-card">
  <div class="course-header">
    <span class="course-code">CS 101</span>
    <span class="credits">3 Credits</span>
  </div>
  <h3>Introduction to Computer Science</h3>
  <div class="course-details">
    <p>👨‍🏫 Dr. Sarah Johnson</p>
    <p>📅 MWF 10:00-11:00 AM</p>
    <p>📍 Available Seats: 15/60</p>
  </div>
  <div class="course-tags">
    <span class="tag">Programming</span>
    <span class="tag">Beginner</span>
  </div>
  <button class="btn-add-course">Add to Schedule</button>
</div>
```

---

## 📋 **PHASE 4: VOICE INTEGRATION (RHYME REPLACEMENT)**

### 4.1 Replace Current Voice Model with Rhyme
**Files to Update:**
- `app.py` - Replace OpenAI TTS/STT endpoints
- `static/js/main.js` - Update voice recording functions

**Current Voice Functions to Replace:**
- `/api/transcribe` - Speech to text
- `/api/text-to-speech` - Text to speech
- JavaScript voice input handlers

**New Rhyme Integration Points:**
```python
# Replace in app.py
@app.route('/api/transcribe-rhyme', methods=['POST'])
def transcribe_with_rhyme():
    # Integrate Rhyme STT API
    pass

@app.route('/api/speak-rhyme', methods=['POST'])  
def speak_with_rhyme():
    # Integrate Rhyme TTS API
    pass
```

### 4.2 Voice Query Examples for Class Finding
**Sample Voice Interactions:**
- 🎤 "Find me computer science classes on Tuesdays and Thursdays"
- 🎤 "I need a 3-credit English course for spring semester"
- 🎤 "Show me beginner math classes with good professors"
- 🎤 "What classes are available after 2 PM?"

---

## 📋 **PHASE 5: SPECIFIC FILE UPDATES**

### 5.1 Templates to Update
**Priority Order:**

1. **`templates/index.html`** 
   - Update hero section content
   - Replace medical features with academic features
   - Update testimonials (medical students → college students)

2. **`templates/cases.html` → `templates/courses.html`**
   - Replace case filters with course filters
   - Update search functionality
   - Replace case cards with course cards

3. **`templates/simulation.html` → `templates/class_finder.html`**
   - Remove patient profile section
   - Add course search filters
   - Update chat prompts and responses
   - Replace medical phase indicators

4. **`templates/results.html` → `templates/schedule.html`**
   - Show selected courses instead of medical results
   - Display schedule overview
   - Show total credits

### 5.2 Static Assets to Update

**CSS (`static/css/styles.css`):**
- Update color scheme (medical → academic)
- Replace medical icons with academic icons
- Update component styles for course cards

**JavaScript (`static/js/main.js`):**
- Update voice input functions for Rhyme
- Replace medical terminology in prompts
- Update search/filter logic for courses

**Images (`static/images/`):**
- Replace doctor-patient.svg with student-studying.svg
- Replace medical icons with academic icons (books, graduation cap, etc.)
- Update placeholder images

### 5.3 Backend Updates (`app.py`)
**Routes to Rename/Update:**
- `/cases` → `/courses`
- `/simulation/<case_id>` → `/find-classes`
- Update chat prompts (medical → academic)
- Replace voice model endpoints

---

## 📋 **PHASE 6: IMPLEMENTATION PRIORITY**

### **Week 1: Core Content Transformation**
1. ✅ Update homepage content and branding
2. ✅ Create sample course data structure
3. ✅ Replace medical terminology in templates

### **Week 2: UI/UX Updates**
4. ✅ Transform main chat interface
5. ✅ Design course cards and filters
6. ✅ Update navigation and page flow

### **Week 3: Voice Integration**
7. ✅ Integrate Rhyme voice model
8. ✅ Update voice input/output functions
9. ✅ Test voice query functionality

### **Week 4: Polish & Testing**
10. ✅ Update all static assets
11. ✅ Cross-browser testing
12. ✅ Mobile responsiveness
13. ✅ Performance optimization

---

## 🔧 **TECHNICAL CONSIDERATIONS**

### Backend Integration Points
- **Course Search API** - Connect to your existing backend
- **Student Preferences** - Store user preferences
- **Schedule Building** - Integration with course scheduling logic

### Responsive Design
- Ensure chat interface works on mobile
- Course cards should be mobile-friendly
- Voice input should work on all devices

### Accessibility
- Voice input alternatives for accessibility
- Keyboard navigation for all features
- Screen reader compatibility

---

## 📝 **CONTENT WRITING NEEDS**

### New Copy Required:
1. **Homepage hero text** - Academic focused
2. **Feature descriptions** - Course finding benefits
3. **Chat prompts** - Academic assistance tone
4. **Error messages** - Student-friendly language
5. **Help text** - Course search guidance

### Tone & Voice:
- **Helpful and encouraging** (not clinical)
- **Student-focused** (not medical professional)
- **Conversational** (maintain chat-friendly tone)

---

## ✅ **SUCCESS METRICS**

### Functionality Checklist:
- [ ] Voice input works with Rhyme
- [ ] Text chat functions properly
- [ ] Course search and filters work
- [ ] Course recommendations display correctly
- [ ] Schedule building interface functions
- [ ] Mobile responsive design
- [ ] Cross-browser compatibility

### User Experience Goals:
- Intuitive course discovery
- Fast voice-to-text response
- Clear course information display
- Easy schedule management
- Seamless voice/text switching

---

**Ready to begin transformation! 🚀** 