
defult_roman = {"M": 1000, "CM": 900, "D": 500, "CD": 400, "C": 100, "XC": 90, "L": 50, "XL": 40,
                 "X": 10, "IX": 9, "V": 5, "IV": 4, "I": 1}
import time
def please_convert():
    request = input('How can I help you? ').split(" ")
    time.sleep(0.1)
    if len(request) < 2 or (request[0] != "Please" or request[1] != "convert"):
        print("I don't get what you want, sorry mate!")
    
    elif len(request) == 3:
        if request[2].isdigit():
            if 0 < int(request[2]) <= 3999 and not request[2].startswith("0"):
                print(f"Sure! It is {convert(int(request[2]), defult_roman)}")
            else:
                print("Hey, ask me something that's not impossible to do!")

        elif request[2].isalpha() and valid_word(request[2], defult_roman):
            if convert(request[2], defult_roman):
                print(f"Sure! It is {convert(request[2], defult_roman)}")
            else:
                print("Hey, ask me something that's not impossible to do!")
        else:
            print("Hey, ask me something that's not impossible to do!")

    elif len(request) == 5 and request[3] == "using":
        if request[2].isdigit() and request[4].isalpha():
            if int(request[2]) > 0:
                print(f"Sure! It is {convert(int(request[2]), generate_dict(request[4]))}")
            else:
                print("I don't get what you want, sorry mate!")

        elif request[2].isalpha() and request[4].isalpha():
            if all(char in request[4] for char in request[2]):
                if valid_word(request[2], generate_dict(request[4])):
                    print(f"Sure! It is {convert(request[2], generate_dict(request[4]))}")
                else:
                    print("Hey, ask me something that's not impossible to do!")
            else:
                print("Hey, ask me something that's not impossible to do!")
        else:
            print("Hey, ask me something that's not impossible to do!")
    
    elif len(request) == 4 and request[3] == "minimally":
        if request[2].isalpha():
            x = test(request[2])
            if x:
                print(f"Sure! It is {x[0]} using {x[1]}")
            else:
                print("Hey, ask me something that's not impossible to do!")
        else:
            print("Hey, ask me something that's not impossible to do!")
    else:
        print("I don't get what you want, sorry mate!")


def test(words):
    d = nodup(words)
    poses = perm(d)
    record = {}
    for pos in poses:
        if valid_word(words, generate_dict(pos)) and convert(words,generate_dict(pos)):
            record[pos] = convert(words,generate_dict(pos))
    
    if record:
        x = min(record, key=record.get)
        return record[x], x
    
    d = d +"_"
    poses = perm(d)
    for pos in poses:
        if valid_word(words, generate_dict(pos)) and convert(words,generate_dict(pos)):
            return convert(words,generate_dict(pos)), pos
    
    d = d +"+"
    poses = perm(d)
    for pos in poses:
        if valid_word(words, generate_dict(pos)) and convert(words,generate_dict(pos)):
            return convert(words,generate_dict(pos)), pos.replace("+","_")

    d = d +"&"
    poses = perm(d)
    for pos in poses:
        if valid_word(words, generate_dict(pos)) and convert(words,generate_dict(pos)):
            return convert(words,generate_dict(pos)), pos.replace("&","_").replace("+","_")
    
    return False

from itertools import permutations
def perm(string):
    return [''.join(perm) for perm in permutations(string)]

def nodup(words):
    role = [word for word in words]
    seen = []
    for word in role:
        if word not in seen:
            seen.append(word)
    new_words = "".join(seen)
    return new_words

def valid_word(words, ref_dict):

    if ref_dict == {}:
        return False
    
    for word in words:
        if word not in ref_dict:
            return False

    prev_word = ''
    rep_count = 0
    for word in words:
        if word == prev_word:
            rep_count += 1
            if rep_count > 3:
                return False
        else:
            rep_count = 1
        prev_word = word

    for i in range(len(words) - 2): ##invalid IXI,...
        if ref_dict[words[i]] < ref_dict[words[i + 1]] and ref_dict[words[i]] == ref_dict[words[i + 2]]:
            return False
    
    for i in range(len(words) - 1): ##invalid VV,LL...
        if ref_dict[words[i]] + ref_dict[words[i]] == ref_dict[words[i + 1]]:
            return False
        if i < len(words) - 2:
            try:
                if ref_dict[words[i]] < ref_dict[words[i+1]+words[i+2]]:
                    return False
            except KeyError:
                pass
        if words[i] == words[i + 1]:
            j = ref_dict[words[i]]
            while j:
                if j%10 == 5:
                    return False
                else:
                    j = j//10
    
    prev = ""
    for i in range(len(words) - 1):
        if prev == words[i]:
            rep = 1
        else:
            prev = words[i]
            rep = 0
        
        if ref_dict[words[i]] < ref_dict[words[i + 1]]:
            if i < len(words) - 2:
                if ref_dict[words[i + 1]] == ref_dict[words[i + 2]]:
                    return False
            if 0.5*ref_dict[words[i+1]] <= ref_dict[words[i + 1]] - ref_dict[words[i]] <= 0.9 * ref_dict[words[i+1]] and rep != 1:
                return True
            else:
                return False
    return True

def convert(words, ref_dict):
    if type(words) == int:
        result = ""
        arabic = [value for value in ref_dict.values()]
        roman = [key for key in ref_dict.keys()]
        i = 0
        while words > 0:
            for _ in range(words // arabic[i]):
                result += roman[i]
                words -= arabic[i]
            i += 1
        return result
    else:
        number = 0
        prev = float('inf')
        nine = 0
        while len(words) > 0:
            for key, value in ref_dict.items():
                if words.startswith(key):
                    if str(value).startswith("9"):
                        nine = value
                    if value > prev:
                        return 0
                    if value == 0.8*prev:
                        return 0
                    if str(value).startswith("1") and str(nine+value).startswith("1") and nine:
                        return 0
                    number += value
                    prev = value
                    words = words[len(key):]
                    break
        return number

def generate_dict(words):
    
    role = [word for word in words]
    if len(role) != len(set(role)):
        return {}

    convert_d = {}
    i = 1
    j = 1
    b1 = 1
    b2 = 1
    for e in reversed(list(words)):
        if i % 2 == 1:
            if i > 2:
                convert_d[words[2 - i] + words[-i]] = 9 * b2
                b2 *= 10
            convert_d[e] = j
            i += 1
            k = j * 5
        elif i % 2 == 0:
            convert_d[words[1 - i] + words[-i]] = 4 * b1
            convert_d[e] = k
            b1 *= 10
            j = k * 2
            i += 1
    convert_d = dict(reversed(list(convert_d.items())))
    return convert_d

    
please_convert()