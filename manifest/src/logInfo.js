// console.log('[DUO-EXT] logInfo.js loaded');

// Extract and save learn page information
function extractLearnPageInfo() {
    // Prefer shared language detection, fall back to URL/guidebook data
    let languageCode = getCurrentLanguage();

    // Fallback 1: Try to extract from pathname (e.g., /learn/pt)
    if (!languageCode) {
        const pathMatch = window.location.pathname.match(/\/learn\/([a-z]{2,3})/);
        if (pathMatch) {
            languageCode = pathMatch[1];
        }
    }

    // Fallback 2: Try to get from guidebook buttons
    if (!languageCode) {
        const guidebookButtons = document.querySelectorAll('[data-test*="guidebook"]');

        if (guidebookButtons.length > 0) {
            const href = guidebookButtons[0].getAttribute('href') || '';
            const langMatch = href.match(/\/guidebook\/([^/]+)\//);
            if (langMatch) {
                languageCode = langMatch[1];
            }
        }
    }
    
    if (!languageCode) {
        console.error('[DUO-EXT] Could not detect language code');
        return;
    }
    
    const sessionInfo = {
        language: languageCode,
        timestamp: new Date().toISOString()
    };
    
    // Send to backend to save in config/session.json
    fetch('http://localhost:5000/save-session', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(sessionInfo)
    })
    .catch(err => console.error('[DUO-EXT] Error saving session:', err));

    console.log('[DUO-EXT] Session info: ', sessionInfo);
}

// Initialize learn page detection
function initLearnPageDetection() {
    // Extract info after DOM is ready (give page time to load)
    setTimeout(() => {
        extractLearnPageInfo();
    }, 3500);
}

