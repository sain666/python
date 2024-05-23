# COMP9021 24T1
# Quiz 2 *** Due Thursday Week 4 @ 9.00pm
#        *** Late penalty 5% per day
#        *** Not accepted after Sunday Week 4 @ 9.00pm

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# Reading the number written in base 8 from right to left,
# keeping the leading 0's, if any:
# 0: move N     1: move NE    2: move E     3: move SE
# 4: move S     5: move SW    6: move W     7: move NW
#
# We start from a position that is the unique position
# where the switch is on.
#
# Moving to a position switches on to off, off to on there.

import sys
import time
on = '\u26aa'
off = '\u26ab'
code = input('Enter a non-strictly negative integer: ').strip()
time.sleep(0.1)
try:
    if code[0] == '-':
        raise ValueError
    int(code)
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
nb_of_leading_zeroes = 0
for i in range(len(code) - 1):
    if code[i] == '0':
        nb_of_leading_zeroes += 1
    else:
        break
print("Keeping leading 0's, if any, in base 8,", code, 'reads as',
      '0' * nb_of_leading_zeroes + f'{int(code):o}.'
     )
print()

n  = '0' * nb_of_leading_zeroes + f"{int(code):o}"
operator = n
x = 0
y = 0

visited = []
visited.append([0,0])

while operator:
    if operator[-1] == "0":
        y += 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
        
    elif operator[-1] == "1":
        x += 1
        y += 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
        
    elif operator[-1] == "2":
        x += 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
        
    elif operator[-1] == "3":
        x += 1
        y -= 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
    
    elif operator[-1] == "4":
        y -= 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
    
    elif operator[-1] == "5":
        x -= 1
        y -= 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])

    
    elif operator[-1] == "6":
        x -= 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
    
    elif operator[-1] == "7":
        x -= 1
        y += 1
        if [x,y] in visited:
            visited.remove([x,y])
        else:
            visited.append([x,y])
    
    operator = operator[:-1]

if visited:
    max_x = max(visit[0] for visit in visited)
    min_x = min(visit[0] for visit in visited)
    range_x = max_x - min_x + 1
    max_y = max(visit[1] for visit in visited)
    min_y = min(visit[1] for visit in visited)
    range_y = max_y - min_y + 1

    while range_y:
        for i in range(min_x, max_x + 1):
            if [i, max_y] in visited:
                print("⚪", end ="")
            else:
                print("⚫️", end ="")
        print()
        max_y -= 1
        range_y -= 1
        
