console.log('[DUO-EXT] background.js loaded');

chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    // Only send message if it's the main frame (not an iframe)
    if (details.frameId === 0) {
        console.log('[DUO-EXT] History state updated:', details.url);
        chrome.tabs.sendMessage(details.tabId, {
            type: "URL_CHANGED",
            url: details.url
        }).catch(err => {
            console.log('[DUO-EXT] Message send failed (content script may not be ready):', err);
        });
    }
}, { url: [{ hostSuffix: 'duolingo.com' }] });