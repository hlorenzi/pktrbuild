import sys
import os
from .toposort import topological_sort


class colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    RESET = "\033[0m"


cur_action_name = "default"


def make(execute_order, actions_def):
	for action in execute_order:
		printc(colors.BOLD, "make " + action)
		globals()["cur_action_name"] = action
	
		if not actions_def[action].make():
			printc(colors.RED, "error")
			return False
	
	printc(colors.GREEN, "success")
	return True


def clean(list, actions_def):
	for action in list:
		printc(colors.BOLD, "clean " + action)
		globals()["cur_action_name"] = action
		
		actions_def[action].clean()
	
	printc(colors.GREEN, "success")
	return True


def list(list, actions_def):
	for action in list:
		printc(colors.BOLD, action)
		for dep in actions_def[action].deps:
			print("  dep: " + dep)
	
	return True
	
	
def printc(color, str):
	print(color + str + colors.RESET)
	sys.stdout.flush()
	
	
def print_command(str):
	print("  " + str)
	sys.stdout.flush()
	
	
def error(str):
	printc(colors.RED, str)
	sys.exit()
	
	
def warning(str):
	printc(colors.YELLOW, str)
	

def get_target_folder():
	return os.path.join(".build")
	

def get_action_folder():
	return os.path.join(".build", os.path.normpath(cur_action_name))
	
	
def execute(actions_def):
	if len(sys.argv) < 3:
		print("usage: command action [action...]")
		sys.exit()
		
	command = sys.argv[1]
	actions = []
	
	for i in range(2, len(sys.argv)):
		if sys.argv[i] not in actions_def:
			error("unknown action '" + sys.argv[i] + "'")
			
		actions.append(sys.argv[i])
	
	actions_execute_order = topological_sort(actions_def, actions)
	
	if actions_execute_order == None:
		error("cyclic dependencies")
	
	if command == "make":
		make(actions_execute_order, actions_def)
	
	elif command == "clean":
		clean(actions, actions_def)
	
	elif command == "cleanr":
		clean(actions_execute_order, actions_def)
		
	elif command == "list":
		list(actions_execute_order, actions_def)
		
	else:
		error("invalid command")
		