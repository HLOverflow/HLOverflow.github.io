#!/usr/bin/env python3

# Assignment - how to represent a rubix cube & apply rotation on it.

# Faces = G, R, O, W, Y, B (Faces will always be static)
# let us represent positions in the form of (G, R, O, W, Y, B). 
# each has a position number 1 to 4.

# Type of Movements (clockwise vs anticlockwise) = F, U, D, L, R, F', U', D', R', L'

# 4x6 = 24 Sides (front,side) - TOP, RIGHT, BOTTOM, LEFT (clockwise)
# G = GW, GO, GY, GR
# R = RW, RG, RY, RB
# O = OW, OB, OY, OG
# W = WO, WG, WR, WB 
# Y = YO, YB, YR, YG
# B = BW, BR, BY, BO

# 4x6 = 24 Corners (Front,side1,side2) - TOPRIGHT,BOTTOMRIGHT,BOTTOMLEFT,TOPLEFT (clockwise)
# G = GWO, GOY, GYR, GRW
# R = RWG, RGY, RYB, RBW
# O = OWB, OBY, OYG, OGW
# W = WOG, WGR, WRB, WBO
# Y = YOB, YBR, YRG, YGO
# B = BWR, BRY, BYO, BOW

POS_KEYS = "GROWYB"
# SIDES positions
TOP = 1; RIGHT = 2; BOTTOM = 3; LEFT = 4
# CORNERS positions
TOPRIGHT = 1; BOTTOMRIGHT = 2; BOTTOMLEFT = 3; TOPLEFT = 4;

# define sides and corners of a solved cube
sides_string = "GW,GO,GY,GR,RW,RG,RY,RB,OW,OB,OY,OG,WO,WG,WR,WB,YO,YB,YR,YG,BW,BR,BY,BO"
corners_string = "GWO,GOY,GYR,GRW,RWG,RGY,RYB,RBW,OWB,OBY,OYG,OGW,WOG,WGR,WRB,WBO,YOB,YBR,YRG,YGO,BWR,BRY,BYO,BOW"

def get_face_for_side(sides, key):
    highest = max(sides[key])
    i = sides[key].index(highest) # assume not zero
    return POS_KEYS[i]

def get_face_for_corner(corners, key):
    highest = max(corners[key])
    i = corners[key].index(highest) # assume not zero
    return POS_KEYS[i]

def print_cube(faces, sides, corners):
    for f in POS_KEYS:
        print("Face: ", f)
        ss = faces[f]['sides']
        for s in ss:
            print(s, sides[s])
        cc = faces[f]['corners']
        for c in cc:
            print(c, corners[c])
        print()

def get_side_from_facepos(faces, sides, face, position):
    slist = faces[face]["sides"]
    for s in slist:
        i = POS_KEYS.index(face)
        if sides[s][i] == position:
            return s
def get_corner_from_facepos(faces, sides, face, position):
    clist = faces[face]["corners"]
    for c in clist:
        i = POS_KEYS.index(face)
        if corners[c][i] == position:
            return c

def update_side(sides, key, faces, newface, position):
    oldface = get_face_for_side(sides, key)
    if(oldface != newface):
        i = POS_KEYS.index(newface)
        sides[key] = sides[key] and [0,0,0,0,0,0] # clear the array
        sides[key][i] = position

        # propagate update to face.
        faces[newface]["sides"].add(key)
        faces[oldface]["sides"].remove(key)

    else: # only change position
        highest = max(sides[key])
        i = sides[key].index(highest)
        sides[key][i] = position

def update_corner(corners, key, faces, newface, position):
    oldface = get_face_for_corner(corners, key)
    if(oldface != newface):
        i = POS_KEYS.index(newface)
        corners[key] = corners[key] and [0,0,0,0,0,0] # clear the array
        corners[key][i] = position

        # propagate update to face.
        faces[newface]["corners"].add(key)
        faces[oldface]["corners"].remove(key)

    else: # only change position
        highest = max(corners[key])
        i = corners[key].index(highest)
        corners[key][i] = position

def rotate_F(faces, sides, corners, front):  
    # --- sides ----
    sides_clockwise = [None, None, None, None]
    sides_clockwise[0] = get_side_from_facepos(faces, sides, front, TOP) [::-1] 
    sides_clockwise[1] = get_side_from_facepos(faces, sides, front, RIGHT) [::-1] 
    sides_clockwise[2] = get_side_from_facepos(faces, sides, front, BOTTOM) [::-1] 
    sides_clockwise[3] = get_side_from_facepos(faces, sides, front, LEFT) [::-1] 

    memo_sides = {} # for tracking prior to updating.
    # [0] -> [1] -> [2] -> [3] -> [0]
    for i in range(4):
        a = sides_clockwise[i]
        b = sides_clockwise[(i+1)%4]
        
        highest = max(sides[b])
        i = sides[b].index(highest)
        newposition = sides[b][i]
        newface = get_face_for_side(sides, b)
        memo_sides.update({a: {"newposition": newposition, "newface": newface}})

    print("Memo update is ", memo_sides)

    for side in sides_clockwise:
        update_side(sides, side, faces, memo_sides[side]["newface"], memo_sides[side]["newposition"])
    print("applied memo updates to sides")
    
    # same face but shift position by 1 (update last)
    for side in faces[front]['sides']:
        oldposition = max(sides[side])
        newposition = (oldposition % 4) + 1
        update_side(sides, side, faces, front,newposition) 
    print("applied same face rotation to sides")

    # --- corners ---

    # Unlike sides, we need to move 2 corners instead 1.
    corners_clockwise1 = [None, None, None, None]
    corners_clockwise2 = [None, None, None, None]

    t = get_corner_from_facepos(faces, sides, front, TOPRIGHT) # GWO -> WOG
    corners_clockwise1[0] = t[1:] + t[0]
    corners_clockwise2[0] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, BOTTOMRIGHT) 
    corners_clockwise1[1] = t[1:] + t[0]
    corners_clockwise2[1] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, BOTTOMLEFT) 
    corners_clockwise1[2] = t[1:] + t[0]
    corners_clockwise2[2] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, TOPLEFT) 
    corners_clockwise1[3] = t[1:] + t[0]
    corners_clockwise2[3] = t[-1] + t[:2]

    memo_corners = {} # for tracking prior to updating.
    # [0] -> [1] -> [2] -> [3] -> [0]

    # First corner
    for i in range(4):
        a = corners_clockwise1[i]
        b = corners_clockwise1[(i+1)%4]
        
        highest = max(corners[b])
        i = corners[b].index(highest)
        newposition = corners[b][i]
        newface = get_face_for_corner(corners, b)
        memo_corners.update({a: {"newposition": newposition, "newface": newface}})

    # next corner
    for i in range(4):
        a = corners_clockwise2[i]
        b = corners_clockwise2[(i+1)%4]
        
        highest = max(corners[b])
        i = corners[b].index(highest)
        newposition = corners[b][i]
        newface = get_face_for_corner(corners, b)
        memo_corners.update({a: {"newposition": newposition, "newface": newface}})
    print("Memo update is ", memo_corners)

    # apply updates for 1st and 2nd
    for corner in corners_clockwise1:
        update_corner(corners, corner, faces, memo_corners[corner]["newface"], memo_corners[corner]["newposition"])
    for corner in corners_clockwise2:
        update_corner(corners, corner, faces, memo_corners[corner]["newface"], memo_corners[corner]["newposition"])
    print("applied memo updates to corners")
    
    # same face but shift position by 1 (update last)
    for corner in faces[front]['corners']:
        oldposition = max(corners[corner])
        newposition = (oldposition % 4) + 1
        update_corner(corners, corner, faces, front,newposition) 
    print("applied same face rotation to corners")

    # --- complete ---
    print_cube(faces, sides, corners)

def inverse_rotate_F(faces, sides, corners, front):
    # ----- sides ------ 
    sides_anticlockwise = [None, None, None, None]
    sides_anticlockwise[0] = get_side_from_facepos(faces, sides, front, TOP) [::-1] 
    sides_anticlockwise[1] = get_side_from_facepos(faces, sides, front, LEFT) [::-1] 
    sides_anticlockwise[2] = get_side_from_facepos(faces, sides, front, BOTTOM) [::-1] 
    sides_anticlockwise[3] = get_side_from_facepos(faces, sides, front, RIGHT) [::-1] 
    memo_sides = {} # for tracking prior to updating.

    # [0] -> [1] -> [2] -> [3] -> [0]
    for i in range(4):
        a = sides_anticlockwise[i]
        b = sides_anticlockwise[(i+1)%4]
        
        highest = max(sides[b])
        i = sides[b].index(highest)
        newposition = sides[b][i]
        newface = get_face_for_side(sides, b)

        memo_sides.update({a: {"newposition": newposition, "newface": newface}})

    print("Memo update for sides is ", memo_sides)

    for side in sides_anticlockwise:
        # apply memo updates
        update_side(sides, side, faces, memo_sides[side]["newface"], memo_sides[side]["newposition"])
        print("applied memo updates to sides")
        pass
    
    for side in faces[front]['sides']:
        # same face but shift position by 1 (update last)
        oldposition = max(sides[side])
        newposition = ((oldposition-2) % 4) + 1
        update_side(sides, side, faces, front,newposition) 
        print("applied same face rotation to sides")

    # --- corners ---
    # Unlike sides, we need to move 2 corners instead 1.
    corners_anticlockwise1 = [None, None, None, None]
    corners_anticlockwise2 = [None, None, None, None]

    t = get_corner_from_facepos(faces, sides, front, TOPRIGHT) # GWO -> WOG
    corners_anticlockwise1[0] = t[1:] + t[0]
    corners_anticlockwise2[0] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, TOPLEFT) 
    corners_anticlockwise1[1] = t[1:] + t[0]
    corners_anticlockwise2[1] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, BOTTOMLEFT) 
    corners_anticlockwise1[2] = t[1:] + t[0]
    corners_anticlockwise2[2] = t[-1] + t[:2]
    t = get_corner_from_facepos(faces, sides, front, BOTTOMRIGHT) 
    corners_anticlockwise1[3] = t[1:] + t[0]
    corners_anticlockwise2[3] = t[-1] + t[:2]

    memo_corners = {} # for tracking prior to updating.
    # [0] -> [1] -> [2] -> [3] -> [0]

    # First corner
    for i in range(4):
        a = corners_anticlockwise1[i]
        b = corners_anticlockwise1[(i+1)%4]
        
        highest = max(corners[b])
        i = corners[b].index(highest)
        newposition = corners[b][i]
        newface = get_face_for_corner(corners, b)
        memo_corners.update({a: {"newposition": newposition, "newface": newface}})

    # next corner
    for i in range(4):
        a = corners_anticlockwise2[i]
        b = corners_anticlockwise2[(i+1)%4]
        
        highest = max(corners[b])
        i = corners[b].index(highest)
        newposition = corners[b][i]
        newface = get_face_for_corner(corners, b)
        memo_corners.update({a: {"newposition": newposition, "newface": newface}})
    print("Memo update is ", memo_corners)

    # apply updates for 1st and 2nd
    for corner in corners_anticlockwise1:
        update_corner(corners, corner, faces, memo_corners[corner]["newface"], memo_corners[corner]["newposition"])
    for corner in corners_anticlockwise2:
        update_corner(corners, corner, faces, memo_corners[corner]["newface"], memo_corners[corner]["newposition"])
    print("applied memo updates to corners")
    
    # same face but shift position by 1 (update last)
    for corner in faces[front]['corners']:
        oldposition = max(corners[corner])
        newposition = ((oldposition-2) % 4) + 1
        update_corner(corners, corner, faces, front,newposition) 
    print("applied same face rotation to corners")
    # --- complete ---
    print_cube(faces, sides, corners)

# rotate_R is rotate_F with the right side as the new front
def rotate_R(faces, sides, corners, front):
    rightside = get_side_from_facepos(faces, sides, front, RIGHT)
    newfront = get_face_for_side(sides, rightside[::-1])
    print("Right side of ", front, " is ", newfront)
    rotate_F(faces, sides, corners, newfront)

# rotate_U is rotate_F with the top side as the new front
def rotate_U(faces, sides, corners, front):
    topside = get_side_from_facepos(faces, sides, front, TOP)
    newfront = get_face_for_side(sides, topside[::-1])
    print("Top side of ", front, " is ", newfront)
    rotate_F(faces, sides, corners, newfront)

# rotate_L is rotate_F with the left side as the new front
def rotate_L(faces, sides, corners, front):
    leftside = get_side_from_facepos(faces, sides, front, LEFT)
    newfront = get_face_for_side(sides, leftside[::-1])
    print("Left side of ", front, " is ", newfront)
    rotate_F(faces, sides, corners, newfront)

# rotate_D is rotate_F with the bottom side as the new front
def rotate_D(faces, sides, corners, front):
    bottomside = get_side_from_facepos(faces, sides, front, BOTTOM)
    newfront = get_face_for_side(sides, bottomside[::-1])
    print("Bottom side of ", front, " is ", newfront)
    rotate_F(faces, sides, corners, newfront)

# inverse_rotate_R is inverse_rotate_F with the right side as the new front
def inverse_rotate_R(faces, sides, corners, front):
    rightside = get_side_from_facepos(faces, sides, front, RIGHT)
    newfront = get_face_for_side(sides, rightside[::-1])
    print("Right side of ", front, " is ", newfront)
    inverse_rotate_F(faces, sides, corners, newfront)

# inverse_rotate_U is inverse_rotate_F with the top side as the new front
def inverse_rotate_U(faces, sides, corners, front):
    topside = get_side_from_facepos(faces, sides, front, TOP)
    newfront = get_face_for_side(sides, topside[::-1])
    print("Top side of ", front, " is ", newfront)
    inverse_rotate_F(faces, sides, corners, newfront)

# inverse_rotate_L is inverse_rotate_F with the left side as the new front
def inverse_rotate_L(faces, sides, corners, front):
    leftside = get_side_from_facepos(faces, sides, front, LEFT)
    newfront = get_face_for_side(sides, leftside[::-1])
    print("Left side of ", front, " is ", newfront)
    inverse_rotate_F(faces, sides, corners, newfront)

# inverse_rotate_D is inverse_rotate_F with the bottom side as the new front
def inverse_rotate_D(faces, sides, corners, front):
    bottomside = get_side_from_facepos(faces, sides, front, BOTTOM)
    newfront = get_face_for_side(sides, bottomside[::-1])
    print("Bottom side of ", front, " is ", newfront)
    inverse_rotate_F(faces, sides, corners, newfront)

if __name__ == "__main__":

    # initialize
    faces = {k: {"sides":set(), "corners":set()} for k in POS_KEYS}

    sides = {}
    sides_keys = sides_string.split(",")
    for i in range(len(sides_keys)):
        k = sides_keys[i]
        array = [0,0,0,0,0,0]
        j = POS_KEYS.index(k[0])
        array[j] = (i%4)+1
        sides.update( {k: array})

    corners = {}
    corners_keys = corners_string.split(",")
    for j in range(len(corners_keys)):
        k = corners_keys[j]
        array = [0,0,0,0,0,0]
        i = POS_KEYS.index(k[0])
        array[i] = (j%4)+1
        corners.update( {k: array})

    for s in sides:
        f = get_face_for_side(sides, s)
        faces[f]["sides"].add( s )

    for c in corners:
        f = get_face_for_corner(corners, c)
        faces[f]["corners"].add( c )

    print_cube(faces,sides,corners)
    input("Press enter to start")

    # F R U R' U' F'
    rotate_F(faces, sides, corners, "R");
    rotate_R(faces, sides, corners, "R");
    rotate_U(faces, sides, corners, "R");
    inverse_rotate_R(faces, sides, corners, "R");
    inverse_rotate_U(faces, sides, corners, "R");
    inverse_rotate_F(faces, sides, corners, "R");
    


    
