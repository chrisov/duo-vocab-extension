chrome.webNavigation.onHistoryStateUpdated.addListener((details) => {
    // Only send message if it's the main frame (not an iframe)
    if (details.frameId === 0) {
        chrome.tabs.sendMessage(details.tabId, {
            type: "URL_CHANGED",
            url: details.url
        });
    }
}, { url: [{ hostSuffix: 'duolingo.com' }] });