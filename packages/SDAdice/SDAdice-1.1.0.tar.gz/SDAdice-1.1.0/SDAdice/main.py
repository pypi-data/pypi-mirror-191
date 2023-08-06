import random

def play_dice_game():
    user_nr = int(input("Input Expectations (dice 1-6): "))
    dice_nr = random.randint(1, 6)
    print(dice_nr)

    if user_nr == dice_nr:
        print("YOU WIN!!")
    else:
        print("YOU LOSE")