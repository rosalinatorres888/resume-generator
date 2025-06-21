// Job Application Tracker - Enhanced Web Application
class JobApplicationTracker {
    constructor() {
        this.applications = this.loadApplications();
        this.dailyGoal = 1;
        this.currentTab = 'dashboard';
        this.selectedTemplate = 'technical';
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStats();
        this.renderRecentApplications();
        this.updateDailyProgress();
        this.generateInsights();
        
        // Load dashboard by default
        this.showTab('dashboard');
    }

    setupEventListeners() {
        // Tab navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tab = e.target.getAttribute('data-tab');
                this.showTab(tab);
            });
        });

        // Add application form
        document.getElementById('add-app-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.addApplication();
        });

        // Search and filter
        document.getElementById('search-apps').addEventListener('input', () => {
            this.filterApplications();
        });

        document.getElementById('status-filter').addEventListener('change', () => {
            this.filterApplications();
        });

        // Template selection
        document.querySelectorAll('.template-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.selectTemplate(e.currentTarget.getAttribute('data-template'));
            });
        });

        // Quick actions
        window.openJobSites = () => this.openJobSites();
        window.quickAddApplication = () => this.showAddApplicationForm();
        window.generateResume = () => this.showTab('resume');
        window.generateTailoredResume = () => this.generateTailoredResume();
        window.showAddApplicationForm = () => this.showAddApplicationForm();
        window.closeModal = () => this.closeModal();
    }

    // Tab Management
    showTab(tabName) {
        // Update navigation
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-tab="${tabName}"]`).classList.add('active');

        // Update content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.getElementById(tabName).classList.add('active');

        this.currentTab = tabName;

        // Load tab-specific content
        if (tabName === 'applications') {
            this.renderApplications();
        } else if (tabName === 'analytics') {
            this.renderAnalytics();
        }
    }

    // Application Management
    addApplication() {
        const formData = {
            id: Date.now(),
            company: document.getElementById('app-company').value,
            position: document.getElementById('app-position').value,
            location: document.getElementById('app-location').value,
            url: document.getElementById('app-url').value,
            salary: document.getElementById('app-salary').value,
            notes: document.getElementById('app-notes').value,
            dateApplied: new Date().toISOString().split('T')[0],
            status: 'applied',
            followUpDate: this.calculateFollowUpDate()
        };

        this.applications.push(formData);
        this.saveApplications();
        this.updateStats();
        this.renderRecentApplications();
        this.updateDailyProgress();
        this.closeModal();
        this.showSuccessMessage(`Application added for ${formData.company}!`);

        // Reset form
        document.getElementById('add-app-form').reset();
    }

    updateApplicationStatus(id, newStatus) {
        const app = this.applications.find(a => a.id === id);
        if (app) {
            app.status = newStatus;
            this.saveApplications();
            this.updateStats();
            this.renderApplications();
            this.showSuccessMessage('Application status updated!');
        }
    }

    deleteApplication(id) {
        if (confirm('Are you sure you want to delete this application?')) {
            this.applications = this.applications.filter(a => a.id !== id);
            this.saveApplications();
            this.updateStats();
            this.renderApplications();
            this.renderRecentApplications();
            this.showSuccessMessage('Application deleted!');
        }
    }

    // Resume Generation
    generateTailoredResume() {
        const company = document.getElementById('resume-company').value;
        const position = document.getElementById('resume-position').value;
        const description = document.getElementById('resume-description').value;

        if (!company || !position) {
            this.showErrorMessage('Please enter both company name and position title');
            return;
        }

        // Create job description data
        const jobData = {
            title: position,
            company: company,
            description: description,
            company_goal: "leverage data and ML to drive business impact",
            requirements: this.extractRequirements(description),
            focus_areas: this.getFocusAreas(position)
        };

        // Show processing message
        this.showSuccessMessage(`Generating tailored resume for ${company} - ${position}...`);

        // In a real implementation, this would call the Python backend
        setTimeout(() => {
            this.simulateResumeGeneration(jobData);
        }, 2000);
    }

    simulateResumeGeneration(jobData) {
        // Simulate resume generation process
        const resumeData = {
            filename: `${jobData.company}_${new Date().getFullYear()}_${Math.random().toString(36).substr(2, 9)}.pdf`,
            generatedAt: new Date().toISOString(),
            tailoredFor: `${jobData.company} - ${jobData.title}`
        };

        this.showSuccessMessage(`Resume generated: ${resumeData.filename}`);
        
        // Add to applications if not already exists
        const existingApp = this.applications.find(app => 
            app.company.toLowerCase() === jobData.company.toLowerCase() && 
            app.position.toLowerCase() === jobData.title.toLowerCase()
        );

        if (!existingApp) {
            const shouldAdd = confirm('Would you like to add this to your applications list?');
            if (shouldAdd) {
                this.applications.push({
                    id: Date.now(),
                    company: jobData.company,
                    position: jobData.title,
                    location: '',
                    url: '',
                    salary: '',
                    notes: `Resume generated: ${resumeData.filename}`,
                    dateApplied: new Date().toISOString().split('T')[0],
                    status: 'applied',
                    followUpDate: this.calculateFollowUpDate(),
                    resumeFile: resumeData.filename
                });
                this.saveApplications();
                this.updateStats();
                this.updateDailyProgress();
            }
        }
    }

    extractRequirements(description) {
        // Extract common data engineering/ML requirements from job description
        const commonRequirements = [
            'Python', 'SQL', 'Machine Learning', 'Data Engineering', 'ETL',
            'AWS', 'GCP', 'Azure', 'Spark', 'Pandas', 'NumPy', 'TensorFlow',
            'PyTorch', 'Docker', 'Kubernetes', 'Airflow', 'Kafka', 'NoSQL'
        ];
        
        const found = [];
        const descLower = description.toLowerCase();
        
        commonRequirements.forEach(req => {
            if (descLower.includes(req.toLowerCase())) {
                found.push(req);
            }
        });
        
        return found.length > 0 ? found : ['Python programming', 'Data analysis', 'Machine Learning'];
    }

    getFocusAreas(position) {
        const positionLower = position.toLowerCase();
        
        if (positionLower.includes('data engineer')) {
            return ['Data Pipeline Architecture', 'ETL Processing', 'Data Infrastructure'];
        } else if (positionLower.includes('machine learning') || positionLower.includes('ml engineer')) {
            return ['ML Model Development', 'Model Deployment', 'Deep Learning'];
        } else if (positionLower.includes('data scientist')) {
            return ['Statistical Analysis', 'Data Visualization', 'Predictive Modeling'];
        }
        
        return ['Data Analysis', 'Statistical Modeling', 'Business Intelligence'];
    }

    // UI Rendering
    renderApplications() {
        const container = document.getElementById('applications-list');
        const filteredApps = this.getFilteredApplications();
        
        if (filteredApps.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No applications found</h3>
                    <p>Start by adding your first job application!</p>
                    <button class="btn primary" onclick="showAddApplicationForm()">Add Application</button>
                </div>
            `;
            return;
        }

        container.innerHTML = filteredApps.map(app => `
            <div class="application-card">
                <div class="app-header">
                    <div class="app-info">
                        <h3>${app.company}</h3>
                        <p>${app.position}</p>
                        <p class="app-location">${app.location || 'Location not specified'}</p>
                        <p class="app-date">Applied: ${this.formatDate(app.dateApplied)}</p>
                        ${app.salary ? `<p class="app-salary">💰 ${app.salary}</p>` : ''}
                    </div>
                    <div class="app-actions">
                        <span class="app-status status-${app.status}">${app.status}</span>
                        <div class="app-controls">
                            <select onchange="tracker.updateApplicationStatus(${app.id}, this.value)" value="${app.status}">
                                <option value="applied" ${app.status === 'applied' ? 'selected' : ''}>Applied</option>
                                <option value="interview" ${app.status === 'interview' ? 'selected' : ''}>Interview</option>
                                <option value="rejected" ${app.status === 'rejected' ? 'selected' : ''}>Rejected</option>
                                <option value="offer" ${app.status === 'offer' ? 'selected' : ''}>Offer</option>
                            </select>
                            <button class="btn-icon" onclick="tracker.deleteApplication(${app.id})" title="Delete">🗑️</button>
                        </div>
                    </div>
                </div>
                ${app.notes ? `<div class="app-notes"><strong>Notes:</strong> ${app.notes}</div>` : ''}
                ${app.url ? `<div class="app-url"><a href="${app.url}" target="_blank">View Job Posting</a></div>` : ''}
                <div class="app-followup">
                    <small>Follow-up: ${this.formatDate(app.followUpDate)}</small>
                </div>
            </div>
        `).join('');
    }

    renderRecentApplications() {
        const container = document.getElementById('recent-apps-list');
        const recentApps = this.applications
            .sort((a, b) => new Date(b.dateApplied) - new Date(a.dateApplied))
            .slice(0, 5);

        if (recentApps.length === 0) {
            container.innerHTML = '<p>No applications yet. Time to start applying! 🚀</p>';
            return;
        }

        container.innerHTML = recentApps.map(app => `
            <div class="recent-app-item">
                <div class="recent-app-info">
                    <h4>${app.company}</h4>
                    <p>${app.position} • ${this.formatDate(app.dateApplied)}</p>
                </div>
                <span class="app-status status-${app.status}">${app.status}</span>
            </div>
        `).join('');
    }

    renderAnalytics() {
        this.renderApplicationsChart();
        this.renderIndustryChart();
        this.generateInsights();
    }

    renderApplicationsChart() {
        // Placeholder for Chart.js implementation
        const canvas = document.getElementById('applications-chart');
        const ctx = canvas.getContext('2d');
        
        // Simple bar chart simulation
        ctx.fillStyle = '#6366f1';
        ctx.fillRect(50, 50, 50, 100);
        ctx.fillRect(120, 75, 50, 75);
        ctx.fillRect(190, 25, 50, 125);
        
        ctx.fillStyle = '#f8fafc';
        ctx.font = '12px Inter';
        ctx.fillText('Week 1', 60, 170);
        ctx.fillText('Week 2', 130, 170);
        ctx.fillText('Week 3', 200, 170);
    }

    renderIndustryChart() {
        // Placeholder for industry success rate chart
        const canvas = document.getElementById('industry-chart');
        const ctx = canvas.getContext('2d');
        
        // Simple pie chart simulation
        ctx.beginPath();
        ctx.arc(150, 100, 50, 0, Math.PI);
        ctx.fillStyle = '#10b981';
        ctx.fill();
        
        ctx.beginPath();
        ctx.arc(150, 100, 50, Math.PI, 2 * Math.PI);
        ctx.fillStyle = '#ef4444';
        ctx.fill();
    }

    generateInsights() {
        const container = document.getElementById('insights-list');
        const insights = [];

        // Calculate metrics
        const totalApps = this.applications.length;
        const interviews = this.applications.filter(app => app.status === 'interview').length;
        const offers = this.applications.filter(app => app.status === 'offer').length;
        const responseRate = totalApps > 0 ? ((interviews + offers) / totalApps * 100).toFixed(1) : 0;

        // Generate insights
        if (totalApps > 0) {
            insights.push(`📊 You've applied to ${totalApps} positions with a ${responseRate}% response rate`);
        }

        if (interviews > 0) {
            insights.push(`🎯 ${interviews} applications led to interviews - great job!`);
        }

        if (totalApps >= 7) {
            insights.push(`🔥 You're on track with your daily goal! Keep up the momentum.`);
        } else {
            insights.push(`💪 Aim for 1 application per day to reach your goals faster.`);
        }

        // Industry insights
        const companies = [...new Set(this.applications.map(app => app.company))];
        if (companies.length > 5) {
            insights.push(`🌟 You're diversifying well across ${companies.length} different companies.`);
        }

        container.innerHTML = insights.map(insight => `
            <div class="insight-item">
                <p>${insight}</p>
            </div>
        `).join('') || '<p>Apply to more positions to see AI-powered insights!</p>';
    }

    // Utility Functions
    getFilteredApplications() {
        const search = document.getElementById('search-apps').value.toLowerCase();
        const statusFilter = document.getElementById('status-filter').value;

        return this.applications.filter(app => {
            const matchesSearch = app.company.toLowerCase().includes(search) || 
                                app.position.toLowerCase().includes(search);
            const matchesStatus = !statusFilter || app.status === statusFilter;
            return matchesSearch && matchesStatus;
        });
    }

    updateStats() {
        const today = new Date().toISOString().split('T')[0];
        const todayApps = this.applications.filter(app => app.dateApplied === today).length;
        const interviews = this.applications.filter(app => app.status === 'interview').length;
        const totalApps = this.applications.length;
        const responses = this.applications.filter(app => ['interview', 'offer'].includes(app.status)).length;
        const responseRate = totalApps > 0 ? Math.round((responses / totalApps) * 100) : 0;

        document.getElementById('total-applications').textContent = totalApps;
        document.getElementById('today-applications').textContent = todayApps;
        document.getElementById('interviews').textContent = interviews;
        document.getElementById('response-rate').textContent = `${responseRate}%`;
    }

    updateDailyProgress() {
        const today = new Date().toISOString().split('T')[0];
        const todayApps = this.applications.filter(app => app.dateApplied === today).length;
        const progress = Math.min((todayApps / this.dailyGoal) * 100, 100);
        
        document.getElementById('daily-progress').style.width = `${progress}%`;
        document.getElementById('goal-text').textContent = 
            `Goal: ${todayApps}/${this.dailyGoal} applications today ${progress >= 100 ? '🎉' : ''}`;
    }

    openJobSites() {
        const jobSites = [
            'https://www.linkedin.com/jobs/search/?keywords=data%20engineer%20machine%20learning&location=Boston%2C%20Massachusetts&f_TPR=r86400',
            'https://www.indeed.com/jobs?q=data+engineer+machine+learning&l=Boston%2C+MA&fromage=1',
            'https://builtin.com/jobs/data-science-analytics/boston'
        ];

        jobSites.forEach((url, index) => {
            setTimeout(() => window.open(url, '_blank'), index * 1000);
        });

        this.showSuccessMessage('Opening job sites... 🚀');
    }

    selectTemplate(templateName) {
        document.querySelectorAll('.template-card').forEach(card => {
            card.classList.remove('selected');
        });
        document.querySelector(`[data-template="${templateName}"]`).classList.add('selected');
        this.selectedTemplate = templateName;
    }

    showAddApplicationForm() {
        document.getElementById('add-app-modal').style.display = 'block';
    }

    closeModal() {
        document.getElementById('add-app-modal').style.display = 'none';
    }

    calculateFollowUpDate() {
        const date = new Date();
        date.setDate(date.getDate() + 7);
        return date.toISOString().split('T')[0];
    }

    formatDate(dateString) {
        return new Date(dateString).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });
    }

    showSuccessMessage(message) {
        this.showMessage(message, 'success');
    }

    showErrorMessage(message) {
        this.showMessage(message, 'error');
    }

    showMessage(message, type) {
        // Create message element
        const messageEl = document.createElement('div');
        messageEl.className = `message ${type}`;
        messageEl.textContent = message;

        // Add to page
        document.body.insertBefore(messageEl, document.body.firstChild);

        // Remove after 3 seconds
        setTimeout(() => {
            messageEl.remove();
        }, 3000);
    }

    // Data Persistence
    loadApplications() {
        const data = localStorage.getItem('jobApplications');
        return data ? JSON.parse(data) : this.getSampleApplications();
    }

    saveApplications() {
        localStorage.setItem('jobApplications', JSON.stringify(this.applications));
    }

    getSampleApplications() {
        return [
            {
                id: 1,
                company: 'Netflix',
                position: 'Machine Learning Intern',
                location: 'Los Gatos, CA',
                url: 'https://jobs.netflix.com/jobs/ml-intern',
                salary: '$8,000/month',
                notes: 'Referred by John Smith',
                dateApplied: '2025-06-20',
                status: 'applied',
                followUpDate: '2025-06-27'
            },
            {
                id: 2,
                company: 'Meta',
                position: 'Data Engineer Intern',
                location: 'Menlo Park, CA',
                url: 'https://careers.facebook.com/jobs/data-engineer',
                salary: '$9,000/month',
                notes: 'Applied through university career fair',
                dateApplied: '2025-06-19',
                status: 'interview',
                followUpDate: '2025-06-26'
            }
        ];
    }

    // Export functionality
    exportToCSV() {
        const headers = ['Company', 'Position', 'Location', 'Date Applied', 'Status', 'Notes'];
        const csvData = [headers];
        
        this.applications.forEach(app => {
            csvData.push([
                app.company,
                app.position,
                app.location,
                app.dateApplied,
                app.status,
                app.notes
            ]);
        });

        const csvString = csvData.map(row => row.join(',')).join('\n');
        const blob = new Blob([csvString], { type: 'text/csv' });
        const url = URL.createObjectURL(blob);
        
        const a = document.createElement('a');
        a.href = url;
        a.download = `job_applications_${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        
        URL.revokeObjectURL(url);
        this.showSuccessMessage('Applications exported to CSV!');
    }
}

// Initialize the application when the page loads
let tracker;
document.addEventListener('DOMContentLoaded', () => {
    tracker = new JobApplicationTracker();
    
    // Add export button to applications tab
    const applicationsHeader = document.querySelector('#applications .section-header');
    const exportBtn = document.createElement('button');
    exportBtn.className = 'btn secondary';
    exportBtn.textContent = '📊 Export CSV';
    exportBtn.onclick = () => tracker.exportToCSV();
    applicationsHeader.appendChild(exportBtn);
});

// Handle modal clicks
document.addEventListener('click', (e) => {
    if (e.target.classList.contains('modal')) {
        tracker.closeModal();
    }
});