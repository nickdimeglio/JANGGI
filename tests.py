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
		


if __name__ == '__main__':
	unittest.main()

