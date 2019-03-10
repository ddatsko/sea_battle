import os


class Game:
    """
    Class fpr representing the whole game
    """

    def __init__(self, fields, players, current_player):
        """
        (Game, list(Field), list(Player), Player) -> None
        Initialize a class object
        :param fields: list of 2 objects of class Field
        :param players: list of 2 objects of class Player
        :param current_player: Player object that is moving nof
        """
        self.__fields = fields
        self.players = players
        self.current_player = current_player

    def shoot_at(self, index):
        """
        (Game, int) -> str
        Shoot at the position
        :param index: index of shooting player
        :return: "win" if the player won after this shot,
        "shot" if he shot the opponent's ship,
        "missed" if player missed,
        "" if player shot at the wrong position
        """
        position = self.players[index].read_position()
        res = self.__fields[index ^ 1].shoot_at(position)
        if not self.__fields[index ^ 1].are_ships():
            return "win"
        return res

    def field_with_ships(self, index):
        """
        (Game, int) -> str
        :param index: index of the field to be shown
        :return: str represantation of the field with all ships shown
        """
        return self.__fields[index].field_view(True)

    def field_without_ships(self, index):
        """
        (Game, int) -> str
        :param index: index of the field to be shown
        :return: str representation of the field with only
        shot ships shown
        """
        return self.__fields[index].field_view(False)

    def change_player(self):
        """
        (Game) -> None
        Change current player for aother one
        """
        self.current_player = self.players[self.players.index(self.current_player) ^ 1]


class Player:
    def __init__(self, name):
        """
        (Player, str) -> None
        Method for initializing object of class Player
        :param name: name of the player
        """
        self.name = name

    def read_position(self):
        """
        (Player) -> (int, int)
        Read position from user and convert it to right format
        :return: position in format (int, int)
        """
        pos = ""
        while not (len(pos) == 2 and 'a' <= pos[0] <= 'j' and '0' <= pos[1] <= '9'):
            pos = input("{}, please enter the position: ".format(self.name.capitalize()))
        return (int(pos[1]), ord(pos[0]) - ord('a'))


class Field:
    def __init__(self, ships=None):
        """
        (Field, list)
        Initialize an object of class Field
        :param ships: list of ships on the field
        """
        self.__ships = ships
        self.__cells = [[None] * 10 for i in range(10)]
        self.shot = set()

    def get_ships_from_user(self, player):
        """
        (Field, Player) -> None
        Get ships from player and add the on the field
        :param player: Player object to take ships from
        """
        ships = [0] * 4
        # loop untill all the 10 ships are read
        while sum(ships) < 10:
            os.system("clear")

            # show the field
            print("Current field: ")
            print(self.field_view(True))
            print()

            # read position and ship details from the user
            x, y = player.read_position()
            orientation = input("Choose orientation: Vertical[v] of horizontal[h]: ")
            while not orientation or orientation not in "vh":
                orientation = input("Try again [v/h]: ").lower()
            length = 0

            # read the length of the ship from user
            while True:
                try:
                    length = int(input("Select length [1..4] or enter -1 to add another ship: "))
                    # -1 means that user wants to choose another position or orientation
                    if length == -1:
                        break

                    # check the validity of chosen position
                    if orientation == "h":
                        if y + length > 10:
                            continue
                    else:
                        if x + length > 10:
                            continue
                    assert (ships[length - 1] <= 4 - length)
                    break
                except:
                    print("Only numbers from 1 to 4 are acceptable")

            # if user wants to choose another position
            if length == -1:
                continue

            # check if the chosen ship is near other ships
            y_mul = x_mul = 0
            if orientation == "h":
                y_mul = 1
            else:
                x_mul = 1
            os.system("clear")
            for i in range(length):
                if self.near_ship(x + i * x_mul, y + i * y_mul):
                    print("This ship can not be so close to another one")
                    break
            else:
                # add ship to the list of added ships and to the field
                ships[length - 1] += 1
                ship = Ship((x, y), orientation == "h", length)
                for i in range(length):
                    self.__cells[x + i * x_mul][y + i * y_mul] = ship

    def near_ship(self, x, y):
        """
        (Field, int, int) -> bool
        :param x: x-coordinate of the checked cell
        :param y: y-coordinate of the checked cell
        :return: if the cell is near the ship
        """
        x_check = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        y_check = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        for i in range(9):
            if 0 <= x + x_check[i] < 10 and 0 <= y + y_check[i] < 10:
                if self.__cells[x + x_check[i]][y + y_check[i]]:
                    return True
        return False

    def shoot_at(self, position):
        """
        (Field, tuple(int, int)) -> str
        :param position: position to shoot at
        :return: "win" if the player won after this shot,
        "shot" if he shot the opponent's ship,
        "missed" if player missed,
        "" if player shot at the wrong position
        """
        x, y = position
        if (x, y) not in self.shot:
            if self.__cells[x][y]:
                return self.__cells[x][y].shoot_at((x, y))
            else:
                self.shot.add((x, y))
                return "missed"
        return None

    def are_ships(self):
        """
        (Field) -> bool
        :return: whether there still are ships on the field
        """
        res = False
        for i in range(10):
            for j in range(10):
                if self.__cells[i][j]:
                    if self.__cells[i][j].view(i, j, True) == "X":
                        res = True
        return res

    def field_view(self, show_ships):
        """
        (Field, bool) -> str
        :param show_ships: whether not beaten ships should be shown
        :return: string representation of the field
        """
        res = ""
        res += '    '
        for i in range(10):
            res += chr(ord('a') + i) + " "
        res += "\n"
        for i in range(10):
            res += "{:2} ".format(i)
            for j in range(10):
                if self.__cells[i][j]:
                    cell = (self.__cells[i][j].view(i, j, show_ships))
                else:
                    cell = "·" if (i, j) in self.shot else "_"
                res += "𝖨{}".format(cell)
            res += "𝖨\n"
        return res


class Ship:
    def __init__(self, bow, horizontal, length):
        """
        (Ship, tuple(int, int), bool, int)
        :param bow: position of left top corner of the ship
        :param horizontal: whether the ship is horizontal
        :param length: length of the ship
        """
        self.bow = bow
        self.horizontal = horizontal
        self.__length = length
        self.fields = []
        self.hit = 0
        if horizontal:
            for i in range(length):
                self.fields.append((bow[0], bow[1] + i, False))
        else:
            for i in range(length):
                self.fields.append((bow[0] + i, bow[1], False))

    def shoot_at(self, position):
        """
        (Ship, tuple(int, int)) -> str
        :param position: position of the cell to be shoot
        :return: "shot" if player shot at the ship else ""
        """
        x, y = position
        if (x, y, True) in self.fields:
            return ""
        self.hit += 1
        self.fields.remove((x, y, False))
        self.fields.append((x, y, True))
        return "shot"

    def view(self, x, y, show_ships):
        """
        (Ship, int, int, bool) -> str
        :param x: x-coordinate of the cell
        :param y: y-coordinate of the cell
        :param show_ships: whether undeaten part should be shown
        :return: string representation of the cell
        """
        if self.hit == self.__length:
            return "■"
        elif (x, y, True) in self.fields:
            return "X"
        elif (x, y, False) in self.fields and show_ships:
            return "X"
        else:
            return "_"
