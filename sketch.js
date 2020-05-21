var white;
var black;
var board;
var tileLength = 65;
var turn = 1;
var moving_piece;
var isMoving = false;
var ai;
var pieces_board = [];
var movesAhead = 3;
var letWhiteDraw = 2;
function setup() {
  createCanvas(900,600);
  // put setup code here
  white = new Player(tileLength, "white");
//  black = new Player(tileLength, "black");
  ai = new AI(tileLength, "black");
  let black = ai.player;
  board = [];
  for(let i = 0; i < 8; i++){
    board.push([]);
    pieces_board.push([]);
    for(let j = 0; j < 8; j++){
      board[i].push(-1);
      pieces_board[i].push(-1);
    }
  }
  for(let i = 0; i < white.pieces.length; i++){
    board[white.pieces[i].x][white.pieces[i].y] = 1;
    board[black.pieces[i].x][black.pieces[i].y] = 0;
    pieces_board[white.pieces[i].x][white.pieces[i].y] = white.pieces[i];
    pieces_board[black.pieces[i].x][black.pieces[i].y] = black.pieces[i];
  }
  white.findPossibleMoves(board);
  black.findPossibleMoves(board);
}

function draw() {
  drawBoard();
  white.draw();

  if(turn == 0){
    letWhiteDraw--;
    if(letWhiteDraw < 0){
    letWhiteDraw = 2;
    console.log("------------------------------------------");
    let bestMoveOutput = ai.findBestMove(white,movesAhead);
    let bestMove = bestMoveOutput[0];
    let bestDifference = bestMoveOutput[1];

    console.log(bestMove);
    console.log(bestDifference);
    ai.movePieceToLocation(bestMove[0],bestMove[1],bestMove[2],white.pieces);
    turn = 1;
    updateBoard();
    white.findPossibleMoves(board);
  }
}
  ai.player.draw();
}

function drawBoard(){
  var blackColor = color(0,0,0);
  var whiteColor = color(255,255,255);
  for(let i = 0; i < 8; i++){
    for(let j = 0; j < 8; j++){
      if((i+j)%2 == 0){
        fill(whiteColor);
      }
      else{
        fill(blackColor);
      }
      rect(i*tileLength,j*tileLength,tileLength,tileLength);
    }
  }
}

//For AI gameplay
function mousePressed(){
  //Make sure the mouse is in the border of the board

  //ONLY FOR AI GAMEPLAY
  if(turn == 0){
    return false;
  }
  let black = ai.player;
  //END OF ONLY FOR AI GAMEPLAY

  if(isMoving){
    return false;
  }
  if(mouseX < tileLength*8 && mouseY < tileLength*8){
    let x_tile = parseInt(mouseX/tileLength);
    let y_tile = parseInt(mouseY/tileLength);
    y_tile = 7 - y_tile;
    let piecesToUse = white.pieces;
    let otherPieces = black.pieces;
    for(let i = 0; i < piecesToUse.length; i++){
      if(piecesToUse[i].x == x_tile && piecesToUse[i].y == y_tile){
        piecesToUse[i].startMoving();
        moving_piece = piecesToUse[i];
        console.log("Got " + moving_piece.color + " piece");
        isMoving = true;
      }
    }
  }
  return false;
}

//For 1v1 gameplay
/*
function mousePressed(){
  //Make sure the mouse is in the border of the board

  if(isMoving){
    return false;
  }
  if(mouseX < tileLength*8 && mouseY < tileLength*8){
    let x_tile = parseInt(mouseX/tileLength);
    let y_tile = parseInt(mouseY/tileLength);
    y_tile = 7 - y_tile;
    let piecesToUse = white.pieces;
    let otherPieces = black.pieces;
    if(turn == 0){
      piecesToUse = black.pieces;
      otherPieces = white.pieces;
    }
    for(let i = 0; i < piecesToUse.length; i++){
      if(piecesToUse[i].x == x_tile && piecesToUse[i].y == y_tile){
        piecesToUse[i].startMoving();
        moving_piece = piecesToUse[i];
        console.log("Got " + moving_piece.color + " piece");
        isMoving = true;
      }
    }
  }
  return false;
}
*/

function move(piecesToUse, otherPieces, x_tile, y_tile){
  y_tile = 7-y_tile;
  if(board[x_tile][y_tile] != -1){
    for(let i = 0; i < otherPieces.length; i++){
      console.log(otherPieces[i].x + " " + otherPieces[i].y);
      if(otherPieces[i].x == x_tile && otherPieces[i].y == y_tile){
        otherPieces.splice(i,1);
        console.log("Capture");
        break;
      }
    }
  }
  updateBoard();
  white.findPossibleMoves(board);
//  black.findPossibleMoves(board);
  return otherPieces;
}

//FOR AI USE
function mouseReleased(){
  //Make sure the mouse is in the border of the board
  noLoop();
  let black = ai.player;
  if(!isMoving){
    return false;
  }
  if(mouseX < tileLength*8 && mouseY < tileLength*8){
    let x_tile = parseInt(mouseX/tileLength);
    let y_tile = parseInt(mouseY/tileLength);
    let poss = moving_piece.possible;
    let piecesToUse = white.pieces;
    let otherPieces = black.pieces;
    for(let j = 0; j < poss.length; j++){
      if(arraysEqual(poss[j],[x_tile,7-y_tile])){
        moving_piece.stopMoving(true);
        move(piecesToUse, otherPieces, x_tile, y_tile);
        console.log("Released piece");
        isMoving = false;
        turn = 1 - turn;
        loop();
        return false;
      }
    }
    moving_piece.stopMoving(false);
    isMoving = false;
    console.log("Released piece");
  }
  loop();
  return false;
}

/*
function mouseReleased(){
  //Make sure the mouse is in the border of the board
  if(!isMoving){
    return false;
  }
  if(mouseX < tileLength*8 && mouseY < tileLength*8){
    let x_tile = parseInt(mouseX/tileLength);
    let y_tile = parseInt(mouseY/tileLength);
    let poss = moving_piece.possible;
    let piecesToUse = white.pieces;
    let otherPieces = black.pieces;
    if(moving_piece.color == "black"){
      piecesToUse = black.pieces;
      otherPieces = white.pieces;
    }
    for(let j = 0; j < poss.length; j++){
      if(arraysEqual(poss[j],[x_tile,7-y_tile])){
        moving_piece.stopMoving(true);
        move(piecesToUse, otherPieces, x_tile, y_tile);
        turn = 1 - turn;
        console.log("Released piece");
        isMoving = false;
        return false;
      }
    }
    moving_piece.stopMoving(false);
    isMoving = false;
    console.log("Released piece");
  }
  return false;
}
*/



function arraysEqual(arr1, arr2) {
    if(arr1.length !== arr2.length)
        return false;
    for(var i = arr1.length; i--;) {
        if(arr1[i] !== arr2[i])
            return false;
    }

    return true;
}

function updateBoard(){
  let black = ai.player;
  for(let i = 0; i < board.length; i++){
    for(let j = 0; j < board.length; j++){
      board[i][j] = -1;
      pieces_board[i][j] = -1;
    }
  }
  for(let i = 0; i < white.pieces.length; i++){
    board[white.pieces[i].x][white.pieces[i].y] = 1;
    pieces_board[white.pieces[i].x][white.pieces[i].y] = white.pieces[i];
  }
  for(let i = 0; i < black.pieces.length; i++){
    board[black.pieces[i].x][black.pieces[i].y] = 0;
    pieces_board[black.pieces[i].x][black.pieces[i].y] = black.pieces[i];
  }

}

function getPiece(x,y){
    if(board[x][y] == -1)
      return -1;
    if(board[x][y] == 1){
      for(let i = 0; i < white.pieces.length; i++){
        if(white.pieces[i].x == x && white.pieces[i].y == y)
          return white.pieces[i];
      }
    }
    if(board[x][y] == 0){
      for(let i = 0; i < black.pieces.length; i++){
        if(black.pieces[i].x == x && black.pieces[i].y == y)
          return black.pieces[i];
      }
    }
  }
