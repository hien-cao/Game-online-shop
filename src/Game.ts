import KeyboardListener from "./controls/keyboardListener";
import GameObject from "./entities/GameObject";
import Player from "./entities/Player";
import Weapon from "./entities/Weapon";
import UserInterface from "./interface/UserInterface";
import { sprites } from "./sprites/Sprite";
import Viewport from "./Viewport";
import Zone from "./zones/Zone";
import { getMeteorSpawns } from "./zones/zones";

export default class Game {
  public canvas: HTMLCanvasElement;
  public viewport: Viewport;
  public loopHandle?: number;
  public keyboardListener: KeyboardListener = new KeyboardListener();

  public ui: UserInterface;
  public score: number = 0;

  public pause = false;

  public prevRender: number = 0;
  public prevLoop: number = Date.now();
  public player: Player;

  public gameObjects: GameObject[];

  public zones: Zone[] = [];

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
    this.canvas.width = 500;
    this.canvas.height = 300;
    this.ui = new UserInterface({ width: this.canvas.width, height: this.canvas.height });

    this.player = new Player({
      initialHeight: 20,
      maxLife: 100,
      scale: 1.7,
      sprite: sprites.ship,

      maxVelocity: [15, 15],
      minVelocity: [0, -15],
    });

    this.player.weapon = new Weapon({
      fireRate: 3,
      offset: [46, 8],
      projectileSettings: {
        damage: 2,
        sprite: sprites.projectile,
      },
      ship: this.player,
    });

    this.viewport = new Viewport(
      this.canvas.width,
      this.canvas.height
    );

    this.gameObjects = [
      this.player,
    ];
  }

  public mount = (element: HTMLElement) => {
    // Clear pre-existing items in the element
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.appendChild(this.canvas);
    element.appendChild(this.ui.canvas);

    this.keyboardListener.mount(); // mount keyboard listener

    this.viewport.pan(
      { x: -this.canvas.width / 3, y: this.player.height / 2, velocity: [0, 0] },
      [-this.canvas.width / 2 + this.player.width, 0],
      0,
      true
    );

    // add spawn zones
    this.zones = [
      ...getMeteorSpawns(this),
    ];

    this.loopHandle = window.requestAnimationFrame(this.loop); // loop
  }

  public loop = () => {
    const time = Date.now();
    if (time - this.prevRender > 1000 / 60) {
      this.render();
    }
    this.update((time - this.prevLoop) / 1000);

    this.prevLoop = time;

    this.loopHandle = window.requestAnimationFrame(this.loop);
  }

  public unmount = () => {
    if (this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas); // remove canvas from DOM
    }

    if (this.loopHandle) {
      window.cancelAnimationFrame(this.loopHandle);
    }

    this.keyboardListener.unmount(); // unmount keyboard listener
  }

  public addGameObject = (obj: GameObject) => {
    this.gameObjects.push(obj);
  }

  public render = (
    ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D,
    viewport = this.viewport
  ) => {
    this.prevRender = Date.now();

    ctx.clearRect(0, 0, this.viewport.width, this.viewport.height); // clear canvas before re-render
    for (const obj of this.gameObjects) { // loop and render all game objects
      if (obj && this.viewport.contains(obj)) {
        obj.render(ctx, viewport);
      }
    }

    this.ui.render({
      life: this.player.life,
      maxLife: this.player.maxLife,
      score: this.score,
      velocity: this.player.velocity,
      x: this.player.x,
      y: this.player.y,
    });
  }

  public update = (d: number) => {
    if (this.pause) {
      return;
    }

    for (const zone of this.zones) {
      if (zone.update) {
        zone.update();
      }
    }

    let i = this.gameObjects.length;
    while (i--) {
      if (this.viewport.contains(this.gameObjects[i], { l: 0, t: 200, b: 200, r: 200 })) {
        this.gameObjects[i].update(d, this, i);
      } else {
        this.gameObjects.splice(i, 1); // delete object from game (not in bounds)
      }
    }

    this.viewport.pan(
      this.player,
      [
        -this.canvas.width / 2 - this.player.acceleration[0] * 20 - this.player.width * .5,
        -(this.player.acceleration[1]) * 40 + this.player.height / 2,
      ],
      d
    );
  }
}
