import KeyboardListener from "./controls/keyboardListener";
import MouseListener from "./controls/MouseListener";
import GameObject, { GameObjectState } from "./entities/GameObject";
import Meteor from "./entities/Meteor";
import Player from "./entities/Player";
import Projectile from "./entities/Projectile";
import Weapon from "./entities/Weapon";
import End from "./interface/End";
import Overlay from "./interface/Overlay";
import Pause from "./interface/Pause";
import UserInterface from "./interface/UserInterface";
import { sprites } from "./sprites/Sprite";
import Viewport from "./Viewport";
import Zone from "./zones/Zone";
import { getMeteorSpawns } from "./zones/zones";

export interface GameState {
  score: number;
  gameObjects: GameObjectState[];
}

export default class Game {

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
  public player?: Player;

  public gameObjects: GameObject[] = [];

  public zones: Zone[] = [];

  private _pause = false;

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
    this.canvas.width = 500;
    this.canvas.height = 300;

    parent.postMessage({
      messageType: "SETTING",
      options: {
        height: this.canvas.height,
        width: this.canvas.width,
      },
    }, window.location.href);

    this.overlays = {
      end: new End({
        game: this,
      }),
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
    this.score = 0;
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

    this.pause = true;
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

  // Send load request to the parent window as described in the project description
  public requestLoad = () => {
    parent.postMessage({
      messageType: "LOAD_REQUEST",
    }, window.location.href);
  }

  public load: EventListener = ({ data }: { [key: string]: any }) => {
    if (typeof data === "object") {
      if ("messageType" in data && data.messageType === "LOAD") {
        if ("gameState" in data) {
          this.gameState = data.gameState;
        }
      } else if (data.messageType === "error") {
        alert(data.info || "Error loading game state");
      }
    }
  }

  // Send save request to the parent window as described in the project description
  public save = () => {
    parent.postMessage({
      messageType: "SAVE",

      gameState: this.gameState,
    }, window.location.href);
  }

  set gameState(state: GameState) {
    this.reset();
    this.score = state.score;

    // populate gameObjects
    state.gameObjects.map((obj) => {
      if (obj.type === Player.prototype.constructor.name) {
        (this.player as Player).state = obj;
      } else if (obj.type === Projectile.prototype.constructor.name) {
        this.gameObjects.push(new Projectile(obj));
      } else {
        this.gameObjects.push(new Meteor(obj));
      }
    });
  }

  get gameState(): GameState {
    return {
      gameObjects: this.gameObjects.map((obj) => obj.state),
      score: this.score,
    };
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
      const state = {
        score: this.score,
      };
      if (this.player) {
        Object.assign(state, {
          life: this.player.life,
          maxLife: this.player.maxLife,
          velocity: this.player.velocity,
          x: this.player.x,
          y: this.player.y,
        });
      }
      this.activeOverlay.render(state);
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

    if (this.player) {
      this.viewport.pan(
        this.player,
        [
          -this.canvas.width / 2 - this.player.acceleration[0] * 20 - this.player.width * .5,
          -(this.player.acceleration[1]) * 40 + this.player.height / 2,
        ],
        d
      );
    }

    let i = this.gameObjects.length;
    while (i--) {
      if (this.viewport.contains(this.gameObjects[i], { l: 0, t: 200, b: 200, r: 200 })) {
        this.gameObjects[i].update(d, this, i);
      } else {
        this.gameObjects.splice(i, 1); // delete object from game (not in bounds)
      }
    }
  }

  public setOverlay = (overlay: Overlay) => {
    this.clearOverlay();
    this.activeOverlay = overlay;
    if (this.canvas.parentNode) {
      this.canvas.parentNode.appendChild(this.activeOverlay.canvas);
    }
  }

  private clearOverlay = () => {
    if (this.canvas.parentNode) {
      const overlay = document.getElementById("overlay");
      if (overlay) {
        this.canvas.parentNode.removeChild(overlay); // remove overlay canvas
      }
    }
  }
}
