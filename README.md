# pygame-tic-tac-toe-ai

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)  
[![Pygame](https://img.shields.io/badge/pygame-2.6.1-green.svg)](https://www.pygame.org/)  
[![License: MIT](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

A classic Tic-Tac-Toe game implemented in Python with Pygame, featuring a Minimax-based AI opponent and a clean, interactive UI.

---

## ✨ Features

- **Human vs AI**: Play as ‘X’ against a Minimax AI (‘O’) that makes optimal moves.  
- **Randomized Opening**: Either player can start; the AI’s opening move is chosen from equally strong options.  
- **Interactive UI**: Clickable grid, status bar, and two-button menu (Play Again / Quit).  
- **Win/Tie Detection**: Highlights the winning line in red and displays win/tie messages.  
- **Clean Code Structure**: All logic encapsulated in a `TicTacToeGame` class for easy extension.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ (tested on 3.11)  
- Pygame 2.6.1

### Installation

```bash
git clone https://github.com/yourusername/pygame-tic-tac-toe-ai.git
cd pygame-tic-tac-toe-ai
python -m venv venv
source venv/bin/activate    # macOS/Linux
venv\Scripts\activate       # Windows
pip install -r requirements.txt
```

### Running the Game
```
python tic_tac_toe.py
```
---

## ⌨️ Controls

- Left-click on an empty cell to place your ‘X’.
- Click ‘Play Again’ to restart.
- Click ‘Quit’ to exit.

---

## 🛠️ Roadmap

- Add unit tests for the game logic.
- Implement difficulty levels (easy, medium, hard).
- Add score tracking and persistent stats.
- Mobile-friendly UI adaptation.
