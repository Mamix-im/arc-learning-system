const username = document.getElementById("username").value;

if(gameOver){
    fetch("/save_score",{
  method:"POST",
  headers:{
    "Content-Type":"application/x-www-form-urlencoded"
  },
  body:"username="+username+"&score="+score
});


  fetch("/save_score",{
    method:"POST",
    headers:{
      "Content-Type":"application/json"
    },
    body:JSON.stringify({
      name:PLAYER,
      score:score
    })
  });

  return;
}
