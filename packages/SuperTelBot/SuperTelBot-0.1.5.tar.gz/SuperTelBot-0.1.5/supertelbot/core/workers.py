from datetime import datetime
import time
from threading import Thread

threads = {}

workers = []


class Worker:

    def __init__(self):
        self._running = True
        self.responses = []
        self.time = None
        self.timeout = None

    def is_alive(self):
        return self._running

    def terminate(self):
        self._running = False
        raise KeyboardInterrupt

    def get_last_response(self):
        return self.responses[-1]

    def run(self, instance_call, function_call, args, time_sleep, callback, loop, timeout):
        if timeout and isinstance(timeout, int) and not self.time:
            self.time = datetime.now()
            self.timeout = int(timeout)

        if loop:

            while self._running:
                try:
                    if timeout and (datetime.now() - self.time).total_seconds() > self.timeout:
                        self.terminate()

                    else:
                        if hasattr(instance_call, function_call):
                            if not args:
                                res = getattr(instance_call, function_call)()
                            else:
                                res = getattr(instance_call, function_call)(args)
                            if callback:
                                callback(res[0][0], res[1])
                            self.responses.append(res)
                        time.sleep(time_sleep)
                except KeyboardInterrupt:
                    pass

        else:
            try:
                if timeout and (datetime.now() - self.time).total_seconds() > self.timeout:
                    self.terminate()

                else:
                    if hasattr(instance_call, function_call):
                        if not args:
                            res = getattr(instance_call, function_call)()
                        else:
                            res = getattr(instance_call, function_call)(args)
                        if callback:
                            callback(res[0][0], res[1])
                        self.responses.append(res)
                    self.terminate()
            except KeyboardInterrupt:
                pass


def start_worker(worker_name, instance_call, function_call, args=(), time_sleep=1, callback=None, loop=True,
                 run_until_end=False, log=False, timeout=None):
    try:
        w = Worker()
        if log:
            print(f"Starting Worker: {worker_name}")
        t = Thread(target=w.run,
                   args=(instance_call, function_call, args, int(time_sleep), callback, loop, timeout),
                   daemon=run_until_end)
        if loop:
            threads[worker_name] = [w, t]
        t.start()
    except Exception as e:
        print(str(e))


def worker(worker_name, instance_call, function_call, args=(), time_sleep=1, callback=None, loop=True,
           run_until_end=False, log=False, timeout=None):
    start_worker(worker_name, instance_call, function_call, args, int(time_sleep), callback, loop, run_until_end, log, timeout)
    if loop:
        workers.append(worker_name)


def stop(worker_name):
    try:
        print(f"Stopping Worker: {worker_name}")
        stop_worker(worker_name)
    except Exception as e:
        print(str(e))


def stop_worker(worker_name):
    global threads
    if worker_name in threads:
        try:
            threads[worker_name][0].terminate()
            threads[worker_name][1].join()
        except Exception as e:
            print(str(e))
        del threads[worker_name]
