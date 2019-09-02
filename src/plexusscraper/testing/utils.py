""" Helper functions to be called from environment.py """

import os

# To successfully install psutil, using "pip install psutil", 
# you need to first have "Python.h":
#	sudo apt-get install python3-dev
# https://psutil.readthedocs.io/en/latest/
# https://pypi.org/project/psutil/
import psutil

from tempfile import NamedTemporaryFile

import time


def create_tmpfile(_suffix='tmpfile'):
	""" Create a temporary file and return file path """
	f = NamedTemporaryFile(delete=False, suffix=_suffix)
	f.close()
	return f.name


def delete_file(file_path):
	os.unlink(file_path)


def wait_for_port(port, min_wait_secs=0, max_wait_secs=60, kill_process=False, process_name=None, debug=False):
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
		(port, pid, exe, cmdline) = check_port(port, False)
		if not pid:
			break
		time_elapsed = time.clock() - start_time
		if time_elapsed > max_wait_secs:
			raise RuntimeError("Waited more than {} secs for port {} to become free! (pid={})".format(max_wait_secs, port, pid))
		print("wait_for_port: elapsed (secs) {}, port {} in use, by pid {}, process {}, cmdline {}".format(time_elapsed, port, pid, exe, cmdline))
		if kill_process == True:
			try:
				ps =  psutil.Process(pid) 	
				exe = ps.name()
				if process_name and not process_name == exe:
					#  Do not kill. Process name not as expected.
					continue
				ps.terminate()
				time.sleep(3)	# Give some time for process clean-up.
			except:
				pass
		time.sleep(3)


def check_port(port, raise_exception=True):
	""" Check if specific port is free, and optionally raise exception if it isn't """
	for conn in psutil.net_connections(kind='inet'):		
		if isinstance(conn.laddr, psutil._common.addr):
			if port == conn.laddr.port:
				ps = psutil.Process(conn.pid)
				if raise_exception == True:
					raise RuntimeError("Port is in use! port={}, pid={} ({})".format(port, ps.pid, ps.name()))
				else:
					return (port, ps.pid, ps.name(), ps.cmdline())
	return ('', '', '', '')


def is_port_in_use(port):
	import socket
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
		return s.connect_ex(('localhost', port)) == 0

