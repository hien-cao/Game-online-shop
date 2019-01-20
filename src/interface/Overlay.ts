import KeyboardListener from "../controls/keyboardListener";
import MouseListener from "../controls/MouseListener";

export interface OverlayArgs {
  width: number;
  height: number;
  onExit?(): any;
}

export interface OverlayUpdateState {
  mouse: MouseListener;
  keyboard: KeyboardListener;
}

export default abstract class Overlay {
  public rendered = false;
  public onExit?: () => any;
  public canvas: HTMLCanvasElement;
  public prevState: any = {};

  constructor({ width, height, onExit }: OverlayArgs) {
    this.canvas = document.createElement("canvas");
    this.canvas.width = width;
    this.canvas.height = height;
    this.onExit = onExit;
    this.canvas.id = "overlay";
  }

  public exit = () => typeof this.onExit === "function" && this.onExit();

  public abstract render(state?: any): any;
  public abstract update?(state: OverlayUpdateState): any;
}
