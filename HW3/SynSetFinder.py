from nltk.corpus import wordnet
class SynSetFinder:

	def __init__(self, word):
		self.word = word #initializes  Synsetfinder class with word
	
	def list_all_synsets(self):
		"""
		Lists all the Synset of the given instance with a word.
		:return: Synset List got from the Natural Language ToolKit Library.
		"""
		synset_list = wordnet.synsets(self.word, pos='n')
		return synset_list
		

