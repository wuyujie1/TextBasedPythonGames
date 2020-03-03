"""
An implementation of Stonehenge.
"""
from game import Game
from stonehenge_state import StonehengeState


class StonehengeGame(Game):
    """
    Game stonehenge which to be played with two players.
    """

    def __init__(self, is_p1_turn: bool) -> None:
        """
        Initialize a new stonehenge game.
        """
        side_length = int(input("Enter the length of side you wish to play:"))
        i = 0
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.grid = []
        grid = []
        for length in range(2, side_length + 2):
            while length > 0:
                grid.append(alpha[i])
                i += 1
                length -= 1
            self.grid.append(grid)
            grid = []
        for leng in range(0, side_length):
            if leng >= 0:
                grid.append(alpha[i])
                i += 1
        self.grid.append(grid)
        self.current_state = StonehengeState(is_p1_turn, self.grid)


    def get_instructions(self) -> str:
        """
        Return the instruction of the game
        """
        return "Players take turns claiming cells. When a player captures" \
    " at least half of the cells in a ley-line, then player" \
    " captures the ley-line. Player wins when captures at" \
    " least half of the lay-lines."

    def is_over(self, state: StonehengeState) -> bool:
        """
        Return whether or not this game is over.
        """
        p1score = 0
        p2score = 0
        check = len(state.at) / 2
        for item in state.at:
            if state.at[item] == 1:
                p1score += 1
            elif state.at[item] == 2:
                p2score += 1
        return p1score >= check or p2score >= check

    def is_winner(self, player: str) -> bool:
        """
        Return whether player has won the game.
        """
        return (self.is_over(self.current_state) and
                self.current_state.get_current_player_name() != player)

    def str_to_move(self, string: str) -> str:
        """
        Return the move in the format that wanted.
        """
        if not string.strip().isalpha() or len(string) != 1:
            return 'Z'

        return string.strip().upper()

if __name__ == "__main__":
    from python_ta import check_all
    check_all(config="a2_pyta.txt")
