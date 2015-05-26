# -*- coding:utf8
import threading


class ThreadWorker(threading.Thread):
    def __init__(self, callable, *args, **kwargs):
        super(ThreadWorker, self).__init__()
        self.callable = callable
        self.args = args
        self.kwargs = kwargs
        self.lock = threading.RLock()
        #self.setDaemon(True)

    def run(self):
        #try:
        self.callable(*self.args, **self.kwargs)
        #except Exception, e:
            #print e


if __name__ == "__main__":
    def test(a):
        print 'hello'
        print a
    #TODO ? 有问题
    worker = ThreadWorker(test,'aaha')
    worker.start()
    #import time
    #time.sleep(3)
