# Claude AI Assistant - Project History & Context

## Project Overview
**Rosalina Torres - Resume Generator & Job Application System**
- Data Analytics Engineering MS student at Northeastern University 
- Seeking data engineer/ML/AI internships for Summer/Fall 2025
- Goal: Apply to at least 1 job per day with tailored resumes

## Current Session (2025-06-21)
### Tasks Completed ✅
1. **Repository Analysis** - Cloned and examined existing resume generator
2. **Code Enhancement** - Improved Python resume generator with:
   - Smart skill prioritization based on job requirements
   - Project highlighting matching job focus areas
   - Content tailoring using job keywords
   - Error handling and validation
   - Application logging to SQLite database

3. **Job Tracking System** - Created comprehensive tracking tools:
   - `job_tracker.py` - CLI application tracker with database
   - `daily_apply.py` - Interactive daily application assistant
   - Web application foundation with modern UI

4. **Web Application** - Built enhanced job tracker web app:
   - Modern responsive design with dark theme
   - Dashboard with application stats and daily goals
   - Application management with search/filter
   - AI-powered resume builder interface
   - Analytics and insights section

### Key Files Created/Modified
- `/scripts/generate_resume.py` - Enhanced with AI-powered tailoring
- `/scripts/job_tracker.py` - SQLite-based application tracking
- `/scripts/daily_apply.py` - Interactive daily application workflow
- `/web_app/index.html` - Modern web interface
- `/web_app/styles.css` - Professional styling
- `/CLAUDE.md` - This context file

### Current Repository Structure
```
resume-generator/
├── data/
│   ├── master_content.json (personal profile data)
│   ├── job_descriptions/ (job-specific requirements)
│   └── applications.db (SQLite tracking database)
├── scripts/
│   ├── generate_resume.py (enhanced AI tailoring)
│   ├── job_tracker.py (CLI tracking tool)
│   └── daily_apply.py (daily workflow assistant)
├── templates/
│   └── resume_template.tex (LaTeX template)
├── web_app/
│   ├── index.html (modern web interface)
│   ├── styles.css (professional styling)
│   └── app.js (JavaScript functionality - pending)
└── output/ (generated resume PDFs)
```

## Technical Improvements Made
### 1. Smart Resume Tailoring
- **Skill Relevance Scoring** - Prioritizes skills based on job requirements
- **Project Matching** - Highlights most relevant projects for each role
- **Experience Ranking** - Reorders experience by relevance while keeping current job first
- **Keyword Integration** - Analyzes job descriptions for optimal content matching

### 2. Application Tracking Database
- **SQLite Integration** - Persistent storage for all applications
- **Daily Goal Tracking** - Monitors daily application targets
- **Status Management** - Tracks application progress (applied/interview/rejected/offer)
- **Follow-up Reminders** - Automated reminders for follow-up actions

### 3. Enhanced User Experience
- **Error Handling** - Robust validation and error messages
- **Interactive CLI** - User-friendly command-line interface
- **Web Application** - Modern, responsive web interface
- **Automation Features** - Quick actions and template generation

## Job Search Strategy
### Target Roles
- Data Engineer positions
- ML Engineer roles
- Data Scientist internships  
- AI/ML internships
- Summer 2025 and Fall 2025 positions

### Target Companies
- Tech companies (Netflix, Google, Meta, etc.)
- Startups in Boston area
- Companies with strong data/ML focus
- Remote-friendly organizations

### Daily Workflow
1. **Morning Setup** - Run `daily_apply.py` to start session
2. **Job Site Browsing** - Automated opening of job boards
3. **Application Process** - Use tailored resume generation
4. **Progress Tracking** - Log applications and follow-ups
5. **Evening Review** - Check daily goals and plan next day

## Integration Points
### Existing Web Application
- **Original URL**: https://aesthetic-longma-7aa42a.netlify.app/job-tracker.html
- **Current Features**: Memory-based tracking, resume builder, cover letter generator
- **Enhancement Plan**: Integrate with new SQLite backend and enhanced tailoring

### Next Steps for Integration
1. **Complete JavaScript Frontend** - Finish `app.js` with API integration
2. **Backend API** - Create Express.js server for database operations
3. **Data Migration** - Import existing web app functionality
4. **Cloud Deployment** - Deploy enhanced system to Netlify/Vercel
5. **Mobile Optimization** - Ensure mobile-responsive design

## Commands to Remember
### Resume Generation
```bash
cd /Users/rosalinatorres/resume-generator
python scripts/generate_resume.py data/job_descriptions/company_position.json output_name
```

### Job Tracking
```bash
# Daily summary
python scripts/job_tracker.py summary

# Add application
python scripts/job_tracker.py add --company "Netflix" --position "ML Engineer"

# Start daily session
python scripts/daily_apply.py
```

### Development Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Start local server (when backend is ready)
python -m http.server 8000
```

## Personal Context
- **Student**: MS Data Analytics Engineering at Northeastern University
- **GPA**: 4.0
- **Languages**: English, Spanish, Portuguese
- **Location**: Boston, Massachusetts
- **Experience**: 8+ years in tech sales, recent pivot to data engineering
- **Strengths**: Business acumen + technical skills, bilingual capabilities
- **Target**: Data engineering and ML roles with business impact

## AI Assistant Guidelines
When continuing this project:
1. **Maintain Context** - Always reference this file for project state
2. **Prioritize Job Search** - Focus on features that accelerate daily applications
3. **Preserve Data** - Never overwrite existing application data
4. **Enhance Tailoring** - Continuously improve resume matching algorithms
5. **User-Centric Design** - Optimize for Rosalina's daily workflow

## Recent Insights
- Resume tailoring significantly improves application quality
- Daily goal tracking maintains momentum
- Automated workflows reduce manual effort
- Web interface provides better user experience than CLI alone
- Integration with existing tools increases adoption

---
*Last Updated: 2025-06-21*
*Next Session: Continue with JavaScript frontend completion and backend API development*