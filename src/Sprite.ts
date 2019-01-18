import ship from "../static/images/ship.svg";

export default class Sprite {
  public img: HTMLImageElement = new Image();

  constructor(img: HTMLImageElement) {
    this.img = img;
  }

  public render = (
    ctx: CanvasRenderingContext2D,
    x: number,
    y: number,
    width = this.img.width,
    height = this.img.height
  ) => {
    ctx.drawImage(this.img, x, y, width, height);
  }
}

const loadSprite = (src: string) => new Promise<Sprite>((resolve, reject) => {
  const img = new Image();
  img.src = src;
  img.onload = () => resolve(new Sprite(img));
});

export const loadSprites = (): Promise<{ [key: string]: Sprite }> => {
  const sprites: { [key: string]: Sprite } = {};
  return Promise.all([
    { name: "ship", src: ship },
  ]
    .map(({ name, src }) => loadSprite(src).then((sprite) => sprites[name] = sprite))
  ).then(() => sprites);
};
