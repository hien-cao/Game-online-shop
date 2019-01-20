export interface OverlayArgs {
  width: number;
  height: number;
}

export default abstract class Overlay {
  public canvas: HTMLCanvasElement;
  public prevState: any = {};

  constructor({ width, height }: OverlayArgs) {
    this.canvas = document.createElement("canvas");
    this.canvas.width = width;
    this.canvas.height = height;
  }

  public abstract render(state: any): any;
}
