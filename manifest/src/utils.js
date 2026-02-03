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

// function getExerciseFingerprint() {
//     const header = document.querySelector('[data-test="challenge-header"]')?.textContent.trim() || '';
//     const spanish = Array.from(document.querySelectorAll('[lang="es"]'))
//         .map(el => el.textContent.trim())
//         .filter(Boolean)
//         .join('|');
//     const type = detectExerciseType();
//     return `${type}::${header}::${spanish}`;
// }

// function getCurrentChallengeId() {
//     const header = document.querySelector('[data-test="challenge-header"]');
//     return header?.getAttribute('data-test') || '';
// };

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