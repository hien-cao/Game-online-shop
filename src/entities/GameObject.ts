import { KeyState } from "../controls/keyboardListener";
import Sprite from "../Sprite";

export interface UpdateArgs {
  keyState: KeyState;
}

export default abstract class GameObject {
  public sprite?: Sprite;
  public acceleration: number = .1;
  public position: xy = [0, 0];
  public velocity: vector = [0, 0];

  public dimensions: dimensions = [0, 0];
  public scale: number = 1;

  constructor(sprite: Sprite, scale: number = 1) {
    if (sprite) {
      this.sprite = sprite;

      this.scale = scale;
      this.dimensions[0] = (sprite.img.width as number) * scale;
      this.dimensions[1] = this.dimensions[0] * (sprite.img.height as number) / (sprite.img.width as number);
    }
  }

  public abstract update(args: UpdateArgs): void;

  public render = (ctx: CanvasRenderingContext2D) => {
    if (this.sprite) {
      this.sprite.render(ctx, this.position, this.dimensions);
    }
  }

  public readonly updatePosition = () => {
    this.position[0] += this.velocity[0] * this.acceleration;
    this.position[1] += this.velocity[1] * this.acceleration;
  }
}
