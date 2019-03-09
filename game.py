from battle import Field, Game, Player, Ship
import os

def main():
    os.system("clear")
    name2 = name1 = input("Enter the name of the first player: ")
    while name2 == name1:
        name2 = input("Enter the name of the second player: ")
    player1, player2 = Player(name1), Player(name2)
    field1, field2 = Field(), Field()
    field1.get_ships_from_user(player1)
    field2.get_ships_from_user(player2)
    game = Game([field1, field2], [player1, player2], 0)
    counter = 0
    while True:
        res = False
        os.system("clear")
        print("Field of player {}".format(eval("name{}".format((counter ^ 1) + 1))))
        print(game.field_without_ships(counter ^ 1))
        while not res or res == "shot":
            res = game.shoot_at(counter)
            if res == "shot":
                os.system("clear")
                print("Field of player {}".format(eval("name{}".format((counter ^ 1) + 1))))
                print(game.field_without_ships(counter ^ 1))
        if res == "win":
            print("Player {} WON!!!".format(eval("name" + str(counter + 1))))
            print("Field of player {}".format(name1))
            print(game.field_with_ships(0))
            print("Field of player {}".format(name2))
            print(game.field_with_ships(1))
            break
        counter = counter ^ 1


if __name__ == "__main__":
    main()
