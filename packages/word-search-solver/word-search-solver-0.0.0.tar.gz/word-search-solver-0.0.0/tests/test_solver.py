from word_search_solver.solver import word_search_solver
import unittest
import getopt
import sys

class TestWordSearchSolver(unittest.TestCase):

	def test_solver_normal_a(self):
		input_file = "tests/word_search_grids/grid_1.txt"
		wordlist = "tests/wordlists/list_1.txt"
		self.assertEqual(word_search_solver(input_file, wordlist, False, False), 0)
	
	def test_solver_normal_b(self):
		input_file = "tests/word_search_grids/grid_2.txt"
		wordlist = "tests/wordlists/list_2.txt"
		self.assertEqual(word_search_solver(input_file, wordlist, False, False), 0)

	def test_solver_normal_c(self):
		input_file = "tests/word_search_grids/grid_3.txt"
		wordlist = "tests/wordlists/list_3.txt"
		self.assertEqual(word_search_solver(input_file, wordlist, False, False), 0)

	def test_solver_empty_grid(self):
		input_file = ""
		wordlist = "tests/wordlists/list_1.txt"
		self.assertEqual(word_search_solver(input_file, wordlist, False, False), -1)

	def test_solver_empty_wordlist(self):
		input_file = "tests/word_search_grids/grid_1.txt"
		wordlist = ""
		self.assertEqual(word_search_solver(input_file, wordlist, False, False), -1)

'''
# Process/parse arguments
    arg_list = []
    if len(sys.argv) > 1:
        arg_list = sys.argv[1:]
    options = "vti:l:"
    long_options = ["verbose", "timing", "input_file=", "wordlist="]
    try:
        args, vals = getopt.getopt(arg_list, options, long_options)
        for currentArg, currentVal in args:
            if currentArg in ("-t" , "--timing"):
                timing = True
            elif currentArg in ("-v", "--verbose"):
                verbose = True
            elif currentArg in ("-i", "--input_file"):
                f = open(str(currentVal), "r")
                for line in f:
                    line_split = line.split(" ")
                    # Check for newline character attached to final character of each row of grid
                    if '\n' in line_split[-1]:
                        pop_elem = line_split.pop()
                        line_split.append(pop_elem[0])
                    puzzle_grid.append(line_split)
                f.close()
            elif currentArg in ("-l", "--wordlist"):
                f = open(str(currentVal), "r")
                for line in f:
                    if words == "":
                        words += line
                    else:
                        words += " " + line
                f.close()
    # Error msgs for command line arguments
    except getopt.error as err:
        if err.opt in ("-i", "--input_file"):
            print("ERROR: Must provide an input file containing word search grid", file=sys.stderr)
        elif err.opt in ("-l", "--wordlist"):
            print("ERROR: Must provide wordlist for corresponding word search grid", file=sys.stderr)
        else:
            print("ERROR: Invalid argument", file=sys.stderr)
        return -1

    # Enforcing command line args
    if puzzle_grid == [] or words == "":
        print("ERROR: Must provide word search grid and/or word list", file=sys.stderr)
        return -1
'''