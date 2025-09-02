let width = 1440;
let height = 900;
let logo, main_menu, play_button, settings_button, upload_button, info_button;

function preload(){
  logo = loadImage('logo.png');
  play_button = loadImage("play_button.png")
  main_menu = loadImage("menu_container.png")
  settings_button = loadImage("settings_button.png")
  upload_button = loadImage("upload_button.png")
  info_button = loadImage("info_button.png")
}

function setup() {
  textAlign(CENTER);
  rectMode(CENTER);
  imageMode(CENTER);
  createCanvas(width, height);
  background(255, 247, 252);
  menu();
  
  logo.resize(1000, 0);
  image(logo, width/2, height-600);
  
  
  play();
}

function draw() {
  
  
}

function play() {
  play_button.resize(450, 0)
  image(play_button, width-550, height/2+80)

}

function menu() {
  let menu_w = 600
  let menu_h = 530
  main_menu.resize(600,0)
  image(main_menu, menu_w, menu_h)
  settings_button.resize(600,0)
  image(settings_button, menu_w+20, menu_h)
  //image(settings_button, menu_w+20, menu_h)
  upload_button.resize(600,0)
  image(upload_button, menu_w+20, menu_h)
  info_button.resize(600,0)
  image(info_button, menu_w+20, menu_h)
}

function settings() {
  print("settings")
}

// function mousePressed(){
//   if (mouseX 
// }