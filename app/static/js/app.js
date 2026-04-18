function logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('userId');
    localStorage.removeItem('username');
    window.location.href = '/login';
}

const publicPaths = ['/', '/login'];
const firstLoginPath = '/first-login';

function apiCall(url, options = {}) {
    const token = localStorage.getItem('token');
    const headers = options.headers || {};
    
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    
    return fetch(url, { ...options, headers });
}

async function enforceAuthState() {
    const token = localStorage.getItem('token');
    const path = window.location.pathname;

    if (!token) {
        if (!publicPaths.includes(path)) {
            window.location.href = '/login';
        }
        return;
    }

    try {
        const response = await apiCall('/api/auth/me');
        if (!response.ok) {
            logout();
            return;
        }

        const user = await response.json();
        localStorage.setItem('username', user.username);

        if (user.must_change_credentials) {
            if (path !== firstLoginPath) {
                window.location.href = firstLoginPath;
            }
            return;
        }

        if (path === '/login' || path === '/' || path === firstLoginPath) {
            window.location.href = '/dashboard';
        }
    } catch (error) {
        logout();
    }
}

function addDevelopedByButton() {
    if (document.getElementById('developedByButton')) {
        return;
    }

    const button = document.createElement('a');
    button.id = 'developedByButton';
    button.className = 'dev-by-button';
    button.href = 'https://work-less.it/';
    button.target = '_blank';
    button.rel = 'noopener noreferrer';
    button.title = 'Developed with love by work-less.it';
    button.textContent = 'Developed with love by work-less.it';

    document.body.appendChild(button);
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!localStorage.getItem('app_language')) {
            localStorage.setItem('app_language', 'en');
        }
        if (typeof applyTranslations === 'function') {
            applyTranslations();
        }
        addDevelopedByButton();
        enforceAuthState();
    });
} else {
    if (!localStorage.getItem('app_language')) {
        localStorage.setItem('app_language', 'en');
    }
    if (typeof applyTranslations === 'function') {
        applyTranslations();
    }
    addDevelopedByButton();
    enforceAuthState();
}
