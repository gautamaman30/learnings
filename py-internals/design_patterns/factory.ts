/**
 * Factory Pattern (Creational): Allow easier creation of different objects by client 
 * without depending on client to change when we need to add more type of objects
 */

abstract class Product {
    public printProduct() {}
}

class Phone extends Product {
    private model: string;

    constructor(model: string) {
        super();
        this.model = model;
        this.printProduct();
    }

    public printProduct(): void {
        console.log('Phone ' + this.model);
    }
}

class Laptop extends Product {
    private model: string;

    constructor(model: string) {
        super();
        this.model = model;
        this.printProduct();
    }
    
    public printProduct(): void {
        console.log('Laptop ' + this.model);
    }
}

class Shirt extends Product {
    private brand: string;

    constructor(brand: string) {
        super();
        this.brand = brand;
        this.printProduct();
    }
    
    public printProduct(): void {
        console.log('Shirt ' + this.brand);
    }
}

abstract class ProductFactory {
    public static createProduct() {}
}

class PhoneFactory extends ProductFactory {
    public static createProduct() {
        return new Phone('iphone');
    }
}

class LaptopFactory extends ProductFactory {
    public static createProduct() {
        return new Laptop('Macbook');
    }
}

class ShirtFactory extends ProductFactory {
    public static createProduct() {
        return new Shirt('Bear house');
    }
}

const phone = PhoneFactory.createProduct();
const shirt = ShirtFactory.createProduct();
const laptop = LaptopFactory.createProduct();

