import denque from 'denque';
import express from 'express';

const app = express();
const ipMap = new Map<string, denque<any>>();
// const queue = new denque();

const rateLimitMiddleWare = (req: any, res: any, next: any) => {
    const ip = req.ip || req.connection.remoteAddress;
    const now = Date.now() 
    const windowStart = now - 60000;
    if (!ipMap.has(ip)) {
        ipMap.set(ip, new denque());
    }
    const queue  = ipMap.get(ip)!;
    while(queue.size() && queue.peekFront() < windowStart) {
        queue.shift();
    }
    if (queue.size() < 5) {
        queue.push(now);
        next();
    } else {
        const wait = Math.ceil((60000 - (now - queue.peekFront())) / 1000);
        res.setHeader('Retry-After', wait);
        res.status(429).send(`Too many requests: wait for ${wait} sec`);
    }
}

app.use(rateLimitMiddleWare);
app.get('/', (req: any, res: any) => {
    res.send('Okay');
});

app.listen(8080, () => {
    console.log('Listening on port 8080');
});
