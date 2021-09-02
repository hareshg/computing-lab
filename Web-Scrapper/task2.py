'''
*   Haresh Gaikwad | 20CS60R09
*   Computing Lab II
*   Assignment 8

'''
import ply.lex as lex
import ply.yacc as yacc
import os
import fnmatch
import re
import warnings
warnings.filterwarnings("ignore")

'''
-------------------------------------------------------------
LEX
-------------------------------------------------------------
'''
tokens = ('STORY', 'GENRE', 'LANG', 'DIRECTOR',
          'PRODUCER', 'WRITER', 'BOXOFF', 'RUNTIME', 'CAST')


t_ignore = '\t\n'


def t_STORY(t):
    # <div id="movieSynopsis" class="movie_synopsis clamp clamp-6 js-clamp" style="clear:both" data-qa="movie-info-synopsis">
    r'(<div\ id="movieSynopsis"\ class="movie_synopsis\ clamp\ clamp-6\ js-clamp"\ style="clear:both"\ data-qa="movie-info-synopsis">[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
    regex = r'(<div\ id="movieSynopsis"\ class="movie_synopsis\ clamp\ clamp-6\ js-clamp"\ style="clear:both"\ data-qa="movie-info-synopsis">[\s]+)([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_GENRE(t):
    # <div class="meta-value genre" data-qa="movie-info-item-value"> adventure, action, fantasy</div>
    r'(<div\ class="meta-value\ genre"\ data-qa="movie-info-item-value">)([a-zA-Z0-9 \, . ]+)(</div>)'
    regex = r'(<div\ class="meta-value\ genre"\ data-qa="movie-info-item-value">)([a-zA-Z0-9 \, . ]+)(</div>)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_LANG(t):
 #  <div class="meta-label subtle" data-qa="movie-info-item-label">Original Language:</div>
    #                    <div class="meta-value" data-qa="movie-info-item-value">English
    r'(Original\ Language:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">)([a-zA-Z0-9á-źÁ-Ź \, . ]+)'
    regex = r'(Original\ Language:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">)([a-zA-Z0-9á-źÁ-Ź \, . ]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


# tokenize the name of the director
def t_DIRECTOR(t):
    # <a href="/celebrity/peter_lord" data-qa="movie-info-director">Peter Lord</a>,
    r'(data-qa="movie-info-director">)([a-zA-Z0-9 ]+)'
    regex = r'(data-qa="movie-info-director">)([a-zA-Z0-9 ]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_PRODUCER(t):
    # <span class="characters subtle smaller" title="Chris Parker">  <br/>  Producer </span>
    r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \, . ]+)(">[\s]+<br/>[\s]+Producer[\s]+</span>)'
    regex = r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \, . ]+)(">[\s]+<br/>[\s]+Producer[\s]+</span>)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_WRITER(t):
    # <span class="characters subtle smaller" title="Chris Parker">  <br/>  Screenwriter </span>
    r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \, . ]+)(">[\s]+<br/>[\s]+Screenwriter[\s]+</span>)'
    regex = r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \, . ]+)(">[\s]+<br/>[\s]+Screenwriter[\s]+</span>)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_BOXOFF(t):
    #  <div class="meta-label subtle" data-qa="movie-info-item-label">Box Office (Gross USA):</div>
    # <div class="meta-value" data-qa="movie-info-item-value">$700.2M</div>
    r'(Box\ Office\ \(Gross\ USA\):</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">)([\$0-9.0-9M]+)'
    regex = r'(Box\ Office\ \(Gross\ USA\):</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">)([\$0-9.0-9M]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_RUNTIME(t):
    # <div class="meta-label subtle" data-qa="movie-info-item-label">Runtime:</div>
    # <div class="meta-value" data-qa="movie-info-item-value">
    # <time datetime="P1h 30mM">
    #     1h 30m
    # </time>
    r'(Runtime:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">[\s]+<time\ datetime="[a-zA-Z0-9 ]+">[\s]+)([a-zA-Z0-9 ]+)'
    regex = r'(Runtime:</div>[\s]+<div\ class="meta-value"\ data-qa="movie-info-item-value">[\s]+<time\ datetime="[a-zA-Z0-9 ]+">[\s]+)([a-zA-Z0-9 ]+)'
    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_CAST(t):
    # <span class="characters subtle smaller" title="Rachel Morrison">
    # <br/>
    # Cinematographer
    # </span>
    r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)(">[\s]+<br/>[\s]+)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)'
    regex = r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)(">[\s]+<br/>[\s]+)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)'
    regex2 = r'(<span\ class="characters\ subtle\ smaller"\ title=")([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)(">[\s]+<br/>[\s]+)([a-zA-Z0-9á-źÁ-Ź \À \ç \. \: \# \; \& \, \' \! \? \- \! ]+)'
    # store only the relevant info
    pattern = re.compile(regex)
    pattern2 = re.compile(regex2)
    t.value = pattern.sub(r'\2', t.value).strip() + \
        " (" + pattern2.sub(r'\4', t.value).strip() + ")"
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


def p_story(p):
    '''
    story : STORY
          | empty

    '''
    global curr_story
    curr_story = str(p[1])


def p_genre(p):
    '''
    genre : GENRE
          | empty

    '''
    p[0] = p[1]
    global curr_genre
    curr_genre += str(p[0])


def p_lang(p):
    '''
    lang : LANG
         | empty

    '''
    global curr_lang
    curr_lang = str(p[1])


def p_direc(p):
    '''
    direc : DIRECTOR
          | DIRECTOR direc
          | empty
    '''
    global curr_director

    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    curr_director = str(p[0]).replace("None", "")


def p_producer(p):
    '''
    producer : PRODUCER
              | PRODUCER producer
              | empty
    '''
    global curr_prod
    if len(p) == 2 and p[1] is not None:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    curr_prod = str(p[0]).replace("None", "")


def p_writer(p):
    '''
    writer : WRITER
           | WRITER writer
           | empty

    '''
    global curr_writer
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    curr_writer = str(p[0]).replace("None", "")


def p_boxoff(p):
    '''
    boxoff : BOXOFF
           | empty

    '''
    global curr_boxoff
    curr_boxoff = str(p[1])


def p_runtime(p):
    '''
    runtime : RUNTIME
            | empty

    '''
    global curr_runtime
    curr_runtime = str(p[1])


def p_cast(p):
    '''
    cast : CAST
         | CAST cast
         | empty

    '''
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + " | " + str(p[2])


def p_entry(p):
    """
    entry : story genre lang direc boxoff runtime cast writer producer cast

    """


def p_error(p):
    print("Syntax error: ", p)


parser = yacc.yacc()


'''
-------------------------------------------------------------
DONE PARSING
-------------------------------------------------------------
'''
console = open("console.log", "w")
console.write("<Genre> <Movie_name> <Field_requested> <Field_value>\n")

mov_fields = ["Movie Name", 'Director', 'Writers', 'Producer', 'Original Language',
              'Cast with the character name', 'Storyline', 'Box Office Collection', 'Runtime']

while True:

    curr_genre = ""
    curr_director = ""
    curr_writer = ""
    curr_prod = ""
    curr_lang = ""
    curr_cast = ""
    curr_story = ""
    curr_boxoff = ""
    curr_runtime = ""

    movies = []
    listOfFiles = os.listdir('.')
    pattern = "*.html"
    for file in listOfFiles:
        if fnmatch.fnmatch(file, pattern):
            movies.append(file)

    print("===============================================================")
    print("\n>> Enter movie of choice from below OR Enter -1 to Exit.")

    for i, mov in enumerate(movies):
        print(i+1, ".\t"+mov[:-5])

    key = input("Enter any number from above: ")
    try:
        key = int(key)
    except ValueError:
        print("\tThat's not an int!")
        continue

    if(key == -1):
        break

    if key > len(movies) or key < 1:
        print("\tEnter any number from above!")
        continue

    movie_html = movies[key-1]
    mov_name = movie_html[:-5]
    print(">> Selected movie: ", mov_name)

    file = open(movie_html, 'r')
    data_f = file.read().replace('\n', '')
    file.close()

    print("\t\t==== LEX YACC INITIATED ====")

    lexer.input(data_f)

    while True:
        tok = lexer.token()
        if not tok:
            break
        if(tok.type == 'CAST'):
            curr_cast += str(tok.value) + ' | '
        if(tok.type == 'WRITER' or tok.type == 'PRODUCER'):
            curr_cast += str(tok.value) + ' (' + str(tok.type) + ')' + " | "

    parser.parse(data_f)

    while True:
        print("Enter your choice OR Enter -1 to go back")

        for i, mov_f in enumerate(mov_fields):
            print(i+1, ".\t"+mov_f)

        key = input("Enter any number from above: ")
        try:
            key = int(key)
        except ValueError:
            print("\tThat's not an int!")
            continue

        if(key == -1):
            break

        if key > len(mov_fields) or key < 1:
            print("\tEnter any number from above!")
            continue
        else:
            console.write(curr_genre + ' ~~ ' + mov_name +
                          ' ~~ ' + mov_fields[key-1] + ' ~~ ')
            print("-------------")
            if key == 1:
                print("Movie Name: ", mov_name)
                console.write(mov_name + '\n')
            elif key == 2:
                print("Directors: ", curr_director)
                console.write(curr_director + '\n')
            elif key == 3:
                print("Writers: ", curr_writer)
                console.write(curr_writer + '\n')
            elif key == 4:
                print("Producers: ", curr_prod)
                console.write(curr_prod + '\n')
            elif key == 5:
                print("Language: ", curr_lang)
                console.write(curr_lang + '\n')
            elif key == 6:
                print("Cast & Crew: ", curr_cast)
                console.write(curr_cast + '\n')
            elif key == 7:
                print("Story: ", curr_story)
                console.write(curr_story + '\n')
            elif key == 8:
                print("Box Office: ", curr_boxoff)
                console.write(curr_boxoff + '\n')
            elif key == 9:
                print("Runtime: ", curr_runtime)
                console.write(curr_runtime + '\n')
            print("-------------")

console.close()
print("\t\tThank You!")
print("===============================================================")