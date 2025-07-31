
// SmartStudy JavaScript functionality

// Global variables
let currentUser = localStorage.getItem('smartstudy_user') || 'Student';
let activityHistory = JSON.parse(localStorage.getItem('smartstudy_activity') || '[]');
let currentTheme = localStorage.getItem('smartstudy_theme') || 'dark';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Load theme
    loadTheme();
    
    // Initialize theme toggle
    initializeThemeToggle();
    
    // Load user preferences
    loadUserPreferences();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Auto-save functionality
    setupAutoSave();
    
    // Keyboard shortcuts
    setupKeyboardShortcuts();
    
    // Initialize search if available
    setupSearch();
}

// Theme management
function loadTheme() {
    const theme = localStorage.getItem('smartstudy_theme') || 'dark';
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.className = theme === 'dark' ? 'dark' : '';
    currentTheme = theme;
    updateThemeToggleIcon();
}

function toggleTheme() {
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    currentTheme = newTheme;
    
    document.documentElement.setAttribute('data-theme', newTheme);
    document.documentElement.className = newTheme === 'dark' ? 'dark' : '';
    
    localStorage.setItem('smartstudy_theme', newTheme);
    updateThemeToggleIcon();
    
    // Add a smooth transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    setTimeout(() => {
        document.body.style.transition = '';
    }, 300);
    
    logActivity('theme_change', `Switched to ${newTheme} mode`);
}

function updateThemeToggleIcon() {
    const toggleButton = document.getElementById('theme-toggle');
    if (toggleButton) {
        const sunIcon = toggleButton.querySelector('.fa-sun');
        const moonIcon = toggleButton.querySelector('.fa-moon');
        
        if (currentTheme === 'dark') {
            if (sunIcon) sunIcon.classList.add('hidden');
            if (moonIcon) moonIcon.classList.remove('hidden');
        } else {
            if (sunIcon) sunIcon.classList.remove('hidden');
            if (moonIcon) moonIcon.classList.add('hidden');
        }
    }
}

function initializeThemeToggle() {
    const toggleButton = document.getElementById('theme-toggle');
    if (toggleButton) {
        toggleButton.addEventListener('click', toggleTheme);
    }
}

// User preferences
function loadUserPreferences() {
    const savedUser = localStorage.getItem('smartstudy_user');
    if (savedUser) {
        currentUser = savedUser;
        updateUserDisplay();
    }
}

function updateUserDisplay() {
    const userElements = document.querySelectorAll('[data-user-name]');
    userElements.forEach(element => {
        element.textContent = currentUser;
    });
}

function saveUserPreference(key, value) {
    localStorage.setItem(`smartstudy_${key}`, value);
}

// Activity tracking
function logActivity(type, details) {
    const activity = {
        id: Date.now(),
        type: type,
        details: details,
        timestamp: new Date().toISOString(),
        user: currentUser
    };
    
    activityHistory.unshift(activity);
    
    // Keep only last 100 activities
    if (activityHistory.length > 100) {
        activityHistory = activityHistory.slice(0, 100);
    }
    
    localStorage.setItem('smartstudy_activity', JSON.stringify(activityHistory));
    updateActivityDisplay();
}

function updateActivityDisplay() {
    const activityElement = document.getElementById('recent-activity');
    if (activityElement) {
        const recentActivities = activityHistory.slice(0, 10);
        activityElement.innerHTML = recentActivities.map(activity => `
            <div class="activity-item p-3 bg-gray-100 dark:bg-slate-700 rounded-lg transition-colors">
                <div class="flex items-center justify-between">
                    <span class="text-sm text-gray-900 dark:text-white">${activity.details}</span>
                    <span class="text-xs text-gray-500 dark:text-gray-400">${formatTime(activity.timestamp)}</span>
                </div>
            </div>
        `).join('');
    }
}

// Utility functions
function formatTime(timestamp) {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 60000) {
        return 'Just now';
    } else if (diff < 3600000) {
        return `${Math.floor(diff / 60000)}m ago`;
    } else if (diff < 86400000) {
        return `${Math.floor(diff / 3600000)}h ago`;
    } else {
        return date.toLocaleDateString();
    }
}

// Text processing utilities
function highlightKeywords(text, keywords) {
    let highlightedText = text;
    keywords.forEach(keyword => {
        const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
        highlightedText = highlightedText.replace(regex, `<mark class="bg-yellow-300 dark:bg-yellow-600 text-black dark:text-white px-1 rounded">${keyword}</mark>`);
    });
    return highlightedText;
}

function extractKeywords(text, count = 5) {
    // Simple keyword extraction
    const words = text.toLowerCase().match(/\b\w{4,}\b/g) || [];
    const frequency = {};
    
    words.forEach(word => {
        if (!['that', 'this', 'with', 'have', 'will', 'from', 'they', 'been', 'said', 'each', 'which', 'their', 'time', 'would', 'there', 'could', 'other'].includes(word)) {
            frequency[word] = (frequency[word] || 0) + 1;
        }
    });
    
    return Object.entries(frequency)
        .sort((a, b) => b[1] - a[1])
        .slice(0, count)
        .map(entry => entry[0]);
}

// Auto-save functionality
function setupAutoSave() {
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        let saveTimeout;
        textarea.addEventListener('input', function() {
            clearTimeout(saveTimeout);
            saveTimeout = setTimeout(() => {
                saveFormData(this);
            }, 2000);
        });
    });
}

function saveFormData(element) {
    const formId = element.closest('form')?.id || 'default';
    const data = {
        value: element.value,
        timestamp: Date.now()
    };
    localStorage.setItem(`smartstudy_draft_${formId}`, JSON.stringify(data));
    showSaveIndicator();
}

function loadFormData(formId) {
    const saved = localStorage.getItem(`smartstudy_draft_${formId}`);
    if (saved) {
        const data = JSON.parse(saved);
        return data.value;
    }
    return '';
}

function showSaveIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'fixed top-4 right-4 bg-green-600 text-white px-3 py-1 rounded-lg text-sm z-50 transition-all';
    indicator.textContent = 'Draft saved';
    document.body.appendChild(indicator);
    
    setTimeout(() => {
        indicator.style.opacity = '0';
        setTimeout(() => indicator.remove(), 300);
    }, 2000);
}

// Keyboard shortcuts
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + S to save
        if ((e.ctrlKey || e.metaKey) && e.key === 's') {
            e.preventDefault();
            const form = document.querySelector('form');
            if (form) {
                form.dispatchEvent(new Event('submit', { bubbles: true }));
            }
        }
        
        // Ctrl/Cmd + K for search/assistant
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            const searchInput = document.querySelector('input[type="search"], input[placeholder*="search"], input[name="message"]');
            if (searchInput) {
                searchInput.focus();
            }
        }
        
        // Ctrl/Cmd + D to toggle theme
        if ((e.ctrlKey || e.metaKey) && e.key === 'd') {
            e.preventDefault();
            toggleTheme();
        }
        
        // Escape to close modals
        if (e.key === 'Escape') {
            const modal = document.querySelector('.modal.active, .fixed.flex');
            if (modal) {
                modal.classList.add('hidden');
                modal.classList.remove('flex');
            }
        }
    });
}

// Tooltip initialization
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
    });
}

function showTooltip(e) {
    const tooltip = document.createElement('div');
    tooltip.className = 'absolute bg-gray-900 dark:bg-slate-800 text-white text-xs px-2 py-1 rounded shadow-lg z-50 pointer-events-none';
    tooltip.textContent = e.target.getAttribute('data-tooltip');
    
    document.body.appendChild(tooltip);
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 5 + 'px';
    
    e.target._tooltip = tooltip;
}

function hideTooltip(e) {
    if (e.target._tooltip) {
        e.target._tooltip.remove();
        delete e.target._tooltip;
    }
}

// Progress tracking
function updateProgress(type, increment = 1) {
    const current = parseInt(localStorage.getItem(`smartstudy_${type}_count`) || '0');
    const newCount = current + increment;
    localStorage.setItem(`smartstudy_${type}_count`, newCount.toString());
    
    // Update UI if elements exist
    const element = document.querySelector(`[data-stat="${type}"]`);
    if (element) {
        element.textContent = newCount;
    }
    
    logActivity(type, `${type} count updated to ${newCount}`);
}

// Notification system
function showNotification(message, type = 'info', duration = 3000) {
    const notification = document.createElement('div');
    notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all ${getNotificationClass(type)}`;
    notification.innerHTML = `
        <div class="flex items-center space-x-2">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" class="ml-2 text-white hover:text-gray-300">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.opacity = '0';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
}

function getNotificationClass(type) {
    const classes = {
        success: 'bg-green-600 text-white',
        error: 'bg-red-600 text-white',
        warning: 'bg-yellow-600 text-black',
        info: 'bg-blue-600 text-white'
    };
    return classes[type] || classes.info;
}

function getNotificationIcon(type) {
    const icons = {
        success: 'fa-check-circle',
        error: 'fa-exclamation-circle',
        warning: 'fa-exclamation-triangle',
        info: 'fa-info-circle'
    };
    return icons[type] || icons.info;
}

// Form validation
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            showFieldError(field, 'This field is required');
            isValid = false;
        } else {
            clearFieldError(field);
        }
    });
    
    return isValid;
}

function showFieldError(field, message) {
    clearFieldError(field);
    
    const error = document.createElement('div');
    error.className = 'field-error text-red-400 text-sm mt-1';
    error.textContent = message;
    
    field.parentElement.appendChild(error);
    field.classList.add('border-red-500');
}

function clearFieldError(field) {
    const error = field.parentElement.querySelector('.field-error');
    if (error) {
        error.remove();
    }
    field.classList.remove('border-red-500');
}

// Search functionality
function setupSearch() {
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', debounce(performSearch, 300));
    }
}

function performSearch(query) {
    // Implementation depends on specific page
    console.log('Searching for:', query);
}

// Debounce utility
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

// Mobile menu toggle
function toggleMobileMenu() {
    const sidebar = document.querySelector('.fixed.w-64');
    const overlay = document.getElementById('mobile-overlay');
    
    if (sidebar) {
        sidebar.classList.toggle('translate-x-0');
        sidebar.classList.toggle('-translate-x-full');
    }
    
    if (overlay) {
        overlay.classList.toggle('hidden');
    }
}

// Export functions for global use
window.SmartStudy = {
    logActivity,
    updateProgress,
    showNotification,
    validateForm,
    extractKeywords,
    highlightKeywords,
    formatTime,
    toggleTheme,
    toggleMobileMenu
};

// Initialize theme on page load
document.addEventListener('DOMContentLoaded', loadTheme);
