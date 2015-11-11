from SynSetFinder import *
class WordonomyAssertion:
	def __init__(self):
		pass


	def check_assertion(self, word, lexical_chain_dict, wdd_cpy):
		SynSetFinder_word_instance = SynSetFinder(word)
		synsets_given_word = SynSetFinder_word_instance.list_all_synsets()
		for key in lexical_chain_dict:
			list_lexical_chain = lexical_chain_dict[key]
			noun_data = wdd_cpy[key]
			
			#Enhancement Code:
			#To be run only in the case where activate_multilevel_wordonomy_transition = True
			#Read from configuration.ini
			if True:
				for synset in synsets_given_word:
					if synset in noun_data.hyponomy_set or \
									synset in noun_data.hypernomy_set or\
									synset in noun_data.meronomy_set:
						if word not in list_lexical_chain:
							list_lexical_chain.append(word)
							return True
					
			

			#compares value existence in hypernym list
			for hypernym in noun_data.hypernym_list:
				for synsets in hypernym:
					for synset in synsets:
						for lemma in synset.lemmas():
							if word in lemma.name() and\
											word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#compares value existence in hyponym list
			for hyponym in noun_data.hyponym_list:
				for synsets in hyponym:
					for synset in synsets:
						for lemma in synset.lemmas():
							if word in lemma.name() and\
											word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#compares value from antonym list
			for antonym in noun_data.antonym_list:
				for synsets in antonym:
					for synset in synsets:
						for lemma in synset:
							if word in lemma.name() and\
											word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#Compares value with a synset itself
			for synsets in noun_data.synset_list:
				for synset in synsets:
					for lemma in synset.lemmas():
						if word in lemma.name() and\
										word not in list_lexical_chain:
							list_lexical_chain.append(word)
							return True
			
			#Compares value from the meronym_list supplied.
			for meronyms in noun_data.meronym_list:
				for synsets in meronyms:
					for synset in synsets:
							if word in synset.name() and\
											word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True