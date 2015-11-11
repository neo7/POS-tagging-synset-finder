from NounData import *
from textblob import TextBlob
from WordonomyAssertion import *
import copy
import ConfigParser

def check_if_element_relation(word, lexical_chain_dict):
	bool_check = wordonomy_assertion.check_assertion(word, lexical_chain_dict, wdd_cpy)
	return bool_check


def print_lexical_chain(lexical_chain_dict):
	chain_count = 1
	for key in lexical_chain_dict:
		print ("Chain " + str(chain_count) +":\t"),
		for lexical_chain_word in lexical_chain_dict[key]:
			if lexical_chain_word in word_details_dict:
				print (lexical_chain_word + "(" +
					   str(word_list.count(lexical_chain_word)) + ")"),
				if lexical_chain_word is not\
						lexical_chain_dict[key][-1]:
						print (", "),
		print
		chain_count += 1
	print


def create_lexical_chain(wdd_cpy, wlist_cpy):
	word = str(wlist_cpy[0])
	word_list =  [wlist_cpy[0]]
	lexical_chain_dict = {word: word_list}
	while len(wlist_cpy) != 0:
		list_lexical_chain = []
		if wlist_cpy[0] not in lexical_chain_dict:
			element_rship =\
				check_if_element_relation(str(wlist_cpy[0]), lexical_chain_dict)
			if element_rship:
				list_lexical_chain.append(wlist_cpy[0])
			else:
				lexical_chain_dict[str(wlist_cpy[0])] = [wlist_cpy[0]]
		wlist_cpy.pop(0)
	print_lexical_chain(lexical_chain_dict)

def clear_global_data_structs():
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
	test_file.read().split(delimiter)
test_file.close()


for paragraph in paragraph_list:
	#word_list = paragraph.split()
	# add noun tagger here and extract nouns
	# added noun tagger v2
	# further supply as word_list
	blob = TextBlob(paragraph)
	wordlistx = []
        wordlistx = blob.tags
	for (word,i) in wordlistx:
            if (i=='NN') or (i=='NNS'):
                word_list.append(word.lower())
		for word in word_list:
			if word not in word_details_dict:
				word_details_dict[word] = NounData(word)
			else:
				noun_data = word_details_dict[word]
				noun_data.increase_count_value()
	wdd_cpy = word_details_dict.copy()
	wlist_cpy = copy.copy(word_list)
	create_lexical_chain(wdd_cpy, wlist_cpy)
	clear_global_data_structs()
