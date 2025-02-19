const PADDING = 50;
const ROWS = 90;
const COLUMNS = 100;
const CELL_SIZE = 6;
const CELL_GAP = 0;
const DEAD_CELL_COLOR = '#222'; 
const CANVAS_COLOR = '#e6a26e';

let run_button;
let run = false;
let left_mouse_down = false;
let right_mouse_down = false;

const ALIVE_CELL_COLOR = "#FFD613"

class Cell{
    constructor(row, col, alive, colour){
        this.row = row;
        this.col = col;
        this.colour = colour;
        this.alive = alive;
    }
}

let cells = []

function setup() {
  let canvas = createCanvas(CELL_SIZE*COLUMNS, CELL_SIZE*ROWS);
  canvas.parent('canvas-container'); // attach the canvas to the div
  noStroke();

  run_button = createButton("Pause/Play Conway's Game of Life")
  run_button.size(250, 30)
  run_button.position(10, 10);
  run_button.mousePressed(() => run = !run);

  picker = createColorPicker(ALIVE_CELL_COLOR);
  picker.position(300, 10);

  fill(DEAD_CELL_COLOR);

  // Making all the cells
  for (let col=0; col < COLUMNS; col++) {
    for (let row=0; row < ROWS; row++) {

      cells.push(new Cell(row, col, false, DEAD_CELL_COLOR));
      
      let left = PADDING + col*(CELL_SIZE + CELL_GAP);
      let top = PADDING + row*(CELL_SIZE + CELL_GAP);
      let size = CELL_SIZE;
      rect(left,top,size,size);
    }
  }
}

function draw() {
  if (run) {
    next_life();
  }

  // Setting cell with left click and erasing with right click
  if (left_mouse_down) {
    setCell(mouseX, mouseY, true);
  }
  else if (right_mouse_down) {
    setCell(mouseX, mouseY, false);
  }
}

// Convert hex code to rgb
function hexToRgb(hex) {
  hex = hex.replace('#', '');
  const r = parseInt(hex.substring(0, 2), 16);
  const g = parseInt(hex.substring(2, 4), 16);
  const b = parseInt(hex.substring(4, 6), 16);
  return [r?r:0, g?g:0, b?b:0];
}

// Perform a single iteration of conways game of life
function next_life() {
  const all_cell_neighbours = cells.map((cell) => [cell, getNeighbours(cell).filter((n) => n.alive)]);
  const to_turn_off = [];
  const to_turn_on = []
  for (const cell_neighbours of all_cell_neighbours) {
    const cell = cell_neighbours[0];
    const alive_neighbours = cell_neighbours[1];
    if (alive_neighbours.length < 2 || alive_neighbours.length > 3) {
      to_turn_off.push(cell);
    }
    else if (alive_neighbours.length == 3) {
      // When converting a dead cell to an alive cell, mix the colours of its surrounding cells
      to_turn_on.push([cell, getAverageColor(alive_neighbours)]);
    }
  }

  to_turn_off.map((cell) => turnOffCell(cell));
  to_turn_on.map((cell_colour) => turnOnCell(cell_colour[0], cell_colour[1]));
}

function getAverageColor(cells) {
  let reds = 0;
  let greens = 0;
  let blues = 0;
  const length = cells.length;
  for (const cell of cells) {
    const rgb = hexToRgb(cell.colour);
    reds += rgb[0];
    greens += rgb[1];
    blues += rgb[2];
  }

  const r = Math.floor(reds/length), g = Math.floor(greens/length), b = Math.floor(blues/length)
  return "#" + hex(r, 2) + hex(g, 2) + hex(b, 2);
}

// Get neighbours (can wrap around to the other side of the cell grid for edge or corner cells)
function getNeighbours(cell) {
  let neighbours = []
  let offsets = [[1, 0], [1, 1], [0, 1], [-1, 0], [-1, -1], [0, -1], [-1, 1], [1, -1]]
  for (const offset of offsets) {
    var row = (cell.row + offset[0]) % ROWS;
    if (row < 0){
      row += ROWS;
    }
    var col = (cell.col + offset[1]) % COLUMNS;
    if (col < 0){
      col += COLUMNS;
    }
    n = getCell(row, col);
    if (n != undefined && n != null) {
      neighbours.push(n);
    }
  }
  return neighbours;
}

function getCell(row, col) {
  if (col < COLUMNS && row < ROWS && col >= 0 && row >= 0) {
    return cells[col * ROWS + row];
  }
  else {
    return undefined;
  }
}

function setCell(pixelX, pixelY, alive) {
  pixelX = pixelX - PADDING;
  pixelY = pixelY - PADDING;
  
  let col = Math.floor(pixelX / (CELL_SIZE + CELL_GAP));
  let row = Math.floor(pixelY / (CELL_SIZE + CELL_GAP)); 
  let cell = getCell(row, col);
  if (cell != undefined && cell != null) {
    if (alive)
      turnOnCell(cell, picker.value().toString())
    else 
      turnOffCell(cell);
  }
}

function turnOnCell(cell, colour) {
  fill(colour);
  let left = PADDING + cell.col*(CELL_SIZE + CELL_GAP);
  let top = PADDING + cell.row*(CELL_SIZE + CELL_GAP);
  let size = CELL_SIZE;

  rect(left,top,size,size);
  cell.alive = true;
  cell.colour = colour;
}

function turnOffCell(cell) {
  fill(DEAD_CELL_COLOR);
  let left = PADDING + cell.col*(CELL_SIZE + CELL_GAP);
  let top = PADDING + cell.row*(CELL_SIZE + CELL_GAP);
  let size = CELL_SIZE;

  rect(left,top,size,size);
  cell.alive = false;
  cell.colour = DEAD_CELL_COLOR;
}

function mousePressed() {
  if (mouseButton == LEFT) {
    left_mouse_down = true;
  }
  if (mouseButton == RIGHT) {
    right_mouse_down = true;
  }
}

function mouseReleased() {
  if (mouseButton == LEFT) {
    left_mouse_down = false;
  }
  else if (mouseButton == RIGHT) {
    right_mouse_down = false;
  }
}
