''' Speech Corrections '''


def move_articles_to_end(string):
    '''moves articles such to the end of the string,
    separated by a comma, changes case to title'''
    # change the case of title to Title case
    string = string.title()
    # remove redundant words at start
    unwanted = ['The ', 'A ', 'An ']
    for word in unwanted:
        if string.startswith(word):
            string = string[len(word):] + ', ' + word
            break
    return string
