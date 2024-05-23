
import sys
def is_valid(word, arity):
    if arity:
        if '(' in word and ')' in word:
            return check(word, arity)
        else:
            return False
    else:
        return check(word, arity)

def check(word, arity):
    n = arity
    left = 0
    mark = 0
    if arity:
        for i in range(len(word)):
            if word[i] == "(":
                left = i
            if word[i] == ")":
                for j in range(left, i):
                    if word[j] == ",":
                        mark = j
                        n -= 1
                for j in range(i, len(word)):
                    if word[j] == "(" or word[j] == ")":
                        break
                    if word[j] == ",":
                        n -= 1
                word = word.replace("_", "a")
                if n == 1:
                    if mark and any(char.isalpha() for char in word[left+1:i]) and any(char.isalpha() for char in word[mark:j]) and any(char.isalpha() for char in word[left+1: mark]):
                        return check(word[:left]+word[i+1:], arity)
                    elif mark == 0 and any(char.isalpha() for char in word[left+1:i]):
                        return check(word[:left]+word[i+1:], arity)
                    else:
                        return False
                else:
                    return False

    word = word.replace("_", "a").strip()
    if word.isalpha():
        return True
    else:
        return False

try:
    arity = int(input('Input an arity : '))
    if arity < 0:
        raise ValueError
except ValueError:
    print('Incorrect arity, giving up...')
    sys.exit()
word = input('Input a word: ')
if is_valid(word, arity):
    print('The word is valid.')
else:
    print('The word is invalid.')
