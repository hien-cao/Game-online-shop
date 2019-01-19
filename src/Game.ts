import KeyboardListener from "./controls/keyboardListener";
import GameObject from "./entities/GameObject";
import Meteor from "./entities/Meteor";
import Player from "./entities/Player";
import Weapon from "./entities/Weapon";
import { sprites } from "./sprites/Sprite";
import Viewport from "./Viewport";

export default class Game {
  public canvas: HTMLCanvasElement;
  public viewport: Viewport;
  public renderLoop?: number;
  public updateLoop?: number;
  public keyboardListener: KeyboardListener = new KeyboardListener();
  public scale = 1;

  public prevUpdate: number = 0;
  public player: Player;

  private gameObjects: GameObject[];

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
    this.canvas.width = 500;
    this.canvas.height = 300;

    this.player = new Player({
      initialHeight: 20,
      scale: .15,
      sprite: sprites.ship,
      weapon: new Weapon({
        Projectile: () => new GameObject({ sprite: sprites.projectile }),
        ballisticVelocity: 15,
        fireRate: 2,
        offset: [46, 8],
      }),
    });

    this.viewport = new Viewport(
      this.canvas.width,
      this.canvas.height
    );

    this.gameObjects = [
      this.player,
      new Meteor({
        x: 100,
        y: 0,
      }),
    ];
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

    this.viewport.pan(
      { x: -this.canvas.width / 3, y: this.player.height / 2, velocity: [0, 0] },
      [-this.canvas.width / 2 + this.player.width, 0],
      true
    );
  }

  public unmount = () => {
    if (this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas); // remove canvas from DOM
    }

    window.clearInterval(this.renderLoop); // clear render loop
    window.clearInterval(this.updateLoop); // clear update loop

    this.keyboardListener.unmount(); // unmount keyboard listener
  }

  public addGameObject = (obj: GameObject) => {
    this.gameObjects.push(obj);
  }

  public render = (
    ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D,
    viewport = this.viewport
  ) => () => {
    ctx.clearRect(0, 0, this.viewport.width, this.viewport.height); // clear canvas before re-render

    for (const obj of this.gameObjects) { // loop and render all game objects
      if (obj) {
        obj.render(ctx, viewport);
      }
    }
  }

  public update = () => {
    this.viewport.pan(
      this.player,
      [
        -this.canvas.width / 2 + this.player.width - this.player.acceleration[0] * 200 - this.player.width * 1.5,
        -this.player.acceleration[1] * 400 + this.player.height / 2,
      ]
    );

    let i = this.gameObjects.length;
    while (i--) {
      if (!this.viewport.contains(this.gameObjects[i]) || this.gameObjects[i].update(this) === false) {
        this.gameObjects.splice(i, 1);
      }
    }

    this.prevUpdate = Date.now();
  }
}
