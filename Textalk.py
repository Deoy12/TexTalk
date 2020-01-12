from word2number import w2n
from recorder import calculate
import csv
words_numeric = set()
words_substituted = {}

# Load in data from txt files
with open('./data/numeric_words.csv', 'r') as file:
    for row in csv.reader(file):
        words_numeric.add(row[0])

with open('./data/substituted_words.csv', 'r') as file:
    for row in csv.reader(file):
        if len(row) == 2:
            words_substituted[row[0]] = row[1]

def parsestr(s):
    return convert(s)

def convert(s):
    return convert_to_proto(s)
    '''convert_fractions(convert_to_proto(s))'''

'''def convert_fractions(s):
    def get_subformula(index, direction):
        counter = 0
        while True:
            if s[index] == '(':
                if direction > 0: counter += 1
                else: counter -= 1
            elif s[index] == ')':
                if direction > 0: counter -= 1
                else: counter += 1
            if counter == 0: return index if direction < 0 else index + 1
            index += direction

    while '/' in s:
        index = s.find('/')
        start_index, end_index = get_subformula(index-1, -1), get_subformula(index+1, 1)
        # print(index, start_index, end_index)
        s = s[:start_index] + '\\frac{' + s[start_index:index] + '}{' + s[index+1:end_index] + '}' + s[end_index:]
    while 'integral' in s:
        index = s.find('integral')
        end_index = get_subformula(index+len('integral'), 1)
        s = s[:index] + '\\int{' + s[index+len('integral'):end_index] + '}' + s[end_index:]
    while 'root' in s:
        index = s.find('root')
        end_index = get_subformula(index+len('root'), 1)
        s = s[:index] + '\\sqrt{' + s[index+len('root'):end_index] + '}' + s[end_index:]
    while 'log' in s:
        index = s.find('log')
        end_index = get_subformula(index+len('log'), 1)
        s = s[:index] + '\\ln{' + s[index+len('log'):end_index] + '}' + s[end_index:]
    return s
    '''

def convert_to_proto(s):
    return quantity(parsestr_numeric(parsestr_substitute(s))).replace(' ', '')

def parsestr_numeric(s):
    words = s.split()
    if len(words) == 0: return ''
    i = 0
    while i < len(words) and words[i] in words_numeric:
        i = i + 1
    if i == 0:
        return words[0] + ' ' + parsestr_numeric(' '.join(words[1:]))
    s = str(w2n.word_to_num(' '.join(words[:i]))) + ' ' + parsestr_numeric(' '.join(words[i:]))
    return s

def parsestr_substitute(s):
    for phrase in sorted(words_substituted.keys(), key=lambda k: -(len(k.split()) * 10 + (len(k) == 1 and len(k[0])))):
        # print(phrase, phrase in s)
        s = s.replace(phrase, words_substituted[phrase])
    return s

# Returns a lst of indices containing <quantity and all>
def quantity(s):
    lst = []
    while 'the quantity of' in s and 'all' in s:

        # Remember to add index by 1 more for end index because second l in all will not be included \
        # in range() if not inclusive
        start_index, end_index = s.find('the quantity of'), s.find('all')
        s = s[:start_index] + '(' + convert(s[start_index+len('the quantity of'):end_index].strip()) + ')' + s[end_index+len('all'):]
    while 'the quantity of' in s:
        start_index = s.find('the quantity of')
        s = s[:start_index] + '(' + convert(s[start_index+len('the quantity of'):].strip()) + ')'
    while 'all' in s:
        end_index = s.find('all')
        s = '(' + convert(s[:end_index]) + ')' + s[end_index+len('all'):]
    return s
