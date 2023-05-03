import numpy as np
import os

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('\n\n', '\n').replace('\n', ' ')
    return text


def get_file_path():
    file_path = input("Please enter the file path or file name: ")
    if not os.path.isabs(file_path):
        file_path = os.path.join(os.getcwd(), file_path)
    return file_path

file_path = get_file_path()

while not os.path.isfile(file_path):
    print("File not found. Please try again.")
    file_path = get_file_path()

oz_txt = load_text(file_path)

oz_art_lst = oz_txt.split('\n\n')
oz_art_lst = [art.split('\n\t') for art in oz_art_lst]
oz_art_lst = [[s.replace('\n', ' ') for s in art] for art in oz_art_lst]

oz_dict = {}
for art in oz_art_lst:
    if art[0] not in oz_dict:
        oz_dict[art[0]] = [art[1:]]
    else:
        if len(art[1]) > 5 and art[1][:5] == 'E.g. ':
            oz_dict[art[0]][-1] += art[1:]
        else:
            oz_dict[art[0]] += [art[1:]]

text = ''
for w in oz_dict:
    for v in oz_dict[w]:
        text += ' '.join(v) + ' '

text = text.replace('E.g.', ' ')
text = text.replace('(', '')
text = text.replace(')', '')
text = text.lower()

text_lst = list(text)

chars, cntrs = np.unique(text_lst, return_counts=True)
chrs_dct = {c: n for c, n in zip(chars, cntrs)}
comb_dct_srtd = {c: n for c, n in sorted(chrs_dct.items(), key=lambda item: item[1], reverse=True)}

C = sum(cntrs)
comb_dct_P = {c: n/C for c, n in chrs_dct.items()}
comb_dct_P_srtd = {c: p for c, p in sorted(comb_dct_P.items(), key=lambda item: item[1], reverse=True)}

print('------------------------------------------')
for c in comb_dct_P:
    print(c, "{:7.6f}".format(comb_dct_P[c]))

print('------------------------------------------')
for c in comb_dct_P_srtd:
    print(c, "{:7.6f}".format(comb_dct_P[c]))

words_lst = text.split()
words_lst = [w.strip(',[]():<>=!;-') for w in words_lst]

words, wcntrs = np.unique(words_lst, return_counts=True)
words_dct = {w: n for w, n in zip(words, wcntrs)}
words_dct_srtd = {w: n for w, n in sorted(words_dct.items(), key=lambda item: item[1], reverse=True)}
