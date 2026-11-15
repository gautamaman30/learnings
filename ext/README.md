# Meet Audio Interceptor Chrome Extension

This Chrome extension allows you to intercept and process audio from your microphone before it reaches Google Meet. You can use this to add custom audio processing, adjust volume, or implement other audio modifications.

## Features

- Intercepts microphone audio before it reaches Google Meet
- Real-time audio processing
- Volume control
- Simple user interface
- Works specifically with Google Meet

## Installation

1. Download or clone this repository
2. Open Chrome and go to `chrome://extensions/`
3. Enable "Developer mode" in the top right corner
4. Click "Load unpacked" and select the directory containing this extension
5. The extension icon should appear in your Chrome toolbar

## Usage

1. Click the extension icon in your Chrome toolbar to open the control panel
2. Use the volume slider to adjust the audio level
3. Toggle the audio processing on/off using the button
4. Join a Google Meet call as usual
5. The extension will automatically intercept and process your microphone audio

## Development

The extension consists of the following components:

- `manifest.json`: Extension configuration
- `content.js`: Handles audio interception and processing
- `background.js`: Manages extension events and communication
- `popup.html` & `popup.js`: User interface for controlling the extension

## Customization

You can modify the audio processing in `content.js` by adding your own processing logic in the `onaudioprocess` event handler. Some examples of what you could add:

- Noise reduction
- Echo cancellation
- Audio effects
- Voice modulation
- Custom filters

## Security Note

This extension requires microphone access to function. Make sure to only install it from trusted sources.

## License

MIT License 