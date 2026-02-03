console.log('[DUO-EXT] challenges.js loaded');

function extractWords() {
    // Verify we're in a gapFill challenge
	const words = [];
    const challengeType = getChallengeType();

	console.log(`[DUO-EXT] ${challengeType} challenge detected!`);
    if (challengeType === 'gapFill') {
        words = gapFillChallenge();
    }
}

/**
 * Extract Spanish words from challenge-gapFill type exercises
 * Structure example:
 * - Main container: <div data-test="challenge challenge-gapFill">
 * - Spanish options: <span data-test="challenge-judge-text" dir="ltr" lang="es">word</span>
 * - Hint tokens: <div data-test="hint-token" aria-label="word"></div>
 * 
 * @returns {Array<string>} Array of extracted Spanish words
 */
function gapFillChallenge() {
	const words = [];
    
    // Find the gapFill challenge container
    const gapFillContainer = document.querySelector('[data-test="challenge challenge-gapFill"]');
    if (!gapFillContainer) {
        console.log('[DUO-EXT] gapFill container not found');
        return words;
    }
	
	// Extract Spanish words from hint-token elements (the sentence context words)
	const hintTokenElements = gapFillContainer.querySelectorAll('[data-test="hint-token"]');
	hintTokenElements.forEach(el => {
		const text = el.getAttribute('aria-label');
		if (text && text.trim() && !words.includes(text.trim())) {
			words.push(text.trim());
		}
	});
    
    // Extract Spanish words from challenge-judge-text elements (the answer options)
    const judgeTextElements = gapFillContainer.querySelectorAll('[data-test="challenge-judge-text"][lang="es"]');
    judgeTextElements.forEach(el => {
        const text = el.textContent.trim();
        if (text && !words.includes(text)) {
            words.push(text);
        }
    });
    
    // Log the extracted words
    if (words.length > 0) {
        console.log(`[DUO-EXT] Extracted ${words.length} Spanish word(s) from gapFill challenge:`, words);
    } else {
        console.log('[DUO-EXT] No Spanish words found in gapFill challenge');
    }
    
    return words;
}
