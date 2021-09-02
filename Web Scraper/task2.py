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

# manually create the directory
dir = 'celeb'
if not os.path.exists(dir):
    os.makedirs(dir)

'''
-------------------------------------------------------------
LEX
-------------------------------------------------------------
'''
tokens = ('RECOMDLINK', 'RECOMD', 'W2W', 'STORY', 'GENRE', 'LANG', 'DIRECTOR',
          'PRODUCER', 'WRITER', 'BOXOFF', 'RUNTIME', 'CAST', 'CASTLINK')


t_ignore = '\t\n'


def t_CASTLINK(t):
    # <a href="/celebrity/anthony_gonzalez_4" data-qa="cast-crew-item-img-link">
    r'(<a\ href=")([a-zA-Z0-9 \- \_ \/]+)"\ data-qa="cast-crew-item-img-link">'
    regex = r'(<a\ href=")([a-zA-Z0-9 \- \_ \/]+)"\ data-qa="cast-crew-item-img-link">'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_RECOMDLINK(t):  # Recommended movies link
    # <a href="/m/interstellar_2014" class="recommendations-panel__poster-link">
    r'(<a\ href=")([a-zA-Z0-9 \- \_ \/]+)("\ class="recommendations-panel__poster-link">)'
    regex = r'(<a\ href=")([a-zA-Z0-9 \- \_ \/]+)("\ class="recommendations-panel__poster-link">)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_RECOMD(t):  # Recommended movies
    # <span slot="title" class="recommendations-panel__poster-title">Interstellar</span>
    r'<span\ slot="title"\ class="recommendations-panel__poster-title">([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'
    regex = r'<span\ slot="title"\ class="recommendations-panel__poster-title">([a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\1', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


def t_W2W(t):  # where to watch
    # data-affiliate="fandango-now"
    r'(data-affiliate=")([a-zA-Z0-9 \-]+)'
    regex = r'(data-affiliate=")([a-zA-Z0-9 \-]+)'

    # store only the relevant info
    pattern = re.compile(regex)
    t.value = pattern.sub(r'\2', t.value).strip()
    t.value = ' '.join(t.value.split())
    return t


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
    r'(data-qa="movie-info-director">)([a-zA-Z0-9 \.]+)'
    regex = r'(data-qa="movie-info-director">)([a-zA-Z0-9 \.]+)'

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


def p_recomd(p):
    '''
    recomd : RECOMDLINK RECOMD
            | RECOMDLINK RECOMD recomd
            | empty

    '''
    global curr_recomd
    if len(p) == 4:
        curr_recomd.append([str(p[2]), str(p[1])])


def p_w2w(p):
    '''
    w2w : W2W
        | W2W w2w
        | empty

    '''
    global curr_w2w
    if len(p) == 2 and p[1] is not None:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    curr_w2w = str(p[0]).replace("None", "")


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
              | PRODUCER CASTLINK producer
              | empty
    '''
    global curr_prod
    if len(p) == 2 and p[1] is not None:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    if len(p) == 4:
        p[0] = str(p[1]) + ", " + str(p[3])
    curr_prod = str(p[0]).replace("None", "")


def p_writer(p):
    '''
    writer : WRITER
           | WRITER writer
           | WRITER CASTLINK writer
           | empty

    '''
    global curr_writer
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + ", " + str(p[2])
    if len(p) == 4:
        p[0] = str(p[1]) + ", " + str(p[3])
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
             | CASTLINK
             | CAST cast
             | CASTLINK cast
             | empty

    '''
    if len(p) == 2:
        p[0] = p[1]
    if len(p) == 3:
        p[0] = str(p[1]) + " | " + str(p[2])


def p_entry(p):
    """
    entry : recomd w2w story genre lang direc boxoff runtime cast writer cast producer cast
    """


def p_error(p):
    print("Syntax error: ", p)


parser = yacc.yacc()


'''
-------------------------------------------------------------
DONE PARSING
-------------------------------------------------------------
'''


mov_fields = ["Movie Name", 'Director', 'Writers', 'Producer', 'Original Language',
              'Cast with the character name', 'Storyline', 'Box Office Collection', 'Runtime', "Where to Watch", "You Might Also Like"]


def celeb_info(ccast):
    for i, k in enumerate(ccast):
        print(i+1, ".\t" + k.title().replace("_", " "))
    key = input("Enter any number from above: ")
    try:
        key = int(key)
    except ValueError:
        print("\tThat's not an int!")
        recommd()

    if(key == -1):
        return

    if key > len(ccast) or key < 1:
        print("\tEnter any number from above!")
        celeb_info(ccast)

    url = "https://www.rottentomatoes.com" + "/celebrity/" + ccast[key-1]
    print("\tFetching page : " + url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f_name = ccast[key-1] + ".html"  # generate a name of the string
    f = open("./celeb/"+f_name, 'wb')
    f.write(webContent)
    f.close()

    print("---- *** ----")
    # print(f_name)
    os.system('python3 getceleb.py {}'.format(f_name))


def recommd():  # YOU MIGHT ALSO LIKE processing
    for i, k in enumerate(curr_recomd):
        print(i+1, ".\t" + k[0])
    key = input("Enter any number from above: ")
    try:
        key = int(key)
    except ValueError:
        print("\tThat's not an int!")
        recommd()

    if(key == -1):
        return

    if key > len(curr_recomd) or key < 1:
        print("\tEnter any number from above!")
        recommd()

    url = "https://www.rottentomatoes.com" + curr_recomd[key-1][1]
    print("\tFetching page : " + url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f_name = curr_recomd[key-1][1] + ".html"  # generate a name of the string
    f_name = f_name.replace("/m/", "")
    f = open(f_name, 'wb')
    f.write(webContent)
    f.close()

    print("---- *** ----")
    os.system('python3 task2.py {}'.format(f_name))


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
    curr_w2w = ""
    curr_recomd = []
    ccast = []

    movies = []
    listOfFiles = os.listdir('.')
    pattern = "*.html"
    for file in listOfFiles:
        if fnmatch.fnmatch(file, pattern):
            movies.append(file)

    if(len(sys.argv)) == 1:
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
        # key = 1

        movie_html = movies[key-1]
    else:
        key = input("Enter 1 to continue OR -1 to exit: ")
        try:
            key = int(key)
        except ValueError:
            print("\tThat's not an int!")
            continue

        if(key == -1):
            break
        movie_html = sys.argv[1]

    mov_name = movie_html[:-5].title().replace("_", " ")

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
        # print(tok)
        if(tok.type == 'CAST'):
            curr_cast += str(tok.value) + ' | '
        if(tok.type == 'WRITER' or tok.type == 'PRODUCER'):
            curr_cast += str(tok.value) + ' (' + str(tok.type) + ')' + " | "
        if(tok.type == 'CASTLINK'):
            ccast.append(str(tok.value).replace("/celebrity/", ""))

    parser.parse(data_f)

    while True:
        print("Current Movie: ", mov_name)
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
            print("-------------")
            if key == 1:
                print("Movie Name: ", mov_name)
            elif key == 2:
                print("Directors: ", curr_director)
            elif key == 3:
                print("Writers: ", curr_writer)
            elif key == 4:
                print("Producers: ", curr_prod)
            elif key == 5:
                print("Language: ", curr_lang)
            elif key == 6:
                print("Cast & Crew: ", curr_cast)
                celeb_info(ccast)
            elif key == 7:
                print("Story: ", curr_story)
            elif key == 8:
                print("Box Office: ", curr_boxoff)
            elif key == 9:
                print("Runtime: ", curr_runtime)
            elif key == 10:
                print("Where To Watch: ", curr_w2w)
            elif key == 11:
                print("You Might Also Like: ")
                recommd()

            print("-------------")

print("\t\tThank You!")
print("===============================================================")
