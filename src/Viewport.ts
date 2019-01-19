import GameObject from "./entities/GameObject";

export default class Viewport {
  public width: number;
  public height: number;
  public x: number;
  public y: number;
  public target?: GameObject;
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

  public pan = (obj: GameObject, offset = [0, 0], instant = false) => {
    if (instant) {
      this.x = obj.x + this.width / 2 + offset[0] - obj.width * 1.5;
      this.y = obj.y - this.height / 2 + offset[1] + obj.height / 2;
    } else {
      this.target = obj;
      this.targetOffset = offset;
    }
  }

  public update = () => {
    if (typeof this.target === "undefined") {
      return;
    }
    const targetX = this.target.x + this.width / 2 +
      this.targetOffset[0] - this.target.width * 1.5 - this.target.velocity[0];
    const targetY = this.target.y - this.height / 2 +
      this.targetOffset[1] + this.target.height / 2 - this.target.velocity[1];

    if (targetX !== this.x) {
      this.x += Math.sign(targetX - this.x) * Math.log10(Math.pow(targetX - this.x, 2)) * .6 + this.target.velocity[0];
    }
    if (targetY !== this.y) {
      this.y += Math.sign(targetY - this.y) * Math.log10(Math.pow(targetY - this.y, 2)) * .6 + this.target.velocity[1];
    }
  }

  public contains = (obj: GameObject, { l, r, t, b }: Bounds = { l: 0, r: 0, t: 0, b: 0 }) => (
    obj.x > this.x - l && obj.x < this.x + this.width + r &&
    obj.y > this.y - t && obj.y < this.y + this.height + b
  )
}
