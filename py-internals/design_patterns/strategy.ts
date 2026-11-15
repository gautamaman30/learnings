/**
 * Strategy Pattern (Behaviour): Allows client to use any strategy available at runtime. They don't need to know the details. 
 * The strategies are encapsulated.
 */

interface ShippingStrategy {
    calculate: (weightInKg: number, distanceInKm: number) => number
}

class FedExShipping implements ShippingStrategy {
    calculate(weightInKg: number, distanceInKm: number): number {
        const baseFare = 10;
        const weightCost = weightInKg * 5;
        const distanceCost = distanceInKm * 6.5;
        return baseFare + weightCost + distanceCost;
    }
}

class UPSShipping implements ShippingStrategy {
    calculate(weightInKg: number, distanceInKm: number): number {
        const baseFare = 9;
        const weightCost = weightInKg * 4;
        const distanceCost = distanceInKm * 8;
        return baseFare + weightCost + distanceCost;
    }
}

class Order {
    private shippingStrategy: ShippingStrategy;
    private weight: number;
    private distance: number;

    constructor(weight: number, distance: number, shippingStrategy: ShippingStrategy) {
        this.weight = weight;
        this.distance = distance;
        this.shippingStrategy = shippingStrategy;
    }

    changeShippingStrategy(shippingStrategy: ShippingStrategy) {
        this.shippingStrategy = shippingStrategy;
    }

    getShippingCost() {
        return this.shippingStrategy.calculate(this.weight, this.distance);
    }

    getWeight(): number {
        return this.weight;
    }
    
    getDistance(): number {
        return this.distance;
    }
}

const fedExShipping = new FedExShipping();
const order = new Order(500, 1000, fedExShipping);
console.log('Shiping cost', order.getShippingCost());
const upsShipping = new UPSShipping();
order.changeShippingStrategy(upsShipping);
console.log('Shiping cost', order.getShippingCost());
