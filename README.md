# calcuScore
III intern calculate score and SQL insert, rank 

# Use instruction
First, download Python(version 3.6), pip, and then run
>pip install -r requirements.txt

on shell.

Second, adjust config.py to server's account and db.

That's it.

Whenever a new play record be produced, calling 
>[path/to/python36] [path/to/calcuScore.py] [UID] [GID] [CID] [Time] [Manip] [Time_std] [Manip_std]

in shell code, it will return player's score, insert/update this record to db, and calculate the Ranking in provided (GID, CID).
