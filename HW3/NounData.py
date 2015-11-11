from SynSetFinder import * 
class NounData:
	def __init__(self, noun):
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
			hyponym_list_p = []
			for syn_set in synsets:
				hyponym_list_p.append(syn_set.hyponyms())
			return hyponym_list_p

	def __get_hypernyms(self, synsets):
		hypernym_list_p = []
		for syn_set in synsets:
			hypernym_list_p.append(syn_set.hypernyms())
		return hypernym_list_p

	def __get_antonyms(self, synsets):
		antonym_list_p = []
		for syn_set in synsets:
			for lemma_word in syn_set.lemmas():
				antonym_list_each_lm = [lemma_word.antonyms()] 
				antonym_list_p.append(antonym_list_each_lm)
		return antonym_list_p
	
	def __get_meronyms(self, synsets):
		meronym_list_p = []
		for syn_set in synsets:
			meronym_list_p.append(syn_set.part_meronyms())
		return meronym_list_p
	
	def __get_hyponomy_set(self, synsets):
		hyponomy_set_p = set([])
		for syn_set in synsets:
			hyponomy_set_p = hyponomy_set_p | set([i for i in syn_set.closure(lambda s:s.hyponyms())])
		return hyponomy_set_p
			
	
	def __get_hypernomy_set(self, synsets):
		hypernomy_set_p = set([])
		for syn_set in synsets:
			hypernomy_set_p = hypernomy_set_p | set([i for i in syn_set.closure(lambda s:s.hypernyms())])
		return hypernomy_set_p
	
	def __get_meronomy_set(self, synsets):
		meronomy_set_p = set([])
		for syn_set in synsets:
			meronomy_set_p = meronomy_set_p | set([i for i in syn_set.closure(lambda s:s.part_meronyms())])
		return meronomy_set_p

		
	def __calculate_all_data(self, noun):
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
		self.count += 1
