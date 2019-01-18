import GameObject from "./entities/GameObject";

import Ship from "./entities/Ship";

export default class Game {
  public canvas: HTMLCanvasElement;
  public renderLoop?: number;
  public updateLoop?: number;

  public gameObjects: GameObject[] = [new Ship()];

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
  }

  public mount = (element: HTMLElement) => {
    // Clear pre-existing items in the element
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.appendChild(this.canvas);

    this.renderLoop = window.setInterval(this.render(), 1000 / 60); // render loop
    this.updateLoop = window.setInterval(this.update, 30); // update loop
  }

  public unmount = () => {
    if (this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas); // remove canvas from DOM
    }

    window.clearInterval(this.renderLoop); // clear render loop
    window.clearInterval(this.updateLoop); // clear update loop
  }

  public render = (ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D) => () => {
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); // clear canvas before re-render

    for (const obj of this.gameObjects) {
      obj.render(ctx);
    }
  }

  public update = () => {
    for (const obj of this.gameObjects) {
      obj.update();
    }
  }
}
