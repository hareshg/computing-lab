'''
*	Haresh Gaikwad | 20CS60R09
*	Computing Lab II
*	Assignment 8

'''
import urllib.request
import os
import re


# manually create the directory
dir = 'data'
if not os.path.exists(dir):
    os.makedirs(dir)

mg_dict = {
    1: "action__adventure",
    2: "animation",
    3: "drama",
    4: "comedy",
    5: "mystery__suspense",
    6: "horror",
    7: "science_fiction__fantasy",
    8: "documentary",
    9: "romance",
    10: "classics"
}


def is_key_present(dict, _key):
    if _key in dict.keys():
        return True
    else:
        return False


while(True):
    print("===============================================================")
    print("\n>> Enter genre of choice from below OR Enter -1 to Exit.")
    print("1. Action & Adventure\n2. Animation\n3. Drama\n4. Comedy\n5. Mystery & Suspense\n6. Horror\n7. Sci-Fi\n8. Documentary\n9. Romance\n10. Classics")

    key = input("Enter any number from 1 to 10: ")

    try:
        key = int(key)
    except ValueError:
        print("\tThat's not an int!")
        continue

    if(key == -1):
        break

    if(not is_key_present(mg_dict, key)):
        print("\tEnter any number from 1 to 10!")
        continue

    genre = mg_dict[key]
    print(">> Selected genre: ", genre)
    os.chdir("./data")
    url = "https://www.rottentomatoes.com/top/bestofrt/top_100_" + \
        genre + "_movies/"
    print("\tFetching page : " + url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f_name = "top100_" + genre + ".html"  # generate a name of the string
    f = open(f_name, 'wb')
    f.write(webContent)
    f.close()
    print("\tDone!")

    file = open(f_name, 'r')
    data_f = file.read().replace('\n', '')
    file.close()

    # Sample Target: <a href="/m/1003707-casablanca" class="unstyled articleLink">        Casablanca (1942)</a>

    top100 = re.findall(
        r'class="unstyled articleLink">[a-zA-Z0-9á-źÁ-Ź, \À \/ \ç \. \: \& \, \' \( \) \! \? \- \! \"]+</a>', data_f)

    print(" ==== Top 100 " + genre + " Movies ===== ")

    for i, curr in enumerate(top100):

        top100[i] = top100[i].replace(r'class="unstyled articleLink">', "")
        top100[i] = top100[i].replace(r'</a>', "")
        top100[i] = top100[i].strip()
        if top100[i] == "View All":
            continue
        print(i+1, ".\t"+top100[i])

    top100.remove("View All")

    print("\n>> Enter Movies of choice from above OR Enter -1 to Exit.")
    mov_num = input("Enter any number from 1 to 100: ")

    try:
        mov_num = int(mov_num)
    except ValueError:
        print("That's not an int!")
        continue

    if(mov_num == -1):
        break

    if mov_num > 100 or mov_num < 1:
        print("\tEnter any number from 1 to 100!")
        continue

    movie = top100[mov_num-1]
    print("Selected Movie: ", movie)
    movie_name = movie

    # Text processing

    special = ['À', '/', 'ç', '.', ':', '&', ',',
               "'", '(', ')', '!', '?', '-', '!', '"']

    for i in special:
        movie = movie.replace(i, "\\"+i)

    mov_link = re.findall(
        r'<a\ href=.*' + movie, data_f)
    mov_link = mov_link[0][-200:].strip()

    start = mov_link.rfind("/m")
    end = mov_link.rfind("\" class=")
    mov_link = mov_link[start:end]

    # Save movie webpage
    os.chdir("..")

    url = "https://www.rottentomatoes.com" + mov_link
    print("\tFetching page : " + url)
    response = urllib.request.urlopen(url)
    webContent = response.read()
    f_name = movie_name + ".html"  # generate a name of the string
    f = open(f_name, 'wb')
    f.write(webContent)
    f.close()
    print("\tSuccessful!")


print("\t\tThank You!")
print("===============================================================")
