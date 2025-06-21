#!/usr/bin/env python3
import json
import os
import sys
from jinja2 import Template
import subprocess
from datetime import datetime
import re
from collections import Counter
import sqlite3

def load_data(master_path, job_path):
    """Load master content and job description"""
    with open(master_path, 'r') as f:
        master_data = json.load(f)
    
    with open(job_path, 'r') as f:
        job_data = json.load(f)
    
    return master_data, job_data

def calculate_skill_relevance(skills, job_requirements):
    """Calculate relevance score for skills based on job requirements"""
    job_keywords = set()
    for req in job_requirements:
        job_keywords.update(req.lower().split())
    
    skill_scores = {}
    for skill in skills:
        skill_words = set(skill.lower().split())
        overlap = len(skill_words.intersection(job_keywords))
        skill_scores[skill] = overlap
    
    return skill_scores

def prioritize_projects(projects, job_data):
    """Prioritize projects based on job focus areas and requirements"""
    focus_areas = job_data.get('focus_areas', [])
    requirements = job_data.get('requirements', [])
    preferred = job_data.get('preferred', [])
    
    job_keywords = set()
    for area in focus_areas + requirements + preferred:
        job_keywords.update(area.lower().split())
    
    project_scores = []
    for project in projects:
        score = 0
        # Check keywords in project
        for keyword in project.get('keywords', []):
            if keyword.lower() in job_keywords:
                score += 2
        
        # Check tools relevance
        tools_text = project.get('tools', '').lower()
        for keyword in job_keywords:
            if keyword in tools_text:
                score += 1
        
        project_scores.append((project, score))
    
    # Sort by score (highest first) and return top 3
    project_scores.sort(key=lambda x: x[1], reverse=True)
    return [p[0] for p in project_scores[:3]]

def tailor_content(master_data, job_data):
    """Customize resume based on job description"""
    tailored = master_data.copy()
    
    # Customize summary with job-specific focus
    company = job_data['company']
    title = job_data['title']
    base_summary = master_data['summary']
    
    # Add job-specific context to summary
    job_focus = f" Seeking {title} role at {company} to apply expertise in machine learning and data engineering."
    tailored['summary'] = base_summary + job_focus
    
    # Prioritize skills based on job requirements
    all_requirements = job_data.get('requirements', []) + job_data.get('preferred', [])
    skill_scores = calculate_skill_relevance(master_data['skills'], all_requirements)
    
    # Sort skills by relevance score
    sorted_skills = sorted(master_data['skills'], 
                          key=lambda x: skill_scores.get(x, 0), 
                          reverse=True)
    tailored['skills'] = sorted_skills
    
    # Prioritize and limit projects to most relevant
    tailored['projects'] = prioritize_projects(master_data['projects'], job_data)
    
    # Highlight relevant experience
    for exp in tailored['experience']:
        exp_keywords = exp.get('keywords', [])
        job_keywords = set()
        for req in all_requirements:
            job_keywords.update(req.lower().split())
        
        # Mark experience as highly relevant if keywords match
        exp['relevance_score'] = len(set(kw.lower() for kw in exp_keywords).intersection(job_keywords))
    
    # Sort experience by relevance (keeping current job first)
    exp_with_scores = [(i, exp) for i, exp in enumerate(tailored['experience'])]
    exp_with_scores.sort(key=lambda x: (x[0] == 0, x[1]['relevance_score']), reverse=True)
    tailored['experience'] = [exp for _, exp in exp_with_scores]
    
    return tailored

def log_application(job_data, output_path):
    """Log job application to tracking database"""
    db_path = 'data/applications.db'
    
    # Create database if it doesn't exist
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            position TEXT NOT NULL,
            location TEXT,
            date_applied TEXT NOT NULL,
            resume_path TEXT,
            status TEXT DEFAULT 'applied',
            notes TEXT
        )
    ''')
    
    # Insert application record
    cursor.execute('''
        INSERT INTO applications (company, position, location, date_applied, resume_path)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        job_data['company'],
        job_data['title'],
        job_data.get('location', ''),
        datetime.now().strftime('%Y-%m-%d'),
        output_path
    ))
    
    conn.commit()
    conn.close()
    print(f"Application logged for {job_data['company']} - {job_data['title']}")

def generate_pdf(tailored_data, template_path, output_path):
    """Generate PDF from tailored data"""
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Load template
        with open(template_path, 'r') as f:
            template = Template(f.read())
        
        # Render LaTeX
        latex_content = template.render(**tailored_data)
        
        # Write temporary LaTeX file
        temp_tex = output_path.replace('.pdf', '.tex')
        with open(temp_tex, 'w') as f:
            f.write(latex_content)
        
        # Compile to PDF
        result = subprocess.run(
            ['pdflatex', '-output-directory', os.path.dirname(output_path), temp_tex],
            capture_output=True, text=True
        )
        
        if result.returncode != 0:
            print(f"LaTeX compilation error: {result.stderr}")
            return False
        
        # Clean up auxiliary files
        for ext in ['.aux', '.log', '.tex']:
            temp_file = output_path.replace('.pdf', ext)
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print(f"Resume generated successfully: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False

def main():
    if len(sys.argv) not in [3, 4]:
        print("Usage: python generate_resume.py <job_description.json> <output_name> [--no-log]")
        sys.exit(1)
    
    job_file = sys.argv[1]
    output_name = sys.argv[2]
    log_application_flag = '--no-log' not in sys.argv
    
    # Validate input files exist
    master_path = 'data/master_content.json'
    template_path = 'templates/resume_template.tex'
    
    if not os.path.exists(job_file):
        print(f"Error: Job description file '{job_file}' not found")
        sys.exit(1)
    
    if not os.path.exists(master_path):
        print(f"Error: Master content file '{master_path}' not found")
        sys.exit(1)
    
    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found")
        sys.exit(1)
    
    output_path = f'output/{output_name}.pdf'
    
    try:
        # Load data
        master_data, job_data = load_data(master_path, job_file)
        
        # Tailor content
        tailored_data = tailor_content(master_data, job_data)
        
        # Generate PDF
        success = generate_pdf(tailored_data, template_path, output_path)
        
        if success and log_application_flag:
            # Log application
            log_application(job_data, output_path)
            
        print(f"\nResume tailored for {job_data['company']} - {job_data['title']}")
        print(f"Generated: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()