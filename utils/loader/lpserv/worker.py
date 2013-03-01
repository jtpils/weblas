"""

   Least-recently used (LRU) queue device
   Demonstrates use of pyzmq IOLoop reactor

   While this example runs in a single process, that is just to make
   it easier to start and stop the example. Each thread has its own
   context and conceptually acts as a separate process.

   Author: Min RK <benjaminrk(at)gmail(dot)com>
   Adapted from lruqueue.py by Guillaume Aubert (gaubert) <guillaume(dot)aubert(at)gmail(dot)com>

"""

import threading
import time
import zmq



NBR_WORKERS = 3

def worker_thread(worker_url, i):
    """ Worker using REQ socket to do LRU routing """
    
    context = zmq.Context()
    socket = context.socket(zmq.REQ)

    identity = "Worker-%d" % (i)

    socket.setsockopt(zmq.IDENTITY, identity) #set worker identity

    socket.connect(worker_url)

    # Tell the borker we are ready for work
    socket.send("READY")

    try:
        while True:

            [address, empty, request] = socket.recv_multipart()

            print("%s: %s\n" %(identity, request))

            socket.send_multipart([address, "", "OK"])

    except zmq.ZMQError, zerr:
        # context terminated so quit silently
        if zerr.strerror == 'Context was terminated':
            return
        else:
            raise zerr




def main():
    """main method"""

    # url_worker = "ipc://backend.ipc" #"tcp://*:5557"
    url_worker = "tcp://0.0.0.0:5557"

    for i in range(NBR_WORKERS):
        thread = threading.Thread(target=worker_thread, args=(url_worker, i, ))
        thread.start()




if __name__ == "__main__":
    main()