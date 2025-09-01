// vars
let width = 1440
let height = 900
let logo

// funcs (setup)
function preload() {
logo = loadImage('logo.png');
}

function setup() {
  createCanvas(width, height);
  background(255, 247, 252)

  image(logo, width/2, height/2);
  describe('logo');
}

function draw() {

}

// funcs (screens)
function startingScreen(){
  
}

function gameScreen(){

}

function songList(){

}


// execute
setup();