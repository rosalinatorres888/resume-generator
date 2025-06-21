#!/usr/bin/env python3
"""
Job Application Tracker
Track daily applications and manage job search progress
"""

import sqlite3
import json
import os
from datetime import datetime, timedelta
import argparse

class JobTracker:
    def __init__(self, db_path='data/applications.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the applications database"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
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
                notes TEXT,
                job_url TEXT,
                follow_up_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS daily_goals (
                date TEXT PRIMARY KEY,
                target_applications INTEGER DEFAULT 1,
                actual_applications INTEGER DEFAULT 0
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_application(self, company, position, location='', job_url='', notes=''):
        """Add a new job application"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        follow_up = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            INSERT INTO applications 
            (company, position, location, date_applied, job_url, notes, follow_up_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (company, position, location, today, job_url, notes, follow_up))
        
        # Update daily count
        cursor.execute('''
            INSERT OR REPLACE INTO daily_goals (date, actual_applications)
            VALUES (?, COALESCE(
                (SELECT actual_applications FROM daily_goals WHERE date = ?) + 1, 
                1
            ))
        ''', (today, today))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Added application: {company} - {position}")
    
    def update_status(self, app_id, status, notes=''):
        """Update application status"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE applications 
            SET status = ?, notes = ?
            WHERE id = ?
        ''', (status, notes, app_id))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Updated application #{app_id} status to: {status}")
    
    def daily_summary(self):
        """Show today's application progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Today's applications
        cursor.execute('''
            SELECT company, position, status FROM applications 
            WHERE date_applied = ?
            ORDER BY id DESC
        ''', (today,))
        
        today_apps = cursor.fetchall()
        
        # Daily goal
        cursor.execute('SELECT actual_applications FROM daily_goals WHERE date = ?', (today,))
        result = cursor.fetchone()
        actual = result[0] if result else 0
        
        conn.close()
        
        print(f"\n📊 Daily Summary ({today})")
        print(f"Goal: 1 application | Actual: {actual}")
        print(f"Status: {'✅ Goal Met!' if actual >= 1 else '⏰ Keep Going!'}")
        
        if today_apps:
            print("\nToday's Applications:")
            for i, (company, position, status) in enumerate(today_apps, 1):
                print(f"  {i}. {company} - {position} ({status})")
        else:
            print("\nNo applications today yet. Time to apply! 🚀")
    
    def weekly_report(self):
        """Show this week's progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT date_applied, COUNT(*) as count 
            FROM applications 
            WHERE date_applied >= ?
            GROUP BY date_applied
            ORDER BY date_applied DESC
        ''', (week_ago,))
        
        weekly_data = cursor.fetchall()
        
        cursor.execute('''
            SELECT COUNT(*) FROM applications 
            WHERE date_applied >= ?
        ''', (week_ago,))
        
        total = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"\n📈 Weekly Report (Last 7 Days)")
        print(f"Total Applications: {total}")
        print(f"Daily Average: {total/7:.1f}")
        
        if weekly_data:
            print("\nDaily Breakdown:")
            for date, count in weekly_data:
                print(f"  {date}: {count} applications")
    
    def list_applications(self, status=None, limit=10):
        """List recent applications"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT id, company, position, date_applied, status, follow_up_date
                FROM applications 
                WHERE status = ?
                ORDER BY date_applied DESC
                LIMIT ?
            ''', (status, limit))
        else:
            cursor.execute('''
                SELECT id, company, position, date_applied, status, follow_up_date
                FROM applications 
                ORDER BY date_applied DESC
                LIMIT ?
            ''', (limit,))
        
        apps = cursor.fetchall()
        conn.close()
        
        if not apps:
            print("No applications found.")
            return
        
        print(f"\n📋 Recent Applications {f'({status})' if status else ''}")
        for app_id, company, position, date, status, follow_up in apps:
            print(f"  #{app_id}: {company} - {position}")
            print(f"    Applied: {date} | Status: {status} | Follow-up: {follow_up}")
    
    def follow_up_reminders(self):
        """Show applications that need follow-up"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        cursor.execute('''
            SELECT id, company, position, date_applied, follow_up_date
            FROM applications 
            WHERE follow_up_date <= ? AND status = 'applied'
            ORDER BY follow_up_date
        ''', (today,))
        
        reminders = cursor.fetchall()
        conn.close()
        
        if reminders:
            print(f"\n🔔 Follow-up Reminders")
            for app_id, company, position, applied, follow_up in reminders:
                print(f"  #{app_id}: {company} - {position}")
                print(f"    Applied: {applied} | Follow-up due: {follow_up}")
        else:
            print("\n✅ No follow-ups needed today!")

def main():
    parser = argparse.ArgumentParser(description='Job Application Tracker')
    parser.add_argument('command', choices=['add', 'update', 'summary', 'weekly', 'list', 'followup'])
    parser.add_argument('--company', help='Company name')
    parser.add_argument('--position', help='Position title')
    parser.add_argument('--location', help='Job location')
    parser.add_argument('--url', help='Job posting URL')
    parser.add_argument('--notes', help='Additional notes')
    parser.add_argument('--id', type=int, help='Application ID')
    parser.add_argument('--status', help='Application status')
    parser.add_argument('--limit', type=int, default=10, help='Limit results')
    
    args = parser.parse_args()
    tracker = JobTracker()
    
    if args.command == 'add':
        if not args.company or not args.position:
            print("Error: --company and --position are required for adding applications")
            return
        tracker.add_application(
            args.company, args.position, 
            args.location or '', args.url or '', args.notes or ''
        )
    
    elif args.command == 'update':
        if not args.id or not args.status:
            print("Error: --id and --status are required for updating")
            return
        tracker.update_status(args.id, args.status, args.notes or '')
    
    elif args.command == 'summary':
        tracker.daily_summary()
    
    elif args.command == 'weekly':
        tracker.weekly_report()
    
    elif args.command == 'list':
        tracker.list_applications(args.status, args.limit)
    
    elif args.command == 'followup':
        tracker.follow_up_reminders()

if __name__ == "__main__":
    main()