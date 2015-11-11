from SynSetFinder import *
class WordonomyAssertion:
	def __init__(self):
		pass


	def check_assertion(self, word, lexical_chain_dict, wdd_cpy, activate_multilevel_wordonomy_transition):
		"""
		Compares the word with every existing relationship of the word which is the parent of
		Lexical chain dictionary.
		:param word:
		:param lexical_chain_dict:
		:param wdd_cpy:
		:param activate_multilevel_wordonomy_transition:
		:return: True when value found and False when nothing matches.
		"""
		# Create SynSetFinder_word_instance and its list
		# only if Enhancement is set to True
		# Which is read from configuration.ini
		if activate_multilevel_wordonomy_transition:
			SynSetFinder_word_instance = SynSetFinder(word)
			# List all Synsets from the word instance
			synsets_given_word = SynSetFinder_word_instance.list_all_synsets()
		for key in lexical_chain_dict: # Iterate over pre-existing lexical chain dictionary
			list_lexical_chain = lexical_chain_dict[key] # Get lexical chain list
			noun_data = wdd_cpy[key] # Get noun data from the class
			
			# Enhancement Code:
			# To be run only in the case where activate_multilevel_wordonomy_transition = True
			# Read from configuration.ini
			if activate_multilevel_wordonomy_transition:
				for synset in synsets_given_word: # Iterate over synsets of the word
					# Check if its present in any of the sets which have been precalculated
					# Using Lambda functions of Python
					if synset in noun_data.hyponomy_set or \
								synset in noun_data.hypernomy_set or\
								synset in noun_data.meronomy_set:
						# Check preconditions and add to the list
						# Return with True
						if word not in list_lexical_chain: # Check if word already exists in chain
							list_lexical_chain.append(word)
							return True
					
			
			#Non Enhancement code, simple lexical chains getting compared
			#each time a word is sent across this method.
			#compares value existence in hypernym list
			for hypernym in noun_data.hypernym_list: #Iterate over hypernym list
				for synsets in hypernym: # Iterate over hypernyms
					for synset in synsets: # Iterare over synsets
						for lemma in synset.lemmas(): #iterate over synset lemmas
							# Check pre-conditions and add to the list of lex chains
							# Return to caller with True
							if word in lemma.name() and\
										word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#compares value existence in hyponym list
			for hyponym in noun_data.hyponym_list: #Iterate over Hyponym List
				for synsets in hyponym: #Iterate over hyponym
					for synset in synsets: # Iterate over synsets
						for lemma in synset.lemmas(): # Iterate over lemmas
							# Check preconditions and add to list return from
							# the method returning True
							if word in lemma.name() and\
										word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#compares value from antonym list
			for antonym in noun_data.antonym_list: # Iterate over Antonym List
				for synsets in antonym: # Iterate over antonyms
					for synset in synsets: # Iterate over synsets
						for lemma in synset: # Iterate over synset for lemma
							# Check preconditions and add to list
							# Return with True
							if word in lemma.name() and\
										word not in list_lexical_chain:
								list_lexical_chain.append(word)
								return True

			#Compares value with a synset itself
			for synsets in noun_data.synset_list: #Iterate over Synset list
				for synset in synsets: # iterate over synsets
					for lemma in synset.lemmas(): #Iterate over Synset Lemmas
						# Check preconditions and adding element into the list
						# Returning with True
						if word in lemma.name() and\
									word not in list_lexical_chain:
							list_lexical_chain.append(word)
							return True
			
			#Compares value from the meronym_list supplied.
			for meronyms in noun_data.meronym_list: #Iterate over meronym List
				for synsets in meronyms: #Iterate over meronyms list
					for synset in synsets: # Iterate over synsets
						#Check preconditions and add the element to the list
						# Return with True
						if word in synset.name() and\
									word not in list_lexical_chain:
							list_lexical_chain.append(word)
							return True
		return False # Return false when none of the given conditions match.
