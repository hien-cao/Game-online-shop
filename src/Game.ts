export default class Game {
  public canvas: HTMLCanvasElement;
  public renderLoop?: number;
  public updateLoop?: number;

  constructor() {
    this.canvas = document.createElement("canvas");
    this.canvas.id = "game";
  }

  public mount = (element: HTMLElement) => {
    // Clear pre-existing items in the element
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }

    element.appendChild(this.canvas);

    window.setInterval(this.render, 1000 / 60); // render loop
    window.setInterval(this.update, 30); // update loop
  }

  public unmount = () => {
    if (this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas); // remove canvas from DOM
    }

    window.clearInterval(this.renderLoop); // clear render loop
    window.clearInterval(this.updateLoop); // clear update loop
  }

  public render = () => {

  }

  public update = () => {

  }
}
