""" Helper functions to be called from environment.py """

# To successfully install psutil, using "pip install psutil", 
# you need to first have "Python.h":
#	sudo apt-get install python3-dev
# https://psutil.readthedocs.io/en/latest/
import psutil

import time


def wait_for_port(port, min_wait_secs=0, max_wait_secs=30, kill_process=False, process_name=None):
	""" Wait for port to become free. Optionally kill the associated process.

		If the "kill_process" argument is True, and the "process_name" argument
		is also passed, an extra check of the process's name will be performed 
		before killing the process, and then continuing to wait for the port to 
		become free.
	"""
	start_time = time.clock()
	if min_wait_secs > 0 and not check_port(port, False):
		time.sleep(min_wait_secs)
	while True:
		(port, pid, name) = check_port(port, False)
		if not pid:
			break
		if time.clock() - start_time > max_wait_secs:
			raise RuntimeError("Waited more than {} secs for port {} to become free! (pid={})".format(max_wait_secs, port, pid))
		time.sleep(0.05)
		if kill_process == True:
			try:
				ps =  psutil.Process(pid)
				name = ps.as_dict()['name']
				if process_name and not process_name == name:
					#  Do not kill. Process name not as expected.
					continue
				ps.terminate()
				time.sleep(3)	# Give some time for process clean-up.
			except:
				pass


def check_port(port, raise_exception=True):
	""" Check if specific port is free, and optionally raise exception if it isn't """
	for conn in psutil.net_connections(kind='all'):
		if isinstance(conn.laddr, psutil._common.addr):
			if port == conn.laddr.port:
				ps = psutil.Process(conn.pid)
				if raise_exception == True:
					raise RuntimeError("Port is in use! port={}, pid={} ({})".format(port, ps.pid, ps._name))
				else:
					return (port, ps.pid, ps._name)
	return ('', '', '')

