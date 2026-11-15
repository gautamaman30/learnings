/**
 * Builder Pattern (Creational): Allows creating complex objects step by step. 
 */

class House {
    rooms: number = 2;
    bathRooms: number = 2;
    workSpace: boolean = false;
    swimmingPool: boolean = false;
    garage: boolean = false;
    garden: boolean = false;
}

interface HouseBuilder {
    setRooms: (rooms: number) => this
    setBathRooms: (bathRooms: number) => this
    addSwimmingPool: () => this
    addGarage: () => this
    addGarden: () => this
    addWorkSpace: () => this
}

class MyHouseBuilder implements HouseBuilder {
    private house: House;

    constructor() {
        this.house = new House();
    }

    setRooms(rooms: number) {
        this.house.rooms = rooms;
        return this;
    }
    setBathRooms(bathRooms: number) {
        this.house.bathRooms = bathRooms;
        return this;
    }

    addSwimmingPool() {
        this.house.swimmingPool = true;
        return this;
    }
    addGarage() {
        this.house.garage = true;
        return this;
    }
    addGarden() {
        this.house.garden = true;
        return this;
    }
    addWorkSpace() {
        this.house.workSpace = true;
        return this;
    }

    build() {
        return this.house;
    }
}

const myHouseBuilder = new MyHouseBuilder();
const house = myHouseBuilder
    .setRooms(4)
    .setBathRooms(5)
    .addSwimmingPool()
    .addGarage()
    .addWorkSpace()
    .build();

console.log('house', house)