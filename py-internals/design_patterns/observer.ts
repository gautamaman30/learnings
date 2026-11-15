/**
 * Observer Pattern (behaviour): This pattern is used to pass signal when state changes to all connected subjects at once
 */

class EmailSubscriber {
    name: string = "";
    email: string = "";

    constructor(name: string, email: string) {
        this.name = name;
        this.email = email;
    }

    update(news: string) {
        console.log('Email sent to', this.email, 'regarding News:', news);
    }
}

class TechNewsPublisher {
    private subscribers: EmailSubscriber[] = [];
    private techNews: string[] = [];

    constructor() {
        this.subscribers = [];
        this.techNews = [];
    }

    subscribe(subscriber: EmailSubscriber) {
        this.subscribers.push(subscriber);
        console.log(subscriber.name, 'subscribed to tech news.');
    }

    unsubscribe(subscriber: EmailSubscriber) {
        this.subscribers = this.subscribers.filter(s => s.email !== subscriber.email);
        console.log(subscriber.name, 'unsubscribed to tech news.')
    }

    addNews(news: string) {
        this.techNews.push(news);
        this.notifySubscribers(news);
    }

    private notifySubscribers(news: string) {
        this.subscribers.forEach(s => s.update(news));
    }
}


const techNewsPub = new TechNewsPublisher();

const subscriber1 = new EmailSubscriber('Aman', 'gautamaman30@gmail.com');
const subscriber2 = new EmailSubscriber('Kirti Rohil', 'kirti.rohil@gmail.com');
techNewsPub.addNews("Waqf ammendment bill challenged in SC");
techNewsPub.subscribe(subscriber1);
techNewsPub.subscribe(subscriber2);
techNewsPub.addNews("Trump added new 245% tariffs to China");
const subscriber3 = new EmailSubscriber('Elon musk', 'elon@gmail.com');
const subscriber4 = new EmailSubscriber('Adani', 'adani@gmail.com');
techNewsPub.subscribe(subscriber3);
techNewsPub.subscribe(subscriber4);
techNewsPub.addNews("China retaliates to US tariffs");
techNewsPub.unsubscribe(subscriber3);
techNewsPub.addNews("India reaches $5 trillion GDP");
