class ActionDummy:
	deps = []
	
	def __init__(self, deps):
		self.deps = deps
	
	def make(self):
		return True
		
	def clean(self):
		return True