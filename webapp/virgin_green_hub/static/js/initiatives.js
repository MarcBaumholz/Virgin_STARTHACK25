// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Initiatives List Page
class InitiativesList {
    constructor() {
        this.filterForm = document.getElementById('filterForm');
        this.initiativesGrid = document.querySelector('.row');
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add event listeners to form inputs
        this.filterForm.querySelectorAll('select, input').forEach(input => {
            input.addEventListener('change', () => this.updateInitiatives());
        });

        // Debounce search input
        const searchInput = this.filterForm.querySelector('input[name="search"]');
        searchInput.addEventListener('input', debounce(() => this.updateInitiatives(), 300));
    }

    async updateInitiatives() {
        const formData = new FormData(this.filterForm);
        const params = new URLSearchParams(formData);
        
        try {
            const response = await fetch(`/api/initiatives?${params}`);
            const initiatives = await response.json();
            this.renderInitiatives(initiatives);
        } catch (error) {
            console.error('Error fetching initiatives:', error);
            this.showError('Failed to load initiatives. Please try again.');
        }
    }

    renderInitiatives(initiatives) {
        if (initiatives.length === 0) {
            this.initiativesGrid.innerHTML = `
                <div class="col-12">
                    <div class="empty-state">
                        <i class="fas fa-search"></i>
                        <h3>No initiatives found</h3>
                        <p>Try adjusting your filters or search terms.</p>
                    </div>
                </div>
            `;
            return;
        }

        this.initiativesGrid.innerHTML = initiatives.map(initiative => `
            <div class="col">
                <div class="card h-100">
                    <div class="card-body">
                        <h5 class="card-title">${initiative.title}</h5>
                        <p class="card-text">${initiative.description}</p>
                        <div class="mb-3">
                            <span class="badge bg-primary">${initiative.category}</span>
                            <span class="badge bg-${initiative.status === 'active' ? 'success' : 'secondary'}">
                                ${initiative.status}
                            </span>
                        </div>
                        <div class="progress mb-3">
                            <div class="progress-bar" role="progressbar" 
                                 style="width: ${initiative.current_progress}%"
                                 aria-valuenow="${initiative.current_progress}" 
                                 aria-valuemin="0" 
                                 aria-valuemax="100">
                                ${initiative.current_progress}%
                            </div>
                        </div>
                        <a href="/initiatives/${initiative.id}" class="btn btn-primary">View Details</a>
                    </div>
                </div>
            </div>
        `).join('');
    }

    showError(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        this.initiativesGrid.insertAdjacentElement('beforebegin', alert);
    }
}

// Initiative Details Page
class InitiativeDetails {
    constructor() {
        this.initiativeId = window.location.pathname.split('/').pop();
        this.setupEventListeners();
    }

    setupEventListeners() {
        // Add event listeners for any interactive elements
        document.querySelectorAll('.progress-bar').forEach(bar => {
            const width = bar.style.width;
            bar.style.width = '0';
            setTimeout(() => {
                bar.style.width = width;
            }, 100);
        });
    }
}

// Initialize based on current page
document.addEventListener('DOMContentLoaded', () => {
    if (document.querySelector('.initiatives-list')) {
        new InitiativesList();
    } else if (document.querySelector('.initiative-details')) {
        new InitiativeDetails();
    }
}); 