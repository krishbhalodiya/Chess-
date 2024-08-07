import pygame as p
import sys
import time
from Chess import chessEngine, chessBot, chessAI, chessAI2

p.init()
WIDTH = HEIGHT = 512  # 400 is another option
DIMENSION = 8  # dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # for animations later on
IMAGES = {}

# Load custom font
FANCY_FONT = p.font.Font("fancy_font.ttf", 32)

# Load background image
BACKGROUND_IMAGE = p.image.load("img.png")
BACKGROUND_IMAGE = p.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))


def loadImages():
    pieces = ['wP', 'wR', 'wN', 'wB', 'wQ', 'wK', 'bP', 'bR', 'bN', 'bB', 'bQ', 'bK']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
    # Promotion pieces
    promotion_pieces = ['wQ', 'wR', 'wB', 'wN']
    for piece in promotion_pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess pieces/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def draw_button(screen, rect, text, font, color, bg_color):
    p.draw.rect(screen, bg_color, rect, border_radius=12)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                               rect.y + (rect.height - text_surface.get_height()) // 2))


def main_menu():
    p.init()
    p.font.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    button_width = 250
    button_height = 70

    player_vs_player_button = p.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 4, button_width, button_height)
    bot_vs_bot_button = p.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
    player_vs_bot_button = p.Rect(WIDTH // 2 - button_width // 2, 3 * HEIGHT // 4, button_width, button_height)

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        draw_button(screen, player_vs_player_button, "Player vs Player", FANCY_FONT, p.Color("white"), p.Color("blue"))
        draw_button(screen, bot_vs_bot_button, "Bot vs Bot", FANCY_FONT, p.Color("white"), p.Color("blue"))
        draw_button(screen, player_vs_bot_button, "Player vs Bot", FANCY_FONT, p.Color("white"), p.Color("blue"))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if player_vs_player_button.collidepoint(event.pos):
                    game_loop("PvP")
                elif bot_vs_bot_button.collidepoint(event.pos):
                    game_loop("BvB")
                elif player_vs_bot_button.collidepoint(event.pos):
                    player_vs_bot_menu()

        p.display.flip()
        clock.tick(MAX_FPS)


def player_vs_bot_menu():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    button_width = 250
    button_height = 70

    krish_button = p.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 4, button_width, button_height)
    hemanth_button = p.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2, button_width, button_height)
    messiah_button = p.Rect(WIDTH // 2 - button_width // 2, 3 * HEIGHT // 4, button_width, button_height)

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        draw_button(screen, krish_button, "Krish (1400)", FANCY_FONT, p.Color("white"), p.Color("blue"))
        draw_button(screen, hemanth_button, "Hemanth (1200)", FANCY_FONT, p.Color("white"), p.Color("blue"))
        draw_button(screen, messiah_button, "Messiah (600)", FANCY_FONT, p.Color("white"), p.Color("blue"))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if krish_button.collidepoint(event.pos):
                    choose_color("Krish")
                elif hemanth_button.collidepoint(event.pos):
                    choose_color("Hemanth")
                elif messiah_button.collidepoint(event.pos):
                    choose_color("Messiah")

        p.display.flip()
        clock.tick(MAX_FPS)


def choose_color(bot):
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()

    button_width = 250
    button_height = 70

    white_button = p.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 3, button_width, button_height)
    black_button = p.Rect(WIDTH // 2 - button_width // 2, 2 * HEIGHT // 3, button_width, button_height)

    while True:
        screen.blit(BACKGROUND_IMAGE, (0, 0))

        draw_button(screen, white_button, "Play as White", FANCY_FONT, p.Color("white"), p.Color("blue"))
        draw_button(screen, black_button, "Play as Black", FANCY_FONT, p.Color("white"), p.Color("blue"))

        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()
                sys.exit()
            elif event.type == p.MOUSEBUTTONDOWN:
                if white_button.collidepoint(event.pos):
                    game_loop("PvB", bot, "white")
                elif black_button.collidepoint(event.pos):
                    game_loop("PvB", bot, "black")

        p.display.flip()
        clock.tick(MAX_FPS)


def game_loop(mode, bot_choice=None, player_color=None):
    p.init()
    p.font.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False  # flag variable for when a move is made
    game_over = False
    game_status = ""  # To store the game status message
    loadImages()  # do this only once before the while loop
    running = True
    playerClicks = []  # keep track of player clicks (two tuples: [(6, 4), (4, 4)])
    dragPiece = False
    pieceToDrag = None
    dragStartPos = ()
    dragPos = ()
    font = p.font.SysFont('Arial', 32)  # Load a font
    highlightedSquares = []  # List of squares to highlight
    validMovesDots = []  # List of squares to show potential moves

    player1 = player2 = False
    if mode == "PvP":
        player1 = player2 = True
    elif mode == "BvB":
        pass  # Both players are bots, logic handled below
    elif mode == "PvB":
        player1 = (player_color == "white")
        player2 = (player_color == "black")

    while running:
        humanTurn = (gs.whiteToMove and player1) or (not gs.whiteToMove and player2)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN and not game_over and humanTurn:
                location = p.mouse.get_pos()  # (x, y) location of the mouse
                col = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE
                if gs.board[row][col] != "--":  # piece to drag
                    dragPiece = True
                    pieceToDrag = gs.board[row][col]
                    dragStartPos = (row, col)
                    sqSelected = (row, col)
                    playerClicks = [sqSelected]
                    validMovesDots = getValidMovesDots(gs, row, col)  # Get valid moves for the clicked piece
            elif e.type == p.MOUSEBUTTONUP and not game_over:
                dragPos = ()
                if dragPiece:
                    location = p.mouse.get_pos()
                    col = location[0] // SQ_SIZE
                    row = location[1] // SQ_SIZE
                    dragPiece = False
                    pieceToDrag = None
                    playerClicks.append((row, col))
                    if len(playerClicks) == 2:
                        move = chessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        if move in validMoves:
                            if move.isPawnPromotion:
                                promotion_choice = draw_promotion_menu(screen, gs.whiteToMove)
                                move.promotion_choice = 'w' + promotion_choice if gs.whiteToMove else 'b' + promotion_choice
                            gs.makeMove(move)
                            moveMade = True
                            highlightedSquares = [playerClicks[0],
                                                  playerClicks[1]]  # Highlight the start and end squares
                        playerClicks = []  # reset player clicks
                        validMovesDots = []  # Clear the dots
            elif e.type == p.MOUSEMOTION:
                if dragPiece:
                    dragPos = p.mouse.get_pos()
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:  # undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
                    dragPiece = False
                    pieceToDrag = None
                    dragStartPos = ()  # reset drag start position
                    highlightedSquares = []  # Clear highlights
                    validMovesDots = []  # Clear the dots

        if not game_over and not humanTurn:
            if gs.whiteToMove:
                start_time = time.time()
                if mode == "BvB":
                    AImove1 = chessAI2.findBestMoveNegaMax(gs, validMoves)
                elif bot_choice == "Krish":
                    AImove1 = chessAI2.findBestMoveNegaMax(gs, validMoves)
                elif bot_choice == "Hemanth":
                    AImove1 = chessAI.findBestMoveNegaMax(gs, validMoves)
                elif bot_choice == "Messiah":
                    AImove1 = chessBot.findBestMove(gs, validMoves)
                end_time = time.time()
                print(f"White AI move time: {end_time - start_time:.2f} seconds")
                if AImove1 is None:
                    AImove1 = chessAI.findRandomMove(validMoves)
                if AImove1.isPawnPromotion:
                    AImove1.promotion_choice = 'wQ' if gs.whiteToMove else 'bQ'  # Auto promote to queen for AI
                gs.makeMove(AImove1)
                moveMade = True
                highlightedSquares = [(AImove1.startRow, AImove1.startCol),
                                      (AImove1.endRow, AImove1.endCol)]  # Highlight the AI move
            else:
                start_time = time.time()
                if mode == "BvB":
                    AImove2 = chessBot.findBestMove(gs, validMoves)
                elif bot_choice == "Krish":
                    AImove2 = chessAI2.findBestMoveNegaMax(gs, validMoves)
                elif bot_choice == "Hemanth":
                    AImove2 = chessAI.findBestMoveNegaMax(gs, validMoves)
                elif bot_choice == "Messiah":
                    AImove2 = chessBot.findBestMove(gs, validMoves)
                end_time = time.time()
                print(f"Black AI move time: {end_time - start_time:.2f} seconds")
                if AImove2 is None:
                    AImove2 = chessAI.findRandomMove(validMoves)
                if AImove2.isPawnPromotion:
                    AImove2.promotion_choice = 'wQ' if gs.whiteToMove else 'bQ'  # Auto promote to queen for AI
                gs.makeMove(AImove2)
                moveMade = True
                highlightedSquares = [(AImove2.startRow, AImove2.startCol),
                                      (AImove2.endRow, AImove2.endCol)]  # Highlight the AI move

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
            dragPiece = False  # reset drag state
            pieceToDrag = None  # reset dragged piece
            dragStartPos = ()  # reset drag start position

            # Check for game over conditions
            if gs.checkForCheckmate():
                game_over = True
                game_status = "Checkmate! " + ("White wins!" if not gs.whiteToMove else "Black wins!")
            elif gs.checkForStalemate():
                game_over = True
                game_status = "Stalemate!"
            else:
                draw_result = gs.checkDrawConditions()
                if draw_result:
                    game_over = True
                    game_status = "Draw by " + draw_result

        drawGameState(screen, gs, pieceToDrag, dragPos if dragPiece else None, dragStartPos, highlightedSquares,
                      validMovesDots)

        if game_over:
            drawEndGameText(screen, game_status, font)

        clock.tick(MAX_FPS)
        p.display.flip()


def drawBoard(screen):
    colors = [p.Color("white"), p.Color("brown")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawPieces(screen, board, pieceToDrag, dragPos, dragStartPos):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                if pieceToDrag and (r, c) == dragStartPos:
                    continue  # Do not draw the piece being dragged at its original position
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
    if pieceToDrag and dragPos:
        screen.blit(IMAGES[pieceToDrag], p.Rect(dragPos[0] - SQ_SIZE // 2, dragPos[1] - SQ_SIZE // 2, SQ_SIZE, SQ_SIZE))


def drawGameState(screen, gs, pieceToDrag, dragPos, dragStartPos, highlightedSquares, validMovesDots):
    drawBoard(screen)  # draw squares on the board
    highlightSquares(screen, highlightedSquares)  # highlight start and end squares
    drawDots(screen, validMovesDots)  # draw dots for valid moves
    drawPieces(screen, gs.board, pieceToDrag, dragPos, dragStartPos)  # draw pieces on top of those squares


def highlightSquares(screen, squares):
    for square in squares:
        row, col = square[0], square[1]
        s = p.Surface((SQ_SIZE, SQ_SIZE))
        s.set_alpha(100)  # transparency value
        s.fill(p.Color('green'))
        screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))


def drawDots(screen, squares):
    for square in squares:
        row, col = square
        center = (col * SQ_SIZE + SQ_SIZE // 2, row * SQ_SIZE + SQ_SIZE // 2)
        p.draw.circle(screen, p.Color('gray'), center, 10)


def getValidMovesDots(gs, row, col):
    piece = gs.board[row][col]
    validMovesDots = []
    if piece[0] == ('w' if gs.whiteToMove else 'b'):
        for move in gs.getValidMoves():
            if move.startRow == row and move.startCol == col:
                validMovesDots.append((move.endRow, move.endCol))
    return validMovesDots


def drawEndGameText(screen, text, font):
    menu_width = 512
    menu_height = 55
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    screen.fill(p.Color("black"), (menu_x, menu_y, menu_width, menu_height))
    text_object = font.render(text, True, p.Color('Red'))
    text_location = p.Rect(0, 0, WIDTH, HEIGHT).move(WIDTH // 2 - text_object.get_width() // 2,
                                                     HEIGHT // 2 - text_object.get_height() // 2)
    screen.blit(text_object, text_location)
    text_object = font.render(text, True, p.Color('white'))
    screen.blit(text_object, text_location.move(2, 2))


def draw_promotion_menu(screen, white_to_move):
    promotion_options = ['Q', 'R', 'B', 'N']
    color = p.Color("white") if white_to_move else p.Color("white")

    menu_width = 83
    menu_height = 300
    menu_x = (WIDTH - menu_width) // 2
    menu_y = (HEIGHT - menu_height) // 2
    option_rects = []

    for i, option in enumerate(promotion_options):
        rect = p.Rect(menu_x, menu_y + i * 75, menu_width, 75)
        option_rects.append((rect, option))

    while True:
        screen.fill(p.Color("gray"), (menu_x, menu_y, menu_width, menu_height))
        for rect, option in option_rects:
            p.draw.rect(screen, color, rect)
            piece_image = IMAGES['w' + option] if white_to_move else IMAGES['b' + option]
            screen.blit(piece_image, (rect.x + 10, rect.y + 10))
        p.display.flip()

        for e in p.event.get():
            if e.type == p.QUIT:
                p.quit()
                quit()
            elif e.type == p.MOUSEBUTTONDOWN:
                for rect, option in option_rects:
                    if rect.collidepoint(e.pos):
                        return option


if __name__ == "__main__":
    main_menu()
