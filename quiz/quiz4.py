# COMP9021 24T1
# Quiz 4 *** Due Thursday Week 7 @ 9.00pm
#        *** Late penalty 5% per day
#        *** Not accepted after Sunday Week 7 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Implements a function that, based on the encoding of
# a single strictly positive integer that in base 2
# reads as b_1 ... b_n, as b_1b_1 ... b_nb_n, encodes
# a sequence of strictly positive integers N_1 ... N_k
# with k >= 1 as N_1* 0 ... 0 N_k* where for all 0 < i <= k,
# N_i* is the encoding of N_i.
#
# Implements a function to decode a strictly positive integer N
# into a sequence of (one or more) strictly positive
# integers according to the previous encoding scheme,
# or return None in case N does not encode such a sequence.


import sys
def helper(number):
    return bin(number)[2:]

def encode(list_of_integers):
    n = len(list_of_integers) - 1
    for i in range(len(list_of_integers)):
        list_of_integers[i] = helper(list_of_integers[i])
        
    l1 = []
    for i in range(len(list_of_integers)):
        for j in range(len(list_of_integers[i])):
            l1.append(str(list_of_integers[i][j]))
            l1.append(str(list_of_integers[i][j]))
        if n:
            l1.append(",")
            n -= 1
    
    result = ""
    for i in range(len(l1)):
        if l1[i] == ",":
            result += "0"
        else:
            result += l1[i]

    return int(result,2)


def decode(integer):
    
    integer = bin(integer)[2:]

    if len(integer) == 1:
        return None

    l1 = []
    i = 0
    while i < len(integer):
        if integer[i] != integer [i + 1]:
            if integer[i] == "0":
                i += 1
                l1.append(",")
            else:
                return None
        else:
            l1.append(integer[i])
            i += 2
        
    temp = ""
    result = []
    for i in range(len(l1)):
        if l1[i] == ",":
            result.append(int(temp,2))
            temp = ""
        else:
            temp += l1[i]

    result.append(int(temp,2))

    return result


# We assume that user input is valid. No need to check
# for validity, nor to take action in case it is invalid.
print('Input either a strictly positive integer')
the_input = eval(input('or a nonempty list of strictly positive integers: '))
if type(the_input) is int:
    print('  In base 2,', the_input, 'reads as', bin(the_input)[2 :])
    decoding = decode(the_input)
    if decoding is None:
        print('Incorrect encoding!')
    else:
        print('  It encodes: ', decode(the_input))
else:
    print('  In base 2,', the_input, 'reads as',
          f'[{", ".join(bin(e)[2: ] for e in the_input)}]'
         )
    print('  It is encoded by', encode(the_input))