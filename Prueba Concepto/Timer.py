import time
import threading

class Timer(threading.Thread):
	def __init__(self, seconds):
		self.runTime = seconds
		threading.Thread.__init__(self)
	def correr(self, callback, arg):
		time.sleep(self.runTime)
		callback(arg)
		print "Buzzzz!! Time's up!"

#>>> t = Timer(10)
#>>> t.start()
#>>> Buzzzz!! Time's up!

