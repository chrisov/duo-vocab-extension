// console.log('[DUO-EXT] scraper.js loaded');

let listening = true;
let isProcessing = false;

function handleInteraction(event) {
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
        extractWords();
        isProcessing = false; // Reset flag after extraction
    }, 150);
}


/**
 * Handle click on check/continue button 
 * */ 
// function handleCheckButtonClick(event) {
//     const nextButton = document.querySelector('[data-test="player-next"]');
//     if (!nextButton)
//         return;

//     const clickedInsideButton = !!event.target.closest('[data-test="player-next"]');
//     if (!clickedInsideButton)
//         return;
    
//     console.log('[DUO-EXT] Check button clicked, extracting vocabulary...');
    
//     // Small delay to let the DOM update after the click
//     setTimeout(() => {
//         extractWords();
//     }, 100);
// }

// Handle Enter key for check/continue
// function handleCheckKeydown(event) {
//     if (event.key !== 'Enter')
//         return;

//     const nextButton = document.querySelector('[data-test="player-next"]');
//     if (!nextButton)
//         return;

//     const activeElement = document.activeElement;
//     if (activeElement && !activeElement.closest('[data-test="player-next"]'))
//         return;

//     console.log('[DUO-EXT] Enter pressed, extracting vocabulary...');

//     setTimeout(() => {
//         extractWords();
//     }, 100);
// }

function startContinuousScrape() {
    if (!listening)
        return;
    listening = false;
    console.log('[DUO-EXT] Attaching click listener to player-next button');
    document.addEventListener('click', handleInteraction, true);
    document.addEventListener('keydown', handleInteraction, true);
    
    // Extract words from the first challenge after a longer delay for DOM to load
    setTimeout(() => {
        console.log('[DUO-EXT] Extracting first challenge...');
        extractWords();
    }, 1500);
}

function stopContinuousScrape() {
    if (listening)
        return;
    listening = true;
    console.log('[DUO-EXT] Removing click listener from player-next button');
    document.removeEventListener('click', handleInteraction, true);
    document.removeEventListener('keydown', handleInteraction, true);
    
    // TODO: Add the extraction of the lesson sector/unit/etc

}