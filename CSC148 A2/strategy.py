"""
A module for strategies.

NOTE: Make sure this file adheres to python-ta.
Adjust the type annotations as needed, and implement both a recursive
and an iterative version of minimax.
"""
from typing import Any
from game_state import GameState
from game import Game

# TODO: Adjust the type annotation as needed.
def interactive_strategy(game: Game) -> Any:
    """
    Return a move for game through interactively asking the user for input.
    """
    move = input("Enter a move: ")
    return game.str_to_move(move)

# TODO: Implement a recursive version of the minimax strategy.
def recursive_helper(game: Game, state: GameState) -> list:
    """
    Helper function for recursive minimax strategy, return score of each move.
    """
    if not game.is_over(state):
        return [-1 * item for item in sum(
            [recursive_helper(game, state.make_move(x))
             for x in state.get_possible_moves()], [])]
    elif game.is_winner(state.get_current_player_name()):
        return [-1]
    return [1]

def recursive_minimax_strategy(game: Game) -> Any:
    """
    Return a move for game through recursive minimax strategy.
    """
    lst = []
    for item in game.current_state.get_possible_moves():
        if max(recursive_helper(game, game.current_state.make_move(item))) > 0:
            lst.append(item)
    if not lst:
        for itemm in game.current_state.get_possible_moves():
            if max(recursive_helper(game, game.current_state.make_move(itemm)))\
                    == 0:
                lst.append(itemm)
    for moves in lst:
        for move in game.current_state.make_move(moves).get_possible_moves():
            if game.is_over(game.current_state.make_move(
                    moves).make_move(move)):
                return [mov for mov in lst if not\
                    game.is_over(game.current_state.make_move(
                        mov).make_move(move))][-1]
    if not lst:
        lst.extend(game.current_state.get_possible_moves())
    return lst[-1]

# TODO: Implement an iterative version of the minimax strategy.
class MinimaxNode:
    """
    Class containes state of game before putting into stack.
    """

    def __init__(self, state: GameState, move=None, children=None) -> None:
        """Initilize a new node which stores a state of game."""
        self.state = state
        self.score = None
        self.children = children
        self.move = move


def iterative_minimax_strategy(game: Game) -> Any:
    """
    Return a move for game through iterative minimax strategy.
    """
    stack = []
    a = MinimaxNode(game.current_state)
    stack.append(a)
    while stack:
        node = stack.pop()
        if node.children and node.state != a.state:
            for ch in node.children:
                node.score.extend([-1 * x for x in ch.score])
        elif not node.children:
            stack.append(node)
            node.children = [MinimaxNode(node.state.make_move(move), str(move))
                             for move in node.state.get_possible_moves()]
            for c in node.children:
                c.score = [1 if game.is_winner(
                    c.state.get_current_player_name()) else None]
                c.score = [-1 if not game.is_winner(
                    c.state.get_current_player_name()) and game.is_over(
                        c.state) else 0]
            stack.extend([ch for ch in
                          node.children if ch.state.get_possible_moves()])
    for item in a.children:
        if min(item.score) < 0:
            stack.append(game.str_to_move(item.move))
    if not stack:
        for itemm in a.children:
            if min(itemm.score) == 0:
                stack.append(game.str_to_move(itemm.move))
    for moves in stack:
        for move in game.current_state.make_move(moves).get_possible_moves():
            if game.is_over(game.current_state.make_move(
                    moves).make_move(move)):
                return [mov for mov in stack if not\
                    game.is_over(game.current_state.make_move(
                        mov).make_move(move))][-1]
    if stack:
        return stack[-1]
    return game.current_state.get_possible_moves()[0]

if __name__ == "__main__":
    from python_ta import check_all

    check_all(config="a2_pyta.txt")
