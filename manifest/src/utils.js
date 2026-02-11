// Utility functions for exercise detection
// console.log('[DUO-EXT] utils.js loaded');

// Detect exercise type based on data-test attributes
function detectExerciseType() {
    if (document.querySelector('[data-test="challenge-select"]'))
        return 'select-challenge';
    if (document.querySelector('[data-test="challenge-translate"]'))
        return 'translate-challenge';
    if (document.querySelector('[data-test="challenge-tap"]'))
        return 'tap-challenge';
    if (document.querySelector('[data-test="challenge-listen"]'))
        return 'listen-challenge';
    if (document.querySelector('[data-test="challenge-speak"]'))
        return 'speak-challenge';
    if (document.querySelector('[data-test="challenge-match"]'))
        return 'match-challenge';
    if (document.querySelector('[data-test="challenge-name"]'))
        return 'name-challenge';
    if (document.querySelector('[data-test="challenge-definition"]'))
        return 'definition-challenge';
    if (document.querySelector('[data-test="challenge-complete-reverse-translation"]'))
        return 'complete-reverse-translation';
    if (document.querySelector('[data-test="challenge-judge"]'))
        return 'judge-challenge';
    return 'unknown';
}

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
