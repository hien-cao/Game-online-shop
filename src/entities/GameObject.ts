import { KeyState } from "../controls/keyboardListener";
import Sprite from "../Sprite";
import Viewport from "../ViewPort";

export interface UpdateArgs {
  keyState: KeyState;
}

export default abstract class GameObject {
  public sprite: Sprite;
  public acceleration: number = .1;
  public x: number = 0;
  public y: number = 0;
  public velocity: vector = [0, 0];

  public width: number;
  public height: number;
  public scale: number = 1;

  constructor(sprite: Sprite, scale: number = 1) {
    this.sprite = sprite;

    this.scale = scale;
    this.width = (sprite.img.width as number) * scale;
    this.height = this.width * (sprite.img.height as number) / (sprite.img.width as number);
  }

  public abstract update(args: UpdateArgs): void;

  public render = (ctx: CanvasRenderingContext2D, viewport: Viewport) => {
    this.sprite.render(
      ctx,
      viewport.x - this.x,
      viewport.y - this.y,
      this.width,
      this.height
    );
  }

  public readonly updatePosition = () => {
    this.x += this.velocity[0] * this.acceleration;
    this.y += this.velocity[1] * this.acceleration;
  }
}
