class Player{
  constructor(tileLength, color){
    //Adding all the pieces for the player
    this.pieces = [];
    this.backrow = 0;
    this.color = color;
    let pawn_start = 1;
    let idMult = 1;
    if(color == "black"){
      pawn_start = 6;
      this.backrow = 7;
      idMult = -1;
    }
    for(let i = 0; i < 8; i++){
      this.pieces.push(new Pawn(i, pawn_start, color, tileLength, (i+1)*idMult));
    }
    this.pieces.push(new Rook(0,this.backrow,color,tileLength, 9*idMult));
    this.pieces.push(new Knight(1,this.backrow,color,tileLength, 10*idMult));
    this.pieces.push(new Bishop(2,this.backrow,color,tileLength, 11*idMult));
    this.pieces.push(new Queen(3,this.backrow,color,tileLength, 12*idMult));
    this.pieces.push(new King(4,this.backrow,color,tileLength, 13*idMult));
    this.pieces.push(new Bishop(5,this.backrow,color,tileLength, 14*idMult));
    this.pieces.push(new Knight(6,this.backrow,color,tileLength, 15*idMult));
    this.pieces.push(new Rook(7,this.backrow,color,tileLength, 16*idMult));
  }

  findPossibleMoves(board){
    for(let i = 0; i < this.pieces.length; i++){
      this.pieces[i].possibleMoves(board);
    }
  }

  draw(){
    for(let i = 0; i < this.pieces.length; i++){
      this.pieces[i].draw();
    }

  }

  countPoints(){
    let sum = 0;
    for(let i = 0; i < this.pieces.length; i++){
      sum += this.pieces[i].points;
    }
    return sum;
  }

  getAllMoves(board){
    this.findPossibleMoves(board);
    let allMoves = [];
    for(let i = 0; i < this.pieces.length; i++){
      allMoves.push([this.pieces[i],this.pieces[i].possible]);
    }
    return allMoves;
  }

  //Precondition: this.possibleMoves(board) is previously called
  getUnusualMoves(board){
//    this.possibleMoves(board);
    let unusualMoves = [];
    let gotPawn = false;
    for(let i = 0; i < this.pieces.length; i++){
      let piece = this.pieces[i];
      if(piece.name == "pawn"){
        if(gotPawn)
          continue;
        for(let j = 0; j < piece.possible.length; j++){
          if(piece.possible[j][1] == 0 || piece.possible[j][1] == 7){
            unusualMoves.push(["Promotion",piece,"queen",9]);
            unusualMoves.push(["Promotion",piece,"rook",5]);
            unusualMoves.push(["Promotion",piece,"knight",3]);
            unusualMoves.push(["Promotion",piece,"bishop",3]);
            piece.possible.splice(j,1);
            gotPawn = true;
            break;
          }
        }
      }
      else if(piece.name == "king"){
        if(piece.hasMoved){
          continue;
        }
        //Check left side
        let tempPiece = getPiece(0,this.backrow);
        let noWork = false;
        for(let i = 1; i < 4; i++){
          if(board[i][this.backrow] != -1){
            noWork = true;
          }
        }
        if(tempPiece != -1 && !noWork)
          if(tempPiece.hasMoved == false)
            unusualMoves.push(["Castle",tempPiece,piece,0.5]);
        tempPiece = getPiece(7,this.backrow);
        noWork = false;
        for(let i = 5; i < 6; i++){
          if(board[i][this.backrow] != -1){
            noWork = true;
          }
        }
        if(tempPiece != -1 && !noWork)
          if(tempPiece.hasMoved == false)
            unusualMoves.push(["Castle",piece,tempPiece,0.5]);
      }
    }
    return unusualMoves;
  }

  getPiece(id){
    for(let i = 0; i < this.pieces.length; i++){
      if(this.pieces[i].id == id)
        return this.pieces[i];
    }
    return None;
  }

}
