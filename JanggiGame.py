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

	def legal_move(self, piece, a, b):
		"""Return true if the given rank can move from square a to square b. It
		is assumed that b is empty or contains a piece from the opponent of player
		whose piece is in square a. This function is used by the JanggiGame class.

		I chose to keep this function generic with branches for each piece. I
		strongly considered creating classes for each rank and providing each
		class with it's own legal_move function, but I believe my implementation
		is more concise and readable.

		Another design choice of mine was to implement legal moves for each rank
		as a list of ALL POSSIBLE legal moves, followed by a check for whether
		the particular move is in that list. I could have just checked the
		particular move based on the rule set, but this implementation seemed
		easier without any noticeable drawbacks."""

		rank = piece.get_rank()
		player = piece.get_player()

		# Functions for finding adjacent squares
		def above(square):
			"""Takes a square and returns the square above the provided square"""
			if not square:
				return None		# Returns None if the provided square is out of bounds
								# Sometimes Above/Below etc. get called out of bounds,
								# like when moving horses
			col = square[0]
			row = square[1:]
			if row == '1':
				return None
			else:
				row = str(int(row) - 1)

			return col + row

		def below(square):
			"""Takes a square and returns the square below the provided square"""
			if not square:
				return None		# Returns None if the provided square is out of bounds

			col = square[0]
			row = square[1:]

			if row == '10':
				return None
			else:
				row = str(int(row) + 1)

			return col + row

		def right_of(square):
			"""Takes a square and returns the square to the right of the provided square"""
			if not square:
				return None		# Returns None if the provided square is out of bounds

			col = square[0]
			row = square[1:]

			if col == 'i':
				return None
			else:
				col_index = self._columns.index(col)
				col = str(self._columns[col_index + 1])

			return col + row

		def left_of(square):
			"""Takes a square and returns the square to the left of the provided square"""
			if not square:
				return None		# Returns None if the provided square is out of bounds

			col = square[0]
			row = square[1:]

			if col == 'a':
				return None
			else:
				col_index = self._columns.index(col)
				col = self._columns[col_index - 1]

			return col + row

		if rank == 'general' or rank == 'guard':
			# Mapping of valid squares the general/guards can move to
			valid_squares = {
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

			moves = valid_squares[player][a]

			return b in moves

		elif rank == 'horse':
			# The horse has eight possible squares to move to
			# The path to each square must be checked for blocking pieces
			moves = []

			up = above(a)
			down = below(a)
			left = left_of(a)
			right = right_of(a)

			if up and not self._pieces[up]:				# Up is in bounds and unblocked
				moves.append(above(left_of(up)))
				moves.append(above(right_of(up)))

			if down and not self._pieces[down]:			# Down is in bounds and unblocked
				moves.append(below(left_of(down)))
				moves.append(below(right_of(down)))

			if left and not self._pieces[left]:			# Left is in bounds and unblocked
				moves.append(left_of(below(left)))
				moves.append(left_of(above(left)))

			if right and not self._pieces[right]:		# Right is in bounds and unblocked
				moves.append(right_of(below(right)))
				moves.append(right_of(above(right)))

			return b in moves

		elif rank == 'elephant':

			moves = []

			up = above(a)
			down = below(a)
			left = left_of(a)
			right = right_of(a)

			if up and not self._pieces[up]:

				# Up is in bounds and unblocked
				moves.append(above(left_of(above(left_of(up)))))
				moves.append(above(right_of(above(right_of(up)))))

			if down and not self._pieces[down]:

				# Down is in bounds and unblocked
				moves.append(below(left_of(below(left_of(down)))))
				moves.append(below(right_of(below(right_of(down)))))

			if left and not self._pieces[left]:

				# Left is in bounds and unblocked
				moves.append(left_of(below(left_of(below(left)))))
				moves.append(left_of(above(left_of(above(left)))))

			if right and not self._pieces[right]:

				# Right is in bounds and unblocked
				moves.append(right_of(below(right_of(below(right)))))
				moves.append(right_of(above(right_of(above(right)))))

			return b in moves

		elif rank == 'chariot':
			moves = []

			"""In some cases, the chariot can move diagonally through a palace"""
			red_center = 'e2'
			red_corners = ['d1', 'd3', 'f1', 'f3']

			if a == red_center:
				moves += red_corners

			elif a in red_corners:
				moves.append(red_center)
				if not self._pieces[red_center]:
					if a == 'd1': moves.append('f3')
					elif a == 'f1': moves.append('d3')
					elif a == 'f3': moves.append('d1')
					elif a == 'd3': moves.append('f1')

			blue_center = 'e9'
			blue_corners = ['d8', 'f8', 'd10', 'f10']

			if a == blue_center:
				moves += blue_corners

			elif a in blue_corners:
				moves.append(blue_center)
				if not self._pieces[blue_center]:
					if a == 'd8': moves.append('f10')
					elif a == 'f8': moves.append('d10')
					elif a == 'd10': moves.append('f8')
					elif a == 'f10': moves.append('d8')

			"""In all cases, the chariot can travel orthogonally 
				until reaching a teammate, an enemy, or a border"""
			chariot_paths = [above, below, left_of, right_of]

			for direction in chariot_paths:
				next_sq = direction(a)

				while next_sq:
					next_sq_pc = self._pieces[next_sq]

					if next_sq_pc:
						if next_sq_pc.get_player() == player:  	# Chariot reached a teammate
							break
						else:									# Chariot reached an enemy
							moves.append(next_sq)
							break

					else:
						moves.append(next_sq)
						next_sq = direction(next_sq)

			return b in moves

		elif rank == 'cannon':
			moves = []

			"""Edge cases where the cannon can jump diagonally 
				over the center of a palace"""
			# Red Palace Diagonal Jumps
			if a in ['d1', 'f1', 'd3', 'f3'] and self._pieces['e2']:
				red_jumps = {'d1': 'f3', 'f1': 'd3', 'd3': 'f1', 'f3': 'd1'}

				for s, f in red_jumps.items():
					if a == s:
						if not self._pieces[f] or self._pieces[f].get_player() != player:
							moves.append(f)

			# Blue Palace Diagonal Jumps
			if a in ['d8', 'f8', 'd10', 'f10'] and self._pieces['e9']:
				blue_jumps = {'d8': 'f10', 'f8': 'd10', 'd10': 'f8', 'f10': 'd8'}

				for s, f in blue_jumps.items():
					if a == s:
						if not self._pieces[f] or self._pieces[f].get_player() != player:
							moves.append(f)

			"""All other standard cannon cases"""

			directions = [above, below, left_of, right_of]

			for direction in directions:
				if direction(a):
					next_sq = direction(a)
					piece_to_jump = False

					while next_sq:
						if next_sq == b:
							return piece_to_jump
						elif self._pieces[next_sq]:
							if self._pieces[next_sq].get_rank() == 'cannon':
								break
							else:
								piece_to_jump = True
								next_sq = direction(next_sq)
						else:
							next_sq = direction(next_sq)

			return b in moves

		elif rank == 'soldier':
			moves = []

			"""Special case for when the soldier is in a palace"""
			# Red Palace
			red_center = self._pieces['e2']
			red_corners = ['d1', 'f1', 'd3', 'f3']

			if a in red_corners:
				if not red_center or (red_center and red_center.get_player() != player):
					moves.append('e2')

			elif a == 'e2':
				for corner in red_corners:
					piece = self._pieces[corner]
					if not piece or (piece and piece.get_player() != player):
						moves.append(corner)

			# Blue Palace
			blue_center = self._pieces['e9']
			blue_corners = ['d8', 'f8', 'd10', 'f10']

			if a in blue_corners:
				if not blue_center or (blue_center and blue_center.get_player() != player):
					moves.append('e9')

			elif a == 'e9':
				for corner in blue_corners:
					piece = self._pieces[corner]
					if not piece or (piece and piece.get_player() != player):
						moves.append(corner)

			"""All other standard cases"""
			if player == 'blue': directions = [above, left_of, right_of]
			if player == 'red': directions = [below, left_of, right_of]

			for direction in directions:
				next_sq = direction(a)
				if next_sq:
					next_pc = self._pieces[next_sq]
					if not next_pc or (next_pc and next_pc.get_player() != player):
						# Blank square or enemy piece is adjacent
						moves.append(next_sq)

			return b in moves

	def find_general(self, player):
		"""Takes a player ('blue' or 'red') as a parameter and returns
		the name of the square which holds that player's general"""
		for square, piece in self._pieces.items():
			if piece:
				if piece.get_player() == player and piece.get_rank() == 'general':
					return square

	def is_in_check(self, player):
		"""Takes a position and returns True if a player is vulnerable there,
			False otherwise"""

		if player == 'blue':
			opponent = 'red'
		else:
			opponent = 'blue'

		in_check = False
		# Check each of the other team's pieces to see if they capture
		for square, piece in self._pieces.items():
			if piece:
				if piece.get_player() == opponent:
					if self.legal_move(piece, square, self.find_general(player)):
						in_check = True

		return in_check

	def is_in_checkmate(self, player):
		"""Takes a player ('blue' or 'red') as a parameter and returns
		True if that player is in checkmate, False otherwise."""

		# Mapping of valid squares the general/guards can move to
		valid_squares = {
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

		hideout = self.find_general(player)
		moves = valid_squares[player][hideout]

		in_checkmate = True

		for move in moves:
			# Return false if the general can escape by moving to any legal spaces
			# Reset the board after each try

			if not self._pieces[move] or (self._pieces[move].get_player() != player):
				original_board = self._pieces.copy()

				# Simulate an attempted escape
				self._pieces[hideout] = None
				self._pieces[move] = Piece(player, 'general')

				self._pieces = original_board.copy()

				if not self.is_in_check(player):
					in_checkmate = False
					self._pieces = original_board.copy()
					break

				self._pieces = original_board.copy()

			# If the general can't escape, try all possible moves for all the general's pieces
			# After each one, set in_checkmate to false if the general isn't in check
			if in_checkmate:
				for square, piece in self._pieces.items():
					if piece and piece.get_player() == player:

						for square2, piece2 in self._pieces.items():
							if not piece2 or (piece2 and piece2.get_player() != player):
								if self.legal_move(piece, square, square2):
									# Simulate an attempted intervention
									original_board2 = self._pieces.copy()

									self._pieces[square] = None
									self._pieces[square2] = piece

									if not self.is_in_check(player):
										self.print_board()
										in_checkmate = False
										self._pieces = original_board2.copy()
										break

									self._pieces = original_board2.copy()


			if in_checkmate:
				if self._turn == 'blue':
					self._game_state = 'RED_WON'
				elif self._turn == 'red':
					self._game_state = 'BLUE_WON'

		return in_checkmate

	def make_move(self, a, b):
		"""Takes two strings that represent squares such as 'a2' and 'g7'
		and moves the piece from the first square into the second square,
		if possible. Returns true if the move is successful, false otherwise."""
		# Check if there is an actual piece being moved
		if not self._pieces[a]:
			return False

		# Check if the game is finished
		if self._game_state != 'UNFINISHED':
			return False

		piece_a = self._pieces[a].get_rank()

		if self._pieces[b]:
			piece_b = self._pieces[b].get_rank()
		else:
			piece_b = "None"

		self.print_board()

		print("\n\nAttempting   " + a + " (" + piece_a + ")" +
			  ' --> ' + b + "(" + piece_b + ")" + "\n")

		piece = self._pieces[a]
		target = self._pieces[b]

		# Check if the right player i playing
		if piece.get_player() != self._turn:
			return False

		# Check if the player is passing their turn (only allowed if not in check)
		if a == b and not self.is_in_check(self._turn):
			if self._turn == 'blue':
				self._turn = 'red'

			elif self._turn == 'red':
				self._turn = 'blue'
			return True

		# Check if the player has a piece in the intended square
		if target and self._turn == target.get_player():
			return False

		# Check if the move is legal
		if not self.legal_move(piece, a, b):
			return False

		else:

			# MOVE THE PIECE
			self._pieces[a] = None
			self._pieces[b] = piece

			if self._turn == 'blue':
				self._turn = 'red'

			elif self._turn == 'red':
				self._turn = 'blue'

			# SEE IF THE GAME IS WON
			if self.is_in_check(self._turn):
				if self.is_in_checkmate(self._turn):
					if self._turn == 'blue':
						self._game_state = 'RED_WON'
					if self._turn == 'red':
						self._game_state = 'BLUE_WON'

			return True
