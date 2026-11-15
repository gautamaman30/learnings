// Overloading works with getter and setter
 
class Temp {
    get name() {
        return this.myName
    }

    set name(myName) {
        this.myName = myName
    }
}

temp = new Temp()

temp.name = 'Aman'
console.log(temp.name)