class AI{
  constructor(tileLength, color){

    this.movesAhead = 3;

    this.tileLength = tileLength;
    this.color = color;
    this.player = new Player(tileLength, color);
    this.allPossibilities = []
    this.backrow = 0;
    if(this.color == "black"){
      this.backrow = 7;
    }
    this.player.pieces[12].points = 100000;
  }

  findPossibleMoves(){
    for(let i = 0; i < this.player.pieces.length; i++){
      this.player.pieces[i].possibleMoves(board);
//      this.checkPawnPromotion(i);
    }
  }
/*
  checkPawnPromotion(i){
    if(this.pieces[i].name == "pawn"){
      if(this.pieces[i].y == 7-this.backrow){
        let pawnToPromote = this.pieces[i];
        if(pawnToPromote.y == this.backrow){
          this.allPossibilities.push([pawnToPromote,["QUEEN","ROOK","BISHOP","KNIGHT"]);
        }
      }
    }
  }
*/
  calculateAllMoves(){
    this.findPossibleMoves();
    this.allPossibilities = [];
    for(let i = 0; i < this.player.pieces.length; i++){
//      console.log("Piece: " + this.player.pieces[i]);
      this.allPossibilities.push([this.player.pieces[i],this.player.pieces[i].possible]);
//      this.checkPawnPromotion(i);
    }
  }

  findBestMove(opponentPlayer,recur){
//    return this.findBestMoveRecur(this.player,opponentPlayer,recur,false);
    let stuff = this.findBestMoveRecur(this.player,opponentPlayer,this.movesAhead,false,false,-1 * Infinity, Infinity);
    console.log(stuff[2]);
    return stuff;
  }

  findBestMoveRecur(playerMoving,playerAgainst,recur,verbose,isMaximizingPlayer,alpha,beta){
    let listyBoi = [];
    recur = recur - 1;
    let piecesToMove = playerMoving.pieces;
    let piecesAgainst = playerAgainst.pieces;
    updateBoard();
    let allMoves = playerMoving.getAllMoves(board);
    let maxRemoved = -Infinity;
    if(!isMaximizingPlayer)
      maxRemoved = Infinity;
    let bestRemovedIndex = -1;
    let bestMove = [];
    let bestRemoved = undefined;
    let allBestMoves = [];

    outer:
    for(let i = 0; i < allMoves.length; i++){
      let currentPiece = allMoves[i][0];
      let currentPossMoves = allMoves[i][1];
      let originalX = currentPiece.x;
      let originalY = currentPiece.y;

      if(verbose){
        console.log("------------------");
        console.log(currentPiece);
        console.log(currentPossMoves);
      }

      for(let j = 0; j < currentPossMoves.length; j++){
        let toMoveX = currentPossMoves[j][0];
        let toMoveY = currentPossMoves[j][1];
        currentPiece.x = toMoveX;
        currentPiece.y = toMoveY;

        let removed = undefined;
        let difference = 0;
        let tempIndex = -1;
        for(let k = piecesAgainst.length-1; k >= 0; k--){
          if(piecesAgainst[k].x == toMoveX && piecesAgainst[k].y == toMoveY){
            removed = piecesAgainst.splice(k,1);
            removed = removed[0];
            difference = removed.points;
            tempIndex = k;
            break;
          }
        }

        if(verbose){
          console.log("-----");
          console.log([currentPiece.x,currentPiece.y]);
          console.log(removed);
          console.log(difference);
        }

        if(recur > 0){
          let oppBestOutput = this.findBestMoveRecur(playerAgainst,playerMoving,recur,verbose,!isMaximizingPlayer,alpha,beta);
          let oppBestMove = oppBestOutput[0];
          let oppDiff = oppBestOutput[1];
          difference -= oppDiff;
          listyBoi.push([currentPiece,toMoveX,toMoveY,difference],oppBestOutput[2],[alpha,beta]);
        }
        else{
          listyBoi.push([currentPiece,toMoveX,toMoveY,difference]);
        }

        if(!isMaximizingPlayer){
          difference *= -1;
        }

        if(removed != undefined){
          piecesAgainst.splice(tempIndex,0,removed);
        }
        currentPiece.x = originalX;
        currentPiece.y = originalY;

        if(difference == maxRemoved){
          allBestMoves.push([currentPiece,toMoveX,toMoveY]);
        }

        if(!isMaximizingPlayer){
          if(difference < maxRemoved){
            maxRemoved = difference;
            bestMove = [currentPiece,toMoveX,toMoveY];
            bestRemovedIndex = tempIndex;
            bestRemoved = removed;
            allBestMoves = [bestMove];
          }
          beta = min(beta,maxRemoved);
        }
        else{
          if(difference > maxRemoved){
            maxRemoved = difference;
            bestMove = [currentPiece,toMoveX,toMoveY];
            bestRemovedIndex = tempIndex;
            bestRemoved = removed;
            allBestMoves = [bestMove];
          }
          alpha = max(alpha,maxRemoved);
        }
        if(beta <= alpha){
          if(verbose)
            console.log(alpha,beta);
          break outer;
        }

      }
    }
    let random = Math.random() * allBestMoves.length;
    let randBestMove = allBestMoves[Math.floor(random)];

    if(verbose){
      if(recur == this.movesAhead-1){
        console.log("All best moves");
        console.log(allBestMoves);
      }
    }

    if(!isMaximizingPlayer)
      maxRemoved *= -1;

    return [randBestMove,maxRemoved,listyBoi];
  }

  movePieceToLocation(piece,x_value,y_value,oppPieces){
    for(let i = 0; i < oppPieces.length; i++){
      if(oppPieces[i].x == x_value && oppPieces[i].y == y_value){
        oppPieces.splice(i,1);
        break;
      }
    }
    piece.x = x_value;
    piece.y = y_value;
  }




}
