"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
var mongodb_1 = require("mongodb");
var faker_1 = require("@faker-js/faker");
var worker_threads_1 = require("worker_threads");
var DbConnection = /** @class */ (function () {
    function DbConnection() {
        this.db = null;
        var uri = process.env.MONGO_URI || '';
        this.client = new mongodb_1.MongoClient(uri, {
            maxPoolSize: 10
        });
    }
    DbConnection.getInstance = function () {
        if (!DbConnection._instance) {
            DbConnection._instance = new DbConnection();
        }
        return DbConnection._instance;
    };
    DbConnection.prototype.connect = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!!this.db) return [3 /*break*/, 2];
                        console.log('Connecting db');
                        return [4 /*yield*/, this.client.connect()];
                    case 1:
                        _a.sent();
                        this.db = this.client.db('runo');
                        console.log('Db connection successful');
                        _a.label = 2;
                    case 2: return [2 /*return*/, this.db];
                }
            });
        });
    };
    DbConnection.prototype.getDb = function () {
        return this.db;
    };
    return DbConnection;
}());
var insertUsers = function (db) { return __awaiter(void 0, void 0, void 0, function () {
    var users, temp, count, i, res, error_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                users = [];
                temp = ['first', 'second'];
                count = 100000;
                console.log('Thread:', worker_threads_1.threadId, 'running');
                i = 0;
                _a.label = 1;
            case 1:
                if (!(i < 100000000)) return [3 /*break*/, 7];
                users.push({
                    name: faker_1.faker.person.fullName(),
                    age: faker_1.faker.number.int({ min: 18, max: 60 }),
                    pincode: faker_1.faker.location.zipCode(),
                    registration: {
                        date: faker_1.faker.date.past(),
                        startTime: faker_1.faker.date.past(),
                        status: temp[Math.floor(Math.random() * 2)]
                    }
                });
                if (!(users.length === 100000)) return [3 /*break*/, 6];
                _a.label = 2;
            case 2:
                _a.trys.push([2, 4, , 5]);
                return [4 /*yield*/, db.collection('users').insertMany(users)];
            case 3:
                res = _a.sent();
                if (!res.acknowledged) {
                    throw new Error();
                }
                console.log('Thread:', worker_threads_1.threadId, 'inserted', count, 'users');
                count += 100000;
                return [3 /*break*/, 5];
            case 4:
                error_1 = _a.sent();
                console.log('Thread:', worker_threads_1.threadId, 'insert error', error_1);
                return [3 /*break*/, 5];
            case 5:
                users.length = 0;
                _a.label = 6;
            case 6:
                i++;
                return [3 /*break*/, 1];
            case 7: return [2 /*return*/];
        }
    });
}); };
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
var dbConnection = DbConnection.getInstance();
var addIndex = function () { return __awaiter(void 0, void 0, void 0, function () {
    var db, error_2;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, dbConnection.connect()];
            case 1:
                db = _a.sent();
                if (!db) {
                    console.log('No database connection');
                    return [2 /*return*/];
                }
                _a.label = 2;
            case 2:
                _a.trys.push([2, 4, , 5]);
                return [4 /*yield*/, db.collection('users').createIndex({ 'registration.status': 1 })];
            case 3:
                _a.sent();
                return [3 /*break*/, 5];
            case 4:
                error_2 = _a.sent();
                console.error('Error fetching users:', error_2);
                return [3 /*break*/, 5];
            case 5:
                process.exit(0);
                return [2 /*return*/];
        }
    });
}); };
var fetchUser = function () { return __awaiter(void 0, void 0, void 0, function () {
    var db, res, error_3;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0: return [4 /*yield*/, dbConnection.connect()];
            case 1:
                db = _a.sent();
                if (!db) {
                    console.log('No database connection');
                    return [2 /*return*/];
                }
                _a.label = 2;
            case 2:
                _a.trys.push([2, 4, , 5]);
                return [4 /*yield*/, db.collection('users').find({ 'registration.status': 'first' }).explain({ verbosity: 'executionStats' })];
            case 3:
                res = _a.sent();
                console.log(res);
                return [3 /*break*/, 5];
            case 4:
                error_3 = _a.sent();
                console.error('Error fetching users:', error_3);
                return [3 /*break*/, 5];
            case 5:
                process.exit(0);
                return [2 /*return*/];
        }
    });
}); };
addIndex();
// fetchUser();
