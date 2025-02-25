import random
import logging
import os
import time
from datetime import datetime

# Global variables
nextMove = None
boardStates = {}
move_counts = {}
warning_count = 0
capture_missed_count = 0
move_time_sum = 0
move_count = 0

# Constants
CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3  # We'll keep this but implement more efficient searching

# Piece scores: Improved values
piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3.25, "N": 3, "p": 1}

# Position-based piece tables for improved evaluation
pawn_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 5, 5, 5, 5, 5, 5, 5],
    [1, 1, 2, 3, 3, 2, 1, 1],
    [0.5, 0.5, 1, 2.5, 2.5, 1, 0.5, 0.5],
    [0, 0, 0, 2, 2, 0, 0, 0],
    [0.5, -0.5, -1, 0, 0, -1, -0.5, 0.5],
    [0.5, 1, 1, -2, -2, 1, 1, 0.5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_table = [
    [-5, -4, -3, -3, -3, -3, -4, -5],
    [-4, -2, 0, 0, 0, 0, -2, -4],
    [-3, 0, 1, 1.5, 1.5, 1, 0, -3],
    [-3, 0.5, 1.5, 2, 2, 1.5, 0.5, -3],
    [-3, 0, 1.5, 2, 2, 1.5, 0, -3],
    [-3, 0.5, 1, 1.5, 1.5, 1, 0.5, -3],
    [-4, -2, 0, 0.5, 0.5, 0, -2, -4],
    [-5, -4, -3, -3, -3, -3, -4, -5]
]

bishop_table = [
    [-2, -1, -1, -1, -1, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 1, 1, 0.5, 0, -1],
    [-1, 0.5, 0.5, 1, 1, 0.5, 0.5, -1],
    [-1, 0, 1, 1, 1, 1, 0, -1],
    [-1, 1, 1, 1, 1, 1, 1, -1],
    [-1, 0.5, 0, 0, 0, 0, 0.5, -1],
    [-2, -1, -1, -1, -1, -1, -1, -2]
]

rook_table = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0.5, 1, 1, 1, 1, 1, 1, 0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [-0.5, 0, 0, 0, 0, 0, 0, -0.5],
    [0, 0, 0, 0.5, 0.5, 0, 0, 0]
]

queen_table = [
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2],
    [-1, 0, 0, 0, 0, 0, 0, -1],
    [-1, 0, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-0.5, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [0, 0, 0.5, 0.5, 0.5, 0.5, 0, -0.5],
    [-1, 0.5, 0.5, 0.5, 0.5, 0.5, 0, -1],
    [-1, 0, 0.5, 0, 0, 0, 0, -1],
    [-2, -1, -1, -0.5, -0.5, -1, -1, -2]
]

king_middle_table = [
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-3, -4, -4, -5, -5, -4, -4, -3],
    [-2, -3, -3, -4, -4, -3, -3, -2],
    [-1, -2, -2, -2, -2, -2, -2, -1],
    [2, 2, 0, 0, 0, 0, 2, 2],
    [2, 3, 1, 0, 0, 1, 3, 2]
]

king_end_table = [
    [-50, -40, -30, -20, -20, -30, -40, -50],
    [-30, -20, -10, 0, 0, -10, -20, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 30, 40, 40, 30, -10, -30],
    [-30, -10, 20, 30, 30, 20, -10, -30],
    [-30, -30, 0, 0, 0, 0, -30, -30],
    [-50, -30, -30, -30, -30, -30, -30, -50]
]

piece_position_tables = {
    "p": pawn_table,
    "N": knight_table,
    "B": bishop_table,
    "R": rook_table,
    "Q": queen_table,
    "K_mid": king_middle_table,
    "K_end": king_end_table
}

# Log file management
LOG_DIR = "chess_logs"
MAX_LOG_FILES = 5

def setup_logging():
    """Set up logging for a new game"""
    # Create logs directory if it doesn't exist
    if not os.path.exists(LOG_DIR):
        try:
            os.makedirs(LOG_DIR)
            print(f"Created log directory at {LOG_DIR}")
        except Exception as e:
            print(f"Error creating log directory: {e}")
    
    # Debug print to verify directory exists
    print(f"Log directory exists: {os.path.exists(LOG_DIR)}")
    
    # Rotate old log files
    rotate_log_files()
    
    # Create new log file with timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_filename = os.path.join(LOG_DIR, f"chess_game_{timestamp}.log")
    
    # Print debug information
    print(f"Creating new log file: {log_filename}")
    
    # Configure logging
    try:
        # Clear existing handlers from root logger
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)
        
        # Configure basic logging to file
        logging.basicConfig(
            filename=log_filename,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filemode='w'  # Overwrite if exists
        )
        
        # Add console handler for important messages
        console = logging.StreamHandler()
        console.setLevel(logging.WARNING)
        formatter = logging.Formatter('%(levelname)s: %(message)s')
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)
        
        print(f"Logging configured to {log_filename}")
        return log_filename
    except Exception as e:
        print(f"Error setting up logging: {e}")
        return None

def rotate_log_files():
    """Rotate log files, keeping only MAX_LOG_FILES most recent"""
    if not os.path.exists(LOG_DIR):
        print(f"Log directory {LOG_DIR} doesn't exist, skipping rotation")
        return
    
    try:
        log_files = [f for f in os.listdir(LOG_DIR) if f.startswith("chess_game_")]
        print(f"Found {len(log_files)} existing log files")
        
        if len(log_files) >= MAX_LOG_FILES:
            # Sort by name (which includes timestamp)
            log_files.sort(reverse=True)
            
            # Delete older files
            files_to_delete = log_files[MAX_LOG_FILES:]
            print(f"Removing {len(files_to_delete)} old log files")
            
            for file in files_to_delete:
                try:
                    file_path = os.path.join(LOG_DIR, file)
                    os.remove(file_path)
                    print(f"Deleted old log file: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file}: {e}")
    except Exception as e:
        print(f"Error during log rotation: {e}")

def reset_game_state():
    """Reset game state variables and start new log"""
    global move_counts, warning_count, capture_missed_count, move_time_sum, move_count
    
    print("Resetting game state...")
    
    # Reset game state
    move_counts = {}
    warning_count = 0
    capture_missed_count = 0
    move_time_sum = 0
    move_count = 0
    
    # Set up new log file
    log_file = setup_logging()
    print(f"New log file created: {log_file}")
    
    try:
        logging.info(f"Starting new chess game at {datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}")
        print("Game start logged successfully")
    except Exception as e:
        print(f"Error writing to log: {e}")

def log_game_result(gs, player_color="black"):
    """Log the game result including scores for each side."""
    logging.info("===== GAME FINISHED =====")
    
    # Calculate material counts
    white_material = 0
    black_material = 0
    piece_counts = {"w": {}, "b": {}}
    
    for row in gs.board:
        for square in row:
            if square != "--":
                piece_color = square[0]
                piece_type = square[1]
                
                # Count material
                if piece_color == "w":
                    white_material += piece_score.get(piece_type, 0)
                    if piece_type in piece_counts["w"]:
                        piece_counts["w"][piece_type] += 1
                    else:
                        piece_counts["w"][piece_type] = 1
                else:
                    black_material += piece_score.get(piece_type, 0)
                    if piece_type in piece_counts["b"]:
                        piece_counts["b"][piece_type] += 1
                    else:
                        piece_counts["b"][piece_type] = 1
    
    # Log game outcome
    if gs.checkmate:
        winner = "Black" if gs.whiteToMove else "White"
        logging.info(f"Checkmate! {winner} wins the game.")
    elif gs.stalemate:
        logging.info("Stalemate! The game is a draw.")
    else:
        logging.info("Game ended without checkmate or stalemate.")
    
    # Log material score
    logging.info(f"Material Score - White: {white_material}, Black: {black_material}")
    
    # Log piece counts
    logging.info(f"White pieces: {piece_counts['w']}")
    logging.info(f"Black pieces: {piece_counts['b']}")
    
    # Log position evaluation from bot's perspective
    final_score = scoreBoard(gs)
    perspective = "Black" if player_color == "black" else "White"
    logging.info(f"Final position score from {perspective}'s perspective: {final_score}")
    
    # Log performance metrics
    log_performance_metrics()
    
    logging.info("========================")

def log_performance_metrics():
    """Log performance metrics for the bot."""
    global warning_count, capture_missed_count, move_time_sum, move_count
    
    logging.info("===== BOT PERFORMANCE METRICS =====")
    
    # Calculate relevant metrics
    avg_move_time = move_time_sum / max(move_count, 1)
    
    logging.info(f"Total moves played: {move_count}")
    logging.info(f"Average move calculation time: {avg_move_time:.2f} seconds")
    logging.info(f"Suboptimal moves selected: {warning_count}")
    logging.info(f"Valuable captures missed: {capture_missed_count}")
    
    # Calculate an estimated performance rating
    estimated_rating = 800  # Base rating for a beginner
    
    # Adjust rating based on metrics
    if avg_move_time > 1.0:  # Thinking time bonus
        estimated_rating += 100
    
    # Penalize for bad moves and missed captures
    error_rate = (warning_count + capture_missed_count) / max(move_count, 1)
    if error_rate < 0.1:
        estimated_rating += 300
    elif error_rate < 0.2:
        estimated_rating += 200
    elif error_rate < 0.3:
        estimated_rating += 100
    elif error_rate > 0.5:
        estimated_rating -= 100
    
    logging.info(f"Error rate: {error_rate:.2f}")
    logging.info(f"Estimated playing strength: ~{estimated_rating} Elo")
    
    logging.info("===================================")

def findBestMove(gs, validMoves):
    global nextMove, boardStates, warning_count, capture_missed_count, move_time_sum, move_count
    
    # Check if this is first move of a new game - THIS IS CRITICAL
    if len(gs.moveLog) == 0:
        print("First move detected, resetting game state...")
        reset_game_state()
        print("Game state reset and new log file created")
    
    # Start timing
    start_time = time.time()
    
    # Log number of valid moves
    logging.info(f"Analyzing {len(validMoves)} valid moves")
    
    # Exit early if no valid moves
    if not validMoves:
        logging.warning("No valid moves available!")
        return None
    
    # First, evaluate all moves directly with simple material counting
    move_scores = []
    for move in validMoves:
        # Make the move
        gs.makeMove(move)
        # Evaluate resulting position
        if gs.checkmate:
            score = -CHECKMATE if gs.whiteToMove else CHECKMATE
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = -scoreBoard(gs) if gs.whiteToMove else scoreBoard(gs)
        # Unmake the move
        gs.undoMove()
        # Store move with score
        move_scores.append((move, score))
    
    # Sort moves by score (higher is better)
    move_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Check for immediate checkmate
    for move, score in move_scores:
        if score >= CHECKMATE - 1:  # Checkmate in 1
            logging.info(f"Found checkmate in 1: {move.getChessNotation()}")
            return move
    
    # Check for high-value captures (queen or rook)
    for move, score in move_scores:
        if move.isCapture() and move.pieceCaptured[1] in ['Q', 'R']:
            logging.info(f"Found high-value capture: {move.getChessNotation()} capturing {move.pieceCaptured}")
            return move
    
    # Initialize nextMove to None (will be set in search)
    nextMove = None
    
    # Run deeper search with iterative deepening
    for depth in range(1, DEPTH + 1):
        logging.info(f"Searching at depth {depth}")
        search_score = findNegaMaxAlphaBeta(gs, validMoves, depth, -CHECKMATE, CHECKMATE, 
                                           1 if gs.whiteToMove else -1)
        if nextMove:  
            logging.info(f"Best move at depth {depth}: {nextMove.getChessNotation()}")
            logging.info(f"Best score at depth {depth}: {search_score}")
    
    # Log top 5 moves from simple evaluation
    logging.info("Top moves by direct evaluation:")
    for i in range(min(5, len(move_scores))):
        move, score = move_scores[i]
        logging.info(f"Top move {i+1}: {move.getChessNotation()} with score {score}")
    
    # *** CRITICAL FIX - ALWAYS SELECT BEST MOVE ***
    # If the search didn't find a move or found a significantly worse move, use the best from direct evaluation
    if not nextMove or (move_scores and nextMove and 
                      next((s for m, s in move_scores if m == nextMove), -float('inf')) < move_scores[0][1] - 0.5):
        # Select the best move from direct evaluation
        best_move = move_scores[0][0]
        best_score = move_scores[0][1]
        
        if nextMove:
            nextMove_score = next((s for m, s in move_scores if m == nextMove), -float('inf'))
            logging.warning(f"Overriding search result: {nextMove.getChessNotation()} with score {nextMove_score}")
            logging.warning(f"Selecting better move: {best_move.getChessNotation()} with score {best_score}")
        else:
            logging.info(f"Search didn't find a move, selecting: {best_move.getChessNotation()} with score {best_score}")
        
        nextMove = best_move
    
    # Final verification
    if nextMove:
        selected_score = next((score for move, score in move_scores if move == nextMove), None)
        best_score = move_scores[0][1] if move_scores else None
        
        logging.info(f"FINAL SELECTION: {nextMove.getChessNotation()} with score {selected_score}")
        logging.info(f"Best available score: {best_score}")
        
        # Still warn if we're not taking the best move (for debugging)
        if selected_score is not None and best_score is not None and selected_score < best_score - 0.5:
            logging.warning(f"Selected move score {selected_score} is significantly worse than best move score {best_score}")
            warning_count += 1
    
    # Track move time
    end_time = time.time()
    move_time = end_time - start_time
    move_time_sum += move_time
    move_count += 1
    
    logging.info(f"Move calculation took {move_time:.2f} seconds")
    
    return nextMove

def findNegaMaxAlphaBeta(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, searchedPositions
    
    # Base case
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    # Move ordering - evaluate captures first
    # Sort moves to help alpha-beta pruning
    if depth > 1:
        validMoves.sort(key=lambda move: 
                       (1000 if move.isCapture() else 0) + 
                       (10 if move.isPawnPromotion else 0),
                       reverse=True)
    
    # Maximizing
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.makeMove(move)
        nextMoves = gs.getValidMoves()
        
        # Check for game-ending conditions first
        if gs.checkmate:
            score = CHECKMATE  # Win for current player
        elif gs.stalemate:
            score = STALEMATE
        else:
            score = -findNegaMaxAlphaBeta(gs, nextMoves, depth - 1, -beta, -alpha, -turnMultiplier)
        
        gs.undoMove()
        
        # Update best score and move
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:  # At the top level, update nextMove
                nextMove = move
        
        # Update alpha for pruning
        alpha = max(alpha, maxScore)
        if alpha >= beta:
            break  # Pruning
    
    return maxScore

def scoreBoard(gs):
    """
    Evaluate the current board position
    Positive score favors white, negative score favors black
    """
    if gs.checkmate:
        if gs.whiteToMove:
            return -CHECKMATE  # Black wins
        else:
            return CHECKMATE  # White wins
    
    if gs.stalemate:
        return STALEMATE
    
    score = 0
    
    # Determine game phase (middlegame or endgame)
    total_material = 0
    for row in gs.board:
        for square in row:
            if square != '--':
                piece_type = square[1]
                if piece_type in piece_score:
                    total_material += piece_score[piece_type]
    
    is_endgame = total_material <= 25  # Threshold for endgame

    # Loop through all board squares
    for r in range(8):
        for c in range(8):
            square = gs.board[r][c]
            if square != '--':  # Not an empty square
                piece_color = square[0]
                piece_type = square[1]
                
                # Material value
                if piece_type in piece_score:
                    if piece_color == 'w':
                        score += piece_score[piece_type]
                    else:
                        score -= piece_score[piece_type]
                
                # Positional value from piece-square tables
                # Flip the row index for black pieces
                if piece_type == 'p':
                    table = piece_position_tables['p']
                    if piece_color == 'w':
                        score += table[r][c]
                    else:
                        score -= table[7-r][c]  # Flip for black perspective
                elif piece_type == 'K':
                    # Different tables for middlegame and endgame
                    if is_endgame:
                        table = piece_position_tables['K_end']
                    else:
                        table = piece_position_tables['K_mid']
                        
                    if piece_color == 'w':
                        score += table[r][c]
                    else:
                        score -= table[7-r][c]  # Flip for black perspective
                elif piece_type in ['N', 'B', 'R', 'Q']:
                    table = piece_position_tables[piece_type]
                    if piece_color == 'w':
                        score += table[r][c]
                    else:
                        score -= table[7-r][c]  # Flip for black perspective
    
    # Mobility bonus (simplified)
    if gs.whiteToMove:
        score += len(gs.getValidMoves()) * 0.05  # Small bonus for each legal move
    else:
        score -= len(gs.getValidMoves()) * 0.05
        
    # Evaluate pawn structure (simplified)
    white_pawns_by_file = [0] * 8
    black_pawns_by_file = [0] * 8
    
    for r in range(8):
        for c in range(8):
            if gs.board[r][c] == 'wp':
                white_pawns_by_file[c] += 1
            elif gs.board[r][c] == 'bp':
                black_pawns_by_file[c] +=.1
    
    # Penalize doubled pawns
    for file in range(8):
        if white_pawns_by_file[file] > 1:
            score -= 0.2 * (white_pawns_by_file[file] - 1)
        if black_pawns_by_file[file] > 1:
            score += 0.2 * (black_pawns_by_file[file] - 1)
    
    # Penalize isolated pawns (simplified)
    for file in range(8):
        if white_pawns_by_file[file] > 0:
            is_isolated = True
            if file > 0 and white_pawns_by_file[file-1] > 0:
                is_isolated = False
            if file < 7 and white_pawns_by_file[file+1] > 0:
                is_isolated = False
            if is_isolated:
                score -= 0.3
                
        if black_pawns_by_file[file] > 0:
            is_isolated = True
            if file > 0 and black_pawns_by_file[file-1] > 0:
                is_isolated = False
            if file < 7 and black_pawns_by_file[file+1] > 0:
                is_isolated = False
            if is_isolated:
                score += 0.3
    
    return score
