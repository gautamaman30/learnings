/**
 * Adapter Pattern (Structural): Allow Clients to use system even if the clients do not support that system
 */

class WeatherApi {
    getCurrentWeatherCelcius() {
        return 30;
    }
}

class WeatherApiAdapter {
    private weatherApi: WeatherApi;
    
    constructor() {
        this.weatherApi = new WeatherApi();
    }

    getCurrentWeatherCelcius() {
        return this.weatherApi.getCurrentWeatherCelcius();
    }

    getCurrentWeatherFahrenheit() {
        return (this.weatherApi.getCurrentWeatherCelcius() * 9 / 5) + 32;
    }
}

const weather = new WeatherApiAdapter();

console.log('Temp in celcius', weather.getCurrentWeatherCelcius());
console.log('Temp in fahrenheit', weather.getCurrentWeatherFahrenheit());
