import sublime, sublime_plugin, random, time
  
class RoboTypeCommand(sublime_plugin.TextCommand):  
	
	# A basic map of the keyboard.
	keys = [
		['q','w','e','r','t','y','u','i','o','p','[',']'],
		['a','s','d','f','g','h','j','k','l',';','\''],
		['z','x','c','v','b','n','m',',','.','/']
	]

	# The fastest possible keystroke, in milliseconds
	intervalLow = 10

	# The slowest possible keystroke, in milliseconds
	intervalHigh = 100

	# The position of the first occuring typo in the current rendered text
	typoIndex = None

	# The delay, in milliseconds for each keystroke. Continually augmented.
	timeout = None

	# The index of the cliboard text currently being rendered
	stringIndex = 0

	def run(self, edit):
		# Get text from clipboard
		self.text_to_print = sublime.get_clipboard()		
		
		# Override from settings
		self.intervalLow = self.view.settings().get('robotype_keystroke_interval_low')
		self.intervalHigh = self.view.settings().get('robotype_keystroke_interval_high')

		# Establish an initial timout
		self.timeout = self.getInterval()
		
		# Loop through the string
		while self.stringIndex < len(self.text_to_print):			
			# If there is a typo on the screen, and the robot "notices" it, backspace.
			if(self.typoIndex is not None):				
				if(self.willBackspace()):					
					self.backspaceTo(self.typoIndex)
					self.typoIndex = None

			nextChar = self.text_to_print[self.stringIndex]
			keystroke = self.generateKeystroke(nextChar)
			
			# If a typo was rendered, capture its position
			if( (keystroke is not nextChar) and (self.typoIndex is None) ):								
				self.typoIndex = self.stringIndex
			
			self.renderChar(keystroke)
			self.stringIndex += 1

		self.reset()

	# Queues the rendering of a character
	def renderChar(self, char):
		self.queueAction(lambda char=char: self.view.run_command('robo_type_add_char', {"args" : { 'char': char }}))

	# Backspaces to a position in the string
	def backspaceTo(self, index):
		while self.stringIndex > index:			
			self.queueAction(lambda: self.view.run_command('robo_type_delete_char'))
			self.stringIndex -= 1

	# Schedule an action, using the incrementing timeout
	def queueAction(self, func):
		self.timeout += self.getInterval()
		sublime.set_timeout(func, self.timeout)

	# Did the robot "notice" the typo?
	def willBackspace(self):
		if(self.stringIndex is (len(self.text_to_print)-1)):
			return true
		
		chance = self.view.settings().get('robotype_typo_reaction')
		rand = random.randrange(1, chance+1)
		
		return rand is 1

	# Gets a random keystroke speed, using the low/high threshold from the settings
	def getInterval(self):
		return random.randrange(self.intervalLow, self.intervalHigh+1)

	# Given a character, render it, or a typo, depending on the outcome
	def generateKeystroke(self, char):
		chance = self.view.settings().get('robotype_keystroke_accuracy')
		rand = random.randrange(1, chance+1)
		if rand is not 1: 
			return char	
		for rowIndex, row in enumerate(self.keys):
			for keyIndex, key in enumerate(row):
				if key is char:					
					badKey = random.randrange(-1, 2)+keyIndex
					badRow = random.randrange(-1, 2)+rowIndex
					if badRow is -1: badRow = 0
					elif badRow >= len(self.keys): badRow = len(self.keys)-1 
						
					if badKey is -1: badKey = 0
					elif badKey >= len(self.keys[badRow]): badKey = len(self.keys[badRow])-1

					return self.keys[badRow][badKey]
		return char

	def reset(self):
		self.stringIndex = 0
		self.typoIndex = None	


# Adds a character to the screen
class RoboTypeAddCharCommand(sublime_plugin.TextCommand):
	
	def run(self, edit, args):
		self.view.insert(edit, self.view.sel()[0].begin(), args['char'])


# Deletes the previous character from the screen
class RoboTypeDeleteCharCommand(sublime_plugin.TextCommand):
	
	def run(self, edit):
		point = self.view.sel()[0].begin()
		region = sublime.Region(point-1, point)
		self.view.erase(edit, region)

