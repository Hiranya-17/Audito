Numvote = 0
total = 0
vote = 0
totals = {}
Numvotes = {}
ratings = {}

def rate(Song, vote):
    if float(vote) < 0 or float(vote) > 5:
        print("This is not a valid rating. Please try again. ")

    song = " ".join(Song.split()).title()
    
    if song in ratings:
        totals[song] += vote
        Numvotes[song] += 1
        ratings[song] = totals[song]/Numvotes[song]
    else:
        ratings[song] = vote
        Numvotes[song] = 1
        totals[song] = int(vote)
    
    print(f"{song}'s rating is now {ratings[song]}.")

def del_rating(Song, vote):
    
    song = " ".join(Song.split()).title()
    totals[song] -= vote
    Numvotes[song] -= 1
    ratings[song] = totals[song]/Numvotes[song]
    print(f"{song}'s rating is now {ratings[song]}")