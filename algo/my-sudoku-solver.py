#!/usr/bin/env python3
# algo assignment
# Solving SUDOKU with constraints solving algo.
# Level: EASY

# --- 9x9 sudoku -----
challenge = [
    [2,0,0,6,0,1,0,0,8],
    [0,0,0,4,3,7,0,0,0],
    [0,0,3,0,9,0,7,0,0],
    [3,5,0,0,0,0,0,9,2],
    [0,4,2,0,0,0,5,7,0],
    [7,8,0,0,0,0,0,6,4],
    [0,0,5,0,1,0,4,0,0],
    [0,0,0,3,4,5,0,0,0],
    [8,0,0,7,0,2,0,0,1]
    ]

PUZZLESIZE = 9
SQSIZE = 3
# -------- display -------------------

def print_puzzle(puzzle, mark=None):
    size = PUZZLESIZE
    for i in range(size):
        for j in range(size):
            print(puzzle[i][j], end="")
            output = ""
            if (j+1)% SQSIZE == 0 and (j+1<size):
            else:
                output = "  "
            if mark and (j,i) == mark:
                output = "*" + output[1:]
            print(output, end="")
        print()
        if (i+1)% SQSIZE == 0:
            print()
    if mark:
        print("Notes: ", note[mark])

def print_square(puzzle, position): # useful for debugging
    x, y = position
    size = SQSIZE
    start_x = x-(x% size)
    start_y = y-(y% size)
    for i in range(size):
        for j in range(size):
            print(puzzle[start_y + i][start_x + j], end="")
            output = ""
            if (j+1)% size == 0 and (j+1<size):
                output = "   "
            else:
                output = "  "
            if (start_x + j, start_y + i) == position:
                output = "*" + output[1:]
            print(output, end="")
        print()
    print("Notes: ", note[position])

# --- retrieve the positions of openspots in relation to rows/cols/square ----

def get_row_openspots(puzzle, position): # exclude current
    x, y = position
    size = PUZZLESIZE
    results = []
    for i in range(size):
        if i == x:
            continue
        else:
            if puzzle[y][i] == 0:
                results.append((i, y))
    return results

def get_col_openspots(puzzle, position): 
    x, y = position
    size = PUZZLESIZE
    results = []
    for i in range(size):
        if i == y: # exclude current
            continue
        else:
            if puzzle[i][x] == 0:
                results.append((x, i))
    return results

def get_square_openspots(puzzle, position):
    x, y = position
    size = SQSIZE
    results = []
    start_x = x-(x% size)
    start_y = y-(y% size)
    for i in range(size):
        for j in range(size):
            if start_y+i == y and start_x+j == x: # exclude current
                continue
            else:
                if puzzle[start_y+i][start_x+j] == 0:
                    results.append((start_x+j, start_y+i))
    return results

# ---- retrieve all the numbers in current rows/cols/square ----

def get_row_set(puzzle, position):
    x, y = position
    size = PUZZLESIZE
    return set(puzzle[y][i] for i in range(size))

def get_col_set(puzzle, position):
    x, y = position
    size = PUZZLESIZE
    return set(puzzle[i][x] for i in range(size))

def get_square_set(puzzle, position):
    x, y = position
    size = SQSIZE
    start_x = x-(x% size)
    start_y = y-(y% size)
    return set( puzzle[start_y+i][start_x+j] for j in range(size) for i in range(size))

# ----- if number exists in set, there is conflict --------

def is_row_safe(puzzle, position, number):
    x, y = position
    return not (number in get_row_set(puzzle, position))

def is_col_safe(puzzle, position, number):
    x, y = position
    return not (number in get_col_set(puzzle, position))
        
def is_square_safe(puzzle, position, number):
    x, y = position
    return not (number in get_square_set(puzzle, position))

# ------ must pass all checks ----------------

def is_safe(puzzle, position, number):
    if(not is_row_safe(puzzle,position,number)):
        return False

    if(not is_col_safe(puzzle,position,number)):
        return False

    if(not is_square_safe(puzzle,position,number)):
        return False

    return True
   
# ----------- notes -------------
def populate_note(puzzle, note):
    size = PUZZLESIZE
    for y in range(size):
        for x in range(size):
            if challenge[y][x] == 0: # open spot
                for k in range(1,10):
                    if is_safe(challenge, (x,y), k):
                        note[x,y].add(k) # add to note when it is safe
            else:
                del note[x,y] # no need to track non-open spot

def update_note(puzzle, note, position, number):
    '''Remove number from the notes appearing in same rows/cols/square'''
    rows = get_row_openspots(challenge, position)
    cols = get_col_openspots(challenge, position)
    squa = get_square_openspots(challenge, position)
    for pos in rows:
        if number in note[pos]:
            note[pos].remove(number)
            print("rows: removed ", number, "from", pos, note[pos])
    for pos in cols:
        if number in note[pos]:
            note[pos].remove(number)
            print("cols: removed ", number, "from", pos, note[pos])
    for pos in squa:
        if number in note[pos]:
            note[pos].remove(number)
            print("square: removed ", number, "from", pos, note[pos])

def update_challenge(puzzle, note, position, number):
    '''Each time a number is decided on which position, we need to update note'''
    x, y = position
    challenge[y][x] = number
    update_note(puzzle, note, position, number)
    print_puzzle(puzzle, position)
    print("------")
    del note[position] # delete after number is inserted

def constraint_scan(puzzle, note, count=0):
    print("Scan count: ", count)
    if not note:
        return;
    if count > 20: #break out of scan loop
        return;
    for k in sorted(note, key=lambda k: len(note[k])):
        print("next:", k, note[k])

        if(len(note[k]) > 1): # re-sort with updated notes
            print("[*] re-sort and scan again...")
            return constraint_scan(puzzle,note, count+1)

        if(len(note[k]) == 1): # only interested in 100% confidence
            number = next(iter(note[k]))
            print("Press enter to update ", k, "with value ", number)
            input()
            update_challenge(puzzle, note, k, number)
    

if __name__ == "__main__":
    print_puzzle(challenge)
    size = PUZZLESIZE
    note = {(i,j):set() for i in range(size) for j in range(size)}
    populate_note(challenge, note)

    constraint_scan(challenge, note)
    print("Solved.")



