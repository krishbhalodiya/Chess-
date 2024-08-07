ChessAI Project
Overview
This project is a Chess engine built using Python. It includes various AI implementations to simulate chess games. The project is structured with multiple Python files, each responsible for different aspects of the game, such as move generation, evaluation, and the graphical user interface (GUI).

Project Structure
chessMain.py: This is the main entry point for the application. It manages the game loop, initializes the game, and handles user interactions through a graphical interface.

chessEngine.py: This file contains the core logic of the chess engine, including board representation, move generation, and game state evaluation.

chessAI.py: This module implements one of the chess AI algorithms, which includes decision-making processes for the AI's move selection.

chessAI2.py: A secondary chess AI implementation with different strategies or heuristics from the first AI.

chessBot.py: Another variant of a chess-playing bot that uses different algorithms or techniques for making decisions.

Features

Move Generation: Generates all legal moves for a given board position.
Evaluation: Evaluates board positions to determine the best moves.

AI Implementation: Multiple AI strategies to play against, each with unique decision-making processes.
Graphical Interface: A Pygame-based GUI that allows users to interact with the chessboard visually.

Requirements
Python 3.x
Pygame
Additional libraries (if any)
Installation
Clone the repository:
bash
Copy code
git clone https://github.com/your-username/ChessAI.git
Navigate to the project directory:
bash
Copy code
cd ChessAI
Install the required dependencies:
bash
Copy code
pip install -r requirements.txt
Usage
To run the game, execute the following command:

bash
Copy code
python chessMain.py
This will launch the chess game with the graphical interface, allowing you to play against the AI or watch AI vs. AI matches.

