# Resume Generator 🚀

An AI-powered resume tailoring system that automatically customizes your resume for each job application, helping you land more interviews.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## ✨ Features

- **🤖 AI-Powered Tailoring**: Automatically reorders skills and selects relevant projects based on job requirements
- **📊 Application Tracking**: Built-in SQLite database to track all your job applications
- **🎯 Daily Goals**: Helps maintain consistency with daily application targets
- **🌐 Web Dashboard**: Modern interface to manage applications and view analytics
- **📄 LaTeX Output**: Generates professional PDF resumes using LaTeX
- **🔄 GitHub Actions**: Automated workflows for continuous resume updates

## 🛠️ Tech Stack

- **Backend**: Python 3.8+
- **Resume Generation**: LaTeX, Jinja2
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **CI/CD**: GitHub Actions

## 📋 Prerequisites

- Python 3.8 or higher
- LaTeX distribution (for PDF generation)
  - macOS: `brew install --cask mactex-no-gui`
  - Ubuntu: `sudo apt-get install texlive-full`
  - Windows: Install [MiKTeX](https://miktex.org/)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/rosalinatorres888/resume-generator.git
cd resume-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Your Master Resume

Edit `data/master_content.json` with your information:

```json
{
  "name": "Your Name",
  "email": "your.email@example.com",
  "phone": "(123) 456-7890",
  "linkedin": "linkedin.com/in/yourprofile",
  "github": "github.com/yourusername",
  "summary": "Your professional summary...",
  "skills": ["Python", "Machine Learning", "SQL", ...],
  "experience": [...],
  "projects": [...],
  "education": [...]
}
```

### 4. Create a Job Description

Add job descriptions in `data/job_descriptions/` as JSON files:

```json
{
  "company": "TechCorp",
  "title": "Machine Learning Engineer",
  "location": "San Francisco, CA",
  "requirements": [
    "3+ years Python experience",
    "Experience with TensorFlow/PyTorch",
    "Strong understanding of ML algorithms"
  ],
  "preferred": [
    "Published ML research",
    "Experience with distributed systems"
  ],
  "focus_areas": [
    "Computer Vision",
    "Natural Language Processing"
  ]
}
```

### 5. Generate Your Tailored Resume

```bash
python scripts/generate_resume.py data/job_descriptions/techcorp_ml.json techcorp_resume
```

This creates `output/techcorp_resume.pdf` tailored specifically for that job!

## 📁 Project Structure

```
resume-generator/
├── data/
│   ├── master_content.json          # Your main resume data
│   ├── job_descriptions/            # Job posting JSONs
│   └── applications.db              # Application tracking database
├── scripts/
│   ├── generate_resume.py           # Resume tailoring engine
│   ├── job_tracker.py              # Application tracking CLI
│   └── daily_apply.py              # Daily workflow automation
├── templates/
│   └── resume_template.tex         # LaTeX template
├── output/                         # Generated PDFs
├── web_app/                        # Web dashboard
│   ├── index.html
│   ├── styles.css
│   └── app.js
└── .github/
    └── workflows/                  # GitHub Actions
```

## 💻 Usage Examples

### Generate a Tailored Resume

```bash
# Basic usage
python scripts/generate_resume.py data/job_descriptions/company.json output_name

# Without logging to tracker
python scripts/generate_resume.py data/job_descriptions/company.json output_name --no-log
```

### Track Your Applications

```bash
# Check daily progress
python scripts/job_tracker.py summary

# Add new application
python scripts/job_tracker.py add --company "Google" --position "ML Engineer" --location "Mountain View, CA"

# List all applications
python scripts/job_tracker.py list

# Update application status
python scripts/job_tracker.py update 1 --status "interviewing"

# View weekly report
python scripts/job_tracker.py report
```

### Use the Web Dashboard

```bash
# Open the web interface
cd web_app
open index.html  # macOS
# OR
xdg-open index.html  # Linux
# OR
start index.html  # Windows
```

## 🎯 Daily Workflow

1. **Find Job Posting**: Browse job boards for relevant positions
2. **Create Job JSON**: Save job requirements in `data/job_descriptions/`
3. **Generate Resume**: Run the generator with the job JSON
4. **Apply**: Submit your tailored resume
5. **Track**: Log the application in your tracker
6. **Repeat**: Aim for at least 1 application per day!

## 🤖 How It Works

The AI-powered tailoring system:

1. **Analyzes Job Requirements**: Extracts keywords and skills from job descriptions
2. **Scores Your Content**: Ranks your skills, projects, and experiences by relevance
3. **Optimizes Layout**: Reorders content to highlight most relevant items first
4. **Customizes Summary**: Adds job-specific focus to your professional summary
5. **Generates PDF**: Creates a professional LaTeX-formatted resume

## 🌐 Web Dashboard Features

- **Dashboard**: Application statistics, daily goals, quick actions
- **Applications**: Searchable list with filters and status updates
- **Resume Builder**: Visual interface for generating tailored resumes
- **Analytics**: Progress tracking and insights

## 🔧 Configuration

### Customize LaTeX Template

Edit `templates/resume_template.tex` to modify the resume design.

### Add Custom Sections

In `master_content.json`, add new sections:

```json
{
  "custom_section": {
    "title": "Publications",
    "items": [...]
  }
}
```

## 📊 Application Status Types

- `applied` - Initial application sent
- `screening` - Under review
- `interviewing` - In interview process
- `rejected` - Application declined
- `offer` - Received job offer
- `accepted` - Offer accepted
- `withdrawn` - Application withdrawn

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built for data science and ML engineering students
- Inspired by the need to streamline job applications


## 📧 Contact

Rosalina Torres - [@rosalinatorres888](https://github.com/rosalinatorres888)

Project Link: [https://github.com/rosalinatorres888/resume-generator](https://github.com/rosalinatorres888/resume-generator)

---

**🎯 Goal**: Apply to at least 1 job per day with a perfectly tailored resume!
