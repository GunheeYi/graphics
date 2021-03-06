document.addEventListener("DOMContentLoaded", function(){

// constants
const FPS = 30;
const canvas = document.getElementById("canvas");
const c = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;
const NEAR = 1;
const FAR = 10;


function bindKey(k, f) {
    document.addEventListener('keydown', function(e) {
        if (e.key == k) {
            f(e);
        }
    });
}

bindKey("w", (e) => {
    console.log("w");
});
bindKey("s", (e) => {
    console.log("s");
});
bindKey("a", (e) => {
    console.log("a");
});
bindKey("d", (e) => {
    console.log("d");
});

class V3 {
    constructor(x, y) {
        this.x = x;
        this.y = y;
    }
}

let UP = new V3()

class Triangle {
    constructor(p1, p2, p3) {
        this.p1 = p1;
        this.p2 = p2;
        this.p3 = p3;
    }
    draw(c) {
        fillLine(this.p1, this.p2, c);
        fillLine(this.p2, this.p3, c);
        fillLine(this.p3, this.p1, c);
    }
}

class RGBA {
    constructor(r, g, b, a) {
        this.r = r;
        this.g = g;
        this.b = b;
        this.a = a;
    }
}

BLACK = new RGBA(0, 0, 0, 255);
GRAY = new RGBA(192, 192, 192, 255);
WHITE = new RGBA(255, 255, 255, 255);
RED = new RGBA(255, 0, 0, 255);
GREEN = new RGBA(0, 255, 0, 255);
BLUE = new RGBA(0, 0, 255, 255);
CYAN = new RGBA(0, 255, 255, 255);
MAGENTA = new RGBA(255, 0, 255, 255);
YELLOW = new RGBA(255, 255, 0, 255);

function intersection(xy1, xy2) {
    
}

function clear() {
    imageData = c.createImageData(W, H);
}

function fill(xy, rgba) {
    x = Math.round(xy.x);
    y = Math.round(xy.y);
    const i = 4*(x + (H-y)*W);
    imageData.data[i] = rgba.r;
    imageData.data[i+1] = rgba.g;
    imageData.data[i+2] = rgba.b;
    imageData.data[i+3] = rgba.a;
}

function fillRow(x1, x2, y, rgba) {
    for (let x = x1; x <= x2; x++) {
        fill(new V3(x,y), rgba);
    }
}
function fillCol(x, y1, y2, rgba) {
    for (let y = y1; y <= y2; y++) {
        fill(new V3(x,y), rgba);
    }
}

function fillLine(xy1, xy2, rgba) {
    let [x1, y1] = [xy1.x, xy1.y];
    let [x2, y2] = [xy2.x, xy2.y];

    // fill a vertical/horizontal line if given so
    if (x1==x2) fillCol(x1, y1, y2, rgba);
    if (y1==y2) fillRow(x1, x2, y1, rgba);

    if (x1 > x2) [x1, x2] = [x2, x1];
    if (y1 > y2) [y1, y2] = [y2, y1];
    let [xRange, yRange] = [x2-x1, y2-y1];

    if(Math.abs(x2-x1) >= Math.abs(y2-y1)) {
        for (let x = x1; x <= x2; x++) {
            y = y1 + yRange * (x-x1) / xRange;
            fill(new V3(x,y), rgba);
        }
    } else {
        for (let y = y1; y <= y2; y++) {
            x = x1 + xRange * (y-y1) / yRange;
            fill(new V3(x,y), rgba);
        }
    }
}

function show() {
    c.putImageData(imageData, 0, 0);
}

let F = 0;

t1 = new Triangle(new V3(100, 100), new V3(300, 300), new V3(500, 700));

function draw() {
    t1.draw(BLACK);
}

setInterval(() => {
    clear();
    t1.draw(BLACK);
    draw();
    F++;
    show();
}, 1000/FPS);

});

