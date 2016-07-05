import os
import glob
import pktrbuild


class ActionGccLink:

	def __init__(
			self,
			out,
			objs,
			deps = [],
			linker = "gcc",
			flags = ""):
		self.deps = list(deps)
		
		self.in_files = []
		for f in objs:
			final_name = os.path.normpath(f)
			
			if f.count(":") == 1:
				split = f.split(":")
				self.deps.append(split[0])
				final_name = os.path.join(os.path.normpath(split[0]), os.path.normpath(split[1]))
			
			self.in_files.append(final_name)
		
		self.out_file = os.path.normpath(out)
		self.linker = linker
		self.linker_flags = flags

	def make(self):
		bin_file = os.path.join(pktrbuild.get_action_folder(), self.out_file)
		
		latest_mtime = 0
		in_files_str = ""
		for in_file in self.in_files:
		
			files = []
			if in_file.count("*") > 0:
				for f in glob.iglob(os.path.join(pktrbuild.get_target_folder(), in_file), recursive=True):
					files.append(f)
			else:
				files.append(os.path.join(pktrbuild.get_target_folder(), in_file))
				
			for filename in files:
				if not os.path.isfile(filename):
					pktrbuild.error("file not found: " + filename)
				
				mtime = os.path.getmtime(filename)
				
				if mtime > latest_mtime:
					latest_mtime = mtime
				
				in_files_str += filename
				in_files_str += " "
		
		if not os.path.isfile(bin_file) or os.path.getmtime(bin_file) < latest_mtime:
			pktrbuild.file_utils.create_folder(pktrbuild.get_action_folder())
			pktrbuild.file_utils.call(self.linker + " -o " + bin_file + " " + in_files_str + " " + self.linker_flags)
			
		return True
		
	def clean(self):
		pktrbuild.file_utils.delete_file(os.path.join(pktrbuild.get_action_folder(), self.out_file))
		return True