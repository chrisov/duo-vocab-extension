console.log('[DUO-EXT] content.js loaded');

// Attach click listener to document
document.addEventListener('click', trackLessonClick, true);

// Update your listener to start the observer when a lesson starts
chrome.runtime.onMessage.addListener((message) => {
    if (message.type === "URL_CHANGED") {
        console.log('[DUO-EXT] Message received:', message);
        handleLessonStateChange();
    }
});

// Initial page load check (fallback)
handleLessonStateChange();

// Combined logic for both initial load and URL changes
function handleLessonStateChange() {
    console.log('[DUO-EXT] Checking lesson state, pathname:', window.location.pathname);
    if (window.location.pathname.includes('/lesson')) {
        console.log('[DUO-EXT] On lesson page, attaching click listener');
        startContinuousScrape();
    } else {
        console.log('[DUO-EXT] Not on lesson page, removing click listener');
        stopContinuousScrape();
    }
}
