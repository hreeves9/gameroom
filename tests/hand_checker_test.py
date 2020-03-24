from hand_checker import *

single_king_diamond = ["KD"]
single_king_spade = ["KS"]
single_ace_spade = ["AS"]
pair_threes = ["3D", "3H"]
pair_fours_low = ["4D", "4C"]
pair_fours_highs = ["4H", "4S"]
threes_fours = ["4D", "4C", "4S"]
threes_fives = ["5D", "5H", "5S"]
straight_four = ["4H", "5D", "6C", "7S", "8C"]
straight_seven = ["7C", "8S", "9H", "10S", "JS"]
flush_hearts = ["7H", "9H", "4H", "KH", "JH"]
flush_spades = ["3S", "AS", "KS", "JS", "6S"]
full_house_1 = ["3S", "3D", "3H", "5S", "5H"]
full_house_2 = ["KS", "KD", "KH", "9S", "9H"]
four_of_a_kind_5 = ["5H", "5D", "5S", "5C", "4H"]
four_of_a_kind_7 = ["7D", "7S", "7H", "7C", "9C"]
straight_flush_5 = ["5H", "6H", "7H", "8H", "9H"]
straight_flush_9 = ["9S", "10S", "JS", "QS", "KS"]
royal_flush_diamonds = ["JD", "QD", "KD", "AD", "2D"]
royal_flush_spades = ["JS", "QS", "KS", "AS", "2S"]

if __name__ == "__main__":

	if(valid_move(single_king_diamond, single_king_spade) == False):
		raise ValueError('FAIL')

	if(valid_move(single_king_spade, single_ace_spade) == False):
		raise ValueError('FAIL')

	if(valid_move(single_king_spade, single_king_diamond) == True):
		raise ValueError('FAIL')

	if(valid_move(single_ace_spade, single_king_spade) == True):
		raise ValueError('FAIL')

	if(valid_move(single_ace_spade, pair_threes) == True):
		raise ValueError('FAIL')

	if(valid_move(pair_threes, pair_fours_low) == False):
		raise ValueError('FAIL')

	if(valid_move(pair_fours_highs, pair_fours_low) == True):
		raise ValueError('FAIL')

	if(valid_move(pair_fours_highs, threes_fours) == True):
		raise ValueError('FAIL')

	if(valid_move(threes_fours, threes_fives) == False):
		raise ValueError('FAIL')

	if(valid_move(straight_seven, straight_four) == True):
		raise ValueError('FAIL')
	
	if(valid_move(flush_hearts, straight_four) == True):
		raise ValueError('FAIL')

	if(valid_move(flush_hearts, flush_spades) == False):
		raise ValueError('FAIL')

	if(valid_move(full_house_1, flush_spades) == True):
		raise ValueError('FAIL')

	if(valid_move(full_house_1, full_house_2) == False):
		raise ValueError('FAIL')

	if(valid_move(four_of_a_kind_7, full_house_1) == True):
		raise ValueError('FAIL')

	if(valid_move(four_of_a_kind_5, four_of_a_kind_7) == False):
		raise ValueError('FAIL')

	if(valid_move(four_of_a_kind_7, straight_flush_9) == False):
		raise ValueError('FAIL')

	if(valid_move(straight_flush_5, straight_flush_9) == False):
		raise ValueError('FAIL')

	if(valid_move(straight_flush_9, royal_flush_diamonds) == False):
		raise ValueError('FAIL')

	if(valid_move(royal_flush_diamonds, royal_flush_spades) == False):
		raise ValueError('FAIL')






