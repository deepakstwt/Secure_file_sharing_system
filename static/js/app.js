// Secure File Sharing Web Application
class SecureFileApp {
    constructor() {
        this.baseURL = '';
        this.token = localStorage.getItem('authToken');
        this.userType = localStorage.getItem('userType');
        this.userName = localStorage.getItem('userName');
        
        this.initializeApp();
        this.bindEvents();
    }

    initializeApp() {
        if (this.token && this.userType) {
            this.showDashboard();
        } else {
            this.showAuth();
        }
    }

    bindEvents() {
        // Authentication events
        document.getElementById('loginBtn').addEventListener('click', () => this.showLoginForm());
        document.getElementById('signupBtn').addEventListener('click', () => this.showSignupForm());
        document.getElementById('showSignup').addEventListener('click', (e) => {
            e.preventDefault();
            this.showSignupForm();
        });
        document.getElementById('showLogin').addEventListener('click', (e) => {
            e.preventDefault();
            this.showLoginForm();
        });
        document.getElementById('logoutBtn').addEventListener('click', () => this.logout());

        // Form events
        document.getElementById('loginFormElement').addEventListener('submit', (e) => this.handleLogin(e));
        document.getElementById('signupFormElement').addEventListener('submit', (e) => this.handleSignup(e));
        document.getElementById('uploadForm').addEventListener('submit', (e) => this.handleUpload(e));

        // File events
        document.getElementById('fileInput').addEventListener('change', (e) => this.handleFileSelect(e));
        document.getElementById('refreshFiles').addEventListener('click', () => this.loadFiles());
    }

    showAuth() {
        document.getElementById('authSection').style.display = 'block';
        document.getElementById('dashboardSection').style.display = 'none';
        document.getElementById('loginBtn').style.display = 'block';
        document.getElementById('signupBtn').style.display = 'block';
        document.getElementById('userMenu').style.display = 'none';
    }

    showDashboard() {
        document.getElementById('authSection').style.display = 'none';
        document.getElementById('dashboardSection').style.display = 'block';
        document.getElementById('loginBtn').style.display = 'none';
        document.getElementById('signupBtn').style.display = 'none';
        document.getElementById('userMenu').style.display = 'flex';
        document.getElementById('userName').textContent = this.userName || 'User';

        if (this.userType === 'ops') {
            document.getElementById('opsDashboard').style.display = 'block';
            document.getElementById('clientDashboard').style.display = 'none';
        } else {
            document.getElementById('opsDashboard').style.display = 'none';
            document.getElementById('clientDashboard').style.display = 'block';
            this.loadFiles();
        }
    }

    showLoginForm() {
        document.getElementById('loginForm').style.display = 'block';
        document.getElementById('signupForm').style.display = 'none';
    }

    showSignupForm() {
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('signupForm').style.display = 'block';
    }

    // Authentication
    async handleLogin(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const email = formData.get('email');
        const password = formData.get('password');
        const userType = formData.get('userType');

        try {
            const endpoint = userType === 'ops' ? '/auth/ops/login' : '/auth/client/login';
            const response = await this.apiRequest(endpoint, 'POST', {
                email,
                password
            });

            if (response.access_token) {
                this.token = response.access_token;
                this.userType = userType;
                this.userName = email;

                localStorage.setItem('authToken', this.token);
                localStorage.setItem('userType', this.userType);
                localStorage.setItem('userName', this.userName);

                this.showNotification('Login successful!', 'success');
                this.showDashboard();
            }
        } catch (error) {
            this.showNotification(error.message || 'Login failed', 'error');
        }
    }

    async handleSignup(e) {
        e.preventDefault();
        const formData = new FormData(e.target);
        const email = formData.get('email');
        const password = formData.get('password');

        try {
            const response = await this.apiRequest('/auth/client/signup', 'POST', {
                email,
                password
            });

            this.showNotification('Signup successful! Please check your email for verification.', 'success');
            this.showLoginForm();
        } catch (error) {
            this.showNotification(error.message || 'Signup failed', 'error');
        }
    }

    logout() {
        this.token = null;
        this.userType = null;
        this.userName = null;
        
        localStorage.removeItem('authToken');
        localStorage.removeItem('userType');
        localStorage.removeItem('userName');
        
        this.showNotification('Logged out successfully', 'success');
        this.showAuth();
    }

    // File Operations
    handleFileSelect(e) {
        const file = e.target.files[0];
        const fileNameSpan = document.getElementById('fileName');
        
        if (file) {
            fileNameSpan.textContent = file.name;
            
            // Validate file type
            const allowedTypes = ['.pptx', '.docx', '.xlsx'];
            const fileExtension = '.' + file.name.split('.').pop().toLowerCase();
            
            if (!allowedTypes.includes(fileExtension)) {
                this.showNotification('Only .pptx, .docx, and .xlsx files are allowed', 'error');
                e.target.value = '';
                fileNameSpan.textContent = '';
            }
        } else {
            fileNameSpan.textContent = '';
        }
    }

    async handleUpload(e) {
        e.preventDefault();
        const fileInput = document.getElementById('fileInput');
        const file = fileInput.files[0];

        if (!file) {
            this.showNotification('Please select a file', 'error');
            return;
        }

        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await this.apiRequest('/file/upload', 'POST', formData, true);
            this.showNotification('File uploaded successfully!', 'success');
            
        
            fileInput.value = '';
            document.getElementById('fileName').textContent = '';
        } catch (error) {
            this.showNotification(error.message || 'Upload failed', 'error');
        }
    }

    async loadFiles() {
        const filesList = document.getElementById('filesList');
        filesList.innerHTML = '<div class="loading"><i class="fas fa-spinner fa-spin"></i> Loading files...</div>';

        try {
            const response = await this.apiRequest('/file/list', 'GET');
            this.displayFiles(response.files || []);
        } catch (error) {
            filesList.innerHTML = '<div class="loading">Failed to load files: ' + (error.message || 'Unknown error') + '</div>';
        }
    }

    displayFiles(files) {
        const filesList = document.getElementById('filesList');
        
        if (files.length === 0) {
            filesList.innerHTML = '<div class="loading">No files available</div>';
            return;
        }

        filesList.innerHTML = files.map(file => `
            <div class="file-item">
                <div class="file-info">
                    <div class="file-name">
                        <i class="fas fa-file-${this.getFileIcon(file.file_type)}"></i>
                        ${file.filename}
                    </div>
                    <div class="file-meta">
                        <span><i class="fas fa-tag"></i> ${file.file_type.toUpperCase()}</span>
                        <span><i class="fas fa-user"></i> ${file.uploader}</span>
                        <span><i class="fas fa-calendar"></i> ${this.formatDate(file.uploaded_at)}</span>
                    </div>
                </div>
                <div class="file-actions">
                    <button class="btn btn-primary btn-sm" onclick="app.downloadFile('${file.file_id}', '${file.filename}')">
                        <i class="fas fa-download"></i> Download
                    </button>
                </div>
            </div>
        `).join('');
    }

    async downloadFile(fileId, filename) {
        try {
            // Generate download link
            const response = await this.apiRequest(`/file/download/${fileId}`, 'GET');
            
            if (response.download_link) {
                this.showNotification('Download link generated! File will download shortly...', 'success');
                
                const link = document.createElement('a');
                link.href = response.download_link;
                link.download = filename;
                document.body.appendChild(link);
                link.click();
                document.body.removeChild(link);
            }
        } catch (error) {
            this.showNotification(error.message || 'Download failed', 'error');
        }
    }

    async apiRequest(endpoint, method = 'GET', data = null, isFormData = false) {
        const config = {
            method,
            headers: {}
        };

        if (this.token) {
            config.headers['Authorization'] = `Bearer ${this.token}`;
        }

        if (data) {
            if (isFormData) {
                config.body = data;
            } else {
                config.headers['Content-Type'] = 'application/json';
                config.body = JSON.stringify(data);
            }
        }

        const response = await fetch(this.baseURL + endpoint, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.detail || result.message || 'Request failed');
        }

        return result;
    }

    showNotification(message, type = 'info') {
        const notifications = document.getElementById('notifications');
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span>${message}</span>
                <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; font-size: 18px; cursor: pointer;">&times;</button>
            </div>
        `;

        notifications.appendChild(notification);

    
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 5000);
    }

    getFileIcon(fileType) {
        const icons = {
            'xlsx': 'excel',
            'docx': 'word',
            'pptx': 'powerpoint'
        };
        return icons[fileType] || 'alt';
    }

    formatDate(dateString) {
        if (!dateString) return 'Unknown';
        try {
            return new Date(dateString).toLocaleDateString();
        } catch {
            return 'Unknown';
        }
    }
}


const app = new SecureFileApp(); 