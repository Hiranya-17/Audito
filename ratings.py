Numvote = 0
total = 0
vote = 0
totals = {}
Numvotes = {}
ratings = {}

def rate(song, vote):
    global ratings
    if song in ratings:
        totals[song] += vote
        Numvotes[song] += 1
        ratings[song] = totals[song]/Numvotes[song]
    else:
        ratings[song] = vote
        Numvotes[song] = 1
        totals[song] = int(vote)


while True:

    txt = input("Rate? ")

    if txt == "y":
        song = input("Which song would you like to rate? ")
        vote = input("What is your rating out of five stars? ")
        x = int(vote)
        if x>0 and x<6:
            rate(song, int(vote))
            print(f"{song}'s rating is now {ratings[song]}.")
        else:
            pass

    elif txt == 'n':
        print("Thank you for rating!")
        print(ratings)
        break
    else:
        pass