const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");


// ---------- RESPONSIVE CANVAS ----------

function resize(){

  if(window.innerWidth < 768){

    canvas.width = window.innerWidth - 20;
    canvas.height = window.innerHeight - 120;

  }else{

    canvas.width = 900;
    canvas.height = 600;
  }
}

resize();
window.addEventListener("resize", resize);


// ---------- USER ----------

const username = document.getElementById("username").value;


// ---------- AUDIO ----------

const music = new Audio("/static/game/sound/saiyarmori.mp3");
const gameOverSound = new Audio("/static/game/sound/wl.mp3");

music.loop = true;


// ---------- IMAGES ----------

const faceImg = new Image();
faceImg.src = "/static/game/vinit-removeb.png";

const pipeImg = new Image();
pipeImg.src = "/static/game/cigarette.png";


// ---------- PLAYER ----------

let bird = {
  x:150,
  y:200,
  size:60,
  gravity:0.45,
  lift:-9,
  velocity:0
};


// ---------- GAME DATA ----------

let pipes = [];
let gap = 200;
let frame = 0;
let score = 0;
let gameOver = false;
let musicStarted = false;


// ---------- CONTROL ----------

function jump(){

  if(gameOver) return;

  bird.velocity = bird.lift;

  if(!musicStarted){

    musicStarted = true;
    music.volume = 0.4;
    music.play();
  }
}


document.addEventListener("touchstart", jump);
document.addEventListener("keydown", e=>{

  if(e.code==="Space"){
    if(gameOver){
      resetGame();
    }else{
      jump();
    }
  }

});


// ---------- PIPE ----------

function createPipe(){

  let min = 100;
  let max = canvas.height-gap-100;

  let top = Math.random()*(max-min)+min;

  pipes.push({
    x:canvas.width,
    top:top,
    bottom:top+gap,
    width:60,
    passed:false
  });
}


// ---------- RESET ----------

function resetGame(){

  bird.y = canvas.height/2;
  bird.velocity = 0;

  pipes = [];
  frame = 0;
  score = 0;

  gameOver = false;

  animate();
}


// ---------- SAVE SCORE ----------

function saveScore(){

  fetch("/save_score",{
    method:"POST",
    headers:{
      "Content-Type":"application/x-www-form-urlencoded"
    },
    body:"username="+username+"&score="+score
  });
}


// ---------- MAIN LOOP ----------

function animate(){

  ctx.clearRect(0,0,canvas.width,canvas.height);


  // Physics
  bird.velocity += bird.gravity;
  bird.y += bird.velocity;


  // Draw player
  ctx.drawImage(
    faceImg,
    bird.x-bird.size/2,
    bird.y-bird.size/2,
    bird.size,
    bird.size
  );


  // Create pipes
  if(frame%120===0){
    createPipe();
  }


  pipes.forEach(p=>{

    p.x -= 3;

    // Top
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


    // Bottom
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

    let pipeL = p.x+15;
    let pipeR = p.x+p.width-15;


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


  if(gameOver){

    ctx.fillStyle="red";
    ctx.font="36px Arial";

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


// ---------- START ----------

animate();
