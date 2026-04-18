let currentMessageId = null;

async function loadNextMessage() {
    try {
        const response = await apiCall('/api/messages/next');
        
        if (!response.ok) {
            if (response.status === 404) {
                showNoMessages();
            } else {
                showError(t('load_mail_error'));
            }
            return;
        }
        
        const message = await response.json();
        currentMessageId = message.id;
        
        displayMessage(message);
    } catch (error) {
        showError('Fehler: ' + error.message);
    }
}

function displayMessage(message) {
    const container = document.getElementById('messageContainer');
    
    const body = message.raw_message || t('no_body');
    const headerOnly = body.split('\n\n')[0];
    
    container.innerHTML = `
        <div class="message-header">
            <div class="message-info">
                <div class="info-label">${t('from')}</div>
                <div class="info-value">${escapeHtml(message.sender || t('unknown'))}</div>
            </div>
            
            <div class="message-info">
                <div class="info-label">${t('to')}</div>
                <div class="info-value">${escapeHtml(message.recipient || '-')}</div>
            </div>
            
            <div class="subject-title">${escapeHtml(message.subject || t('no_subject'))}</div>
            
            <div class="message-info">
                <div class="info-label">${t('date')}</div>
                <div class="info-value">${message.received_date ? formatDateLocalized(message.received_date) : t('unknown')}</div>
            </div>
        </div>
        
        <div class="message-body">
${escapeHtml(body.substring(0, 2000))}${body.length > 2000 ? `\n\n${t('shortened')}` : ''}
        </div>
        
        <div class="message-actions">
            <button class="btn btn-success btn-large" onclick="classifyMessage('ham')" title="H">
                ✓ ${t('not_spam')} (H)
            </button>
            <button class="btn btn-danger btn-large" onclick="classifyMessage('spam')" title="S">
                ✗ ${t('spam')} (S)
            </button>
            <button class="btn btn-secondary btn-large" onclick="skipMessage()" title="U">
                ⊘ ${t('skip')} (U)
            </button>
        </div>
    `;
}

function showNoMessages() {
    document.getElementById('messageContainer').style.display = 'none';
    document.getElementById('noMessagesDiv').style.display = 'block';
}

async function classifyMessage(decision) {
    try {
        const response = await apiCall(`/api/messages/${currentMessageId}/classify`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ decision })
        });
        
        if (response.ok) {
            loadNextMessage();
        } else {
            showError(t('save_error'));
        }
    } catch (error) {
        showError(t('error_prefix') + error.message);
    }
}

async function skipMessage() {
    try {
        const response = await apiCall(`/api/messages/${currentMessageId}/skip`, {
            method: 'POST'
        });
        
        if (response.ok) {
            loadNextMessage();
        } else {
            showError(t('skip_error'));
        }
    } catch (error) {
        showError(t('error_prefix') + error.message);
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function showError(message) {
    alert(message);
}

document.addEventListener('keydown', (e) => {
    if (!currentMessageId) return;
    
    if (e.key.toUpperCase() === 'S') {
        classifyMessage('spam');
    } else if (e.key.toUpperCase() === 'H') {
        classifyMessage('ham');
    } else if (e.key.toUpperCase() === 'U') {
        skipMessage();
    }
});

document.getElementById('username').textContent = localStorage.getItem('username');
loadNextMessage();
