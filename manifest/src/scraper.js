console.log('[DUO-EXT] scraper.js loaded');

let listening = true;

// Extract Spanish words from various exercise types
// function extractWords() {
//     const words = [];
    
//     // Helper function to get parent challenge data-test
//     function getChallengeDataTest(element) {
//         const challengeContainer = element.closest('[data-test*="challenge"]');
//         return challengeContainer?.getAttribute('data-test') || '';
//     }

//     // Method 1: Find all elements with lang="es" attribute (most reliable)
//     const spanishElements = document.querySelectorAll('[lang="es"]');
//     spanishElements.forEach(el => {
//         const text = el.textContent.trim();
//         if (text && text.length > 0 && !words.some(w => w.word === text)) {
//             const dataTest = getChallengeDataTest(el);
//             console.log(`[DUO-EXT] Challenge data test: ${dataTest}`);
//             words.push({
//                 word: text,
//                 context: 'lang-es',
//                 dataTest: dataTest,
//                 exerciseType: detectExerciseType()
//             });
//         }
//     });
    
//     // Method 2: Find elements with dir="ltr" lang="es" combination
//     const dirLtrElements = document.querySelectorAll('[dir="ltr"][lang="es"]');
//     dirLtrElements.forEach(el => {
//         const text = el.textContent.trim();
//         if (text && text.length > 0 && !words.some(w => w.word === text)) {
//             const dataTest = getChallengeDataTest(el);
//             words.push({
//                 word: text,
//                 context: 'dir-ltr-lang-es',
//                 dataTest: dataTest,
//                 exerciseType: detectExerciseType()
//             });
//         }
//     });
    
//     // Method 3: Find challenge choices (multiple choice exercises)
//     const challengeChoices = document.querySelectorAll('[data-test="challenge-choice"]');
//     challengeChoices.forEach(choice => {
//         const spanishSpan = choice.querySelector('span[lang="es"]');
//         if (spanishSpan) {
//             const text = spanishSpan.textContent.trim();
//             if (text && !words.some(w => w.word === text)) {
//                 const dataTest = getChallengeDataTest(spanishSpan);
//                 words.push({
//                     word: text,
//                     context: 'challenge-choice',
//                     dataTest: dataTest,
//                     exerciseType: 'select-challenge'
//                 });
//             }
//         }
//     });
    
//     // Method 4: Find tap tokens (word bank exercises)
//     const tapTokens = document.querySelectorAll('[data-test="challenge-tap-token"]');
//     tapTokens.forEach(token => {
//         const spanishSpan = token.querySelector('span[lang="es"]');
//         if (spanishSpan) {
//             const text = spanishSpan.textContent.trim();
//             if (text && !words.some(w => w.word === text)) {
//                 const dataTest = getChallengeDataTest(spanishSpan);
//                 words.push({
//                     word: text,
//                     context: 'tap-token',
//                     dataTest: dataTest,
//                     exerciseType: 'tap-challenge'
//                 });
//             }
//         }
//     });
    
//     // Method 5: Find listen/speak exercises
//     const listenChallenge = document.querySelector('[data-test="challenge-listen"]');
//     if (listenChallenge) {
//         const spanishText = listenChallenge.querySelector('span[lang="es"]');
//         if (spanishText) {
//             const text = spanishText.textContent.trim();
//             if (text && !words.some(w => w.word === text)) {
//                 const dataTest = getChallengeDataTest(spanishText);
//                 words.push({
//                     word: text,
//                     context: 'listen-challenge',
//                     dataTest: dataTest,
//                     exerciseType: 'listen-challenge'
//                 });
//             }
//         }
//     }
    
//     // Get challenge header for context
//     const challengeHeader = document.querySelector('[data-test="challenge-header"]');
//     const questionText = challengeHeader ? challengeHeader.textContent.trim() : '';
    
//     // Send to Python backend if we found any words
//     if (words.length > 0) {
//         const payload = {
//             url: window.location.href,
//             question: questionText,
//             words: words,
//             timestamp: new Date().toISOString()
//         };
        
//         fetch('http://localhost:5000/save-vocabulary', {
//             method: 'POST',
//             headers: { 'Content-Type': 'application/json' },
//             body: JSON.stringify(payload)
//         })
//         .then(() => console.log(`Extracted ${words.length} Spanish word(s):`, words.map(w => w.word)))
//         .catch(err => console.error("Error saving vocabulary:", err));
//     }
// }

/**
 * Handle click on check/continue button 
 * */ 
function handleCheckButtonClick(event) {
    const nextButton = document.querySelector('[data-test="player-next"]');
    if (!nextButton) {
        return;
    }

    const clickedInsideButton = !!event.target.closest('[data-test="player-next"]');
    if (!clickedInsideButton) {
        return;
    }
    
    console.log('[DUO-EXT] Check button clicked, extracting vocabulary...');
    
    // Small delay to let the DOM update after the click
    setTimeout(() => {
        extractWords();
    }, 100);
}

// Handle Enter key for check/continue
function handleCheckKeydown(event) {
    if (event.key !== 'Enter') {
        return;
    }

    const nextButton = document.querySelector('[data-test="player-next"]');
    if (!nextButton) {
        return;
    }

    const activeElement = document.activeElement;
    if (activeElement && !activeElement.closest('[data-test="player-next"]')) {
        return;
    }

    console.log('[DUO-EXT] Enter pressed, extracting vocabulary...');

    setTimeout(() => {
        extractWords();
    }, 100);
}

function startContinuousScrape() {
    if (!listening) {
        return;
    }
    listening = false;
    console.log('[DUO-EXT] Attaching click listener to player-next button');
    document.addEventListener('click', handleCheckButtonClick, true);
    document.addEventListener('keydown', handleCheckKeydown, true);
    
    // Extract words from the first challenge after a small delay for DOM to load
    setTimeout(() => {
        console.log('[DUO-EXT] Extracting first challenge...');
        extractWords();
    }, 500);
}

function stopContinuousScrape() {
    if (listening) {
        return;
    }
    listening = true;
    console.log('[DUO-EXT] Removing click listener from player-next button');
    document.removeEventListener('click', handleCheckButtonClick, true);
    document.removeEventListener('keydown', handleCheckKeydown, true);
}