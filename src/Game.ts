import GameObject from "./entities/GameObject";

import KeyboardListener from "./controls/keyboardListener";
import Player from "./entities/Player";
import Sprite from "./Sprite";
import Viewport from "./Viewport";

export default class Game {
  public canvas: HTMLCanvasElement;
  public viewport: Viewport;
  public renderLoop?: number;
  public updateLoop?: number;
  public keyboardListener: KeyboardListener = new KeyboardListener();

  public gameObjects: GameObject[];
  public player: Player;

  constructor(sprites: { [key: string]: Sprite }) {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";

    this.player = new Player(sprites.ship, .15);

    this.viewport = new Viewport(
      this.canvas.width,
      this.canvas.height
    );

    this.gameObjects = [];

  }

  public mount = (element: HTMLElement) => {
    // Clear pre-existing items in the element
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.appendChild(this.canvas);

    this.renderLoop = window.setInterval(this.render(), 1000 / 60); // render loop
    this.updateLoop = window.setInterval(this.update, 30); // update loop

    this.keyboardListener.mount(); // mount keyboard listener

  }

  public unmount = () => {
    if (this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas); // remove canvas from DOM
    }

    window.clearInterval(this.renderLoop); // clear render loop
    window.clearInterval(this.updateLoop); // clear update loop

    this.keyboardListener.unmount(); // unmount keyboard listener
  }

  public render = (
    ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D,
    viewport = this.viewport
  ) => () => {
    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height); // clear canvas before re-render

    this.player.render(ctx, viewport);

    for (const obj of this.gameObjects) { // loop and render all game objects
      obj.render(ctx, viewport);
    }
  }

  public update = () => {
    const ctx = { keyState: this.keyboardListener.keyState };

    this.player.update(ctx);
    this.viewport.pan(
      this.player,
      [-this.canvas.width / 2 + this.player.width, 0]
    );

    for (const obj of this.gameObjects) { // loop and update all game objects
      obj.update(ctx);
    }
  }
}
