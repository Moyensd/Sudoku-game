# Sudoku Game Generator
    #### Video Demo:  https://www.youtube.com/watch?v=z9_bYZiR4xI
    #### Description:
This Python program allows you to play Sudoku and solve Sudoku puzzles.
It uses the Pygame library for the graphical user interface.

## How to Play

1. Run the program.
2. To select a cell, click on it with the left mouse button or use the arrow keys to navigate between cells
3. To input a number, select a cell and press the number key (1-9).
4. To solve the puzzle, click the "Solve" button.
5. To reset the puzzle, click the "Reset" button.
6. Click the "Check" button to toggle a check for correctness on answers.

## Features

- Sudoku puzzle generation with random puzzles.
- All puzzles have only one unique solutions.
- Interactive Sudoku board with highlighting of selected cells.
- Ability to input and validate your Sudoku solution.
- Solving the puzzle with a single click.
- Resetting the puzzle to a new state.
- Checking if your solution is correct.
- Displaying feedback on the correctness of your solution.

## Dependencies

- Python 3.x
- Pygame library

## Installation and Usage

1. Download the clone repository

2. Install the required dependencies:

pip install pygame

3. Run the program:

python project.py

## Methodology

To make the game easier to program I used 2 layers for the graphical interface, 1 for the user and one for the puzzle.
this way the 2 won't conflict and it's easier to modify both without issues.

A backtracking recursion algorithm was used to solve the sudoku puzzle.
the hardest part was creating the logic for making the system be able to process,
and backtrack again to find a single unique solution for the sudoku puzzle.
the loops and if statements were deeply nested which made it difficult to properly break or assign global values.

## Customization

You can customize the difficulty of generated Sudoku puzzles by modifying 'attempts' variable from the range of 1-15.
using too many attempts will slow down the program drastically.

```python
# Adjust the difficulty by changing the number of removed numbers

Credits

This Sudoku solver and game was created by Kiyomichi Suzuki.
