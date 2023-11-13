

/* Youtube Link: https://www.youtube.com/watch?v=i7bW41JTL8U */
/* Created by Truzz Blogg */
/* https://www.youtube.com/c/TruzzBlogg/videos */

let redBtn = document.getElementById("red");
let blueBtn = document.getElementById("blue");
let yellowBtn = document.getElementById("yellow");
let lightgreenBtn = document.getElementById("lightgreen");
let grayBtn = document.getElementById("gray");
let greenBtn = document.getElementById("green");
let orangeBtn = document.getElementById("orange");
let imgchange = document.getElementById("imgchange");

redBtn.onclick = function() {

    imgchange.src = "/media/productos/camiseta_roja.jpg";
}

blueBtn.onclick = function() {
    imgchange.src = "/media/productos/camiseta_azul.jpg";
}

yellowBtn.onclick = function() {
    imgchange.src = "/media/productos/camiseta_amarilla.jpg";
}

lightgreenBtn.onclick = function() {

    imgchange.src = "/media/productos/camiseta_verde_claro.jpg";
}

grayBtn.onclick = function() {
    imgchange.src = "/media/productos/camiseta_gris.jpg";
}

greenBtn.onclick = function() {
    imgchange.src = "/media/productos/camiseta_verde.jpg";
}

orangeBtn.onclick = function() {
    imgchange.src = "/media/productos/camiseta_naranja.jpg";
}


let isDragging = false;
let initialX, initialY;

const imageContainer = document.getElementById('image-container');

// Escuchar el evento "mousedown" para comenzar el arrastre
imageContainer.addEventListener('mousedown', (event) => {
  isDragging = true;
  initialX = event.clientX - imageContainer.offsetLeft;
  initialY = event.clientY - imageContainer.offsetTop;
});

// Escuchar el evento "mousemove" para mover la imagen y el texto mientras se hace el clic sostenido
document.addEventListener('mousemove', (event) => {
  if (isDragging) {
    const offsetX = event.clientX - initialX;
    const offsetY = event.clientY - initialY;
    imageContainer.style.left = `${offsetX}px`;
    imageContainer.style.top = `${offsetY}px`;
  }
});

// Escuchar el evento "mouseup" para finalizar el arrastre
document.addEventListener('mouseup', () => {
  isDragging = false;
});


const imagenInput = document.getElementById('imagenInput');
const imagenMostrada = document.getElementById('imagenMostrada');

imagenInput.addEventListener('change', function() {
    const imagenSeleccionada = imagenInput.files[0];
    
    if (imagenSeleccionada) {
        const reader = new FileReader();
        
        reader.addEventListener('load', function() {
            imagenMostrada.setAttribute('src', reader.result);
        });
        
        reader.readAsDataURL(imagenSeleccionada);
    }
});





  
