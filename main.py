"""
Author: Nils Kohring
Date: 12.02.2020

Sudoku: Backtracking Solver

"""

import numpy as np



class Sudoku():
    def __init__(
            self,
            n: int = 9,
            grid: np.array = None
        ):
        assert n > 0, "size ´n´ must be positive"
        assert int(round(n ** (1/2))) == n ** (1/2), \
            "size ´n´ must have a integer square root"

        self.n = n
        self.box_length = int(np.sqrt(n))
        if grid is None:
            self.build_random()
        else:
            self.grid = grid
        self.initial_grid = self.grid.copy()

        self._RECURSION_DEPTH = 0

    @classmethod
    def build_grid(cls, grid: np.array):
        assert len(set(grid.shape)) == 1, \
            'all dimensions must be of equal length'
        
        return cls(grid.shape[0], grid)

    def build_random(self, percentage_filled: float=0.3):
        """
        Creates a random Sudoku with at least ´percentage_filled´
        of fields filled and without errors. But it might not be 
        possible to solve for high values of ´percentage_filled´.
        """
        assert 0 <= percentage_filled and percentage_filled <= 1, \
            'percentage_filled must be within [0,1]'
        self.grid = np.zeros((self.n, self.n), dtype=int)

        while (len(self.grid[self.grid != 0]) / (self.n ** 2) \
                < percentage_filled):
            x = np.random.randint(0, self.n, 1)
            y = np.random.randint(0, self.n, 1)
            entry = np.random.randint(1, self.n + 1, 1)
            if self.feasible(x, y, entry):
                self.grid[x,y] = entry

    def feasible(self, x: int, y: int, entry: int):
        for var in (x, y):
            assert 0 <= var and var < self.n, \
                'indecies must be in number range' 
        assert 1 <= entry and entry < self.n + 1, \
            'entry must be in number range'
        
        # set temp. to zero
        backup = self.grid[x,y].copy()
        self.grid[x,y] = 0

        # verify columns and rows
        if len(np.where(self.grid[x,:] == entry)[0]) != 0:
            self.grid[x,y] = backup
            return False
        if len(np.where(self.grid[:,y] == entry)[0]) != 0:
            self.grid[x,y] = backup
            return False

        # verify box
        box = self.grid[self.get_box(x, y)[0], self.get_box(x, y)[1]]
        if len(np.where(box == entry)[0]) != 0:
            self.grid[x,y] = backup
            return False
        self.grid[x,y] = backup
        return True

    def get_box(self, x: int, y: int):
        x_box = x // self.box_length
        y_box = y // self.box_length

        x_start = x_box * self.box_length
        y_start = y_box * self.box_length
        x_end = (x_box + 1) * self.box_length
        y_end = (y_box + 1) * self.box_length

        x_idx = np.arange(x_start, x_end).repeat(self.box_length)
        y_idx = np.arange(y_start, y_end).repeat(self.box_length)
        y_idx = y_idx.reshape(self.box_length, self.box_length) \
            .transpose().reshape(self.n)

        return (x_idx.astype(int), y_idx.astype(int))

    def solve(self, verbose=False):
        """
        Solves the Sudoku via Backtracking.
        """
        self._RECURSION_DEPTH += 1
        assert self._RECURSION_DEPTH < 1e5, \
            'maximum recursion depth exceeded'

        for i in range(self.n):
            for j in range(self.n):
                if verbose:
                    print(sample_sudoku.draw())
                if self.grid[i,j] == 0:
                    for entry in range(1, self.n + 1):
                        if self.feasible(i, j, entry):
                            self.grid[i,j] = entry
                            # print(self.draw())
                            if self.solve(verbose):
                                return True
                    self.grid[i,j] = 0
                    return False
        return True

    def n_feasibles(self, x: int, y: int):
        """
        Returns number of feasible values at (x, y).
        """
        return sum([int(self.feasible(x, y, entry))
            for entry in range(1, self.n + 1)])

    def draw(self):
        """
        Returns Sudoku grid as string.
        """
        def newline():
            s = ''
            l = '---' if self.n > 9 else '--'
            for _ in range(self.n + self.box_length):
                s += l
            s = s[:-1]
            if self.n > 9:
                s = s[:-self.box_length]
            return s + '\n'

        empty = '  ' if self.n > 9 else ' '
        out = newline()
        for i in range(self.n):
            out += '| '
            for j in range(self.n):
                if self.grid[i,j] != 0:
                    entry = str(self.grid[i,j])
                    if self.n > 9 and self.grid[i,j] < 10:
                        entry = ' ' + entry
                    if self.initial_grid[i,j] == self.grid[i,j]:
                        out += entry
                    elif self.feasible(i, j, self.grid[i,j]):
                        out += '\033[94m' + entry + '\033[0m'
                    else:
                        out += '\033[91m' + entry + '\033[0m'
                else:
                    out += empty
                if (j + 1) % self.box_length == 0:
                    out += ' | '
                else:
                    out += ' '
            out = out[:-1]
            if (i + 1) % self.box_length == 0:
                out += '\n ' + newline()
            else:
                out += '\n'

        return out



if __name__ == "__main__":

    np.random.seed(4321)

    sample_sudoku_9x9 = np.array([
        [3, 6, 1, 0, 7, 0, 0, 0, 0],
        [0, 0, 4, 0, 2, 5, 0, 0, 0],
        [0, 8, 0, 0, 0, 0, 7, 0, 1],
        [1, 0, 0, 9, 0, 0, 0, 0, 5],
        [0, 0, 8, 5, 0, 0, 9, 0, 0],
        [0, 0, 0, 0, 8, 2, 1, 6, 4],
        [9, 0, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 0, 5, 8, 4, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 5, 0]
    ])
    sample_sudoku_4x4 = np.array([
        [3, 1, 4, 0],
        [0, 0, 0, 0],
        [0, 2, 3, 1],
        [1, 0, 0, 0],
    ])

    sample_sudoku = Sudoku(9)
    # sample_sudoku = Sudoku.build_grid(sample_sudoku_9x9)
    print('Initial\n', sample_sudoku.draw())

    solvable = sample_sudoku.solve(verbose=True)
    print('Is solvable:', solvable)
    if solvable:
        print('\nSolved\n', sample_sudoku.draw())
    