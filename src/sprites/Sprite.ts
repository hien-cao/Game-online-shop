import ship from "../../static/images/ship.svg";
import projectile from "./projectile";

type ImageSource = HTMLImageElement | HTMLCanvasElement;

export default class Sprite {
  public img: ImageSource = new Image();

  constructor(img: ImageSource | string) {
    if (typeof img === "string") {
      this.img = new Image();
      this.img.src = img;
    } else {
      this.img = img;
    }
  }

  public render = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width = this.img.width,
    height = this.img.height
  ) => {
    ctx.drawImage(this.img, ~~x, ~~y, width, height);
  }
}

export const sprites: { [key: string]: Sprite } = {
  projectile: new Sprite(projectile),
  ship: new Sprite(ship),
};
