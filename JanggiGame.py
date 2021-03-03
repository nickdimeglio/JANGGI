# Author: Nick DiMeglio
# Date: 11 March 2021
# Description: A class for playing the abstract board game Janggi


class Piece:
	"""A class for pieces"""
	def __init__(self, player, rank):
		"""Create a piece"""
		self._player = player
		self._rank = rank

	def get_player(self):
		"""Get a piece's player ('blue' or 'red')"""
		return self._player

	def get_rank(self):
		"""Return a pieces' rank"""
		return self._rank


def legal_move(rank, a, b):
	"""Return true if the given rank can move from square a to square b"""
	if rank == 'general':
		if a == b:
			return True

	if rank == 'guard':
		return True

	if rank == 'horse':
		return True

	if rank == 'elephant':
		return True

	if rank == 'chariot':
		return True

	if rank == 'cannon':
		return True

	if rank == 'soldier':
		return True


class JanggiGame:
	def __init__(self):
		self._game_state = 'UNFINISHED'
		self._pieces = {
			'a1': Piece('red', 'chariot'), 'b1': Piece('red', 'elephant'),
			'c1': Piece('red', 'horse'), 'd1': Piece('red', 'guard'), 'e1': None,
			'f1': Piece('red', 'guard'), 'g1': Piece('red', 'elephant'),
			# TODO: FINISH PIECE INITIALIZATION
		}
		self._turn = 'blue'

	def get_game_state(self):
		"""Get the current state of the game"""
		return self._game_state

	def find_general(self, player):
		"""Returns the square of the player's general"""
		for square, piece in self._pieces.items():
			if piece.get_player() == player and piece.get_rank() == 'general':
				return square

	def is_in_check(self, player):
		"""Returns True if the player is in check"""
		if player == 'blue':
			opponent = 'red'
		else:
			opponent = 'blue'

		hideout = self.find_general(player)

		in_check = False
		# Check each of the other team's pieces to see if they capture
		for square, piece in self._pieces.items():
			if piece.get_player() == opponent:
				if legal_move(piece.get_rank(), square, hideout):
					in_check = True

		return in_check

	def is_in_checkmate(self, player):
		if player == 'blue':
			opponent = 'red'
		else:
			opponent = 'blue'

		hideout = self.find_general(player)

		# CHECK IF THE GENERAL IS IN CHECK
		# CHECK IF THE GENERAL WOULD BE IN CHECK IF IT MOVED TO
		# EACH OF IT'S 8 POSSIBLE SPACES

		return False

	def make_move(self, a, b):
		"""Move the piece in square a to square b, if possible"""
		# Check if the game is finished
		if self._game_state != 'UNFINISHED':
			return False

		# Check if the right player i playing
		if self._pieces[a].get_player() != self._turn:
			return False

		# Check if the player has a piece in the intended square
		if self._pieces[a].get_player() == self._pieces[b].get_player():
			return False

		# Check if the move is legal
		if legal_move(self._pieces[a].get_rank(), a, b):

			# MOVE THE PIECE

			if self._turn == 'blue':
				self._turn = 'red'

			if self._turn == 'red':
				self._turn = 'blue'

			if self.is_in_checkmate(self._turn):
				if self._turn == 'blue':
					self._game_state = 'RED_WON'
				if self._turn == 'red':
					self._game_state = 'BLUE_WON'

			return True

