from random import randint, shuffle
import sys, pygame as pg


pg.init()
screen_size = 750, 840
screen = pg.display.set_mode(screen_size)
font = pg.font.SysFont(None, 80)
selected_row, selected_col = -1, -1
user_input = None
show_result_text = False
darker_green = (0, 100, 0)
pg.display.set_caption("Sudoku")


# Initialize an empty 9x9 grid
grid = [[0] * 9 for _ in range(9)]
user_grid = [[0] * 9 for _ in range(9)]


def is_valid_move(row, col, num):
    # Check if the number is not in the same row or column
    for i in range(9):
        if grid[row][i] == num or grid[i][col] == num:
            return False

    # Check if the number is not in the same 3x3 square
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[start_row + i][start_col + j] == num:
                return False

    return True

def solve_grid(grid):
    global counter
    #Find next empty cell
    for i in range(0,81):
        row=i//9
        col=i%9
        if grid[row][col]==0:
            for value in range (1,10):
                #Check that this value has not already be used on this row
                if not(value in grid[row]):
                #Check that this value has not already be used on this column
                    if not any(row[col] == value for row in grid):
                        #Identify which of the 9 squares we are working on
                        square=[]
                        if row<3:
                            if col<3:
                                square=[grid[i][0:3] for i in range(0,3)]
                            elif col<6:
                                square=[grid[i][3:6] for i in range(0,3)]
                            else:  
                                square=[grid[i][6:9] for i in range(0,3)]
                        elif row<6:
                            if col<3:
                                square=[grid[i][0:3] for i in range(3,6)]
                            elif col<6:
                                square=[grid[i][3:6] for i in range(3,6)]
                            else:  
                                square=[grid[i][6:9] for i in range(3,6)]
                        else:
                            if col<3:
                                square=[grid[i][0:3] for i in range(6,9)]
                            elif col<6:
                                square=[grid[i][3:6] for i in range(6,9)]
                            else:  
                                square=[grid[i][6:9] for i in range(6,9)]
                        #Check that this value has not already be used on this 3x3 square
                        if not value in (square[0] + square[1] + square[2]):
                            grid[row][col]=value
                            if check_grid(grid):
                                counter += 1
                                break
                            else:
                                if solve_grid(grid):
                                    return True
            break
    grid[row][col]=0  

def fill_sudoku(grid):
    global counter
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                # Generate a random order for trying numbers
                numbers = list(range(1, 10))
                shuffle(numbers)

                for num in numbers:
                    if is_valid_move(row, col, num):
                        grid[row][col] = num
                        if check_grid(grid):
                            
                            return True
                        if fill_sudoku(grid):
                            return True
                        grid[row][col] = 0

                return False

    return True


def check_grid(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                return False
    return True

def gen_sudoku(grid):
    global counter
    attempts = 5
    """
    Customize the difficulty of generated Sudoku puzzles by modifying 'attempts' variable from the range of 1-15.
    using too many attempts will slow down the program drastically.
    """
    while attempts > 0:
        #Select a random cell that is not already empty
        row = randint(0,8)
        col = randint(0,8)
        while grid[row][col]==0:
            row = randint(0,8)
            col = randint(0,8)
        #Remember its cell value in case we need to put it back  
        backup = grid[row][col]
        grid[row][col]=0
    
        #Take a full copy of the grid
        copyGrid = []
        for r in range(0,9):
            copyGrid.append([])
            for c in range(0,9):
                copyGrid[r].append(grid[r][c])
    
        #Count the number of solutions that this grid has (using a backtracking approach implemented in the solve_grid()
        counter = 0      
        solve_grid(copyGrid)   
        #If the number of solution is different from 1 then we need to cancel the change by putting the value we took away back in the grid
        if counter!=1:
            grid[row][col]=backup
            #We could stop here, but we can also have another attempt with a different cell just to try to remove more numbers
            attempts -= 1

def game_loop():
    global selected_row, selected_col, user_input, grid, user_grid, solved_grid, show_result_text

    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button clicked
                # Calculate the row and column based on the mouse position
                x, y = event.pos
                row = (y - 15) // 80
                col = (x - 15) // 80

                # Check if the clicked cell is within the Sudoku grid
                if 0 <= row < 9 and 0 <= col < 9:
                    selected_row, selected_col = row, col

                # Check if buttons were clicked
                elif 15 <= x <= 135 and 760 <= y <= 820:
                    user_grid = [[0] * 9 for _ in range(9)]
                    fill_sudoku(grid)
                    
                elif 150 <= x <= 270 and 760 <= y <= 820:
                    user_grid = [[0] * 9 for _ in range(9)]
                    grid = [[0] * 9 for _ in range(9)]
                    fill_sudoku(grid)
                    solved_grid = [row[:] for row in grid]
                    gen_sudoku(grid)
                    print("Solved board:")
                    for row in solved_grid:
                        print(row)
                elif 615 <= x <= 750 and 760 <= y <= 820:
                    show_result_text = not show_result_text


        elif event.type == pg.KEYDOWN:
            if selected_row != -1 and selected_col != -1:
                if event.key == pg.K_LEFT and selected_col > 0:
                    selected_col -= 1
                elif event.key == pg.K_RIGHT and selected_col < 8:
                    selected_col += 1
                elif event.key == pg.K_UP and selected_row > 0:
                    selected_row -= 1
                elif event.key == pg.K_DOWN and selected_row < 8:
                    selected_row += 1
                elif event.key in [pg.K_1, pg.K_2, pg.K_3, pg.K_4, pg.K_5, pg.K_6, pg.K_7, pg.K_8, pg.K_9, pg.K_0]:
                    user_input = int(event.unicode)  # Get the numerical input
                    if grid[selected_row][selected_col] == 0:
                        user_grid[selected_row][selected_col] = user_input  # Update the Sudoku board
                # Numpad
                elif event.key in [pg.K_KP1, pg.K_KP2, pg.K_KP3, pg.K_KP4, pg.K_KP5, pg.K_KP6, pg.K_KP7, pg.K_KP8, pg.K_KP9, pg.K_KP0]:
                    user_input = int(event.unicode)
                    if grid[selected_row][selected_col] == 0:
                        user_grid[selected_row][selected_col] = user_input

    draw_background()
    board_nums()
    input_board()
    highlight_selected_cell(selected_row, selected_col)
    solve_button()
    reset_button()
    check_button()

    pg.display.flip()

def check_user_input_board():
    for row in range(9):
        for col in range(9):
            if user_grid[row][col] != 0:
                # Check if the user's input is different from the solution
                if user_grid[row][col] != solved_grid[row][col]:
                    return False
    return True

def solve_button():
    button_color = (0, 100, 0)
    button_rect = pg.Rect(15, 760, 120, 60)
    pg.draw.rect(screen, button_color, button_rect)
    button_font = pg.font.SysFont(None, 40)
    button_text = button_font.render("Solve", True, pg.Color("white"))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def reset_button():
    button_color = pg.Color("red")
    button_rect = pg.Rect(150, 760, 120, 60)
    pg.draw.rect(screen, button_color, button_rect)
    button_font = pg.font.SysFont(None, 40)
    button_text = button_font.render("Reset", True, pg.Color("white"))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

def check_button():
    global show_result_text

    button_color = pg.Color("blue")
    button_rect = pg.Rect(615, 760, 120, 60)
    pg.draw.rect(screen, button_color, button_rect)
    button_font = pg.font.SysFont(None, 40)
    button_text = button_font.render("Check", True, pg.Color("white"))
    text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, text_rect)

    if show_result_text:
        # Define button_font and button_rect for the "incorrect" text
        result_font = pg.font.SysFont(None, 40)
        result_text = None
        result_rect = None

        # Check user input and display "incorrect" if needed
        if check_user_input_board():
            result_text = result_font.render("Correct", True, darker_green)
        else:
            result_text = result_font.render("Incorrect", True, pg.Color("red"))

        result_rect = result_text.get_rect(center=(button_rect.centerx - 140, button_rect.centery))
        screen.blit(result_text, result_rect)


def highlight_selected_cell(row, col):
    if row != -1 and col != -1:
        x = 15 + col * 80
        y = 15 + row * 80
        pg.draw.rect(screen, pg.Color("red"), pg.Rect(x, y, 80, 80), 3)

def draw_background():
    screen.fill(pg.Color("white"))
    pg.draw.rect(screen, pg.Color("black"), pg.Rect(11, 11, 728, 728), 10)
    i = 1
    while (i * 80) < 720:
        if i % 3 > 0:
            line_wid = 5
        else:
            line_wid = 10
        pg.draw.line(screen, pg.Color("black"), pg.Vector2((i * 80) + 15, 15), pg.Vector2((i * 80) + 15, 735), line_wid)
        pg.draw.line(screen, pg.Color("black"), pg.Vector2(15, (i * 80) + 15), pg.Vector2(735, (i * 80) + 15), line_wid)
        i += 1


def input_board():
    row = 0
    offset = 35

    while row < 9:
        col = 0
        while col < 9:

            output = user_grid[row][col]
            if output == 0:
                n_text = font.render("", True, pg.Color('blue'))

            else:
                n_text = font.render(str(output), True, pg.Color('blue'))

            screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 4))

            col += 1

        row += 1

def board_nums():
    row = 0
    offset = 35
    while row < 9:
        col = 0
        while col < 9:

            output = grid[row][col]
            if output == 0:
                n_text = font.render("", True, pg.Color('blue'))

            else:
                n_text = font.render(str(output), True, pg.Color('black'))

            screen.blit(n_text, pg.Vector2((col * 80) + offset + 5, (row * 80) + offset - 4))

            col += 1

        row += 1


fill_sudoku(grid)

solved_grid = [row[:] for row in grid]
gen_sudoku(grid)
print("Solved board:")
for row in solved_grid:
    print(row)

print("Puzzle board:")
for row in grid:
    print(row)

if __name__ == "__main__":

    while True:
        game_loop()