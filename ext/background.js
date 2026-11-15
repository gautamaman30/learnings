// Listen for extension installation or update
chrome.runtime.onInstalled.addListener(() => {
    console.log('Meet Audio Interceptor installed/updated');
});

// Listen for messages from content script or popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getStatus') {
        // Get the active tab
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                // Send message to content script
                chrome.tabs.sendMessage(tabs[0].id, {action: 'getAudioState'}, function(response) {
                    sendResponse(response);
                });
            }
        });
        return true; // Required for async response
    }
}); 