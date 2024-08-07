# Chess AI
The game chess along with an AI bot for the user to play against.

## Implementation

This repo incorporates the game of Chess that can be played by either a person using the mouse, or by an AI. The UI allows players to use their mouse to manually make moves if the person mode is chosen.

The AI is implemented using the [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm, along with the [alpha-beta pruning](https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning) optimization. With this optimization, the AI is able to look 5 moves into the future, which isn't much.

**Future Work:** Some things I hope to incorporate in the near future include:
- Using bitboards to get possible moves and apply chosen moves faster.
- Implementing an opening book. The opening is the hardest part of the Chess game because it involves many many moves of studied play that can't be seen with a simple minimax AI. An opening book can be generated by looking at previous games by famous players. Unfortunately, though, a simple opening book can be easily broken by playing a non-standard move.
- An improved heuristic. The current heuristic is simply the piece values of either team, however a lot more factors matter in chess including position, mid control, king safety, etc.
- A supervised version of the AlphaZero Chess AI. While a completely unsupervised version would take forever to train on a standard laptop, a supervised / guided version should be able to converge faster, although it may not be as optimal.


## Usage

**Pre-requisites:** Make sure you first install the pre-reqs using `pip install -r requirements.txt`.

The main code is in `main.py`. Simply run the `start_game` method to construct a `Game` object to either play AI vs. AI, Human vs. AI (Human is white), AI vs. Human (Human is black), or Human vs. Human.

Additionally, there exists a `test_minimax.py` that provides a nice visual display of the searching performed by the `MinimaxAI`.

