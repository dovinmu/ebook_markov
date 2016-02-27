import random
import nltk

def to_corpus(raw):
    tokens = nltk.word_tokenize(raw)
    return nltk.Text(tokens)

def to_conditional_frequency_dist(text):
    bigrams = nltk.bigrams(text)
    return nltk.ConditionalFreqDist(bigrams)

def load_CFD(fname):
    '''Load the precomputed conditional frequency distribution, or compute from the raw text of the given filename.'''
    try:
        with open(fname + '_cfd.pkl', 'rb') as inp:
            cfd = pickle.load(inp)
    except:
        with open(fname) as f:
            corpus = to_corpus(f.read())
            cfd = to_conditional_frequency_dist(corpus)
        with open(fname + '_cfd.pkl', 'wb') as out:
            pickle.dump(cfd, out, pickle.HIGHEST_PROTOCOL)
    return cfd

def generate_words(cfdist, word, num=30):
    for i in range(num):
        print(word, end=" ")
        total_prob = 0
        word = next_word(cfdist, word)

def next_word(counter):
#    items = sorted(counter.items(), reverse=True, key=lambda x: x[1])
#    total_prob = items[0][1] * 30
    total_prob = 10000
    overturn_count = 0
    while True:
        items = list(counter.items())
        if len(items) == 0:
            return '.'
        for key, value in items:
            if random.randint(0, total_prob) < value:
                return key
        if overturn_count > 2:
            i = random.randint(0, len(items)-1)
            return items[i][0]
        overturn_count += 1

def generate_sentence(cfdist):
    word = next_word(cfdist['.'])
    if word in ['.']:
        word = next_word(cfdist['.'])
    word = word.capitalize()
    s = ''
    while word != '.':
        if word in [',', '”', ';', '?', '!']:
            s = s.strip() + word + ' '
        else:
            s += word + ' '
        word = next_word(cfdist[word])
    s = (s.strip() + '. ')
    return s

def generate_paragraph(cfdist):
    s = '   '
    for i in range(random.randint(2,5)):
        s += (generate_sentence(cfdist))
    print(s)

def load_character_filenames():
    #return [fname for fname in os.listdir('characters')]
    if not '0_index' in os.listdir():
        os.chdir('characters')
    with open('0_index') as f:
        return f.read().strip().split(',')

def generate_book():
    char_files = load_character_filenames()
    char_files = random.sample(char_files, 5)
    char = 'prologue'
    for i in range(10):
        cfd = load_CFD('{}'.format(char))
        print('\t' + char.upper() + '\n')
        generate_paragraph(cfd)
        print('\n\n')
        prev_char = char
        char = char_files[random.randint(0, len(char_files))-1]
        while char in ['prologue', prev_char, 'epilogue']:
            char = char_files[random.randint(0, len(char_files))-1]
    if random.randint(0,2) == 1:
        cfd = load_CFD('epilogue')
        print('\t' + char.upper() + '\n')
        generate_paragraph(cfd)
        print('\n\n')
