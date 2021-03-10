# Author: Nick DiMeglio
# Date: 11 March 2021
# Description: A class for playing the abstract board game Janggi


class Piece:
	"""A class for pieces. A dictionary of these pieces is instantiated
	for each team when a new JanggiGame is created. This class does
	not need to communicate with any other classes, but the legal move
	function and the JanggiGame class will need to access rank and player,
	so we provide getters for those private data members."""
	def __init__(self, player, rank):
		"""Create a piece by providing a player ('blue' or 'red') and a rank,
		which can be any of the ranks of Janggi pieces such as 'general'
		or 'elephant'. This function returns a Piece instance."""
		self._player = player
		self._rank = rank

	def to_string(self):
		"""Takes no parameters and returns nothing. Creates a string
		representing a piece for printing the board."""
		player = self._player[0]
		rank = self._rank[0:2].upper()
		return (" " + player + rank + " ")


	def get_player(self):
		"""Get a piece's player ('blue' or 'red'). No parameters, return
		type is a string 'blue' or 'red'."""
		return self._player

	def get_rank(self):
		"""Return a pieces' rank (for determining how it can move). No
		parameters, return type is a string like 'general' or 'elephant'."""
		return self._rank

class JanggiGame:
	"""This class creates a board represented by a dictionary whose keys
	are squares and whose values are pieces. An empty square has the value
	None. The JanggiGame class can get the game state (unfinished, blue_won,
	or red_won), check if a player is in check, and check if a player is in
	checkmate. It will also keep track of whose turn it is, starting with blue.
	The make_move function can move a piece to a new square based on the rules
	of Janggi. This class will need to communicate with the Piece class,
	because certain functions (like find_general) need to access the Rank
	data member of Piece to guide behavior."""

	def __init__(self):
		"""Instantiates a new JanggiGame. No parameters, returns
		a new JanggiGame ready to be played."""
		self._game_state = 'UNFINISHED'
		self._pieces = {

			# Row 1
			'a1': Piece('red', 'chariot'), 'b1': Piece('red', 'elephant'),
			'c1': Piece('red', 'horse'), 'd1': Piece('red', 'guard'), 'e1': None,
			'f1': Piece('red', 'guard'), 'g1': Piece('red', 'elephant'),
			'h1': Piece('red', 'horse'), 'i1': Piece('red', 'chariot'),

			# Row 2
			'a2': None, 'b2': None, 'c2': None, 'd2': None,
			'e2': Piece('red', 'general'), 'f2': None, 'g2': None, 'h2': None,
			'i2': None,

			# Row 3
			'a3': None, 'b3': Piece('red', 'cannon'), 'c3': None, 'd3': None,
			'e3': None, 'f3': None, 'g3': None, 'h3': Piece('red', 'cannon'),
			'i3': None,

			# Row 4
			'a4': Piece('red', 'soldier'), 'b4': None, 'c4': Piece('red', 'soldier'),
			'd4': None, 'e4': Piece('red', 'soldier'), 'f4': None, 
			'g4': Piece('red', 'soldier'), 'h4': None, 'i4': Piece('red', 'soldier'),	
			# Row 5
			'a5': None, 'b5': None, 'c5': None, 'd5': None, 'e5': None, 'f5': None,
			'g5': None, 'h5': None, 'i5': None,

			# Row 6
			'a6': None, 'b6': None, 'c6': None, 'd6': None, 'e6': None, 'f6': None,
			'g6': None, 'h6': None, 'i6': None,

			# Row 7
			'a7': Piece('blue', 'soldier'), 'b7': None, 'c7': Piece('blue', 'soldier'),
			'd7': None, 'e7': Piece('blue', 'soldier'), 'f7': None,
			'g7': Piece('blue', 'soldier'), 'h7': None, 'i7': Piece('blue', 'soldier'),

			# Row 8
			'a8': None, 'b8': Piece('blue', 'cannon'), 'c8': None, 'd8': None,
			'e8': None, 'f8': None, 'g8': None, 'h8': Piece('blue', 'cannon'),
			'i8': None,

			# Row 9
			'a9': None, 'b9': None, 'c9': None, 'd9': None,
			'e9': Piece('blue', 'general'), 'f9': None, 'g9': None, 'h9': None,
			'i9': None,

			# Row 10
			'a10': Piece('blue', 'chariot'), 'b10': Piece('blue', 'elephant'),
			'c10': Piece('blue', 'horse'), 'd10': Piece('blue', 'guard'),
			'e10': None, 'f10': Piece('blue', 'guard'),
			'g10': Piece('blue', 'elephant'), 'h10': Piece('blue', 'horse'),
			'i10': Piece('blue', 'chariot'),

		}
		self._turn = 'blue'
		# An ordered list of the board's columns for calculating moves
		self._columns = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']


	def print_board(self):
		"""Print a representation of the current state of the Janggi
		board. No parameters, no return value."""
		for row in range(1, 11):
			line = ""
			for column in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']:
				square = column + str(row)
				piece = self._pieces[square]
				if piece:
					line += piece.to_string()
				else:
					line += " --- " 
			print(line)

	def get_game_state(self):
		"""Get the current state of the game. No parameters, returns
		one of: 'UNFINISHED', 'BLUE_WON', 'RED_WON'"""
		return self._game_state

	
	# Functions for finding adjacent squares
	def above(self, square):
		"""Returns the square above the provided square"""
		col = square[0]
		row = square[1]
		if row == '1':
			return None
		else:
			row = str(int(row) - 1)
		
		return col + row

	def below(self, square):
		"""Returns the square below the provided square"""
		col = square[0]
		row = square[1]

		if row == '10':
			return None
		else:
			row = str(int(row) + 1)

		return col + row

	def right_of(self, square):
		"""Returns the square to the right of the provided square"""
		col = square[0]
		row = square[1]

		if col == 'i':
			return None
		else:
			col_index = self._columns.index(col)
			col = str(self._columns[col_index + 1])
		
		return col + row
		
	def left_of(self, square):
		"""Returns the square to the left of the provided square"""
		col = square[0]
		row = square[1]

		if col == 'a':
			return None
		else:
			col_index = self._columns.index(col)
			col = self._columns[col_index - 1]
	
		return col + row

	def legal_move(self, piece, a, b):
		"""Return true if the given rank can move from square a to square b. It
		is assumed that b is empty or contains a piece from the opponent of player
		whose piece is in square a. This function is used by the JanggiGame class."""
	
		rank = piece.get_rank()
		player = piece.get_player()

		if rank == 'general' or rank == 'guard':
			# Mapping of valid squares the general/guards can move to
			moves = {
				'red': {
					'd1': ['e1', 'd2', 'e2'], 'e1': ['d1', 'f1', 'e2'],
					'f1': ['e1', 'e2', 'f2'], 'd2': ['d1', 'e2', 'd3'],
					'e2': ['d1', 'e1', 'f1', 'd2', 'f2', 'd3', 'e3', 'f3'],
					'f2': ['f1', 'e2', 'f3'], 'd3': ['d2', 'e2', 'e3'],
					'e3': ['e2', 'd3', 'f3'], 'f3': ['e2', 'f2', 'e3'],
					},

				'blue': {
					'd8': ['e8', 'd9', 'e9'], 'e8': ['d8', 'f8', 'e9'],
					'f8': ['e8', 'e9', 'f9'], 'd9': ['d8', 'e9', 'd10'],
					'e9': ['d8', 'e8', 'f8', 'd9', 'f9', 'd10', 'e10', 'f10'],
					'f9': ['f8', 'e9', 'f10'], 'd10': ['d9', 'e9', 'e10'],
					'e10': ['e9', 'd10', 'f10'], 'f10': ['e9', 'f9', 'e10'],
					},	
				}
	
			valid_squares = moves[player][a]

			return (b in valid_squares)

		elif rank == 'horse':
			#TODO implement legal horse moves
			# The fourse has eight possible squares to move to
			# The path to each square must be checked for blocking pieces
			moves = []

			up = self.above(a)		
			down = self.below(a)
			left  = self.left_of(a)
			right = self.right_of(a)

			if not up:
				moves.append(self.above(self.left_of(up)))		# Up and left
				moves.append(self.above(self.right_of(up)))		# Up and right 

			if not down:
				moves.append(self.below(self.left_of(down)))		# Down and left
				moves.append(self.below(self.right_of(down)))		# Down and right

			if not left:
				moves.append(self.left_of(self.below(left)))		# Left and down
				moves.append(self.left_of(self.above(left)))		# Left and up

			if not right:
				moves.append(self.right_of(self.below(right)))	# Right and down
				moves.append(self.right_of(self.above(right)))	# Right and up

			return (b in moves)

		elif rank == 'elephant':
			#TODO implement legal elephant moves
			return True

		elif rank == 'chariot':
			#TODO implement legal chariot moves
			return True

		elif rank == 'cannon':
			#TODO implement legal cannon moves
			return True

		elif rank == 'soldier':
			#TODO implement legal soldier moves
			return True

	def find_general(self, player):
		"""Takes a player ('blue' or 'red') as a parameter and returns
		the name of the square which holds that player's general"""
		for square, piece in self._pieces.items():



			if piece.get_player() == player and piece.get_rank() == 'general':
				return square

	def is_in_check(self, player):
		"""Takes a player ('blue' or 'red') as a parameter and returns
		True if that player is in check, False otherwise."""
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
		"""Takes a player ('blue' or 'red') as a parameter and returns
		True if that player is in checkmate, False otherwise."""
		if player == 'blue':
			opponent = 'red'
		else:
			opponent = 'blue'

		hideout = self.find_general(opponent)

		# CHECK IF THE GENERAL IS IN CHECK
		# CHECK IF THE GENERAL WOULD BE IN CHECK IF IT MOVED TO
		# EACH OF IT'S 8 POSSIBLE SPACES

		return False

	def make_move(self, a, b):
		"""Takes two strings that represent squares such as 'a2' and 'g7'
		and moves the piece from the first square into the second square,
		if possible. Returns true if the move is succesful, false otherwise."""
		# Check if the game is finished
		if self._game_state != 'UNFINISHED':
			return False

		piece = self._pieces[a]

		# Check if the right player i playing
		if piece.get_player() != self._turn:
			return False

		# Check if the player has a piece in the intended square
		if piece.get_player() == self._pieces[b].get_player():
			return False

		# Check if the move is legal
		if legal_move(piece, a, b):

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



"""
DETAILED TEXT DESCRIPTIONS OF HOW TO HANDLE THE SCENARIOS
1. A call to JanggiGame() instantiates a new game and initializes the board.
The board is represented as a dictionary with keys being the squares of the
board: 'a1', 'b1', ..., 'h10', 'i10'. The value for each key in the board
is the piece on that space, or None if the space is empty.

2. Pieces are represented at a given location through the values of the
Board dictionary.

3. Make_move first checks to be sure the game is not over, that it is the
correct player's turn, and that there is not a piece from the same team
in the intended square. It then calls legal_move, which validates a given move
by comparing its start and end coordinates to the movement pattern for the
provided piece's rank.

4. If legal_move returns true, the dictionary value for the intended square
will be set to the moved piece, regardless of what value is currently there.
This way, if an opponent's piece was there, it will be removed from the board.

5. The JanggiGame has a data member _turn which defaults to 'blue'. If
legal_move returns True (during make_move), then _turn will be set to the
opposite team.

6. Checkmate will first check if any of opposing pieces can legally move
to the position the General is currently in (using in_check). 
If so, it will check to see if any of the threatened General's other pieces 
can legally move to the threatening piece's square to save the general. 
If not, it will then sequentially check the each square the General can 
legally move to and check whether the General would be in check there (using 
in_check). Thus, if the General IS in check AND none of the general's pieces 
can take the threatening piece AND the General would be in check after all 
possible legal moves, THEN the player is in checkmate.

7. After each move, the game will see if the opposing player is in checkmate.
If is_in_checkmate returns True, the JanggiGame's _game_state will update
accordingly.
"""




