'''
*   Haresh Gaikwad | 20CS60R09
*   Computing Lab II
*   Assignment 9

'''
import ply.lex as lex
import ply.yacc as yacc
import os
import sys
import urllib.request
import fnmatch
import re
import warnings
warnings.filterwarnings("ignore")

os.chdir(r"celeb")

'''
-------------------------------------------------------------
LEX
-------------------------------------------------------------
'''

tokens = ('RF', 'BIRTH', 'MOV', 'MOV2', 'MOVYEAR')


t_ignore = '\t\n'


def t_RF(t):
	# <a class="celebrity-bio__link" href="/m/cleaner"> Cleaner (2007)
	r'(<a\ class="celebrity-bio__link"\ href="[a-zA-Z0-9 \- \_ \/]+">[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	regex = r'(<a\ class="celebrity-bio__link"\ href="[a-zA-Z0-9 \- \_ \/]+">[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	pattern = re.compile(regex)
	t.value = pattern.sub(r'\2', t.value).strip()
	t.value = ' '.join(t.value.split())
	return t


def t_BIRTH(t):
	# <p class="celebrity-bio__item" data-qa="celebrity-bio-bday">
	# Birthday:
	# Jul 22, 1973
	# </p>
	r'(<p\ class="celebrity-bio__item"\ data-qa="celebrity-bio-bday">[\s]+Birthday:[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	regex = r'(<p\ class="celebrity-bio__item"\ data-qa="celebrity-bio-bday">[\s]+Birthday:[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	pattern = re.compile(regex)
	t.value = pattern.sub(r'\2', t.value).strip()
	t.value = ' '.join(t.value.split())
	return t


def t_MOV(t):
	# <td class="celebrity-filmography__title"> <a href="/m/spinning_man">Spinning Man</a>
	r'(<td\ class="celebrity-filmography__title">[\s]+<a\ href="[a-zA-Z0-9 \- \_ \/]+">)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \( \) \' \! \? \- \! ]+)'
	regex = r'(<td\ class="celebrity-filmography__title">[\s]+<a\ href="[a-zA-Z0-9 \- \_ \/]+">)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \( \) \; \& \, \' \! \? \- \! ]+)'
	pattern = re.compile(regex)
	t.value = pattern.sub(r'\2', t.value).strip()
	t.value = ' '.join(t.value.split())
	return t


def t_MOV2(t):
   # <td class="celebrity-filmography__title"> <span>Morena</span>
	r'(<td\ class="celebrity-filmography__title">[\s]+<span>)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \( \) \; \& \, \' \! \? \- \! ]+)'
	regex = r'(<td\ class="celebrity-filmography__title">[\s]+<span>)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \( \) \; \& \, \' \! \? \- \! ]+)'
	pattern = re.compile(regex)
	t.value = pattern.sub(r'\2', t.value).strip()
	t.value = ' '.join(t.value.split())
	return t


def t_MOVYEAR(t):
	# <td class="celebrity-filmography__year">2018</td>
	r'(<td\ class="celebrity-filmography__year">)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	regex = r'(<td\ class="celebrity-filmography__year">)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
	pattern = re.compile(regex)
	t.value = pattern.sub(r'\2', t.value).strip()
	t.value = ' '.join(t.value.split())
	return t


# Define a rule so we can track line numbers
def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)


def t_error(t):
	t.lexer.skip(1)


lexer = lex.lex()


'''
-------------------------------------------------------------
YACC
-------------------------------------------------------------
'''


start = 'entry'


def p_empty(p):
	'empty :'
	pass


def p_mov(p):
	'''
	mov : MOV MOVYEAR
			| MOV2 MOVYEAR
			| MOV MOVYEAR mov
			| MOV2 MOVYEAR mov
			| empty

	'''
	global curr_list
	if len(p) == 4:
		curr_list.append([str(p[1]), str(p[2])])


def p_entry(p):
	"""
	entry : RF RF BIRTH mov
	"""
	global hrf
	global lrf
	global birthday
	hrf = p[1]
	lrf = p[2]
	birthday = p[3]


def p_error(p):
	print("Syntax error: ", p)


parser = yacc.yacc()


'''
-------------------------------------------------------------
DONE PARSING
-------------------------------------------------------------
'''


celeb_fields = ["Highest Rated film", "Lowest Rated film",
				"Birthday", "His/Her other movies"]


while True:

	hrf = ""
	lrf = ""
	curr_list = []
	birthday = ""

	celebs = []
	listOfFiles = os.listdir('.')
	pattern = "*.html"
	for file in listOfFiles:
		if fnmatch.fnmatch(file, pattern):
			celebs.append(file)

	if(len(sys.argv)) == 1:
		print("===============================================================")
		print("\n>> Enter celebrity of choice from below OR Enter -1 to Exit.")

		for i, mov in enumerate(celebs):
			print(i+1, ".\t"+mov[:-5])

		key = input("Enter any number from above: ")
		try:
			key = int(key)
		except ValueError:
			print("\tThat's not an int!")
			continue

		if(key == -1):
			break

		if key > len(celebs) or key < 1:
			print("\tEnter any number from above!")
			continue

		celeb_html = celebs[key-1]
	else:
		key = input("Enter 1 to continue OR -1 to exit: ")
		try:
			key = int(key)
		except ValueError:
			print("\tThat's not an int!")
			continue

		if(key == -1):
			break
		celeb_html = sys.argv[1]

	celeb_name = celeb_html[:-5].title().replace("_", " ")

	print(">> Selected celeb: ", celeb_name)

	file = open(celeb_html, 'r')
	data_f = file.read().replace('\n', '')
	file.close()

	print("\t\t==== LEX YACC INITIATED ====")

	lexer.input(data_f)

	while True:
		tok = lexer.token()
		if not tok:
			break
		# print(tok)

	parser.parse(data_f)

	while True:
		print("Enter your choice OR Enter -1 to go back")

		for i, mov_f in enumerate(celeb_fields):
			print(i+1, ".\t"+mov_f)

		key = input("Enter any number from above: ")
		try:
			key = int(key)
		except ValueError:
			print("\tThat's not an int!")
			continue

		if(key == -1):
			break

		if key > len(celeb_fields) or key < 1:
			print("\tEnter any number from above!")
			continue
		else:
			print("-------------")
			if key == 1:
				print("Highest Rated film: ", hrf)
			elif key == 2:
				print("Lowest Rated film: ", lrf)
			elif key == 3:
				print("Birthday: ", birthday)
			elif key == 4:
				year = input("\tEnter year: ")
				try:
					year = int(year)
				except ValueError:
					print("\tThat's not an int!")
					continue

				if year > 2021 or year <= 1600:
					print("\tEnter any number between 1600 and 2021!")
					continue
				for curr in curr_list:
					try:
						curr[1] = int(curr[1])
					except ValueError:
						curr[1] = -1
					if curr[1] >= year:
						print("\t\t", curr[0] + " - ", curr[1])

			print("-------------")

print("\t\tThank You!")
print("===============================================================")
