#!/usr/bin/env python3
import json
import os
import sys
from jinja2 import Template
import subprocess

def load_data(master_path, job_path):
    """Load master content and job description"""
    with open(master_path, 'r') as f:
        master_data = json.load(f)
    
    with open(job_path, 'r') as f:
        job_data = json.load(f)
    
    return master_data, job_data

def tailor_content(master_data, job_data):
    """Customize resume based on job description"""
    # Start with all master data
    tailored = master_data.copy()
    
    # Customize objective based on job
    tailored['objective'] = f"Seeking {job_data['title']} position at {job_data['company']} to {job_data.get('company_goal', 'drive innovation and create value through data-driven solutions')}."
    
    # For now, pass through most data as-is
    # In a full implementation, we'd analyze keywords and reorder/filter content
    
    return tailored

def generate_pdf(tailored_data, template_path, output_path):
    """Generate PDF from tailored data"""
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
    subprocess.run(['pdflatex', '-output-directory', os.path.dirname(output_path), temp_tex], 
                   capture_output=True)
    
    # Clean up auxiliary files
    for ext in ['.aux', '.log']:
        temp_file = output_path.replace('.pdf', ext)
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print(f"Resume generated: {output_path}")

def main():
    if len(sys.argv) != 3:
        print("Usage: python generate_resume.py <job_description.json> <output_name>")
        sys.exit(1)
    
    job_file = sys.argv[1]
    output_name = sys.argv[2]
    
    # Paths
    master_path = 'data/master_content.json'
    template_path = 'templates/resume_template.tex'
    output_path = f'output/{output_name}.pdf'
    
    # Load data
    master_data, job_data = load_data(master_path, job_file)
    
    # Tailor content
    tailored_data = tailor_content(master_data, job_data)
    
    # Generate PDF
    generate_pdf(tailored_data, template_path, output_path)

if __name__ == "__main__":
    main()