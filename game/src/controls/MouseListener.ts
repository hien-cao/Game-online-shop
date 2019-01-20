export default class MouseListener {
  public x: number = 0;
  public y: number = 0;

  public mouseDown = false;
  public mouseClick?: number;

  public mount = (gameContainer: HTMLElement) => {
    gameContainer.addEventListener(
      "mousemove",
      this.handleMouseMove,
      false
    );
    gameContainer.addEventListener(
      "mousedown",
      this.handleMouseDown,
      false
    );
    gameContainer.addEventListener(
      "mouseup",
      this.handleMouseUp,
      false
    );
  }

  public unmount = (gameContainer: HTMLElement) => {
    gameContainer.removeEventListener("mousemove", this.handleMouseMove);
    gameContainer.removeEventListener("mousedown", this.handleMouseDown);
    gameContainer.removeEventListener("mouseup", this.handleMouseUp);
  }

  private handleMouseMove = (e: MouseEvent) => {
    this.x = e.offsetX;
    this.y = e.offsetY;
  }

  private handleMouseDown = (e: MouseEvent) => {
    this.mouseDown = true;
    this.mouseClick = this.mouseClick || Date.now();
  }

  private handleMouseUp = (e: MouseEvent) => {
    this.mouseDown = false;
    this.mouseClick = undefined;
  }
}
