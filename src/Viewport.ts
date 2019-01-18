import GameObject from "./entities/GameObject";

export default class Viewport {
  public width: number;
  public height: number;
  public x: number;
  public y: number;

  constructor(width: number, height: number, x = 0, y = 0) {
    this.x = x;
    this.y = y;
    this.width = width;
    this.width = width;
    this.height = height;
  }

  public resize(width: number, height: number) {
    this.width = width;
    this.height = height;
  }

  public translate(x: number, y: number) {
    this.x = this.x + x;
    this.y = this.y + y;
  }

  public pan = (gameObject: GameObject, offset: xy = [0, 0]) => {
    this.x = gameObject.x + this.width / 2 + offset[0] - gameObject.width / 2;
    this.y = gameObject.y + this.height / 2 + offset[1] - gameObject.height / 2;
  }
}
