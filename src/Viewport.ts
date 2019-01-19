import GameObject from "./entities/GameObject";

export default class Viewport {
  public width: number;
  public height: number;
  public x: number;
  public y: number;
  public target?: Trackable;
  public targetOffset = [0, 0];

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

  public pan = (obj: Trackable, offset = [0, 0], instant = false) => {
    if (instant) {
      this.x = obj.x + this.width / 2 + offset[0];
      this.y = obj.y - this.height / 2 + offset[1];
    } else {
      this.target = obj;
      this.targetOffset = offset;
    }
    this.update();
  }

  public update = () => {
    if (typeof this.target === "undefined") {
      return;
    }
    const { x, y, velocity } = this.target;
    const targetX = x + this.width / 2 + this.targetOffset[0] - velocity[0];
    const targetY = y - this.height / 2 + this.targetOffset[1] - velocity[1];

    if (targetX !== this.x) {
      this.x += Math.sign(targetX - this.x) * Math.log10(Math.pow(targetX - this.x, 2)) + velocity[0];
    }
    if (targetY !== this.y) {
      this.y += Math.sign(targetY - this.y) * Math.log10(Math.pow(targetY - this.y, 2)) + velocity[1];
    }
  }

  public contains = (obj: GameObject, { l, r, t, b }: Bounds = { l: 0, r: 0, t: 0, b: 0 }) => (
    obj.x + obj.width > this.x - r && obj.x < this.x + this.width + l &&
    obj.y + obj.height > this.y - t && obj.y < this.y + this.height + b
  )
}
