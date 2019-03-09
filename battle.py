import os


class Game:
    def __init__(self, fields, players, current_player):
        self.__fields = fields
        self.__players = players
        self.__current_player = current_player

    def shoot_at(self, index):
        position = self.__players[index].read_position()
        res = self.__fields[index ^ 1].shoot_at(position)
        if not self.__fields[index ^ 1].are_ships():
            return "win"
        return res

    def field_with_ships(self, index):
        return self.__fields[index].field_view(True)

    def field_without_ships(self, index):
        return self.__fields[index].field_view(False)


class Player:
    def __init__(self, name):
        self.__name = name

    def read_position(self):
        pos = ""
        while not (len(pos) == 2 and 'a' <= pos[0] <= 'j' and '0' <= pos[1] <= '9'):
            pos = input("{}, please enter the position: ".format(self.__name.lower()))
        return (int(pos[1]), ord(pos[0]) - ord('a'))


class Field:
    def __init__(self, ships=None):
        self.__ships = ships
        self.__cells = [[None] * 10 for i in range(10)]
        self.shot = set()

    def get_ships_from_user(self, player):
        ships = [0] * 4
        while sum(ships) < 1:
            os.system("clear")
            print("Current field: ")
            print(self.field_view(True))
            print()
            x, y = player.read_position()
            orientation = input("Choose orientation: Vertical[v] of horizontal[h]: ")
            while not orientation or orientation not in "vh":
                orientation = input("Try again [v/h]: ").lower()
            length = 0
            try:
                length = int(input("Select length [1..4]: "))
                if orientation == "h":
                    if y + length > 10:
                        continue
                else:
                    if x + length > 10:
                        continue
                assert (ships[length - 1] <= 4 - length)
            except:
                print("Only numbers from 1 to 4 are acceptable")
                while True:
                    try:
                        length = int(input("Try again [1..4]: "))
                        assert (ships[length - 1] <= 4 - length)
                        os.system("clear")
                        break
                    except:
                        continue
            ships[length - 1] += 1
            y_mul = x_mul = 0
            if orientation == "h":
                y_mul = 1
            else:
                x_mul = 1
            os.system("clear")
            for i in range(length):
                if self.near_ship(x + i*x_mul, y + i*y_mul):
                    print("This ship can not be so close to another one")
                    break
            else:
                ship = Ship((x, y), orientation == "h", length)
                for i in range(length):
                    self.__cells[x + i * x_mul][y + i*y_mul] = ship



    def near_ship(self, x, y):
        x_check = [0, -1, -1, 0, 1, 1, 1, 0, -1]
        y_check = [0, 0, 1, 1, 1, 0, -1, -1, -1]
        for i in range(9):
            if 0 <= x + x_check[i] < 10 and 0 <= y + y_check[i] < 10:
                if self.__cells[x+x_check[i]][y + y_check[i]]:
                    return True
        return False


    def shoot_at(self, position):
        x, y = position
        if (x, y) not in self.shot:
            if self.__cells[x][y]:
                return self.__cells[x][y].shoot_at((x, y))
            else:
                self.shot.add((x, y))
                return "missed"

    def are_ships(self):
        res = False
        for i in range(10):
            for j in range(10):
                if self.__cells[i][j]:
                    if self.__cells[i][j].view(i, j, True) == "X":
                        res = True
        return res

    def field_view(self, show_ships):
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
                res += "|{}".format(cell)
            res += "|\n"
        return res


class Ship:
    def __init__(self, bow, horizontal, length):
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
        x, y = position
        if (x, y, True) in self.fields:
            return False
        self.hit += 1
        self.fields.remove((x, y, False))
        self.fields.append((x, y, True))
        return "shot"

    def view(self, x, y, show_ships):
        if self.hit == self.__length:
            return "■"
        elif (x, y, True) in self.fields:
            return "X"
        elif (x, y, False) in self.fields and show_ships:
            return "X"
        else:
            return "_"
