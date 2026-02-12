const reveal = document.querySelector(".reveal");

let mouseX = innerWidth / 2;
let mouseY = innerHeight / 2;

let currentX = mouseX;
let currentY = mouseY;

let pulse = 0;


document.addEventListener("mousemove", (e) => {
  mouseX = e.clientX;
  mouseY = e.clientY;
});


function animate() {

  currentX += (mouseX - currentX) * 0.06;
  currentY += (mouseY - currentY) * 0.06;

  pulse += 0.02;

  const radius = 320 + Math.sin(pulse) * 6;

  const mask = `radial-gradient(
    circle ${radius}px at ${currentX}px ${currentY}px,
    black 0%,
    rgba(205, 49, 49, 0.85) 50%,
    rgba(54, 3, 3, 0.4) 65%,
    transparent 80%
  )`;

  reveal.style.webkitMaskImage = mask;
  reveal.style.maskImage = mask;

  requestAnimationFrame(animate);
}

animate();
