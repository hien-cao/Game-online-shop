export interface KeyState {
  [key: string]: boolean;
}

export default class KeyboardListener {
  public keyState: KeyState = {}; // initialize empty keystate helper

  public mount = () => {
    document.addEventListener(
      "keydown",
      this.onKeyDownHandler,
      false
    );
    document.addEventListener(
      "keyup",
      this.onKeyUpHandler,
      false
    );
  }

  public unmount = () => {
    document.removeEventListener("keydown", this.onKeyDownHandler);
    document.removeEventListener("keyup", this.onKeyUpHandler);
  }

  private onKeyDownHandler = (e: KeyboardEvent) => {
    this.keyState[e.key] = true;
  }

  private onKeyUpHandler = (e: KeyboardEvent) => {
    this.keyState[e.key] = false;
  }
}
