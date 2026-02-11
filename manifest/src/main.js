// console.log('[DUO-EXT] main.js loaded successfully');
// console.log('[DUO-EXT] Current URL:', window.location.href);
// console.log('[DUO-EXT] Current pathname:', window.location.pathname);

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
    const pathname = window.location.pathname;
    
    if (pathname.includes('/lesson')) {
        console.log('[DUO-EXT] On lesson page, starting vocabulary scraper');
        startContinuousScrape();
    } else if (pathname.includes('/learn')) {
        console.log('[DUO-EXT] On learn page, extracting session info');
        try {
            stopContinuousScrape();
        } catch (e) {
            console.log('[DUO-EXT] Error stopping scraper:', e);
        }
        initLearnPageDetection();
    } else {
        console.log('[DUO-EXT] On other page, cleaning up');
        try {
            stopContinuousScrape();
        } catch (e) {
            console.log('[DUO-EXT] Error cleaning up:', e);
        }
    }
}
