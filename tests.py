# TESTS FOR JANGGIGAME ARE HERE
from JanggiGame import *
import unittest

class TestLegalMove(unittest.TestCase):
	"""Tests the Legal Move function"""

	def test_general(self):
		game = JanggiGame()

		# Red General
		gen = Piece('red', 'general')

		self.assertTrue(game.legal_move(gen, 'd1', 'e2'))
		self.assertTrue(game.legal_move(gen, 'f3', 'f2'))
		self.assertTrue(game.legal_move(gen, 'e1', 'f1'))

		self.assertFalse(game.legal_move(gen, 'e1', 'f2'))
		self.assertFalse(game.legal_move(gen, 'f1', 'd3'))
		self.assertFalse(game.legal_move(gen, 'e3', 'e1'))

		# Blue General
		gen = Piece('blue', 'general')

		self.assertTrue(game.legal_move(gen, 'e9', 'f8'))
		self.assertTrue(game.legal_move(gen, 'f9', 'f10'))
		self.assertTrue(game.legal_move(gen, 'd8', 'e8'))

		self.assertFalse(game.legal_move(gen, 'e8', 'e10'))
		self.assertFalse(game.legal_move(gen, 'f9', 'e8'))
		self.assertFalse(game.legal_move(gen, 'd10', 'f10'))
		
			
	def test_guard(self):
		game = JanggiGame()

		# Red Guard
		gen = Piece('red', 'guard')

		self.assertTrue(game.legal_move(gen, 'd1', 'e2'))
		self.assertTrue(game.legal_move(gen, 'f3', 'f2'))
		self.assertTrue(game.legal_move(gen, 'e1', 'f1'))

		self.assertFalse(game.legal_move(gen, 'e1', 'f2'))
		self.assertFalse(game.legal_move(gen, 'f1', 'd3'))
		self.assertFalse(game.legal_move(gen, 'e3', 'e1'))

		# Blue Guard
		gen = Piece('blue', 'guard')

		self.assertTrue(game.legal_move(gen, 'e9', 'f8'))
		self.assertTrue(game.legal_move(gen, 'f9', 'f10'))
		self.assertTrue(game.legal_move(gen, 'd8', 'e8'))

		self.assertFalse(game.legal_move(gen, 'e8', 'e10'))
		self.assertFalse(game.legal_move(gen, 'f9', 'e8'))
		self.assertFalse(game.legal_move(gen, 'd10', 'f10'))
		
	def test_horse(self):
		game = JanggiGame()

		# Move red soldier to B5
		game._pieces['a4'] = None
		game._pieces['b5'] = Piece('red', 'soldier')

		# Place a blue horse on A7
		game._pieces['a7'] = Piece('blue', 'horse')

		# Blue horse should be able to take red soldier
		self.assertTrue(game.legal_move(Piece('blue', 'horse'), 'a7', 'b5'))

		# Block blue horse with another red soldier
		game._pieces['a6'] = Piece('red', 'soldier')
	
		# Blue horse should now be blocked
		self.assertFalse(game.legal_move(Piece('blue', 'horse'), 'a7', 'b5'))

		# Blue horse should not be able to move in a straight line
		self.assertFalse(game.legal_move(Piece('blue', 'horse'), 'h10', 'h9'))

	def test_elephant(self):
		game = JanggiGame()
		
		# Move red soldier to D7
		game._pieces['c4'] = None
		game._pieces['d7'] = Piece('red', 'soldier')	

		# Blue elephant should be able to take red soldier
		self.assertTrue(game.legal_move(Piece('blue', 'elephant'), 'b10', 'd7'))

		# Block blue elephant with a blue cannon
		game._pieces['b8'] = None
		game._pieces['b9'] = Piece('blue', 'cannon')

		# Blue elephant should now be blocked
		self.assertFalse(game.legal_move(Piece('blue', 'elephant'), 'b10', 'd7'))

	def test_chariot(self):
		game = JanggiGame()

		# Remove Blue Guards
		game._pieces['d10'] = None
		game._pieces['f10'] = None

		# Place Red chariot in Blue Palace
		game._pieces['d10'] = Piece('red', 'chariot')

		# Chariot can move diagonally to take the General
		self.assertTrue(game.legal_move(Piece('red', 'chariot'), 'd10', 'e9'))

		# Chariot can move to the other corner of the palace
		game._pieces['e9'] = None		# Remove general
		self.assertTrue(game.legal_move(Piece('red', 'chariot'), 'd10', 'f8'))

		# Chariot can move out of the palace and take the Elephant
		self.assertTrue(game.legal_move(Piece('red', 'chariot'), 'd10', 'g10'))

		# Chariot can escape back to it's side across the board
		self.assertTrue(game.legal_move(Piece('red', 'chariot'), 'd10', 'd2'))

		# Chariot cannot move on top of it's own elephant
		self.assertFalse(game.legal_move(Piece('red', 'chariot'), 'd10', 'd1'))

		# Chariot cannot skip over the General
		game._pieces['e9'] = Piece('blue', 'general')	# Add general back
		self.assertFalse(game.legal_move(Piece('red', 'chariot'), 'd10', 'f8'))

		# Chariot cannot skip over the elephant
		self.assertFalse(game.legal_move(Piece('red', 'chariot'), 'd10', 'h10'))

	def test_cannon(self):
		game = JanggiGame()

		# Jump an enemy piece
		self.assertTrue(game.legal_move(Piece('blue', 'cannon'), 'a5', 'a3'))

		# Jump a friendly piece
		self.assertTrue(game.legal_move(Piece('blue', 'cannon'), 'a8', 'a6'))

		# Jump two enemy pieces
		game._pieces['a4'] = None
		game._pieces['b4'] = Piece('red', 'soldier')
		self.assertTrue(game.legal_move(Piece('blue', 'cannon'), 'a4', 'd4'))

		# Can't jump a cannon
		self.assertFalse(game.legal_move(Piece('blue', 'cannon'), 'c8', 'a8'))

		# Can't land on an enemy piece
		self.assertFalse(game.legal_move(Piece('blue', 'cannon'), 'a4', 'c4'))

		# Jump a piece in the center of the red palace
		game._pieces['d1'] = None
		self.assertTrue(game.legal_move(Piece('red', 'cannon'), 'd1', 'f3'))

		# Jump a piece in the center of the blue palace
		game._pieces['d10'] = None
		self.assertTrue(game.legal_move(Piece('red', 'cannon'), 'd10', 'f8'))

	def test_soldier(self):
		game = JanggiGame()

		# Blue soldier can move up, left, right, but not down
		self.assertTrue(game.legal_move(Piece('blue', 'soldier'), 'c7', 'c6'))
		self.assertTrue(game.legal_move(Piece('blue', 'soldier'), 'c7', 'b7'))
		self.assertTrue(game.legal_move(Piece('blue', 'soldier'), 'c7', 'd7'))
		self.assertFalse(game.legal_move(Piece('blue', 'soldier'), 'c7', 'c8'))

		# Red soldier can move down, left, right, but not up
		self.assertTrue(game.legal_move(Piece('red', 'soldier'), 'c4', 'c5'))
		self.assertTrue(game.legal_move(Piece('red', 'soldier'), 'c4', 'b4'))
		self.assertTrue(game.legal_move(Piece('red', 'soldier'), 'c4', 'd4'))
		self.assertFalse(game.legal_move(Piece('red', 'soldier'), 'c4', 'c3'))

		# Red can take blue's general diagonally in blue's palace
		self.assertTrue(game.legal_move(Piece('red', 'soldier'), 'd8', 'e9'))

		# Blue can take blue's general diagonally in red's palace
		self.assertTrue(game.legal_move(Piece('blue', 'soldier'), 'd3', 'e2'))

		# Blue can't take it's own peice
		self.assertFalse(game.legal_move(Piece('blue', 'soldier'), 'b9', 'b8'))


class TestMakeMove(unittest.TestCase):

	def test_move_general(self):
		game = JanggiGame()

		self.assertTrue(game.make_move('e9', 'e8'))
		self.assertFalse(game.make_move('d10', 'd9'))
		self.assertTrue(game.make_move('e2', 'e3'))



if __name__ == '__main__':
	unittest.main()

