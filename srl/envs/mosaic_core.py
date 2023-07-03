from ctypes import *
import os
from typing import Iterable, Optional


class Game:
    __size: int
    __board_buffer_size: int
    __pointer: int
    __lib: CDLL

    def __init__(self, size: int):
        self.__lib = load_library()
        self.__size = size
        self.__board_buffer_size = sum([i * i for i in range(1, size + 1)])
        self.__pointer = self.__lib.create(size)

    def __del__(self):
        try:
            self.__lib.destroy(self.__pointer)
        except AttributeError:
            pass

    def is_legal_move(self, move: int) -> bool:
        return c_bool(self.__lib.isLegalMove(self.__pointer, move)).value

    def make_move(self, move: int):
        self.__lib.makeMove(self.__pointer, move)

    @property
    def is_over(self) -> bool:
        return c_bool(self.__lib.isOver(self.__pointer)).value

    @property
    def pieces_per_player(self) -> int:
        return c_int(self.__lib.piecesPerPlayer(self.__pointer)).value

    @property
    def player_score(self) -> int:
        return c_int(self.__lib.playerScore(self.__pointer)).value

    @property
    def opponent_score(self) -> int:
        return c_int(self.__lib.opponentScore(self.__pointer)).value

    @property
    def first_score(self) -> int:
        return c_int(self.__lib.firstScore(self.__pointer)).value

    @property
    def second_score(self) -> int:
        return c_int(self.__lib.secondScore(self.__pointer)).value

    @property
    def is_first_turn(self) -> bool:
        return c_bool(self.__lib.isFirstTurn(self.__pointer)).value

    @property
    def is_second_turn(self) -> bool:
        return c_bool(self.__lib.isSecondTurn(self.__pointer)).value

    @property
    def first_wins(self) -> bool:
        return c_bool(self.__lib.firstWins(self.__pointer)).value

    @property
    def second_wins(self) -> bool:
        return c_bool(self.__lib.secondWins(self.__pointer)).value

    @property
    def player_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyPlayerBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def opponent_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyOpponentBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def first_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyFirstBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def second_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copySecondBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def neutral_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyNeutralBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def legal_board(self) -> str:
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyLegalBoard(c_void_p(self.__pointer), buffer)
        return buffer.value.decode()

    @property
    def legal_moves(self):
        buffer = create_string_buffer(self.__board_buffer_size)
        self.__lib.copyLegalBoard(c_void_p(self.__pointer), buffer)
        tuples = [(index, bit) for index, bit in enumerate(list(reversed(buffer.value.decode())))]
        filtered = filter(lambda t: t[1] == '1', tuples)
        return map(lambda f: f[0], filtered)

    @property
    def moves_made(self) -> int:
        return c_int(self.__lib.movesMade(self.__pointer)).value

    @property
    def moves(self) -> Iterable[int]:
        return map(lambda i: self.get_move(i), range(self.moves_made))

    def get_move(self, move_index: int) -> int:
        return c_int(self.__lib.getMove(self.__pointer, move_index)).value

    @property
    def last_move(self) -> Optional[int]:
        return None if self.moves_made == 0 else self.get_move(self.moves_made - 1)


for p in os.environ['PATH'].split(os.pathsep):
    if os.path.isdir(p):
        os.add_dll_directory(p)
os.add_dll_directory(os.path.dirname(__file__))


def load_library():
    is_windows = os.name == 'nt'
    path = 'libmosaicgame.dll' if is_windows else os.path.join(os.path.dirname(__file__), 'libmosaicgame.dll')
    lib = cdll.LoadLibrary(path)
    lib.create.argtypes = (c_uint8,)
    lib.create.restype = c_void_p
    lib.destroy.argtypes = (c_void_p,)
    lib.destroy.restype = None
    lib.copyPlayerBoard.argtypes = (c_void_p, c_char_p)
    lib.copyPlayerBoard.restype = None
    lib.copyOpponentBoard.argtypes = (c_void_p, c_char_p)
    lib.copyOpponentBoard.restype = None
    lib.piecesPerPlayer.argtypes = (c_void_p,)
    lib.piecesPerPlayer.restype = c_uint16
    lib.playerScore.argtypes = (c_void_p,)
    lib.playerScore.restype = c_uint16
    lib.opponentScore.argtypes = (c_void_p,)
    lib.opponentScore.restype = c_uint16
    lib.firstScore.argtypes = (c_void_p,)
    lib.firstScore.restype = c_uint16
    lib.secondScore.argtypes = (c_void_p,)
    lib.secondScore.restype = c_uint16
    lib.isOver.argtypes = (c_void_p,)
    lib.isOver.restype = c_bool
    lib.isFirstTurn.argtypes = (c_void_p,)
    lib.isFirstTurn.restype = c_bool
    lib.isSecondTurn.argtypes = (c_void_p,)
    lib.isSecondTurn.restype = c_bool
    lib.firstWins.argtypes = (c_void_p,)
    lib.firstWins.restype = c_bool
    lib.secondWins.argtypes = (c_void_p,)
    lib.secondWins.restype = c_bool
    lib.isLegalMove.argtypes = (c_void_p, c_uint)
    lib.isLegalMove.restype = c_bool
    lib.makeMove.argtypes = (c_void_p, c_uint)
    lib.makeMove.restype = None
    # lib.undo.argtypes = (c_void_p, c_uint16)
    # lib.undo.restype = None
    lib.movesMade.argtypes = (c_void_p,)
    lib.movesMade.restype = c_uint16
    lib.getMove.argtypes = (c_void_p, c_uint16)
    lib.getMove.restype = c_uint16
    # lib.getTransformedMove.argtypes = (c_void_p, c_uint16)
    # lib.getTransformedMove.restype = c_uint16
    # lib.flipVertical.argtypes = (c_void_p,)
    # lib.flipVertical.restype = None
    # lib.mirrorHorizontal.argtypes = (c_void_p,)
    # lib.mirrorHorizontal.restype = None
    # lib.flipDiagonal.argtypes = (c_void_p,)
    # lib.flipDiagonal.restype = None
    # lib.rotate90.argtypes = (c_void_p,)
    # lib.rotate90.restype = None
    # lib.rotate180.argtypes = (c_void_p,)
    # lib.rotate180.restype = None
    # lib.rotate270.argtypes = (c_void_p,)
    # lib.rotate270.restype = None
    # lib.flipVertical.argtypes = (c_void_p,)
    # lib.flipVertical.restype = None
    # lib.transform.argtypes = (c_void_p,)
    # lib.transform.restype = None
    # lib.resetTransformation.argtypes = (c_void_p,)
    # lib.resetTransformation.restype = None
    return lib
