const buff = Buffer.alloc(5);
console.log(buff);
buff[0] = 20;
console.log(buff);

const stringBuf = Buffer.from("Hello world");
console.log(stringBuf);
console.log(stringBuf.length);

const tempBuf = Buffer.alloc(10);
tempBuf.write("this is longer than 10");
console.log('tempBuf', tempBuf.length);

const newBuf = Buffer.from(tempBuf + "nger than 10");
console.log('newBuf', newBuf);
console.log(newBuf.toString());

// Encodes in binary
const buf = Buffer.from("Hello", 'binary');
// Decodes in ascii
console.log(buf.toString('ascii'))


// Character from ascii code
console.log(String.fromCharCode(65));
// ASCII code from character
console.log('A'.charCodeAt(0));

let a = 12;
// Decimal to binary string
console.log(a.toString(2));

// Binary string to decimal
console.log(parseInt(a.toString(2), 2));
