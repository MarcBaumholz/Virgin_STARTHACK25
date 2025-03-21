// Utility Functions
const debounce = (func, wait) => {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Form Validation
const validateForm = (formId) => {
    const form = document.getElementById(formId);
    if (!form) return false;

    let isValid = true;
    const requiredFields = form.querySelectorAll('[required]');

    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });

    return isValid;
};

// Password Strength Checker
const checkPasswordStrength = (password) => {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/) && password.match(/[A-Z]/)) strength++;
    if (password.match(/\d/)) strength++;
    if (password.match(/[^a-zA-Z\d]/)) strength++;
    return strength;
};

// Real-time Password Strength Indicator
const updatePasswordStrength = (passwordInput, strengthIndicator) => {
    const strength = checkPasswordStrength(passwordInput.value);
    const strengthText = ['Very Weak', 'Weak', 'Medium', 'Strong'];
    const strengthColors = ['danger', 'warning', 'info', 'success'];
    
    if (strengthIndicator) {
        strengthIndicator.textContent = strengthText[strength - 1];
        strengthIndicator.className = `badge bg-${strengthColors[strength - 1]}`;
    }
};

// Dynamic Form Updates
const updateFormFields = (triggerElement, targetElement, options) => {
    const trigger = document.getElementById(triggerElement);
    const target = document.getElementById(targetElement);
    
    if (!trigger || !target) return;

    trigger.addEventListener('change', () => {
        const selectedValue = trigger.value;
        const option = options.find(opt => opt.value === selectedValue);
        
        if (option) {
            target.innerHTML = option.html;
        }
    });
};

// Flash Message Handler
const showFlashMessage = (message, type = 'success') => {
    const flashContainer = document.createElement('div');
    flashContainer.className = `alert alert-${type} alert-dismissible fade show`;
    flashContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(flashContainer, container.firstChild);
    
    setTimeout(() => {
        flashContainer.remove();
    }, 5000);
};

// Project Progress Updates
const updateProjectProgress = (projectId, progress) => {
    const progressBar = document.querySelector(`#project-${projectId} .progress-bar`);
    if (progressBar) {
        progressBar.style.width = `${progress}%`;
        progressBar.textContent = `${progress}%`;
    }
};

// Idea Voting System
const handleIdeaVote = async (ideaId, voteType) => {
    try {
        const response = await fetch(`/api/ideas/${ideaId}/vote`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ vote_type: voteType }),
        });
        
        if (response.ok) {
            const data = await response.json();
            updateVoteCount(ideaId, data.votes);
        } else {
            showFlashMessage('Failed to vote. Please try again.', 'danger');
        }
    } catch (error) {
        console.error('Error voting:', error);
        showFlashMessage('An error occurred. Please try again.', 'danger');
    }
};

// Update Vote Count Display
const updateVoteCount = (ideaId, votes) => {
    const voteCount = document.querySelector(`#idea-${ideaId} .vote-count`);
    if (voteCount) {
        voteCount.textContent = votes;
    }
};

// Chat System
class ChatSystem {
    constructor(roomId) {
        this.roomId = roomId;
        this.socket = null;
        this.messageContainer = document.querySelector('.chat-messages');
        this.messageForm = document.querySelector('.message-form');
        this.messageInput = document.querySelector('.message-input');
        
        this.initialize();
    }
    
    initialize() {
        this.connectWebSocket();
        this.setupEventListeners();
    }
    
    connectWebSocket() {
        this.socket = new WebSocket(`ws://${window.location.host}/ws/chat/${this.roomId}`);
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.displayMessage(data);
        };
        
        this.socket.onclose = () => {
            setTimeout(() => this.connectWebSocket(), 1000);
        };
    }
    
    setupEventListeners() {
        if (this.messageForm) {
            this.messageForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage();
            });
        }
    }
    
    sendMessage() {
        if (!this.messageInput || !this.messageInput.value.trim()) return;
        
        const message = {
            content: this.messageInput.value.trim(),
            room_id: this.roomId
        };
        
        this.socket.send(JSON.stringify(message));
        this.messageInput.value = '';
    }
    
    displayMessage(data) {
        if (!this.messageContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = `message ${data.user_id === currentUserId ? 'sent' : 'received'}`;
        messageElement.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="username">${data.username}</span>
                    <span class="timestamp">${new Date(data.timestamp).toLocaleTimeString()}</span>
                </div>
                <div class="message-text">${data.content}</div>
            </div>
        `;
        
        this.messageContainer.appendChild(messageElement);
        this.messageContainer.scrollTop = this.messageContainer.scrollHeight;
    }
}

// Initialize Chat System
document.addEventListener('DOMContentLoaded', () => {
    const roomId = document.querySelector('[data-room-id]')?.dataset.roomId;
    if (roomId) {
        new ChatSystem(roomId);
    }
});

// Green Points System
class GreenPointsSystem {
    constructor() {
        this.pointsDisplay = document.querySelector('.points-display');
        this.levelDisplay = document.querySelector('.level-display');
        this.progressBar = document.querySelector('.points-progress');
        
        this.initialize();
    }
    
    initialize() {
        this.updatePoints();
        this.setupEventListeners();
    }
    
    async updatePoints() {
        try {
            const response = await fetch('/api/user/points');
            if (response.ok) {
                const data = await response.json();
                this.updateDisplay(data);
            }
        } catch (error) {
            console.error('Error updating points:', error);
        }
    }
    
    updateDisplay(data) {
        if (this.pointsDisplay) {
            this.pointsDisplay.textContent = data.points;
        }
        
        if (this.levelDisplay) {
            this.levelDisplay.textContent = `Level ${data.level}`;
        }
        
        if (this.progressBar) {
            const progress = (data.points / data.next_level_points) * 100;
            this.progressBar.style.width = `${progress}%`;
            this.progressBar.textContent = `${Math.round(progress)}%`;
        }
    }
    
    setupEventListeners() {
        // Listen for points updates from server
        const eventSource = new EventSource('/api/user/points/stream');
        
        eventSource.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.updateDisplay(data);
        };
        
        eventSource.onerror = () => {
            eventSource.close();
        };
    }
}

// Initialize Green Points System
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.points-display')) {
        new GreenPointsSystem();
    }
});

// Project Filtering System
class ProjectFilteringSystem {
    constructor() {
        this.filterForm = document.querySelector('.project-filters');
        this.projectGrid = document.querySelector('.project-grid');
        
        this.initialize();
    }
    
    initialize() {
        if (this.filterForm) {
            this.setupEventListeners();
        }
    }
    
    setupEventListeners() {
        const inputs = this.filterForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('change', debounce(() => this.applyFilters(), 300));
        });
    }
    
    async applyFilters() {
        const formData = new FormData(this.filterForm);
        const params = new URLSearchParams(formData);
        
        try {
            const response = await fetch(`/api/projects?${params}`);
            if (response.ok) {
                const projects = await response.json();
                this.updateProjectGrid(projects);
            }
        } catch (error) {
            console.error('Error applying filters:', error);
        }
    }
    
    updateProjectGrid(projects) {
        if (!this.projectGrid) return;
        
        this.projectGrid.innerHTML = projects.map(project => `
            <div class="project-card" id="project-${project.id}">
                <h5>${project.title}</h5>
                <p class="text-muted">${project.company}</p>
                <div class="progress mb-2">
                    <div class="progress-bar" role="progressbar" style="width: ${project.progress}%">
                        ${project.progress}%
                    </div>
                </div>
                <p>${project.description}</p>
                <div class="d-flex justify-content-between align-items-center">
                    <span class="badge bg-${project.status_color}">${project.status}</span>
                    <small class="text-muted">${new Date(project.last_updated).toLocaleDateString()}</small>
                </div>
            </div>
        `).join('');
    }
}

// Initialize Project Filtering System
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.project-filters')) {
        new ProjectFilteringSystem();
    }
});

// Export functions for use in other modules
export {
    debounce,
    validateForm,
    checkPasswordStrength,
    updatePasswordStrength,
    updateFormFields,
    showFlashMessage,
    updateProjectProgress,
    handleIdeaVote,
    updateVoteCount,
    ChatSystem,
    GreenPointsSystem,
    ProjectFilteringSystem
}; 