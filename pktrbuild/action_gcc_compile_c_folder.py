import os
import glob
import pktrbuild


class ActionGccCompileCFolder:

	def __init__(
			self,
			folder,
			deps = [],
			compiler = "gcc",
			flags = ""):
		self.deps = list(deps)
		self.proj_folder = os.path.normpath(folder)
		self.compiler = compiler
		self.compiler_flags = flags

		
	def make(self):
		if not os.path.exists(self.proj_folder):
			pktrbuild.warning("folder does not exist: " + self.proj_folder)
			return False
			
		source_files = []
		object_files = []
		self.find_src_files("*.c", source_files, object_files)
		self.find_src_files("*.cpp", source_files, object_files)
		
		all_headers_mtime = self.get_files_last_mtime(glob.iglob(os.path.join(self.proj_folder, "**", "*.h"), recursive=True))
		
		had_changes = False
		for source_file, object_file in zip(source_files, object_files):
			if os.path.isfile(object_file):
				src_mtime = os.path.getmtime(source_file)
				obj_mtime = os.path.getmtime(object_file)
				if obj_mtime >= src_mtime and obj_mtime >= all_headers_mtime:
					continue
			
			had_changes = True
			pktrbuild.file_utils.create_folder(os.path.split(object_file)[0])
			pktrbuild.file_utils.call(self.compiler + " " + self.compiler_flags + " -c " + source_file + " -o " + object_file)

		return True
		
		
	def clean(self):
		if not os.path.exists(self.proj_folder):
			pktrbuild.warning("folder does not exist: " + self.proj_folder)
			return False
		
		pktrbuild.file_utils.delete_folder(pktrbuild.get_action_folder())
		return True
		
		
	def find_src_files(self, wildcard, source_files, object_files):
		for filename in glob.iglob(os.path.join(self.proj_folder, "**", wildcard), recursive=True):
			relfilename = os.path.relpath(filename, self.proj_folder)
			source_files.append(os.path.join(self.proj_folder, relfilename))
			object_files.append(os.path.join(pktrbuild.get_action_folder(), os.path.splitext(relfilename)[0] + ".o"))
			
		
	def get_files_last_mtime(self, files):
		last_mtime = 0
		for f in files:
			mtime = os.path.getmtime(f)
			if mtime > last_mtime:
				last_mtime = mtime
		return last_mtime