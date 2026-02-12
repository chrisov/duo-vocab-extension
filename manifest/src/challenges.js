// console.log('[DUO-EXT] challenges.js loaded');

function extractWords(words) {
    const challengeType = getChallengeType();
    const language = getCurrentLanguage();

    console.log('Challenge type:', challengeType);
    if (!language) {
        console.error('[DUO-EXT] Could not detect language, skipping extraction');
        return;
    }
    
    let localWords = new Set();
    if (challengeType === 'gapFill') {
        localWords = gapFillChallenge(language);
    } else if (challengeType === 'translate') {
        localWords = translateChallenge(language);
    } else if (challengeType === 'tapComplete') {
        localWords = tapCompleteChallenge(language);
    }
    
    // Add extracted words to global vocabulary collection
    if (localWords && localWords.size > 0) {
        localWords.forEach(word => words.add(word));
        console.log(`[DUO-EXT] Total vocabulary accumulated: ${words.size} word(s)`);
    }
    return words;
}

function gapFillChallenge(language) {
	const localWords = new Set();
    
    // Find the gapFill challenge container
    const gapFillContainer = document.querySelector('[data-test="challenge challenge-gapFill"]');
    if (!gapFillContainer) {
        console.log('[DUO-EXT] gapFill container not found');
        return localWords;
    }
	
	// Extract localWords from hint-token elements (the sentence context localWords)
	const hintTokenElements = gapFillContainer.querySelectorAll('[data-test="hint-token"]');
	hintTokenElements.forEach(el => {
		const text = el.getAttribute('aria-label');
		if (text && text.trim()) {
			localWords.add(text.trim());
		}
	});
    
    // Extract localWords from challenge-judge-text elements with the detected language
    const judgeTextElements = gapFillContainer.querySelectorAll(`[data-test="challenge-judge-text"][lang="${language}"]`);
    judgeTextElements.forEach(el => {
        const text = el.textContent.trim();
        if (text) {
            localWords.add(text);
        }
    });
    
    // Log the extracted localWords
    if (localWords.size > 0) {
        console.log(`[DUO-EXT] Extracted ${localWords.size} word(s):`, Array.from(localWords));
    } else {
        console.log('[DUO-EXT] No localWords found!');
    }
    
    return localWords;
}

function translateChallenge(language) {
    const localWords = new Set();
    
    // Find the translate challenge container
    const translateContainer = document.querySelector('[data-test="challenge challenge-translate"]');
    if (!translateContainer) {
        console.log('[DUO-EXT] translate container not found');
        return localWords;
    }
    
    // Extract localWords from hint-token elements only when lang matches the detected language
    const hintTokenElements = translateContainer.querySelectorAll('[data-test="hint-token"]');
    hintTokenElements.forEach(el => {
        const langElement = el.closest('[lang]');
        const tokenLang = langElement ? langElement.getAttribute('lang') : null;
        if (!tokenLang || tokenLang === 'en' || tokenLang !== language) {
            return;
        }

        const text = el.getAttribute('aria-label');
        if (text && text.trim()) {
            localWords.add(text.trim());
        }
    });

    // Extract localWords from tap tokens only when lang matches the detected language
    const tapTokenElements = translateContainer.querySelectorAll(
        `[data-test*="challenge-tap-token"][lang="${language}"] ` +
        `[data-test="challenge-tap-token-text"]`
    );
    tapTokenElements.forEach(el => {
        const tokenText = el.textContent.trim();
        if (!tokenText) {
            return;
        }
        localWords.add(tokenText);
    });
    
    // Log the extracted localWords
    if (localWords.size > 0) {
        console.log(`[DUO-EXT] Extracted ${localWords.size} word(s):`, Array.from(localWords));
    } else {
        console.log('[DUO-EXT] No localWords found!');
    }
    
    return localWords;
}

function tapCompleteChallenge (language) {
    const localWords = new Set();

    // Find the tapComplete challenge container
    const tapCompleteContainer = document.querySelector('[data-test="challenge challenge-tapComplete"]');
    if (!tapCompleteContainer) {
        console.log('[DUO-EXT] tapComplete container not found');
        return localWords;
    }

    // Extract words from hint-token elements only when lang matches the detected language
    const hintTokenElements = tapCompleteContainer.querySelectorAll('[data-test="hint-token"]');
    hintTokenElements.forEach(el => {
        const langElement = el.closest('[lang]');
        const tokenLang = langElement ? langElement.getAttribute('lang') : null;
        if (!tokenLang || tokenLang === 'en' || tokenLang !== language) {
            return;
        }

        const text = el.getAttribute('aria-label');
        if (text && text.trim()) {
            localWords.add(text.trim());
        }
    });

    // Extract words from tap-token-text elements (word bank options), filtered by language
    const tapTokenElements = tapCompleteContainer.querySelectorAll('[data-test="challenge-tap-token-text"]');
    tapTokenElements.forEach(el => {
        const langElement = el.closest('[lang]');
        const tokenLang = langElement ? langElement.getAttribute('lang') : null;
        if (!tokenLang || tokenLang === 'en' || tokenLang !== language) {
            return;
        }

        const tokenText = el.textContent.trim();
        if (!tokenText) {
            return;
        }
        localWords.add(tokenText);
    });

    // Log the extracted words
    if (localWords.size > 0) {
        console.log(`[DUO-EXT] Extracted ${localWords.size} word(s):`, Array.from(localWords));
    } else {
        console.log('[DUO-EXT] No words found!');
    }

    return localWords;
}