document.addEventListener("DOMContentLoaded", function(){

const canvas = document.getElementById("canvas");
const c = canvas.getContext('2d');
const W = canvas.width;
const H = canvas.height;
console.log(W, H);
let imageData = c.createImageData(W, H);

class XY {
    constructor(x, y) {
        this.x = x;
        this.y = y;
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

function swap(x, y) {
    return [y, x];
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
        fill(XY(x,y), rgba);
    }
}
function fillCol(x, y1, y2, rgba) {
    for (let y = y1; y <= y2; y++) {
        fill(XY(x,y), rgba);
    }
}

function fillLine(xy1, xy2, rgba) {
    let [x1, y1] = [xy1.x, xy1.y];
    let [x2, y2] = [xy2.x, xy2.y];

    // fill a vertical/horizontal line if given so
    if (x1==x2) fillCol(x1, y1, y2, rgba);
    if (y1==y2) fillRow(x1, x2, y1, rgba);

    if (x1 > x2) [x1, x2] = swap(x1, x2);
    if (y1 > y2) [y1, y2] = swap(y1, y2);
    let [xRange, yRange] = [x2-x1, y2-y1];

    if(Math.abs(x2-x1) >= Math.abs(y2-y1)) {
        for (let x = x1; x <= x2; x++) {
            y = y1 + yRange * (x-x1) / xRange;
            fill(new XY(x,y), rgba);
        }
    } else {
        for (let y = y1; y <= y2; y++) {
            x = x1 + xRange * (y-y1) / yRange;
            fill(new XY(x,y), rgba);
        }
    }
}

function show() {
    c.putImageData(imageData, 0, 0);
}

let F = 0;

function draw() {
    fillLine(new XY(100, 100), new XY(200, 700), BLACK);
    fillLine(new XY(520, 320), new XY(920, 270), BLACK);
    fillLine(new XY(520, 540), new XY(430, 310), BLACK);
}

setInterval(() => {
    clear();
    draw();
    F++;
    show();
}, 1000/10);

});

