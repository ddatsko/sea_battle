from battle import Field, Game, Player, Ship
import os


def main():
    os.system("clear")

    # Get players names
    name2 = name1 = input("Enter the name of the first player: ")
    while name2 == name1:
        name2 = input("Enter the name of the second player: ")

    # initialize game objects and the game itself
    player1, player2 = Player(name1), Player(name2)
    field1, field2 = Field(), Field()
    field1.get_ships_from_user(player1)
    field2.get_ships_from_user(player2)
    game = Game([field1, field2], [player1, player2], player1)

    # main loop of the game
    while True:
        # extract current player and his index
        player = game.current_player
        player_index = game.players.index(player)
        res = False

        # make player make a right move (loop if move is ot right or if he shot a ship)
        while not res or res == "shot":
            # print opponent`s field
            os.system("clear")
            print("Field of player {}".format(game.players[player_index ^ 1].name))
            print(game.field_without_ships(player_index ^ 1))

            # make a shot and save it`s result to res
            res = game.shoot_at(player_index)

        # when someone wins
        if res == "win":
            print("Player {} WON!!!".format(player.name))
            print("Field of player {}".format(name1))
            print(game.field_with_ships(0))
            print("Field of player {}".format(name2))
            print(game.field_with_ships(1))
            break
        # change current player
        game.change_player()


if __name__ == "__main__":
    main()
