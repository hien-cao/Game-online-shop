import MouseListener from "./MouseListener";

export interface ButtonArgs {
  label: string;
  x: number;
  y: number;
  font: string;
  onClick(): any;
}

export class Button {
  public isActive: boolean = false;
  public onClick: () => any;
  public label: string;
  public width: number;
  public height: number;
  public prevClick?: number;
  public canvas: HTMLCanvasElement;
  public font = "12px Arial, Helvetica, sans-serif";

  private _x: number;
  get x() {
    return this._x;
  }
  set x(x: number) {
    this._x = x;
    this.bounds.l = x;
    this.bounds.r = x + this.width;
  }

  private _y: number;
  get y() {
    return this._y;
  }
  set y(y: number) {
    this._y = y;
    this.bounds.t = y;
    this.bounds.b = y + this.height;
  }

  private bounds: Bounds;

  constructor({ label, font, onClick, x, y }: ButtonArgs) {
    this.label = label;
    this._x = x;
    this._y = y;
    this.font = font;
    this.onClick = onClick;

    this.canvas = document.createElement("canvas");
    const ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;

    ctx.font = this.font;
    this.width = ctx.measureText(this.label).width;
    this.height = parseInt(this.font, 10) * 1.3;
    this.canvas.width = this.width;
    this.canvas.height = this.height;
    ctx.font = this.font;
    ctx.fillStyle = "#eee";
    ctx.fillText(this.label, 0, this.canvas.height / 1.3);

    this.bounds = {
      b: this._y + this.height,
      l: this._x,
      r: this._x + this.width,
      t: this._y,
    };

  }

  public update = (mouse: MouseListener) => {
    this.isActive = (
      mouse.x > this.bounds.l && mouse.x < this.bounds.r &&
      mouse.y > this.bounds.t && mouse.y < this.bounds.b
    );
    if (
      this.isActive &&
      mouse.mouseClick && this.prevClick !== mouse.mouseClick &&
      typeof this.onClick === "function"
    ) {
      this.prevClick = mouse.mouseClick;
      this.onClick();
    }
  }

  public render = (ctx: CanvasRenderingContext2D) => {
    ctx.drawImage(this.canvas, this._x, this._y);
  }
}
