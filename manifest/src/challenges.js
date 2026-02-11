// console.log('[DUO-EXT] challenges.js loaded');

function extractWords() {
    const challengeType = getChallengeType();
    const language = getCurrentLanguage();

    console.log('Challenge type: ', challengeType);
    if (!language) {
        console.error('[DUO-EXT] Could not detect language, skipping extraction');
        return;
    }
    
    if (challengeType === 'gapFill') {
        const words = gapFillChallenge(language);
    } else if (challengeType === 'translate') {
        const words = translateChallenge(language);
    }
}

function gapFillChallenge(language) {
	const words = new Set();
    
    // Find the gapFill challenge container
    const gapFillContainer = document.querySelector('[data-test="challenge challenge-gapFill"]');
    if (!gapFillContainer) {
        console.log('[DUO-EXT] gapFill container not found');
        return words;
    }
	
	// Extract words from hint-token elements (the sentence context words)
	const hintTokenElements = gapFillContainer.querySelectorAll('[data-test="hint-token"]');
	hintTokenElements.forEach(el => {
		const text = el.getAttribute('aria-label');
		if (text && text.trim()) {
			words.add(text.trim());
		}
	});
    
    // Extract words from challenge-judge-text elements with the detected language
    const judgeTextElements = gapFillContainer.querySelectorAll(`[data-test="challenge-judge-text"][lang="${language}"]`);
    judgeTextElements.forEach(el => {
        const text = el.textContent.trim();
        if (text) {
            words.add(text);
        }
    });
    
    // Log the extracted words
    if (words.size > 0) {
        console.log(`[DUO-EXT] Extracted ${words.size} word(s) from gapFill challenge:`, Array.from(words));
    } else {
        console.log('[DUO-EXT] No words found in gapFill challenge');
    }
    
    return words;
}

function translateChallenge(language) {
    const words = new Set();
    
    // Find the translate challenge container
    const translateContainer = document.querySelector('[data-test="challenge challenge-translate"]');
    if (!translateContainer) {
        console.log('[DUO-EXT] translate container not found');
        return words;
    }
    
    // Extract words from hint-token elements only when lang matches the detected language
    const hintTokenElements = translateContainer.querySelectorAll('[data-test="hint-token"]');
    hintTokenElements.forEach(el => {
        const langElement = el.closest('[lang]');
        const tokenLang = langElement ? langElement.getAttribute('lang') : null;
        if (!tokenLang || tokenLang === 'en' || tokenLang !== language) {
            return;
        }

        const text = el.getAttribute('aria-label');
        if (text && text.trim()) {
            words.add(text.trim());
        }
    });

    // Extract words from tap tokens only when lang matches the detected language
    const tapTokenElements = translateContainer.querySelectorAll(
        `[data-test*="challenge-tap-token"][lang="${language}"] ` +
        `[data-test="challenge-tap-token-text"]`
    );
    tapTokenElements.forEach(el => {
        const tokenText = el.textContent.trim();
        if (!tokenText) {
            return;
        }
        words.add(tokenText);
    });
    
    // Log the extracted words
    if (words.size > 0) {
        console.log(`[DUO-EXT] Extracted ${words.size} word(s) from translate challenge:`, Array.from(words));
    } else {
        console.log('[DUO-EXT] No words found in translate challenge');
    }
    
    return words;
}
