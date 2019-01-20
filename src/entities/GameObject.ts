import Game from "../Game";
import Sprite from "../sprites/Sprite";
import Viewport from "../ViewPort";

export const globalSpeedModifier = 20;

export interface GameObjectArgs {
  sprite?: Sprite;
  scale?: number;
  initialWidth?: number;
  initialHeight?: number;
  x?: number;
  y?: number;
  velocity?: vector;
  maxVelocity?: vector;
  minVelocity?: vector;
  maxLife: number;
  onUpdate?: Array<(d: number, game: Game) => any>;
}

export interface GameObjectState {
  type: string;
  x: number;
  y: number;
  velocity: vector;
  maxLife: number;
  life: number;
}

export default abstract class GameObject {
  get sprite() {
    return this._sprite;
  }
  set sprite(sprite: Sprite | undefined) {
    this._sprite = sprite;
    this.rescale(this.scale);
  }

  public scale: number;
  public x: number;
  public y: number;
  public acceleration: vector = [0, 0];
  public velocity: vector = [0, 0];
  public maxVelocity?: vector;
  public minVelocity?: vector;
  public immuneTo?: GameObject[];

  public onUpdate?: Array<(d: number, game: Game) => any>;

  public width: number = 0;
  public height: number = 0;

  // Life determines damage caused upon collosion
  // An object will trigger
  public life: number;
  public maxLife: number;

  private _sprite?: Sprite;

  constructor({
    sprite,
    initialWidth = 1,
    initialHeight = 1,
    scale = 1,
    x = 0,
    y = 0,
    maxLife = 1,
    velocity = [0, 0],
    maxVelocity,
    minVelocity,
  }: GameObjectArgs) {
    this.sprite = sprite;

    this.width = initialWidth;
    this.height = initialHeight;

    this.x = x;
    this.y = y;

    this.maxLife = Math.floor(maxLife);
    this.life = this.maxLife;

    this.velocity = velocity;
    this.maxVelocity = maxVelocity;
    this.minVelocity = minVelocity;

    this.scale = scale;

    if (this._sprite) {
      this._sprite.img.onload = () => this.rescale(scale); // to update dimensions after image has been loaded
      this.rescale(scale);
    }
  }

  public rescale = (scale: number) => {
    if (typeof this.sprite === "undefined") {
      return;
    }
    const width = (this.sprite.img.width as number) * scale;
    const height = width * (this.sprite.img.height as number) / (this.sprite.img.width as number);

    if (!isNaN(width) && !isNaN(height)) {
      this.width = width;
      this.height = height;
    }
  }

  public getDistance = (obj: Trackable) => Math.sqrt(
    Math.pow(this.x - obj.x, 2) + Math.pow(this.y - obj.y, 2)
  )

  public collides = (obj: GameObject) => (
    obj.x + obj.width > this.x && obj.x < this.x + this.width &&
    obj.y + obj.height > this.y && obj.y < this.y + this.height
  )

  public update = (d: number, game: Game, objIndex: number) => {
    this.updatePosition(d);

    // loop and invoke all update listeners
    if (Array.isArray(this.onUpdate)) {
      for (const notify of this.onUpdate) {
        notify(d, game);
      }
    }

    if (this.life <= 0) {
      this.life = 0;
      return this.destroy(game, objIndex);
    }
    // check for collisions
    const collision = this.checkCollisions(game, objIndex);
    if (collision) {
      const damage = collision.life;
      collision.life -= this.life;
      this.life -= damage;

      if (collision.life <= 0 && this.source === game.player) { // increment score on succesful kill
        game.score += collision.maxLife * 1.2;
      }
    }
  }

  public render = (ctx: CanvasRenderingContext2D, viewport: Viewport, scale = 1) =>
    this.sprite && this.sprite.render(
      ctx,
      this.x - viewport.x,
      this.y - viewport.y,
      this.width,
      this.height
    )

  get state(): GameObjectState {
    return {
      life: this.life,
      maxLife: this.maxLife,
      type: this.constructor.name,
      velocity: this.velocity,
      x: this.x,
      y: this.y,
    };
  }

  set state(state: GameObjectState) {
    Object.assign(this, state);
  }

  protected destroy = (game: Game, objIndex: number) => {
    const obj = game.gameObjects[objIndex];
    this.velocity = [0, 0];
    if (typeof obj.onDestroy === "function") {
      obj.onDestroy(game);
    }
    game.gameObjects.splice(objIndex, 1);
  }

  protected onDestroy?(game: Game): any;

  private checkCollisions = (game: Game, objIndex: number): GameObject | null => {
    // loop through non-checked game objects
    while (objIndex--) {
      if (
        !(Array.isArray(this.immuneTo) && this.immuneTo.find((obj) => obj === game.gameObjects[objIndex])) &&
        this.collides(game.gameObjects[objIndex])
      ) {
        return game.gameObjects[objIndex];
      }
    }
    return null;
  }

  private readonly updatePosition = (d: number) => {
    this.x += this.velocity[0] * d * globalSpeedModifier;
    this.y += this.velocity[1] * d * globalSpeedModifier;

    this.velocity[0] += this.acceleration[0] * d * globalSpeedModifier;
    this.velocity[1] += this.acceleration[1] * d * globalSpeedModifier;

    if (this.minVelocity) {
      this.velocity[0] = Math.max(this.minVelocity[0], this.velocity[0]);
      this.velocity[1] = Math.max(this.minVelocity[1], this.velocity[1]);
    }
    if (this.maxVelocity) {
      this.velocity[0] = Math.min(this.maxVelocity[0], this.velocity[0]);
      this.velocity[1] = Math.min(this.maxVelocity[1], this.velocity[1]);
    }
  }
}
