// Audio processing setup
let audioContext;
let mediaStream;
let sourceNode;
let processorNode;
let destinationNode;

// Initialize audio processing
async function initializeAudioProcessing() {
    try {
        // Get user media with audio
        mediaStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        
        // Create audio context
        audioContext = new AudioContext();
        
        // Create source node from media stream
        sourceNode = audioContext.createMediaStreamSource(mediaStream);
        
        // Create script processor node for audio processing
        processorNode = audioContext.createScriptProcessor(4096, 1, 1);
        
        // Create destination node
        destinationNode = audioContext.createMediaStreamDestination();
        
        // Connect nodes
        sourceNode.connect(processorNode);
        processorNode.connect(destinationNode);
        
        // Process audio data
        processorNode.onaudioprocess = (audioProcessingEvent) => {
            const inputBuffer = audioProcessingEvent.inputBuffer;
            const outputBuffer = audioProcessingEvent.outputBuffer;
            
            // Get input data
            const inputData = inputBuffer.getChannelData(0);
            // Get output data
            const outputData = outputBuffer.getChannelData(0);
            
            // Process audio data here
            for (let i = 0; i < outputData.length; i++) {
                // Example: Simple pass-through with volume adjustment
                outputData[i] = inputData[i] * 1.0; // Adjust volume multiplier as needed
                
                // Add your custom audio processing here
                // For example: noise reduction, echo cancellation, etc.
            }
        };
        
        // Replace the original media stream with our processed stream
        const processedStream = destinationNode.stream;
        
        // Find and replace the audio track in all video elements
        document.querySelectorAll('video').forEach(video => {
            if (video.srcObject) {
                const tracks = video.srcObject.getTracks();
                const audioTrack = tracks.find(track => track.kind === 'audio');
                if (audioTrack) {
                    audioTrack.stop();
                    video.srcObject = processedStream;
                }
            }
        });
        
        console.log('Audio processing initialized successfully');
    } catch (error) {
        console.error('Error initializing audio processing:', error);
    }
}

// Start audio processing when the page loads
initializeAudioProcessing();

// Listen for messages from the popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'getAudioState') {
        sendResponse({
            isProcessing: !!audioContext,
            volume: 1.0 // Add volume control if needed
        });
    }
}); 