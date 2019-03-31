class Board{
  constructor(tileLength){
    this.matrix = [];
    this.square_width = tileLength;
    this.width = this.square_width *8;
  }

  draw(){
    //Draw board
    var black = color(0,0,0);
    var white = color(255,255,255);
    for(let i = 0; i < 8; i++){
      for(let j = 0; j < 8; j++){
        if((i+j)%2 == 0){
          fill(black);
        }
        else{
          fill(white);
        }
        rect(i*this.square_width,j*this.square_width,this.square_width,this.square_width);
      }
    }

  }


}
