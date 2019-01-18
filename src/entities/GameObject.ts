import Sprite from "../Sprite";

export default abstract class GameObject {
  public sprite: Sprite;
  public position: xy = [0, 0];

  constructor(sprite: Sprite) {
    this.sprite = sprite;
  }

  public render = (ctx: CanvasRenderingContext2D) => {
    this.sprite.render(ctx, this.position);
  }

  public update = (): any => {
    return false;
  }
}
