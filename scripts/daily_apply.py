#!/usr/bin/env python3
"""
Daily Job Application Automation
Streamlines the daily job application process
"""

import os
import json
import webbrowser
from datetime import datetime
from job_tracker import JobTracker

class DailyApplyAssistant:
    def __init__(self):
        self.tracker = JobTracker()
        self.job_sites = {
            'linkedin': 'https://www.linkedin.com/jobs/search/?keywords=data%20engineer%20machine%20learning&location=Boston%2C%20Massachusetts&f_TPR=r86400',
            'indeed': 'https://www.indeed.com/jobs?q=data+engineer+machine+learning&l=Boston%2C+MA&fromage=1',
            'glassdoor': 'https://www.glassdoor.com/Job/boston-data-engineer-jobs-SRCH_IL.0,6_IC1154532_KO7,20.htm',
            'builtin': 'https://builtin.com/jobs/data-science-analytics/boston',
            'angellist': 'https://angel.co/jobs?locationSlug=boston&roleTypes=data-scientist',
        }
    
    def start_daily_session(self):
        """Start the daily application session"""
        print("🚀 Starting Daily Job Application Session")
        print("=" * 50)
        
        # Show daily summary
        self.tracker.daily_summary()
        
        # Show follow-up reminders
        self.tracker.follow_up_reminders()
        
        # Open job sites
        self.open_job_sites()
        
        # Interactive mode
        self.interactive_mode()
    
    def open_job_sites(self):
        """Open job search sites in browser"""
        print("\n🌐 Opening Job Sites...")
        
        response = input("Open job sites in browser? (y/n): ").lower()
        if response == 'y':
            for site, url in self.job_sites.items():
                print(f"Opening {site}...")
                webbrowser.open(url)
        
        print("\n💡 Focus Areas for Today:")
        print("- Data Engineer positions")
        print("- ML Engineer roles") 
        print("- Data Scientist internships")
        print("- AI/ML internships")
        print("- Summer 2025 and Fall 2025 positions")
    
    def interactive_mode(self):
        """Interactive application tracking"""
        print("\n" + "=" * 50)
        print("📝 Interactive Application Mode")
        print("Commands: add, status, summary, done")
        
        while True:
            command = input("\nEnter command: ").lower().strip()
            
            if command == 'add':
                self.add_application_interactive()
            
            elif command == 'status':
                self.update_status_interactive()
            
            elif command == 'summary':
                self.tracker.daily_summary()
            
            elif command == 'done':
                self.end_session()
                break
            
            elif command in ['help', 'h']:
                print("Available commands:")
                print("  add - Add new application")
                print("  status - Update application status")
                print("  summary - Show daily summary")
                print("  done - End session")
            
            else:
                print("Unknown command. Type 'help' for available commands.")
    
    def add_application_interactive(self):
        """Interactive application adding"""
        print("\n📋 Adding New Application")
        
        company = input("Company name: ").strip()
        if not company:
            print("Company name required!")
            return
        
        position = input("Position title: ").strip()
        if not position:
            print("Position title required!")
            return
        
        location = input("Location (optional): ").strip()
        job_url = input("Job URL (optional): ").strip()
        notes = input("Notes (optional): ").strip()
        
        # Ask about resume generation
        generate_resume = input("Generate tailored resume? (y/n): ").lower()
        
        if generate_resume == 'y':
            self.generate_resume_interactive(company, position, location)
        
        # Add to tracker
        self.tracker.add_application(company, position, location, job_url, notes)
        
        print(f"✅ Application added and tracked!")
    
    def generate_resume_interactive(self, company, position, location):
        """Interactive resume generation"""
        print("\n📄 Generating Tailored Resume")
        
        # Create job description JSON
        job_data = {
            "title": position,
            "company": company,
            "location": location,
            "description": f"{position} role at {company}",
            "company_goal": "leverage data and ML to drive business impact",
            "requirements": self.get_common_requirements(position),
            "focus_areas": self.get_focus_areas(position)
        }
        
        # Save job description
        job_filename = f"data/job_descriptions/{company.lower().replace(' ', '_')}_{position.lower().replace(' ', '_')}.json"
        os.makedirs(os.path.dirname(job_filename), exist_ok=True)
        
        with open(job_filename, 'w') as f:
            json.dump(job_data, f, indent=2)
        
        # Generate resume
        output_name = f"{company.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        print(f"Generating resume for {company}...")
        os.system(f"cd /Users/rosalinatorres/resume-generator && python scripts/generate_resume.py {job_filename} {output_name}")
    
    def get_common_requirements(self, position):
        """Get common requirements based on position type"""
        position_lower = position.lower()
        
        if 'data engineer' in position_lower:
            return [
                "Python programming",
                "SQL databases", 
                "ETL pipelines",
                "Cloud platforms (AWS/GCP)",
                "Apache Spark",
                "Data warehousing",
                "Docker/Kubernetes"
            ]
        elif 'machine learning' in position_lower or 'ml engineer' in position_lower:
            return [
                "Python programming",
                "Machine Learning",
                "PyTorch/TensorFlow",
                "MLOps pipelines",
                "Model deployment",
                "Statistical analysis",
                "Computer vision or NLP"
            ]
        elif 'data scientist' in position_lower:
            return [
                "Python/R programming",
                "Statistical modeling",
                "Machine Learning",
                "Data visualization",
                "Experimental design",
                "Business intelligence",
                "Communication skills"
            ]
        else:
            return [
                "Python programming",
                "Data analysis",
                "Machine Learning",
                "Statistics",
                "Problem solving"
            ]
    
    def get_focus_areas(self, position):
        """Get focus areas based on position"""
        position_lower = position.lower()
        
        if 'data engineer' in position_lower:
            return [
                "Data Pipeline Architecture",
                "ETL/ELT Processing",
                "Data Infrastructure",
                "Cloud Data Platforms"
            ]
        elif 'machine learning' in position_lower:
            return [
                "ML Model Development",
                "Model Deployment & MLOps",
                "Deep Learning",
                "AI Research"
            ]
        else:
            return [
                "Data Analysis",
                "Statistical Modeling",
                "Business Intelligence",
                "Data Visualization"
            ]
    
    def update_status_interactive(self):
        """Interactive status update"""
        print("\n📊 Update Application Status")
        
        # Show recent applications
        self.tracker.list_applications(limit=5)
        
        try:
            app_id = int(input("\nEnter application ID to update: "))
            status = input("New status (applied/interview/rejected/offer): ").strip()
            notes = input("Notes (optional): ").strip()
            
            self.tracker.update_status(app_id, status, notes)
        except ValueError:
            print("Invalid application ID!")
    
    def end_session(self):
        """End the daily session"""
        print("\n🎯 Session Complete!")
        self.tracker.daily_summary()
        self.tracker.weekly_report()
        
        print("\n💪 Keep up the great work!")
        print("Remember: Consistency is key to landing your dream role!")

def main():
    assistant = DailyApplyAssistant()
    assistant.start_daily_session()

if __name__ == "__main__":
    main()