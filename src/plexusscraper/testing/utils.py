""" Various utility functions for use by automated tests """

import os
import time
from tempfile import NamedTemporaryFile

# To successfully install psutil, using "pip install psutil", 
# you need to first have "Python.h":
#	sudo apt-get install python3-dev
# https://psutil.readthedocs.io/en/latest/
# https://pypi.org/project/psutil/
import psutil


def create_tmpfile(_suffix='tmpfile'):
	""" Create a temporary file and return the file path """
	f = NamedTemporaryFile(delete=False, suffix=_suffix)
	f.close()
	return f.name


def delete_file(file_path):
	""" Delete a file """
	os.unlink(file_path)


def wait_for_port(port, min_wait_secs=0, max_wait_secs=120, kill_process=False, process_name=None, debug=False):
	""" Wait for port to become free. Optionally kill the associated process. """

	start_time = time.clock()
	if min_wait_secs > 0 and not check_port(port, False):
		time.sleep(min_wait_secs)

	while True:
		(port, pid, exe, cmdline) = check_port(port, False)
		if not pid:
			break

		time_elapsed = time.clock() - start_time
		if time_elapsed > max_wait_secs:
			raise RuntimeError("Waited more than {} secs for port {} to become free! (pid={})".format(max_wait_secs, port, pid))

		# https://stackoverflow.com/questions/5598181/python-multiple-prints-on-the-same-line
		print("waited {} secs for port {} to become available\r".format(int(time_elapsed), port), end='', flush=True)

		if debug == True:
			print("wait_for_port: elapsed (secs) {}, port {} in use, by pid {}, process {}, cmdline {}".format(time_elapsed, port, pid, exe, cmdline))

		if kill_process == True:
			try:
				ps =  psutil.Process(pid) 	
				# If the "kill_process" argument is True, and the "process_name" argument
				# is also passed, an extra check of the process's name will be performed 
				# before killing the process, and then continuing to wait for the port to 
				# become free.
				exe = ps.name()
				if process_name and not process_name == exe:
					#  Do not kill - process name not as expected.
					continue
				ps.terminate()
				time.sleep(1)	# Give time for process clean-up.
			except:
				pass
	print("")


def check_port(port, raise_exception=True):
	""" Check if specified port is free, by examining the running processes 
	Returns: 	
		(port, pid, exe, cmdline)
	"""

	for conn in psutil.net_connections(kind='inet'):		
		if isinstance(conn.laddr, psutil._common.addr):
			if port == conn.laddr.port:
				ps = psutil.Process(conn.pid)
				if raise_exception == True:
					raise RuntimeError("Port is in use! port={}, pid={} ({})".format(port, ps.pid, ps.name()))
				else:
					return (port, ps.pid, ps.name(), ps.cmdline())
	return ('', '', '', '')


#def check_port2(port):
#	""" Check if specified port is free, by trying to connect to it. """
#	import socket
#	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#		return s.connect_ex(('localhost', port)) == 0

