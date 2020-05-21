# Chess AI
The game chess along with an AI bot for the user to play against.

## Libraries

- [p5.js](https://p5js.org/)

## Structure
*sketch.js* contains the code for drawing the board and pieces on the screen as well as controlling mouse movements.

*pieces.js* contains accessor methods for the pieces, including drawing the pieces and find their possible moves.

*player.js* creates a player object and handles their pieces.

*AI.js* creates an AI object and handles its pieces. The AI uses minimax to look ahead 3 moves, although this number can be altered by changing the *movesAhead* variable in *sketch.js*. Note: increasing this value will delay the AI's response time.

## TODO
- Implement pawn promotions
- Implement castling
- Implement checkmate along with a game over screen

## Running the Code

Start a [local server](https://github.com/processing/p5.js/wiki/Local-server) that allows the browser to access local .png files.

Then open the index.html file on your local server and start playing!
