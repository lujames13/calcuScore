import sys
import numpy as np
import datetime

import dbTool

'''
    input:
        UID(int) -- User ID
        GID(int) -- Game ID
        CID(int) -- Class ID
        Time(int) -- the time player used to finish the game.
        Manip(int) -- the manipulate times player used in game.
        Time_std(int) -- the standard required time to finish the game.
        Manip_std(int) -- the standard required manipulate times to finish the game.
        
    output:
        if success:
            'score' -- the player's score which is between 0 to 2000000
            'INSERT success' / 'UPDATE success' -- success message
        if fail:
            'Error: ...' -- Error message
'''
'''
    Score rule:
        Calculate score by Time and Manip,
        Time score is a inverse tanh curve, using less time to get more score. The highest score is 500000*(tanh(4)+1).
        Manip score is a linear line which has two slope, using less step to get more score. The highest score is 1000000.
'''

def score(UID, GID, Time, Manip, Time_std, Manip_std, CID):
    Manip_score, Time_score, score = calculate_score(Time, Manip, Time_std, Manip_std)
    db = dbTool.Database()
    try:
        db.add_score(UID, GID, score, Time, Manip, Time_score, Manip_score, CID)
        db.update_ranking(GID, CID)
        db.sql_commit()
        print(score)
        return "INSERT success"
    except:
        db.update_score(UID, GID, score, Time, Manip, Time_score, Manip_score, CID)
        db.update_ranking(GID, CID)
        db.sql_commit()
        print(score)

        return "UPDATE success"


def calculate_score(Time, Manip, Time_std=300, Manip_std=10):
    time_rev = 4 - (Time / Time_std) * 4
    Time_score = np.tanh(time_rev) + 1  # let the value be 0~2
    if Manip < Manip_std:  # Manip < Manip_std
        Manip = 0
        Manip_score = 0
    else:  # Manip_std < Manip < 2*Manip_std
        Manip -= Manip_std
        Manip_score = 11237 * Manip
        if Manip > Manip_std:  # Manip > 2*Manip_std
            Manip -= Manip_std
            Manip_score += 12379 * Manip

    Time_score = 500000 * Time_score
    Manip_score = 1000000 - Manip_score
    if Manip_score < 0: Manip_score = 0
    score = Time_score + Manip_score
    # if score < 1000000:
    #     score = 1000000
    return int(Manip_score), int(Time_score), int(score)


try:

    UID = int(sys.argv[1])
    GID = int(sys.argv[2])
    CID = int(sys.argv[3])
    Time = int(sys.argv[4])
    Manip = int(sys.argv[5])
    Time_std = int(sys.argv[6])
    Manip_std = int(sys.argv[7])
    query_status = score(UID, GID, Time, Manip, Time_std, Manip_std, CID)

    print(query_status, datetime.datetime.now())

except Exception as e:

    print("Error:", str(e))
