# (nxn)-Sudoku Solver & (naive) Genearator
In this project the standard Backtracking Algorithm for solving Sudokus with arbitrary size is implemented.

## Example Usage
Set up a sample Sudoku and run the algorithm.
```
sample_grid = np.array([
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

sudoku = Sudoku.build_grid(sample_grid)
solvable = sudoku.solve()
```
##

