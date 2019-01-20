import KeyboardListener from "./controls/keyboardListener";
import MouseListener from "./controls/MouseListener";
import GameObject from "./entities/GameObject";
import Player from "./entities/Player";
import Weapon from "./entities/Weapon";
import Overlay from "./interface/Overlay";
import Pause from "./interface/Pause";
import UserInterface from "./interface/UserInterface";
import { sprites } from "./sprites/Sprite";
import Viewport from "./Viewport";
import Zone from "./zones/Zone";
import { getMeteorSpawns } from "./zones/zones";

export default class Game {
  public readonly fps: number = 60;

  public canvas: HTMLCanvasElement;
  public viewport: Viewport;
  public loopHandle?: number;
  public keyboard: KeyboardListener = new KeyboardListener();
  public mouse: MouseListener = new MouseListener();

  public activeOverlay?: Overlay;
  public overlays: { [key: string]: Overlay };

  public score: number = 0;

  public prevRender: number = 0;
  public prevLoop: number = Date.now();
  public player: Player;

  public gameObjects: GameObject[] = [];

  public zones: Zone[] = [];

  private _pause = false;

  set pause(pause: boolean) {
    this._pause = pause;
    if (pause) {
      this.setOverlay(this.overlays.pause);
      return;
    }
    this.setOverlay(this.overlays.ui);
  }

  get pause() {
    return this._pause;
  }

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
    this.canvas.width = 500;
    this.canvas.height = 300;
    this.overlays = {
      pause: new Pause({
        game: this,
        onExit: () => this.pause = false,
      }),
      ui: new UserInterface({
        height: this.canvas.height,
        pause: () => this.pause = true,
        width: this.canvas.width,
      }),
    };

    this.viewport = new Viewport(
      this.canvas.width,
      this.canvas.height
    );
  }

  public mount = (element: HTMLElement) => {
    // Clear pre-existing items in the element
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.appendChild(this.canvas);

    this.reset();

    this.pause = true;
    this.loopHandle = window.requestAnimationFrame(this.loop); // loop

    // input
    this.keyboard.mount(); // mount keyboard listener
    this.mouse.mount(this.canvas.parentNode as HTMLElement); // mount mouse listener
  }

  public unmount = () => {
    this.gameObjects.length = 0;
    if (this.canvas.parentNode) {
      // input
      this.keyboard.unmount(); // unmount keyboard listener
      this.mouse.unmount(this.canvas.parentNode as HTMLElement); // unmount keyboard listener

      while (this.canvas.parentNode.firstChild) {
        this.canvas.parentNode.removeChild(this.canvas.parentNode.firstChild);
      }
    }

    if (this.loopHandle) {
      window.cancelAnimationFrame(this.loopHandle);
    }
  }

  public reset = () => {
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

    this.viewport.pan(
      { x: -this.canvas.width / 3, y: this.player.height / 2, velocity: [0, 0] },
      [-this.canvas.width / 2 + this.player.width, 0],
      0,
      true
    );

    // add initial game objects
    this.gameObjects = [
      this.player,
    ];
    // add initial spawn zones
    this.zones = [
      ...getMeteorSpawns(this),
    ];
  }

  public addGameObject = (obj: GameObject) => {
    this.gameObjects.push(obj);
  }

  public loop = () => {
    const time = Date.now();
    if (time - this.prevRender > 1000 / this.fps) {
      this.render();
    }
    this.update((time - this.prevLoop) / 1000);

    this.prevLoop = time;

    this.loopHandle = window.requestAnimationFrame(this.loop);
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

    if (this.activeOverlay) {
      this.activeOverlay.render({
        life: this.player.life,
        maxLife: this.player.maxLife,
        score: this.score,
        velocity: this.player.velocity,
        x: this.player.x,
        y: this.player.y,
      });
    }
  }

  public update = (d: number) => {
    if (this.activeOverlay && this.activeOverlay.update) {
      this.activeOverlay.update({ mouse: this.mouse, keyboard: this.keyboard });
    }

    if (this._pause) { // Don't update the game if it has been paused
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

  private clearOverlay = () => {
    if (this.canvas.parentNode) {
      const overlay = document.getElementById("overlay");
      if (overlay) {
        this.canvas.parentNode.removeChild(overlay); // remove overlay canvas
      }
    }
  }

  private setOverlay = (overlay: Overlay) => {
    this.clearOverlay();
    this.activeOverlay = overlay;
    if (this.canvas.parentNode) {
      this.canvas.parentNode.appendChild(this.activeOverlay.canvas);
    }
  }
}
