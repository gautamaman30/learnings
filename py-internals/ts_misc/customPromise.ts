type Executor<T> = (
  resolve: (value: T) => void,
  reject: (reason?: any) => void
) => void;

type State = 'pending' | 'fulfilled' | 'rejected';

class MyPromise<T> {
  private state: State = 'pending';
  private value: T | null = null;
  private reason: any = null;
  private thenCallbacks: Array<(value: T) => void> = [];
  private catchCallbacks: Array<(reason: any) => void> = [];

  constructor(executor: Executor<T>) {
      const resolve = (value: T) => {
          if (this.state !== 'pending') return;
          this.state = 'fulfilled';
          this.value = value;
          this.thenCallbacks.forEach(cb => cb(value));
      };

      const reject = (reason: any) => {
          if (this.state !== 'pending') return;
          this.state = 'rejected';
          this.reason = reason;
          this.catchCallbacks.forEach(cb => cb(reason));
      };

      try {
          executor(resolve, reject);
      } catch (err) {
          reject(err);
      }
  }

  then(onFulfilled: (value: T) => void): MyPromise<T> {
      if (this.state === 'fulfilled' && this.value !== null) {
          onFulfilled(this.value);
      } else {
          this.thenCallbacks.push(onFulfilled);
      }
      return this;
  }

  catch(onRejected: (reason: any) => void): MyPromise<T> {
      if (this.state === 'rejected') {
          onRejected(this.reason);
      } else {
          this.catchCallbacks.push(onRejected);
      }
      return this;
  }
}
