export default class Sprite {
  public sprite: CanvasImageSource;
  public width: number;
  public height: number;
  public readonly scale: number = 1;

  constructor(sprite: CanvasImageSource, scale = 1) {
    this.sprite = sprite;
    this.scale = scale;
    this.width = (sprite.width as number) * scale;
    this.height = this.width * (sprite.height as number) / (sprite.width as number);
  }

  public render = (ctx: CanvasRenderingContext2D, position: xy) => {
    ctx.drawImage(this.sprite, position[0], position[1], this.width, this.height);
  }
}
