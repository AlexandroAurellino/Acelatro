
# Acelatro Poker Assistant

A command-line tool to help you play Balatro-style poker strategically, using knowledge-based system (KBS) and rule-based reasoning to recommend optimal plays.

## Overview

Acelatro Poker Assistant is designed to help players make informed decisions in Balatro poker games. The app uses a combination of knowledge representation techniques and rule-based reasoning to analyze your current hand and recommend the best possible plays.

## Features

- **Combo Analysis**: Identify and recommend the best possible poker hands based on your current cards
- **Hand Management**: Track your current hand, played cards, and discarded cards
- **Balatro Rules**: Implements the scoring system and combo definitions specific to Balatro poker
- **Discard Strategy**: Suggest optimal cards to discard based on probability and potential combos
- **Multi-Round Support**: Reset the game state to start fresh in each round

## Installation

1. Clone the repository:
```bash
git clone https://github.com/AlexandroAurellino/Acelatro.git
cd Acelatro
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Run the application:
```bash
python ace.py
```

2. Use the following commands in the main menu:
- `1`: Check current hand
- `2`: Play combo (select cards)
- `3`: Discard cards (select indices)
- `4`: Check discarded cards
- `5`: Check played cards
- `6`: Analyze hand for combos
- `7`: Show combo scores
- `8`: Reset round
- `9`: Quit

## Contributing

Contributions are welcome! Please submit pull requests or open issues for any bugs or feature requests.
