/**
 * Singleton Pattern (Creational): A class will only have one instance that will be used throughout the program
 * It is applied where we want to reuse the same instance. Example: DBConnectionPool
 */

interface ConnectionDetails {
    username: string,
    password: string,
    port: number,
    dbName: string,
    host: string
}

class DbConnectionPool {
    private availableConnections: Set<Number> = new Set();
    private busyConnections: Set<Number> = new Set();
    private connectionDetails: ConnectionDetails | undefined = undefined;
    private totalConnections: number = 10;
    public isConnected: boolean = false;
    private static _instance: DbConnectionPool | undefined;
    
    constructor(connectionDetails: ConnectionDetails, numberOfConnections: number = 10) {
        if (!DbConnectionPool._instance) {
            this.connectionDetails = connectionDetails;
            this.totalConnections = numberOfConnections;
            const connections = Array.from({ length: numberOfConnections }, (_, i) => i);
            this.availableConnections = new Set(connections);
            this.busyConnections = new Set();
            this.isConnected = true;           
            DbConnectionPool._instance = this; 
        }
        return DbConnectionPool._instance;
    }

    private ensureConnected(): void {
        if (!this.isConnected) {
            throw new Error("Not connected to the database.");
        }
    }

    get connection(): number {
        this.ensureConnected();
        const size = this.availableConnections.size;
        if (!size) {
            throw new Error('No connection available');
        }
        this.availableConnections.delete(size-1);
        this.busyConnections.add(size-1);
        return size-1;
    }

    public closeConnection(conn: number) {
        this.ensureConnected();
        if (conn >= this.totalConnections) {
            throw new Error('Invalid connection');
        }
        if (this.availableConnections.has(conn)) {
            throw new Error('Connection already closed');    
        }
        this.busyConnections.delete(conn);
        this.availableConnections.add(conn);
    }

    public endConnection(): void {
        this.ensureConnected();
        DbConnectionPool._instance = undefined;
    }
}

const dbPool = new DbConnectionPool({
    username: 'aman',
    password: 'sdhfldks',
    port: 5432,
    host: 'dflksdf',
    dbName: 'sdfljksd'
}, 5); 

// console.log(dbPool.connection);
// console.log(dbPool.connection);
// console.log(dbPool.connection);
// dbPool.closeConnection(3);
// dbPool.closeConnection(4);
// dbPool.closeConnection(1);