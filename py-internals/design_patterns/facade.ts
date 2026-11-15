/**
 * Facade Pattern (Structural): This pattern hides the complexity of subsystems from the client
 */

class VideoSystem {
    turnOn() {
        console.log('Turning on video system...');
    }

    setInput(input: string) {
        console.log('Now playing:', input);
    }

    turnOff() {
        console.log('Turning off video system...');
    }
}

class AudioSystem {
    turnOn() {
        console.log('Turning on audio system...');
    }

    setVolume(level: number) {
        console.log('Volume set to level', level);
    }

    playTrack(track: string) {
        console.log('Playing track:', track);
    }

    turnOff() {
        console.log('Turning off audio system...');
    }
}

class LightningSystem {
    dimLights(level: number) {
        console.log('Dim lights to level', level);
    }

    turnOff() {
        console.log('Turning off lights...');
    }
}

class HomeTheaterSystem {
    private videoSystem: VideoSystem;
    private audioSystem: AudioSystem;
    private lightningSystem: LightningSystem;

    constructor(videoSystem: VideoSystem, audioSystem: AudioSystem, lightningSystem: LightningSystem) {
        this.videoSystem = videoSystem;
        this.audioSystem = audioSystem;
        this.lightningSystem = lightningSystem;
    }

    playMovie(movie: string) {
        console.log('Setting up home theatre system to play:', movie);
        this.lightningSystem.dimLights(5);
        this.videoSystem.turnOn();
        this.videoSystem.setInput(movie);
        this.audioSystem.turnOn();
        this.audioSystem.setVolume(10);
    }

    playMusic(track: string) {
        console.log('Setting up home theatre system to play music track:', track);
        this.audioSystem.turnOn();
        this.audioSystem.setVolume(15);
        this.audioSystem.playTrack(track);
    }
}

const video = new VideoSystem();
const audio = new AudioSystem();
const light = new LightningSystem();

const homeTheatre = new HomeTheaterSystem(video, audio, light);
homeTheatre.playMovie('Batman Begin');
homeTheatre.playMusic('Not afraid by Eminem');