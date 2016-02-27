
from epub_handler import get_soups_from_ebook
import os

def generate_word_probability_by_character(bookname, title_tag, attrs=None):
    os.chdir('books')
    char_dict = {}
    soups = get_soups_from_ebook(bookname)
    for soup in soups:
        if attrs:
            title = soup.find(title_tag, attrs=attrs)
        else:
            title = soup.find(title_tag)
        if title and title.text.lower() != 'contents':
            character = title.text.lower()
            chapter_text = soup.find('body').text.strip()[len(character):]
            if character not in char_dict:
                char_dict[character] = [chapter_text]
            else:
                char_dict[character].append(chapter_text)
            if character == 'epilogue':
                break
    os.chdir('..')
    if '' in char_dict:
        del char_dict['']
    print(sorted(char_dict.keys()))
    for char in char_dict.keys():
        s = ''
        try:
            with open('characters/{}'.format(char)) as f:
                s = f.read()
        except:
            pass
        with open('characters/{}'.format(char), 'w') as f:
            f.write(s)
            for chapter in char_dict[char]:
                f.write(chapter.strip() + '\n\n')
    #need to update 0_index
    return char_dict.keys()
