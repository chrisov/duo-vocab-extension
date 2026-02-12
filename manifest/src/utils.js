// Utility functions for exercise detection
// console.log('[DUO-EXT] utils.js loaded');

// Configure your backend endpoint here
const BACKEND_URL = 'http://localhost:5000/save-vocab';

/**
 * Get the current challenge type from the DOM
 * @returns {string|null} Challenge type (e.g., 'gapFill', 'listenTap', 'tapComplete') or null if not found
 */
function getChallengeType() {
    const challengeElement = document.querySelector('[data-test*="challenge "]');
    if (!challengeElement) {
        return null;
    }
    
    const dataTest = challengeElement.getAttribute('data-test');
    // Extract the challenge type from "challenge challenge-gapFill"
    const match = dataTest.match(/challenge challenge-(\w+)/);
    return match ? match[1] : null;
}
/**
 * Detect the current language being learned
 * @returns {string|null} Language code (e.g., 'pt', 'es', 'fr') or null if not found
 */
function getCurrentLanguage() {
    let languageCode = null;
    
    // Method 1: Try to find from elements with lang attribute
    const langElements = document.querySelectorAll('[lang]');
    if (langElements.length > 0) {
        // Get the most common language code (excluding 'en')
        const langCounts = {};
        langElements.forEach(el => {
            const lang = el.getAttribute('lang');
            if (lang && lang !== 'en') {
                langCounts[lang] = (langCounts[lang] || 0) + 1;
            }
        });
        
        // Find the most frequent language
        let maxCount = 0;
        for (const [lang, count] of Object.entries(langCounts)) {
            if (count > maxCount) {
                maxCount = count;
                languageCode = lang;
            }
        }
    }
    
    // Method 2: Try to extract from page title
    if (!languageCode) {
        const titleText = document.title || '';
        const titleMatch = titleText.match(/Learn (\w+)/i);
        if (titleMatch) {
            const langName = titleMatch[1];
            const langMap = {
                'Spanish': 'es',
                'Portuguese': 'pt',
                'French': 'fr',
                'German': 'de',
                'Italian': 'it',
                'Japanese': 'ja',
                'Korean': 'ko',
                'Chinese': 'zh'
            };
            languageCode = langMap[langName] || langName.toLowerCase().substring(0, 2);
        }
    }
    
    return languageCode;
}


function sendVocabularyToBackend(vocabularyList) {
    console.log(`[DUO-EXT] Sending ${vocabularyList.length} word(s) to backend...`);
    
    fetch(BACKEND_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            vocabulary: vocabularyList,
            timestamp: new Date().toISOString(),
            language: getCurrentLanguage()
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('[DUO-EXT] Vocabulary sent successfully:', data);
    })
    .catch(error => {
        console.error('[DUO-EXT] Error sending vocabulary to backend:', error);
    });
}

// Clear vocabulary for next lesson
function resetVocabulary(words) {
    words.clear();
    console.log('[DUO-EXT] Vocabulary collection reset');
}
