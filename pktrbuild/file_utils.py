import os
import shutil
import subprocess
import pktrbuild


def call(command):
	pktrbuild.print_command(command)
	if subprocess.call(command) != 0:
		pktrbuild.error("error")
		
		
def create_folder(dir):
	if not os.path.exists(dir):
		pktrbuild.print_command("create folder " + dir)
		os.makedirs(dir)
		
		
def delete_folder(dir):
	if os.path.exists(dir):
		pktrbuild.print_command("delete folder " + dir)
		shutil.rmtree(dir)
		
		uptree = os.path.split(dir)[0]
		if os.path.exists(uptree):
			try:
				os.removedirs(uptree)
			except:
				return
		
		
def delete_file(file):
	if os.path.isfile(file):
		pktrbuild.print_command("delete file " + file)
		os.remove(file)
		
		uptree = os.path.split(file)[0]
		if os.path.exists(uptree):
			try:
				os.removedirs(uptree)
			except:
				return