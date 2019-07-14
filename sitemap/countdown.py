from threading import Thread
import time


class myThread(Thread):
 	"""docstring for myThread"""
 	def __init__(self, downtime, jump):
		 super(myThread, self).__init__()
		 self.downtime=downtime
		 self.jump=jump
		 print("crawl data in {} min".format(self.downtime/60))

 	def run(self):
		 while self.downtime >= 0:
			 time.sleep(self.jump)
			 self.downtime-=1
		 print("end")
		 return