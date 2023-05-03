import numpy as np
import os

def load_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace('\n\n', ' ').replace('\n', ' ')
    return text

file_path = input("Please enter the file path or file name: ")

while not os.path.isfile(file_path):
    print("File not found. Please try again.")
    file_path = input("Please enter the file path or file name: ")

text = load_text(file_path)
text = text.lower()

# Character frequency analysis
chars, cntrs = np.unique(list(text), return_counts=True)
char_freq = {c: n for c, n in zip(chars, cntrs)}
char_freq_sorted = {c: n for c, n in sorted(char_freq.items(), key=lambda item: item[1], reverse=True)}

total_chars = sum(cntrs)
char_prob = {c: n/total_chars for c, n in char_freq.items()}
char_prob_sorted = {c: p for c, p in sorted(char_prob.items(), key=lambda item: item[1], reverse=True)}

print('------------------------------------------')
for c in char_prob:
    percentage = char_prob[c] * 100
    if c == '\t':
        print(f"\\t: {char_prob[c]:.6f} ~ {percentage:.2f}%")
    elif c == ' ':
        print(f"space: {char_prob[c]:.6f} ~ {percentage:.2f}%")
    else:
        print(f"{c}: {char_prob[c]:.6f} ~ {percentage:.2f}%")

print('------------------------------------------')
for c in char_prob_sorted:
    percentage = char_prob[c] * 100
    if c == '\t':
        print(f"\\t: {char_prob_sorted[c]:.6f} ~ {percentage:.2f}%")
    elif c == ' ':
        print(f"space: {char_prob_sorted[c]:.6f} ~ {percentage:.2f}%")
    else:
        print(f"{c}: {char_prob_sorted[c]:.6f} ~ {percentage:.2f}%")


# Word frequency analysis
words_lst = text.split()
words_lst = [w.strip(',[]():<>=!;-') for w in words_lst]

words, wcntrs = np.unique(words_lst, return_counts=True)
words_dct = {w: n for w, n in zip(words, wcntrs)}
words_dct_srtd = {w: n for w, n in sorted(words_dct.items(), key=lambda item: item[1], reverse=True)}

print('------------------------------------------')
print("Top 10 words:")
for i, (word, count) in enumerate(sorted(words_dct_srtd.items(), key=lambda x: x[1], reverse=True)[:10]):
    print(f"{i + 1}. {word}: {count}")
