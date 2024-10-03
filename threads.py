import threading
import queue
import psutil
import time
import os
import atexit

_running = False
_qiu = queue.Queue()
_lock = threading.Lock()
_window_size = 1800  # Window size of 1h
_cpu_percentage = _window_size * [0.0]
_processes = {}


def monitor():
    global _cpu_percentage
    global _processes

    while True:
        marker = time.time()
        total = 0.0
        pids = psutil.pids()
        processes = {}
        for pid in pids:
            process = _processes.get(pid)
            if process is None:
                try:
                    process = psutil.Process(pid)
                    processes[pid] = process
                    total += process.cpu_percent()
                except psutil.NoSuchProcess:
                    pass
        print(len(_processes), total, psutil.cpu_percent())
        _processes = processes
        # Push new measurement to front of list
        _cpu_percentage.insert(0, total)
        # Apply FIFO rule to get freshest 1800 values
        _cpu_percentage = _cpu_percentage[:1800]
        duration = max(0.0, 1.0 - (time.time() - marker))

        try:
            return _qiu.get(timeout=duration)
        except queue.Empty:
            pass


thread = threading.Thread(target=monitor)
thread.setDaemon(True)


def exiting():
    try:
        _qiu.put(True)
    except:
        pass
    thread.join()


# def track_changes(path):
#     if not path in files:
#         files.append(path)


def start_monitor():
    global _running
    _lock.acquire()
    if not _running:
        prefix = "monitor (pid={}):".format(os.getpid())
        print("{} Starting CPU monitor.".format(prefix))
        _running = True
        thread.start()
        atexit.register(exiting)
    _lock.release()


def cpu_average(interval: int = 1):
    return sum(_cpu_percentage[:min(interval, _window_size)]) / interval
