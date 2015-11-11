from NounData import *
from textblob import TextBlob
from WordonomyAssertion import *
import copy
import ConfigParser

def check_if_element_relation(word, lexical_chain_dict):
	"""
	Method that takes word and a lexical chain and compares it
	through the wordonomy assertion
	:param word:
	:param lexical_chain_dict:
	:return: True if relation found else false
	"""
	# Call for wordonomy assertion.
	bool_check = wordonomy_assertion.check_assertion(word,
							 lexical_chain_dict,
							 wdd_cpy,
							 activate_multilevel_wordonomy_transition)
	return bool_check


def print_lexical_chain(lexical_chain_dict):
	"""
	Method that prints lexical chains in the format of the assignment.
	:param lexical_chain_dict:
	:return: None
	"""
	chain_count = 1
	for key in lexical_chain_dict:
		print ("Chain " + str(chain_count) +":\t"),
		for lexical_chain_word in lexical_chain_dict[key]: # Iterate over lexical chain dictionary
			if lexical_chain_word in word_details_dict: # check if word in global word dict
				print (lexical_chain_word + "(" +
					   str(word_list.count(lexical_chain_word)) + ")"),
				if lexical_chain_word is not\
						lexical_chain_dict[key][-1]:
						print (", "),
		print
		chain_count += 1
	print


def create_lexical_chain(wdd_cpy, wlist_cpy):
	"""
	Method that creates lexical chains based on Word dictionary in
	a paragraph and the wordlist in the paragraph.
	This method is the algorithmic implementation of how we are searching
	for each and every element and building chains our of it.
	:param wdd_cpy:
	:param wlist_cpy:
	:return: None
	"""
	word = str(wlist_cpy[0]) # Assign first word from the list
	word_list =  [wlist_cpy[0]] # Create the wordlist with 0th element
	lexical_chain_dict = {word: word_list} # Create first lexical chain with word and wordlist
	while len(wlist_cpy) != 0: #check if wlist_cpy has all the elements popped
		list_lexical_chain = [] # Create new lexical chain list
		if wlist_cpy[0] not in lexical_chain_dict: # check if present in dictionary
			# Call element relationship method to check if
			element_rship =\
				check_if_element_relation(str(wlist_cpy[0]),
							  lexical_chain_dict)
			if element_rship:
				list_lexical_chain.append(wlist_cpy[0]) # Append the word to the list
			# else create a new lexical chain dictionary
			else:
				lexical_chain_dict[str(wlist_cpy[0])] = [wlist_cpy[0]]
		# Pop the element from the top of the list once done
		# Continue with the next element in the list.
		wlist_cpy.pop(0)
	# Print lexical chain once done.
	print_lexical_chain(lexical_chain_dict)

def clear_global_data_structs():
	"""
	Clears all the global data structures that have been used in the program
	so as to serve for the calculation
	:return: None
	"""
	global word_list
	word_details_dict.clear()
	lexical_chain_dict.clear()
	word_list = []


word_details_dict = dict() # Initializing empty word dictionary
lexical_chain_dict = dict() # Initialize the lexical chain dictionary.
word_list = [] # Empty list for holding all the words given in a paragraph.
# Call the clear method after processing every paragraph to clear
# the contents of the dictionary.
# For considering the whole document in the chain, DO NOT call the 
# Clear method
Config = ConfigParser.ConfigParser()
Config.read("configuration.ini")
activate_multilevel_wordonomy_transition =\
	Config.getboolean("SectionOne", "activate_multilevel_wordonomy_transition")
test_file = open('test_data.bin', 'r')

#single wordonomy assertion object.
#Saves multiple instance memory block.
wordonomy_assertion = WordonomyAssertion()


delimiter = "\n" # Delimiter, currently taken as a new line.
# splits the document into paragraph
# separated by a new line \n being the delimiter
paragraph_list =\
	test_file.read().split(delimiter) # read files as bunch of paragraph
test_file.close() # Close the file.


for paragraph in paragraph_list:
	# word_list = paragraph.split()
	# add noun tagger here and extract nouns
	# added noun tagger v2
	# further supply as word_list
	blob = TextBlob(paragraph)
	wordlistx = []
        wordlistx = blob.tags
	for (word,i) in wordlistx:
            if (i=='NN') or (i=='NNS'):
                word_list.append(word.lower())
		for word in word_list: #Iterate over every wordlist
			if word not in word_details_dict:
				word_details_dict[word] = NounData(word)# Create dictionary with word and NounData instance
			else:
				noun_data = word_details_dict[word]
				noun_data.increase_count_value()# increase the noun data count variable.
	wdd_cpy = word_details_dict.copy() # copies the dictionary element.
	wlist_cpy = copy.copy(word_list) # does a deep copy of the wordlist
	create_lexical_chain(wdd_cpy, wlist_cpy) # call to create lexical chain
	clear_global_data_structs() # calls for clearing global data structures
