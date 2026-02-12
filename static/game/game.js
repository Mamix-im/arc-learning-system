const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");


// ---------------- RESPONSIVE CANVAS ----------------

function resizeCanvas(){

  if(window.innerWidth < 800){

    canvas.width = window.innerWidth - 10;
    canvas.height = window.innerHeight - 100;

  }else{

    canvas.width = 900;
    canvas.height = 600;
  }
}

resizeCanvas();
window.addEventListener("resize", resizeCanvas);


// ---------------- USER ----------------

const username = document.getElementById("username").value;


// ---------------- AUDIO ----------------

const music = new Audio("/static/game/sound/saiyarmori.mp3");
const gameOverSound = new Audio("/static/game/sound/wl.mp3");

music.loop = true;


// ---------------- IMAGES ----------------

const faceImg = new Image();
faceImg.src = "/static/game/vinit-removeb.png";

const pipeImg = new Image();
pipeImg.src = "/static/game/cigarette.png";


// ---------------- PLAYER ----------------

let bird = {
  x:150,
  y:200,
  size:55,
  gravity:0.45,
  lift:-9,
  velocity:0
};


// ---------------- GAME DATA ----------------

let pipes = [];
let gap = 190;
let frame = 0;
let score = 0;
let gameOver = false;
let musicStarted = false;
let scoreSaved = false;


// ---------------- CONTROL ----------------

function jump(){

  if(gameOver) return;

  bird.velocity = bird.lift;

  if(!musicStarted){

    musicStarted = true;
    music.volume = 0.4;
    music.play();
  }
}


function handleInput(){

  if(gameOver){

    resetGame();

  }else{

    jump();
  }
}


// MOBILE
document.addEventListener("touchstart", function(e){

  e.preventDefault();
  handleInput();

},{passive:false});


// KEYBOARD
document.addEventListener("keydown", e=>{

  if(e.code==="Space"){
    handleInput();
  }

});


// ---------------- PIPE ----------------

function createPipe(){

  let min = 100;
  let max = canvas.height-gap-100;

  let top = Math.random()*(max-min)+min;

  pipes.push({
    x:canvas.width,
    top:top,
    bottom:top+gap,
    width:55,
    passed:false
  });
}


// ---------------- RESET ----------------

function resetGame(){

  bird.y = canvas.height/2;
  bird.velocity = 0;

  pipes = [];
  frame = 0;
  score = 0;

  gameOver = false;
  scoreSaved = false;

  animate();
}


// ---------------- SAVE SCORE ----------------

function saveScore(){

  if(scoreSaved) return;

  scoreSaved = true;

  fetch("/save_score",{
    method:"POST",
    headers:{
      "Content-Type":"application/x-www-form-urlencoded"
    },
    body:"username="+username+"&score="+score
  });
}


// ---------------- MAIN LOOP ----------------

function animate(){

  ctx.clearRect(0,0,canvas.width,canvas.height);


  // Physics
  bird.velocity += bird.gravity;
  bird.y += bird.velocity;


  // Draw Player
  ctx.drawImage(
    faceImg,
    bird.x-bird.size/2,
    bird.y-bird.size/2,
    bird.size,
    bird.size
  );


  // Create Pipes
  if(frame%120===0){
    createPipe();
  }


  pipes.forEach(p=>{

    p.x -= 3;


    // Top Pipe
    ctx.save();

    ctx.translate(p.x+p.width/2, p.top/2);
    ctx.rotate(Math.PI);

    ctx.drawImage(
      pipeImg,
      -p.width/2,
      -p.top/2,
      p.width,
      p.top
    );

    ctx.restore();


    // Bottom Pipe
    ctx.drawImage(
      pipeImg,
      p.x,
      p.bottom,
      p.width,
      canvas.height-p.bottom
    );


    // Collision
    let birdL = bird.x-bird.size/2+8;
    let birdR = bird.x+bird.size/2-8;
    let birdT = bird.y-bird.size/2+8;
    let birdB = bird.y+bird.size/2-8;

    let pipeL = p.x+12;
    let pipeR = p.x+p.width-12;


    if(
      birdR > pipeL &&
      birdL < pipeR &&
      (birdT < p.top || birdB > p.bottom)
    ){

      if(!gameOver){

        gameOverSound.play();
        saveScore();
      }

      gameOver = true;
      music.pause();
    }


    // Score
    if(p.x+p.width < bird.x && !p.passed){

      score++;
      p.passed = true;
    }

  });


  // Ground
  if(
    bird.y+bird.size/2 > canvas.height ||
    bird.y-bird.size/2 < 0
  ){

    if(!gameOver){

      gameOverSound.play();
      saveScore();
    }

    gameOver = true;
    music.pause();
  }


  // UI
  ctx.fillStyle="black";
  ctx.font="20px Arial";

  ctx.fillText("Score: "+score,15,30);


  // Game Over
  if(gameOver){

    ctx.fillStyle="red";
    ctx.font="34px Arial";

    ctx.fillText(
      "GAME OVER",
      canvas.width/2-110,
      canvas.height/2
    );

    ctx.font="18px Arial";

    ctx.fillText(
      "Tap / Space to Restart",
      canvas.width/2-110,
      canvas.height/2+35
    );

    return;
  }


  frame++;
  requestAnimationFrame(animate);

}


// ---------------- START ----------------

animate();
