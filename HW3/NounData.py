from SynSetFinder import * 
class NounData:
	def __init__(self, noun):
		"""
		Initializes the noun data class,
		it recieves a noun and creates list of hypernym hyponym meronym
		as a part of enhancement it also creates the sets that corrspond to 
		multilevel hyponomy and meronomy.
		"""
		self.count           = 0
        	self.synset_list     = []
       		self.hypernym_list   = []
       		self.hyponym_list    = []
        	self.meronym_list    = []
        	self.antonym_list    = []
		self.meronym_list    = []
		self.hyponomy_set    = set([]) 
		self.hypernomy_set   = set([])
		self.meronomy_set    = set([])
		self.noun = noun 
		self.__calculate_all_data(noun)
		self.count += 1
	
	def __get_hyponyms(self, synsets):
		"""
		method that creates a list of hyponyms
		:param:synset
		:return:hyponym_list_p
		"""
		hyponym_list_p = []
		for syn_set in synsets:# Iterate over synsets
			hyponym_list_p.append(syn_set.hyponyms())# Append hyponyms to the list
		return hyponym_list_p

	def __get_hypernyms(self, synsets):
		"""
		This method returns the list of hypernyms 
		to the caller.
		:param:synset
		:return:hypernym_list_p
		"""
		hypernym_list_p = []
		for syn_set in synsets:
			hypernym_list_p.append(syn_set.hypernyms())
		return hypernym_list_p

	def __get_antonyms(self, synsets):
		"""
		This method returns the list of antonyms
		to the caller method
		:param:synset
		:return: antonym_list_p
		"""
		antonym_list_p = []
		for syn_set in synsets:
			for lemma_word in syn_set.lemmas():
				antonym_list_each_lm = [lemma_word.antonyms()] 
				antonym_list_p.append(antonym_list_each_lm)
		return antonym_list_p
	
	def __get_meronyms(self, synsets):
		"""
		Returns the list of Meronyms to the caller method
		:param:synsets
		:returns: meronym_list_p
		"""
		meronym_list_p = []
		for syn_set in synsets:
			meronym_list_p.append(syn_set.part_meronyms())
		return meronym_list_p
	
	def __get_hyponomy_set(self, synsets):
		"""
		Method returns the Union set of all the direct hyponym of the set
		:param:synsets
		:return:hyponomy_set_p
		"""
		hyponomy_set_p = set([])
		for syn_set in synsets:
			# Lambda function to calculate the deepest hyponym set and union it with previous one
			hyponomy_set_p = hyponomy_set_p | set([i for i in syn_set.closure(lambda s:s.hyponyms())])
		return hyponomy_set_p
			
	
	def __get_hypernomy_set(self, synsets):
		"""
		method returns the union set of all the direct hypernym of the set
		:param: synsets
		:return: hypernomy_set_p
		"""
		hypernomy_set_p = set([])
		for syn_set in synsets:
			# Lambda function to calculate the deepest hypernym set and union it with previous one
			hypernomy_set_p = hypernomy_set_p | set([i for i in syn_set.closure(lambda s:s.hypernyms())])
		return hypernomy_set_p
	
	def __get_meronomy_set(self, synsets):
		"""
		This method returns the union set of all the direct meronym set
		:param: synsets
		:return: meronym_set_p
		"""
		meronomy_set_p = set([])
		for syn_set in synsets:
			# Lambda function to calculate the deepest meronym set and union it with the previous one
			meronomy_set_p = meronomy_set_p | set([i for i in syn_set.closure(lambda s:s.part_meronyms())])
		return meronomy_set_p

		
	def __calculate_all_data(self, noun):
		"""
		calculates synsets and all the related data 
		like hypernym hyponym meronym and thier sets.
		:param: noun
		:return: None
		"""
		synsetFinder = SynSetFinder(noun)
		synsets = synsetFinder.list_all_synsets()
		self.synset_list.append(synsets)
		self.hypernym_list.append(self.__get_hypernyms(synsets))
		self.hyponym_list.append(self.__get_hyponyms(synsets))
		self.antonym_list.append(self.__get_antonyms(synsets))
		self.meronym_list.append(self.__get_meronyms(synsets))
		
		##Enhancement listing All Hypernym and Hypernyms using 
		##Lambda functions of python
		self.hyponomy_set = self.__get_hyponomy_set(synsets)
		self.hypernomy_set = self.__get_hypernomy_set(synsets)
		self.meronomy_set = self.__get_meronomy_set(synsets)

	def increase_count_value(self):
		"""
		increases the count of the word 
		everytime somebody hits this method
		:param:
		:return:
		"""
		self.count += 1
