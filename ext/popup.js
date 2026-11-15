document.addEventListener('DOMContentLoaded', function() {
    const statusElement = document.getElementById('status');
    const volumeSlider = document.getElementById('volume');
    const toggleButton = document.getElementById('toggleProcessing');
    
    let isProcessing = false;
    
    // Check initial status
    chrome.runtime.sendMessage({action: 'getStatus'}, function(response) {
        if (response) {
            isProcessing = response.isProcessing;
            updateStatus();
        }
    });
    
    // Update status display
    function updateStatus() {
        statusElement.textContent = `Status: ${isProcessing ? 'Processing' : 'Not Processing'}`;
        toggleButton.textContent = isProcessing ? 'Stop Processing' : 'Start Processing';
    }
    
    // Handle volume changes
    volumeSlider.addEventListener('input', function(e) {
        const volume = e.target.value / 100;
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: 'setVolume',
                    volume: volume
                });
            }
        });
    });
    
    // Handle toggle button
    toggleButton.addEventListener('click', function() {
        chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
            if (tabs[0]) {
                chrome.tabs.sendMessage(tabs[0].id, {
                    action: 'toggleProcessing',
                    enabled: !isProcessing
                }, function(response) {
                    if (response && response.success) {
                        isProcessing = !isProcessing;
                        updateStatus();
                    }
                });
            }
        });
    });
}); 