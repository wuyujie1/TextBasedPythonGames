"""
An implementation of a state for Stonehenge.
"""
from typing import Any
import copy
from game_state import GameState


class StonehengeState(GameState):
    """
    The state of a stonehenge game at a certain point in time.
    """

    def __init__(self, is_p1_turn: bool, grid: list) -> None:
        """
        Initialize this game satate and set the current player based on
        is_p1_turn.

        >>> grid = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        >>> state = StonehengeState(True, grid)
        >>> state.at
        {0: '@', 1: '@', 2: '@', 3: '@', 4: '@', 5: '@', 6: '@', 7: '@', 8: '@'}
        >>> state.lay
        [['A', 'C'], ['B', 'D', 'F'], ['E', 'G'], ['B', 'E'], ['A', 'D', 'G'],\
 ['C', 'F']]
        """
        GameState.__init__(self, is_p1_turn)
        self.grid = grid
        self.lay = []
        l = []
        for i in range(0, len(self.grid) - 1):
            l.append(self.grid[i][0])
        self.lay.append(l)
        l = []
        for ii in range(1, len(self.grid)):
            for item in self.grid:
                if len(item) > ii and\
                        self.grid.index(item) != len(self.grid) - 1:
                    l.append(item[ii])
                elif self.grid.index(item) == len(self.grid) - 1:
                    l.append(item[ii - 1])
            self.lay.append(l)
            l = []
        for iii in range(-1, -1* len(self.grid) - 1, -1):
            for itm in self.grid:
                if -1 * len(itm) <= iii and\
                        self.grid.index(itm) != len(self.grid) - 1:
                    l.append(itm[iii])
                elif self.grid.index(itm) == len(self.grid) -1 and iii != -1:
                    l.append(itm[iii + 1])
            self.lay.append(l)
            l = []
        self.at = {}
        for iiii in range(0, 3 * len(self.grid)):
            self.at[iiii] = '@'

    def __str__(self) -> str:
        """
        Return a string representation of the current state of the game.
        """
        ifront = 2 * len(self.grid)
        iback = 2
        s = '\n'
        ss = ''
        down = '/ \\ '
        up = '\\ / '
        s += ((len(self.grid) - 1) * 2 + 4)\
             * ' ' + str(self.at[0]) + 3 * ' ' + str(self.at[1]) + '\n' +\
             ((len(self.grid) - 1) * 2 + 3) * ' ' + '/   /\n'
        for item in self.grid:
            ss += ((len(self.grid) - len(item) + 1) * 2 - 2)\
                  * ' ' + str(self.at[ifront])
            for itm in item:
                ss += str(itm)
            ss = ss[:((len(self.grid) - len(item) + 1) * 2) - 2] +\
                 ' - '.join(ss[((len(self.grid) - len(item) + 1)
                                * 2) - 2:])
            if self.grid.index(item) != len(self.grid) - 2:
                ss += '   ' + str(self.at[iback]) + '\n'
                iback += 1
            ifront += 1
            if self.grid.index(item) < len(self.grid) - 2:
                s += ss + ((len(self.grid) - self.grid.index(item) - 1)
                           * 2 + 1) * ' ' + len(item) * down + down[0] + '\n'
            elif self.grid.index(item) == len(self.grid) - 2:
                s += ss + ((len(self.grid) - self.grid.index(item) - 1)
                           * 2 + 3) * ' ' + '\n' +\
                     '     ' + (len(item) - 1) * up + up[0] + '\n'
            elif self.grid.index(item) == len(self.grid) - 1:
                s += ss + '       ' +\
                     '   '.join(len(item) * '\\') + '\n'
                ss = ''
                for r in range(2 * len(self.grid) - 1, iback - 1, -1):
                    ss += str(self.at[r])
                s += '        ' + '   '.join(ss) + '\n'
            ss = ''
        return s

    def get_possible_moves(self) -> list:
        """
        Retuan all possible moves for the current player.

        >>> grid = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        >>> state = StonehengeState(True, grid)
        >>> state.get_possible_moves()
        ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        """
        moves = []
        count1 = 0
        count2 = 0
        for item in self.at:
            if self.at[item] == 1:
                count1 += 1
            elif self.at[item] == 2:
                count2 += 1
        for line in self.grid:
            for cell in line:
                if str(cell).isalpha():
                    moves.append(cell)
        if count1 >= len(self.at) / 2 or count2 >= len(self.at) / 2:
            moves = []
        return moves

    def make_move(self, move: Any) -> "StonehengeState":
        """
        Return a new stonehenge state after player made a move.

        >>> grid = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        >>> state = StonehengeState(True, grid)
        >>> new_state = state.make_move('D')
        >>> new_state.grid
        [['A', 'B'], ['C', 1, 'E'], ['F', 'G']]
        """
        m = str(move)
        new_state = copy.deepcopy(self)
        player = int(self.get_current_player_name()[1])
        for lines in new_state.grid:
            for cells in lines:
                if cells == m:
                    new_state.grid[new_state.grid.index(
                        lines)][lines.index(cells)] = player
        for lay in new_state.lay:
            for cell in lay:
                if cell == m:
                    new_state.lay[new_state.lay.index(lay)][lay.index(cell)] =\
                        player
        for linenum in range(2 * len(new_state.grid), 3 * len(new_state.grid)):
            if new_state.grid[linenum - 2 * len(new_state.grid)].count(1) >=\
                    len(new_state.grid[linenum - 2 * len(new_state.grid)]) / 2\
                    and new_state.at[linenum] == '@':
                new_state.at[linenum] = 1
            elif new_state.grid[linenum - 2 * len(new_state.grid)].count(2) >= \
                    len(new_state.grid[linenum - 2 * len(new_state.grid)]) / 2\
                    and new_state.at[linenum] == '@':
                new_state.at[linenum] = 2
        for rightlay in range(0, len(new_state.grid)):
            if new_state.lay[rightlay].count(1) >= len(new_state.lay[rightlay])\
                    / 2 and new_state.at[rightlay] == '@':
                new_state.at[rightlay] = 1
            elif new_state.lay[rightlay].count(2) >= len(
                    new_state.lay[rightlay])\
                    / 2 and new_state.at[rightlay] == '@':
                new_state.at[rightlay] = 2
        for leftlay in range(len(new_state.grid), 2 * len(new_state.grid)):
            if new_state.lay[leftlay].count(1) >= len(new_state.lay[leftlay])\
                    / 2 and new_state.at[leftlay] == '@':
                new_state.at[leftlay] = 1
            elif new_state.lay[leftlay].count(2) >= len(new_state.lay[leftlay])\
                    / 2 and new_state.at[leftlay] == '@':
                new_state.at[leftlay] = 2
        if self.p1_turn:
            new_state.p1_turn = False
        else:
            new_state.p1_turn = True
        return new_state

    def __repr__(self) -> str:
        """
        Return a representation of this state.
        """
        return "P1's Turn: {} - Grids: {} - Lays: {}".format(
            self.p1_turn, self.grid, self.lay)

    def rough_outcome(self) -> float:
        """
        Return an estimate in interval
        [LOSE, WIN] of best outcome of current player.

        >>> grid = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        >>> state = StonehengeState(True, grid)
        >>> state.rough_outcome()
        -1

        >>> anothergrid = [['A', 'B'], ['C']]
        >>> anotherstate = StonehengeState(True, anothergrid)
        >>> anotherstate.make_move('A').rough_outcome()
        -1
        """
        lst = []
        for move in self.get_possible_moves():
            i = self.lines_occupied(move)
            if i >= (len(self.grid) + len(self.lay)) / 2:
                return self.WIN
        for mov in self.get_possible_moves():
            for m in self.make_move(mov).get_possible_moves():
                if self.make_move(mov).lines_occupied(m) >= \
                        (len(self.grid) + len(self.lay)) / 2:
                    lst.append(False)
        if all(lst):
            return self.LOSE
        return self.DRAW

    def lines_occupied(self, move: str) -> int:
        """
        Return the number of lays and lines that current player occupied.

        >>> grid = [['A', 'B'], ['C', 'D', 'E'], ['F', 'G']]
        >>> state = StonehengeState(True, grid)
        >>> state.lines_occupied('A')
        2

        >>> anothergrid = [['A', 'B'], ['C']]
        >>> anotherstate = StonehengeState(True, anothergrid)
        >>> anotherstate.lines_occupied('C')
        3
        """
        player = int(self.get_current_player_name()[1])
        i = 0
        for lines in self.make_move(move).grid:
            if lines.count(player) >= len(lines) / 2:
                i += 1
        for line in self.make_move(move).lay:
            if line.count(player) >= len(line) / 2:
                i += 1
        return i

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
