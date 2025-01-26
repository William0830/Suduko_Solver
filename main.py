# This is a sample Python script.
import copy
from display import display_sudoku_board

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
row_number = 9
column_number = 9

def index_to_box(row,column):
    row = row + 1
    column = column + 1
    if row <= 3:
        row_section = 1
    elif row<= 6:
        row_section = 2
    else:
        row_section = 3

    if column <= 3:
        column_section = 1
    elif column<= 6:
        column_section = 2
    else:
        column_section = 3
    box = row_section + 3*(column_section-1)
    return box

def box_to_list(box):
    row_section = (box-1) % 3 + 1
    column_section = (box-1) // 3 + 1
    center = ((row_section-1)*3+2,(column_section-1)*3+2)
    ran = [-1,0,1]
    box_coord_list = []
    for i in ran:
        for j in ran:
            box_coord_list.append((center[0]+i-1,center[1]+j-1))
    return box_coord_list


class grid_point:
    def __init__(self,value=0,possible=None):
        self.value = value
        self.possible = possible if possible is not None else set(range(1, 10))
class sudoki:
    def __init__(self):
        self.board = np.array([[grid_point() for _ in range(column_number)] for _ in range(row_number)])
        self.nfilled = 0
        self.allow_table = [None] + [np.full((9, 9), 0, dtype=int) for _ in range(9)]
        self.question_board = None


    def fix_question_board(self):
        self.question_board = self.get_board()

    def get_board(self):
        board = np.zeros(shape=(9,9))
        for row in range(row_number):
            for col in range(column_number):
                board[row][col] = self.board[row][col].value
        board = board.astype(int)
        return np.array(board)

    def update_row_possible(self,row,value):
        for column in range (0,9):
            self.board[row][column].possible.discard(value)

    def update_column_possible(self,column,value):
        for row in range(0, 9):
            self.board[row][column].possible.discard(value)

    def update_box_possible(self,box,value):
        coord_list = box_to_list(box)
        for (row,column) in coord_list:
            self.board[row][column].possible.discard(value)

    def update_possible(self,row,column,value):
        self.update_row_possible(row=row,value=value)
        self.update_column_possible(column=column,value=value)
        box = index_to_box(row=row,column=column)
        self.update_box_possible(box=box,value=value)


    def update_allow_table(self,row,column,value):
        self.update_row_allow_table(row=row, value=value)
        self.update_column_allow_table(column=column, value=value)
        box = index_to_box(row=row, column=column)
        self.update_box_allow_table(box=box, value=value)


    def update_row_allow_table(self,row,value):
        for column in range(0,9):
            if self.allow_table[value][row][column] ==0:
                self.allow_table[value][row][column] = -1


    def update_column_allow_table(self,column,value):
        for row in range(0, 9):
            if self.allow_table[value][row][column] == 0:
                self.allow_table[value][row][column] = -1

    def update_box_allow_table(self,box,value):
        coords = box_to_list(box)
        for (row,column) in coords:
            if self.allow_table[value][row][column] == 0:
                self.allow_table[value][row][column] = -1

    def update_board(self,row,column,value):
        #first update the value at the position.
        if self.board[row][column].value != 0:
            raise Exception('trying to fill a filled grid')
        if value not in self.board[row][column].possible:
            raise Exception('invalid fulling')
        self.nfilled += 1
        self.board[row][column].value = value
        self.allow_table[value][row][column] = 1
        for rvalue in range(1,10):
            if rvalue != value:
                self.allow_table[rvalue][row][column] = -1
        self.update_possible(row=row,column=column,value=value)
        self.update_allow_table(row=row,column=column,value=value)

    def check_legal_move(self,row,column,value):
        legal = True
        if self.board[row][column].value != 0:
            legal = False
        if value not in self.board[row][column].possible:
            legal = False
        return legal

    def find_only_possible(self):
        '''return the first coord (and the only allowed value) of the grid which has only one possible solution'''
        for row in range(0,9):
            for column in range(0,9):
                if self.board[row][column].value == 0:
                    #print(f"coord={(row,column)},possible = {self.board[row][column].possible}")
                    if len(self.board[row][column].possible) == 1:
                        return (row,column), next(iter(self.board[row][column].possible))
        return None

    def check_sanity(self):
        def check_row(row,value):
            for col in range(column_number):
                temp = self.allow_table[value][row][col]
                if temp == 1 or temp == 0:
                    return True
            return False
        def check_col(col,value):
            for row in range(row_number):
                temp = self.allow_table[value][row][col]
                if temp == 1 or temp == 0:
                    return True
            return False
        def check_box(box,value):
            coords = box_to_list(box)
            for (row,col) in coords:
                temp = self.allow_table[value][row][col]
                if temp == 1 or temp == 0:
                    return True
            return False
        for value in range(1,10):
            for i in range (0,9):
                if check_row(i,value) == False or check_col(i,value) == False or check_box(i+1,value) == False:
                    return False
        return True




    def find_min_alternative_coord(self):
        assert self.nfilled < 81
        min_coord = (0,0)
        min_option = 100
        for row in range(row_number):
            for col in range(column_number):
                if self.board[row][col].value == 0:
                    if len(self.board[row][col].possible) < min_option:
                        min_coord = (row,col)
                        min_option = len(self.board[row][col].possible)

        return min_coord, self.board[min_coord[0]][min_coord[1]].possible

    def mandatory_transform(self):
        while True:
            if self.find_only_possible() == None and self.find_only_spot() == None:
                break
            else:
                if self.find_only_possible() != None:
                    (row, column), value = self.find_only_possible()
                else:
                    (row, column), value = self.find_only_spot()
            if self.check_legal_move(row, column, value) == False:
                raise Exception("No solution")

            self.update_board(row, column, value)
        if self.check_sanity() == False:
            raise Exception("No solution")


    def iterate_solver(self):
        if self.check_sanity() == False:
            raise Exception("No solution")

        self.mandatory_transform()

        if self.nfilled == 81:
            return self
        else:
            (row,col),alternatives = self.find_min_alternative_coord()
            for alternative in alternatives:
                try:
                    new_game = copy.deepcopy(self)
                    new_game.update_board(row,col,alternative)
                    return new_game.iterate_solver()
                except:
                    continue
            raise Exception("No solution")










    def find_only_spot(self):
        '''find the coord, and the value, of the grid which the row, column, or box limitation requires it to take certain value'''
        def row_search(row,value):
            count_one = 0
            count_zero = 0
            column_find = 0
            for column in range(0,9):
                temp = self.allow_table[value][row][column]
                if temp == 1:
                    count_one +=1
                elif temp == 0:
                    count_zero +=1
                    column_find = column
            if count_one == 0 and count_zero == 1:
                return (row,column_find),value
            else:
                return None

        def column_search(column,value):
            count_one = 0
            count_zero = 0
            row_find = 0
            for row in range(0,9):
                temp = self.allow_table[value][row][column]
                if temp == 1:
                    count_one +=1
                elif temp == 0:
                    count_zero +=1
                    row_find = row
            if count_one == 0 and count_zero == 1:
                return (row_find,column), value
            else:
                return None

        def box_search(box,value):
            count_one = 0
            count_zero = 0
            row_find = 0
            column_find = 0
            coords = box_to_list(box)
            for (row,column) in coords:
                temp = self.allow_table[value][row][column]
                if temp == 1:
                    count_one += 1
                elif temp == 0:
                    count_zero += 1
                    row_find = row
                    column_find = column

            if count_one == 0 and count_zero == 1:
                return (row_find,column_find), value
            else:
                return None

        for value in range(1,10):
            for row in range(0,9):
                if row_search(row,value) != None:
                    return row_search(row,value)

            for column in range(0,9):
                if column_search(row,value) != None:
                    return column_search(row,value)

            for box in range(1,10):
                if box_search(box,value) != None:
                    return box_search(box,value)
        return None


    def log(self,allow_table=None):
        print(f"The board has {self.nfilled} filled spot")
        print("The board of the sudoki is:")
        board = np.full((9,9),0,dtype=int)
        for i in range(0,9):
            for j in range(0,9):
                board[i][j] = self.board[i][j].value
        print(board)
        if allow_table !=None:
            print(self.allow_table[allow_table])

    def fancy_log(self):
        display_sudoku_board(original_grid=self.question_board,solved_grid=self.get_board())


    def print_possible(self,row,column):
        print(self.board[row][column].possible)




if __name__ == '__main__':
    print(box_to_list(4))
    game = sudoki()



    '''
    game.update_board(0,0,1)
    game.update_board(2, 0, 2)
    game.update_board(4, 1, 3)
    game.update_board(7,2,3)
    '''

    '''
    game.update_board(row=0, column=0, value=5)
    game.update_board(row=0, column=1, value=3)
    game.update_board(row=0, column=4, value=7)
    game.update_board(row=1, column=0, value=6)
    game.update_board(row=1, column=3, value=1)
    game.update_board(row=1, column=4, value=9)
    game.update_board(row=1, column=5, value=5)
    game.update_board(row=2, column=1, value=9)
    game.update_board(row=2, column=2, value=8)
    game.update_board(row=2, column=7, value=6)
    game.update_board(row=3, column=0, value=8)
    game.update_board(row=3, column=4, value=6)
    game.update_board(row=3, column=8, value=3)
    game.update_board(row=4, column=0, value=4)
    game.update_board(row=4, column=3, value=8)
    game.update_board(row=4, column=5, value=3)
    game.update_board(row=4, column=8, value=1)
    game.update_board(row=5, column=0, value=7)
    game.update_board(row=5, column=4, value=2)
    game.update_board(row=5, column=8, value=6)
    game.update_board(row=6, column=1, value=6)
    game.update_board(row=6, column=6, value=2)
    game.update_board(row=6, column=7, value=8)
    game.update_board(row=7, column=3, value=4)
    game.update_board(row=7, column=4, value=1)
    game.update_board(row=7, column=5, value=9)
    game.update_board(row=7, column=8, value=5)
    game.update_board(row=8, column=4, value=8)
    game.update_board(row=8, column=7, value=7)
    game.update_board(row=8, column=8, value=9)
    '''

    '''
    game.update_board(row=0, column=1, value=4)
    game.update_board(row=0, column=7, value=7)

    game.update_board(row=1, column=3, value=5)
    game.update_board(row=1, column=7, value=8)
    game.update_board(row=1, column=8, value=1)

    game.update_board(row=2, column=3, value=9)
    game.update_board(row=2, column=4, value=3)
    game.update_board(row=2, column=5, value=6)


    game.update_board(row=3, column=7, value=1)
    game.update_board(row=3, column=8, value=9)

    game.update_board(row=4, column=0, value=5)
    game.update_board(row=4, column=8, value=7)

    game.update_board(row=5, column=0, value=7)
    game.update_board(row=5, column=1, value=9)

    game.update_board(row=6, column=4, value=6)
    game.update_board(row=6, column=5, value=7)

    game.update_board(row=7, column=0, value=6)
    game.update_board(row=7, column=3, value=4)
    game.update_board(row=7, column=5, value=8)

    game.update_board(row=8, column=1, value=7)
    game.update_board(row=8, column=7, value=6)
    '''
    '''
    game.update_board(row=0, column=4, value=1)
    game.update_board(row=0, column=7, value=9)

    game.update_board(row=1, column=5, value=4)
    game.update_board(row=1, column=6, value=8)

    game.update_board(row=2, column=0, value=8)
    game.update_board(row=2, column=2, value=7)
    game.update_board(row=2, column=3, value=3)

    game.update_board(row=3, column=1, value=2)
    game.update_board(row=3, column=4, value=9)
    game.update_board(row=3, column=6, value=1)

    game.update_board(row=4, column=0, value=4)
    game.update_board(row=4, column=4, value=2)
    game.update_board(row=4, column=5, value=6)

    game.update_board(row=5, column=1, value=6)

    game.update_board(row=6, column=2, value=5)
    game.update_board(row=6, column=8, value=4)

    game.update_board(row=7, column=1, value=3)
    game.update_board(row=7, column=2, value=4)
    game.update_board(row=7, column=8, value=1)

    game.update_board(row=8, column=6, value=9)
    game.update_board(row=8, column=7, value=6)
    '''

    game.update_board(row=0, column=1, value=7)
    game.update_board(row=0, column=4, value=5)
    game.update_board(row=0, column=7, value=8)

    game.update_board(row=1, column=0, value=5)
    game.update_board(row=1, column=3, value=7)
    game.update_board(row=1, column=5, value=3)
    game.update_board(row=1, column=8, value=9)

    game.update_board(row=2, column=2, value=1)
    game.update_board(row=2, column=6, value=6)

    game.update_board(row=3, column=1, value=1)
    game.update_board(row=3, column=4, value=3)
    game.update_board(row=3, column=7, value=6)

    game.update_board(row=4, column=0, value=8)
    game.update_board(row=4, column=3, value=6)
    game.update_board(row=4, column=5, value=9)
    game.update_board(row=4, column=8, value=3)

    game.update_board(row=5, column=1, value=6)
    game.update_board(row=5, column=4, value=8)
    game.update_board(row=5, column=7, value=2)

    game.update_board(row=6, column=2, value=4)
    game.update_board(row=6, column=6, value=2)

    game.update_board(row=7, column=0, value=6)
    game.update_board(row=7, column=3, value=3)
    game.update_board(row=7, column=5, value=4)
    game.update_board(row=7, column=8, value=5)

    game.update_board(row=8, column=1, value=5)
    game.update_board(row=8, column=4, value=7)
    game.update_board(row=8, column=7, value=3)

    game.fix_question_board()


    # game.fancy_log()
    print(f"After rudimentary strategy, we get...")
    game.mandatory_transform()
    game.log()

    try:
        print(f"After recurrent algorithm, we solve...")
        ans = game.iterate_solver()
        ans.log()
    except:
        print("Unfortunately, the suduko is unsolvable")


    ans.fancy_log()


    '''
    coord,option = game.find_min_alternative_coord()
    print(f"coord={coord},alternatives={option}")
    '''
