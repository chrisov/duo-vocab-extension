// console.log('[DUO-EXT] scraper.js loaded');

let listening = true;
let isProcessing = false;

function handleInteraction(event, words) {
    // If we are currently in a timeout/processing, ignore new inputs
    if (isProcessing)
        return;

    const nextButton = document.querySelector('[data-test="player-next"]');
    if (!nextButton)
        return;

    // Check if it's a click on the button or an Enter keypress
    const isButtonClick = event.type === 'click' && event.target.closest('[data-test="player-next"]');
    const isEnterKey = event.type === 'keydown' && event.key === 'Enter';

    if (!isButtonClick && !isEnterKey)
        return;

    // IMPORTANT: Only extract when the button is in "Check" mode.
    // Once clicked, Duolingo changes the label to "Continue" or "Next".
    const buttonText = nextButton.innerText.toLowerCase();
    
    // Adjust these strings based on your UI language (e.g., 'verificar' for PT)
    if (buttonText !== 'check')
        return; 

    isProcessing = true;
    console.log(`[DUO-EXT] ${event.type === 'click' ? 'Mouse' : 'Enter'} trigger: Extracting...`);

    setTimeout(() => {
        extractWords(words);
        isProcessing = false; // Reset flag after extraction
    }, 150);
}

function startContinuousScrape(words) {
    if (!listening)
        return;
    listening = false;
    console.log('[DUO-EXT] Attaching click listener to player-next button');
    document.addEventListener('click', (event) => handleInteraction(event, words), true);
    document.addEventListener('keydown', (event) => handleInteraction(event, words), true);
    
    // Extract words from the first challenge after a longer delay for DOM to load
    setTimeout(() => {
        console.log('[DUO-EXT] Extracting first challenge...');
        extractWords(words);
    }, 1500);
}

function stopContinuousScrape(words) {
    if (listening)
        return;
    listening = true;
    console.log('[DUO-EXT] Removing click listener from player-next button');
    document.removeEventListener('click', (event) => handleInteraction(event, words), true);
    document.removeEventListener('keydown', (event) => handleInteraction(event, words), true);
    
    // Send extracted vocabulary to backend
    if (words.size > 0) {
        sendVocabularyToBackend(Array.from(words));
        resetVocabulary(words)
    } else {
        console.log('[DUO-EXT] No vocabulary extracted from this lesson');
    }
}
