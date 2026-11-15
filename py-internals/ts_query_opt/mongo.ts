import { MongoClient, Db } from 'mongodb';
import { faker } from '@faker-js/faker';
import { Worker, isMainThread, threadId } from 'worker_threads';

class DbConnection {
    private static _instance: DbConnection;
    private client: MongoClient;
    private db: Db | null = null;

    private constructor() {
        const uri = process.env.MONGO_URI || '';
        this.client = new MongoClient(uri, {
            maxPoolSize: 10
        });
    }

    static getInstance(): DbConnection {
        if (!DbConnection._instance) {
            DbConnection._instance = new DbConnection();
        }
        return DbConnection._instance;
    }

    async connect(): Promise<Db> {
        if (!this.db) {
            console.log('Connecting db');
            await this.client.connect();
            this.db = this.client.db('runo');
            console.log('Db connection successful');
        }
        return this.db;
    }

    getDb(): Db | null {
        return this.db;
    }
}

const insertUsers = async (db: Db) => {
    const users: any[] = [];
    const temp = ['first', 'second'];
    let count = 100000;
    console.log('Thread:', threadId, 'running');
    for (let i = 0; i < 100000000; i++) {
        users.push({
            name: faker.person.fullName(),
            age: faker.number.int({ min: 18, max: 60 }),
            pincode: faker.location.zipCode(),
            registration: {
                date: faker.date.past(),
                startTime: faker.date.past(),
                status: temp[Math.floor(Math.random() * 2)]
            }
        });

        if (users.length === 100000) {
            try {
                const res = await db.collection('users').insertMany(users);
                if (!res.acknowledged) {
                    throw new Error();
                }
                console.log('Thread:', threadId, 'inserted', count, 'users');
                count += 100000;
            } catch(error) {
                console.log('Thread:', threadId, 'insert error', error);
            }            
            users.length = 0;
        }
    }
}

// if (isMainThread) {
//     const workers: Set<Worker> = new Set();
//     for (let i = 0; i < 10; i++) {
//         workers.add(new Worker(__filename));
//     }
//     for (let worker of workers) {
//         worker.on('error', (err: any) => { throw err; });
//         worker.on('exit', () => {
//             workers.delete(worker);
//             console.log(`Thread exiting, ${workers.size} running...`);
//         });
//     }
// } else {
//     const dbConnection = DbConnection.getInstance();
//     dbConnection.connect().then((db: Db) => {
//         insertUsers(db);
//     }).catch(error => {
//         console.log('Error', error);
//     });
// }


// insertUsers();

// const fetchAdmins = async () => {
//     const db = await connectDb();
//     if (!db) {
//         console.log('No db');
//         return;
//     }
//     const admins = await db.collection('admins').find().toArray();
//     console.log('Admins', admins);
// }

const dbConnection = DbConnection.getInstance();

const addIndex = async () => {
    const db = await dbConnection.connect();
    if (!db) {
        console.log('No database connection');
        return;
    }
    try {
        await db.collection('users').createIndex({ 'registration.status': 1 });
    } catch (error) {
        console.error('Error fetching users:', error);
    }
    process.exit(0);
}

const fetchUser = async () => {
    const db = await dbConnection.connect();
    if (!db) {
        console.log('No database connection');
        return;
    }
    try {
        const res = await db.collection('users').find({ 'registration.status': 'first' }).explain({ verbosity: 'executionStats' });
        console.log(res);
    } catch (error) {
        console.error('Error fetching users:', error);
    }
    process.exit(0);
}


addIndex();
// fetchUser();