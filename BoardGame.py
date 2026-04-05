import random

final_space = 100

def loadGameData(filename):
    """Reads game data from a file and returns it as a list."""
    data = []
    with open(filename, "r") as file:
        for line in file:
            data.append(line.strip())
    return data


def turnOrder(players):
    rolls = {}
    print("Rolling determines order!")
    for player in players:
        roll = random.randint(1, 6)
        rolls[player] = roll
        print(f"{player} rolled {roll}")

    sorted_players = sorted(rolls, key=rolls.get, reverse=True)
    print("Turn order:", sorted_players)
    return sorted_players


def getEventSymbol(event):
    if event == "Treasure":
        return "X"
    elif event == "Trap":
        return "T"
    elif event == "Heal":
        return "H"
    else: 
        return "?"


def displayGame(players, events):
   print("\nBoard:")
   row_length = 10
   for row in range (10):
       print(f"{row*row_length+1:3d}-", end="")
       for col in range(1, row_length + 1):
           i = row * row_length + col
           markers = []
           for player, pos in players.items():
             if pos == i:
               markers.append(player[-1])
           if i in events:
             markers.append(getEventSymbol(events[i]))
           cell = "|" + ("".join(markers) if markers else " ")
           print(cell, end="")
       print("|")
   print("\nLegend: 1=Player1, 2=Player2, 3=Player3, X=Treasure, H=Heal, T=Trap")
   print("\nPlayer Positions (after this turn):")
   for player, pos in players.items():
       print(f"{player}: {pos}")


def movePlayerExact(players, current_turn):
    roll = random.randint(1,3)
    current_pos = players[current_turn]
    print(f"{current_turn} rolled {roll}")

    if current_pos + roll > final_space:
        print(f"You need exact roll to reach {final_space}!")
        return current_pos
    else: 
        new_pos = current_pos + roll
        players[current_turn] = new_pos
        return new_pos
    

def handleEvent(position, events):
    if position in events:
        event = events[position]
        print(f"Landed on {event}!")

        if event == "Trap":
            print("Move back 2 spaces!")
            return -2 
        elif event == "Treasure":
            print("Move forward 2 spaces!")
            return 2
        elif event == "Heal":
            print("You feel better! Move forward 1 space!")
            return 1
    return 0

def nextTurn(turn_order, current_index):
    return (current_index + 1) % len(turn_order)


def main():
    filename = "events.txt"   # Students can rename if needed
    data = loadGameData(filename)

    players = {}
    events = {}

    for line in data:
        if line.startswith("Turn:"):
            continue
        space, value = line.split(":")
        space = int(space.strip())
        value = value.strip()
        if value.startswith("Player"):
            players[value] = 0
        else: 
            events[space] = value

    turn_order = turnOrder(players)
    current_index = 0 
    game_over = False

    while not game_over:
        current_turn = turn_order[current_index]
        print(f"\n--- {current_turn}'s Turn---")
        displayGame(players, events)

        input("Press Enter to roll dice!")
        new_pos = movePlayerExact(players, current_turn)

        change = handleEvent(new_pos, events)
        players[current_turn] += change
        if players[current_turn] < 0:
            players[current_turn] = 0 

        if players[current_turn] == final_space:
            print(f"\n {current_turn} wins the game!!!")
            displayGame(players, events)
            game_over = True
            break

        current_index = nextTurn(turn_order, current_index)


if __name__ == "__main__":
    main()
# Homework 3 - Board Game System
# Name: Mariana Chavez 
# Date: 04.05.2026

