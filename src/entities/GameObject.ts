import Game from "../Game";
import Sprite from "../sprites/Sprite";
import Viewport from "../ViewPort";

export interface GameObjectArgs {
  sprite: Sprite;
  scale?: number;
  initialWidth?: number;
  initialHeight?: number;
  onUpdate?: Array<(game: Game) => any>;
}

export default class GameObject {
  public sprite: Sprite;
  public x: number = 0;
  public y: number = 0;
  public acceleration: vector = [0, 0];
  public velocity: vector = [0, 0];

  public onUpdate?: Array<(game: Game) => any>;

  public width: number = 0;
  public height: number = 0;

  // Life determines damage caused upon collosion
  // An object will trigger
  public life: number = 0;

  constructor({
    sprite,
    initialWidth = 1,
    initialHeight = 1,
    scale = 1,
  }: GameObjectArgs) {
    this.sprite = sprite;

    this.width = initialWidth;
    this.height = initialHeight;

    this.sprite.img.onload = () => this.scale(scale); // to update dimensions after image has been loaded
    this.scale(scale);
  }

  public scale = (scale: number) => {
    const width = (this.sprite.img.width as number) * scale;
    const height = width * (this.sprite.img.height as number) / (this.sprite.img.width as number);

    if (!isNaN(width) && !isNaN(height)) {
      this.width = width;
      this.height = height;
    }
  }

  public update = (game: Game) => {
    this.updatePosition();

    // loop and invoke all update listeners
    if (Array.isArray(this.onUpdate)) {
      for (const notify of this.onUpdate) {
        notify(game);
      }
    }
  }

  public render = (ctx: CanvasRenderingContext2D, viewport: Viewport, scale = 1) => {
    this.sprite.render(
      ctx,
      this.x - viewport.x,
      this.y - viewport.y,
      this.width,
      this.height
    );
  }

  private readonly updatePosition = () => {
    this.x += this.velocity[0];
    this.y += this.velocity[1];

    this.velocity = [
      this.velocity[0] + this.acceleration[0],
      this.velocity[1] + this.acceleration[1],
    ];
  }
}
