class Piece{
  constructor(startx, starty, tileLength, starting_imageFile, color, points, id){
    this.id = id;
    this.name = starting_imageFile;
    let filepath = starting_imageFile;
    var black = "black";
    var white = "white";
    if(color == black){
      filepath = "b" + filepath;
      this.board_piecenum = 0;
    }
    else{
      filepath = "w" + filepath;
      this.board_piecenum = 1;
    }
    filepath = "images/" + filepath + ".png";
    this.x = startx;
    this.y = starty;
    this.tileLength = tileLength;
    this.image = loadImage(filepath);
    this.points = points;
    this.moving = false;
    this.color = color;
    this.possible = [];
    this.hasMoved = false;
  }
  draw(){
    let bottom = this.tileLength*7;
    if(this.moving){
      image(this.image, mouseX-(this.tileLength/2), mouseY-(this.tileLength/2), this.tileLength, this.tileLength);
    }
    else{
      image(this.image, this.tileLength*this.x, bottom - this.tileLength*this.y, this.tileLength, this.tileLength);
    }
  }

  possibleMoves(board){
    throw new Error("You have to implement the possibleMoves method");
  }

  startMoving(){
    this.moving = true;
  }

  stopMoving(possible){
    this.moving = false;
    if(possible){
      this.x = parseInt(mouseX/this.tileLength);
      this.y = 7 - parseInt(mouseY/this.tileLength);
      this.hasMoved = true;
    }
    this.draw();
  }

  moveToLocation(xvalue, yvalue){
    this.x = xvalue;
    this.y = yvalue;
    this.hasMoved = true;
  }




}

class King extends Piece{
  constructor(startx, starty, color, tileLength){
    let filepath = "king";
    super(startx, starty, tileLength, filepath, color, 100);
  }

  possibleMoves(board){
    let poss = [];
    for(let a = -1; a <= 1; a++){
      for(let b = -1; b <= 1; b++){
        if(a == 0 && b == 0){
          continue;
        }
        if(this.x + a >= 0 && this.x + a < 8 && this.y + b >= 0 && this.y + b < 8){
          if(board[this.x+a][this.y+b] == -1)
            poss.push([this.x+a,this.y+b]);
          else if(board[this.x+a][this.y+b] == 1 - this.board_piecenum)
            poss.push([this.x+a,this.y+b])
        }

      }
    }
    this.possible = poss;
  }

}

class Queen extends Piece{
  constructor(startx, starty, color, tileLength, id){
    let filepath = "queen";
    super(startx, starty, tileLength, filepath, color, 9, id);
  }

  possibleMoves(board){
    let poss = [];
    //Diagonal
    for(let i = 1; i < 8-this.x && i < 8-this.y; i++){
      if(board[this.x+i][this.y+i] != -1){
        if(board[this.x+i][this.y+i] == this.board_piecenum - 1)
          poss.push([this.x+i,this.y+i]);
        break;
      }
      else{
        poss.push([this.x+i,this.y+i]);
      }
    }
    for(let i = 1; i <= this.x && i <= this.y; i++){
      if(board[this.x-i][this.y-i] != -1){
        if(board[this.x-i][this.y-i] == this.board_piecenum - 1)
          poss.push([this.x-i,this.y-i]);
        break;
      }
      else{
        poss.push([this.x-i,this.y-i]);
      }
    }
    for(let i = 1; i < 8-this.x && i <= this.y; i++){
      if(board[this.x+i][this.y-i] != -1){
        if(board[this.x+i][this.y-i] == this.board_piecenum - 1)
          poss.push([this.x+i,this.y-i]);
        break;
      }
      else{
        poss.push([this.x+i,this.y-i]);
      }
    }
    for(let i = 1; i <= this.x && i < 8-this.y; i++){
      if(board[this.x-i][this.y+i] != -1){
        if(board[this.x-i][this.y+i] == this.board_piecenum - 1)
          poss.push([this.x-i,this.y+i]);
        break;
      }
      else{
        poss.push([this.x-i,this.y+i]);
      }
    }


    let closeUp = 7;
    let closeDown = 0;
    let closeRight = 7;
    let closeLeft = 0;

    for(let i = 0; i < board.length; i++){
      if(i < this.x){
        if(board[i][this.y] != -1){
          closeLeft = i;
        }
      }
      else if(i > this.x && closeRight == 7){
        if(board[i][this.y] != -1){
          closeRight = i;
        }
      }
      if(i < this.y){
        if(board[this.x][i] != -1){
          closeDown = i;
        }
      }
      else if(i > this.y && closeUp == 7){
        if(board[this.x][i] != -1){
          closeUp = i;
        }
      }
    }

    if(board[closeLeft][this.y] == 1 - this.board_piecenum || board[closeLeft][this.y] == -1)
      poss.push([closeLeft,this.y]);
    if(board[closeRight][this.y] == 1 - this.board_piecenum || board[closeRight][this.y] == -1)
      poss.push([closeRight,this.y]);
    if(board[this.x][closeUp] == 1 - this.board_piecenum || board[this.x][closeUp] == -1)
      poss.push([this.x,closeUp]);
    if(board[this.x][closeDown] == 1 - this.board_piecenum || board[this.x][closeDown] == -1)
      poss.push([this.x,closeDown]);

    for(let i = closeLeft + 1; i < closeRight; i++){
      if(i == this.x)
        continue;
      poss.push([i,this.y]);
    }
    for(let i = closeDown + 1; i < closeUp; i++){
      if(i == this.y)
        continue;
      poss.push([this.x,i]);
    }
    this.possible = poss;
  }

}

class Bishop extends Piece{
  constructor(startx, starty, color, tileLength, id){
    let filepath = "bishop";
    super(startx, starty, tileLength, filepath, color, 3, id);
  }

  possibleMoves(board){
    let poss = [];
    //Diagonal
    for(let i = 1; i < 8-this.x && i < 8-this.y; i++){
      if(board[this.x+i][this.y+i] != -1){
        if(board[this.x+i][this.y+i] == this.board_piecenum - 1)
          poss.push([this.x+i,this.y+i]);
        break;
      }
      else{
        poss.push([this.x+i,this.y+i]);
      }
    }
    for(let i = 1; i <= this.x && i <= this.y; i++){
      if(board[this.x-i][this.y-i] != -1){
        if(board[this.x-i][this.y-i] == this.board_piecenum - 1)
          poss.push([this.x-i,this.y-i]);
        break;
      }
      else{
        poss.push([this.x-i,this.y-i]);
      }
    }
    for(let i = 1; i < 8-this.x && i <= this.y; i++){
      if(board[this.x+i][this.y-i] != -1){
        if(board[this.x+i][this.y-i] == this.board_piecenum - 1)
          poss.push([this.x+i,this.y-i]);
        break;
      }
      else{
        poss.push([this.x+i,this.y-i]);
      }
    }
    for(let i = 1; i <= this.x && i < 8-this.y; i++){
      if(board[this.x-i][this.y+i] != -1){
        if(board[this.x-i][this.y+i] == this.board_piecenum - 1)
          poss.push([this.x-i,this.y+i]);
        break;
      }
      else{
        poss.push([this.x-i,this.y+i]);
      }
    }
    this.possible = poss;
  }

}

class Rook extends Piece{
  constructor(startx, starty, color, tileLength, id){
    let filepath = "rook";
    super(startx, starty, tileLength, filepath, color, 5, id);
  }

  possibleMoves(board){
    //Lines
    let poss = []
    let closeUp = 7;
    let closeDown = 0;
    let closeRight = 7;
    let closeLeft = 0;

    for(let i = 0; i < board.length; i++){
      if(i < this.x){
        if(board[i][this.y] != -1){
          closeLeft = i;
        }
      }
      else if(i > this.x && closeRight == 7){
        if(board[i][this.y] != -1){
          closeRight = i;
        }
      }
      if(i < this.y){
        if(board[this.x][i] != -1){
          closeDown = i;
        }
      }
      else if(i > this.y && closeUp == 7){
        if(board[this.x][i] != -1){
          closeUp = i;
        }
      }
    }

    if(board[closeLeft][this.y] == 1 - this.board_piecenum || board[closeLeft][this.y] == -1)
      poss.push([closeLeft,this.y]);
    if(board[closeRight][this.y] == 1 - this.board_piecenum || board[closeRight][this.y] == -1)
      poss.push([closeRight,this.y]);
    if(board[this.x][closeUp] == 1 - this.board_piecenum || board[this.x][closeUp] == -1)
      poss.push([this.x,closeUp]);
    if(board[this.x][closeDown] == 1 - this.board_piecenum || board[this.x][closeDown] == -1)
      poss.push([this.x,closeDown]);

    for(let i = closeLeft + 1; i < closeRight; i++){
      if(i == this.x)
        continue;
      poss.push([i,this.y]);
    }
    for(let i = closeDown + 1; i < closeUp; i++){
      if(i == this.y)
        continue;
      poss.push([this.x,i]);
    }
    this.possible = poss;
  }
}

class Knight extends Piece{
  constructor(startx, starty, color, tileLength, id){
    let filepath = "knight";
    super(startx, starty, tileLength, filepath, color, 3, id);
  }

  possibleMoves(board){
    let poss = [];
    if(this.x + 2 < 8){
      if(this.y + 1 < 8){
        if(board[this.x+2][this.y+1] == -1)
          poss.push([this.x+2,this.y+1]);
        if(board[this.x+2][this.y+1] == 1 - this.board_piecenum)
            poss.push([this.x+2,this.y+1]);
      }
      if(this.y - 1 >= 0){
        if(board[this.x+2][this.y-1] != this.board_piecenum)
          poss.push([this.x+2,this.y-1]);
        if(board[this.x+2][this.y-1] == 1 - this.board_piecenum)
            poss.push([this.x+2,this.y-1]);
      }
    }
    if(this.x - 2 >= 0){
      if(this.y + 1 < 8){
        if(board[this.x-2][this.y+1] != this.board_piecenum)
          poss.push([this.x-2,this.y+1]);
        if(board[this.x-2][this.y+1] == 1 - this.board_piecenum)
            poss.push([this.x-2,this.y+1]);
      }
      if(this.y - 1 >= 0){
        if(board[this.x-2][this.y-1] != this.board_piecenum)
          poss.push([this.x-2,this.y-1]);
        if(board[this.x-2][this.y-1] == 1 - this.board_piecenum)
            poss.push([this.x-2,this.y-1]);
      }
    }
    if(this.y + 2 < 8){
      if(this.x + 1 < 8){
        if(board[this.x+1][this.y+2] != this.board_piecenum)
          poss.push([this.x+1,this.y+2]);
        if(board[this.x+1][this.y+2] == 1 - this.board_piecenum)
            poss.push([this.x+1,this.y+2]);
      }
      if(this.x - 1 >= 0){
        if(board[this.x-1][this.y+2] != this.board_piecenum)
          poss.push([this.x-1,this.y+2]);
        if(board[this.x-1][this.y+2] == 1 - this.board_piecenum)
            poss.push([this.x-1,this.y+2]);
      }
    }
    if(this.y - 2 >= 0){
      if(this.x + 1 < 8){
        if(board[this.x+1][this.y-2] != this.board_piecenum)
          poss.push([this.x+1,this.y-2]);
        if(board[this.x+1][this.y-2] == 1 - this.board_piecenum)
            poss.push([this.x+1,this.y-2]);
      }
      if(this.x - 1 >= 0){
        if(board[this.x-1][this.y-2] != this.board_piecenum)
          poss.push([this.x-1,this.y-2]);
        if(board[this.x-1][this.y-2] == 1 - this.board_piecenum)
            poss.push([this.x-1,this.y-2]);
      }
    }
    this.possible = poss;
  }

}

class Pawn extends Piece{
  constructor(startx, starty, color, tileLength, id){
    let filepath = "pawn";
    super(startx, starty, tileLength, filepath, color, 1, id);
  }

  possibleMoves(board){
    let poss = []
    let start_y = 1;
    let change = 1;
    let promoteRow = 7;
    if(this.color == "black"){
      start_y = 6;
      change = -1;
      promoteRow = 0;
    }
    if(this.y != promoteRow){
      if(board[this.x][this.y+change] == -1){
        poss.push([this.x,this.y+change]);
        if(this.y == start_y && board[this.x][this.y+change*2] == -1){
          poss.push([this.x,this.y+change*2])
        }
      }
      if(this.x < 7 && board[this.x+1][this.y+change] == 1-this.board_piecenum){
        poss.push([this.x+1,this.y+change])
      }
      if(this.x > 0 && board[this.x-1][this.y+change] == 1-this.board_piecenum){
        poss.push([this.x-1,this.y+change])
      }
    }
    this.possible = poss;
  }

}
