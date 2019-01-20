import Overlay from "./Overlay";

export default class Pause extends Overlay {
  public render = () => {
    const ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;
    ctx.restore();
    ctx.font = "12 Arial, Helvetica, sans-serif";
    ctx.fillStyle = "rgba(0, 0, 0, .2)";

    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    ctx.save();
  }

  public update = () => {

  }
}
