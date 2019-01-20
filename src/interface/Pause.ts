import { Button } from "../controls/Button";
import Game from "../Game";
import Overlay, { OverlayUpdateState } from "./Overlay";

export interface PauseArgs {
  game: Game;
  onExit(): any;
}

export default class Pause extends Overlay {
  public prevState: {
    buttons: Button[]
  };

  constructor({ game, ...args }: PauseArgs) {
    super({
      ...args,
      height: game.canvas.height,
      width: game.canvas.width,
    });

    const saveButton = new Button({
      font: "14px Arial, Helvetica, sans-serif",
      label: "Save game",
      onClick: () => console.log("jej"),
      x: 5,
      y: this.canvas.height - 20,
    });
    const loadButton = new Button({
      font: "14px Arial, Helvetica, sans-serif",
      label: "Load game",
      onClick: () => console.log("jej"),
      x: 0,
      y: this.canvas.height - 20,
    });
    loadButton.x = this.canvas.width - 5 - loadButton.width;

    this.prevState = {
      buttons: [
        saveButton,
        loadButton,
      ],
    };
  }

  public render = () => {
    if (this.rendered) {
      return; // no need to re-render
    }
    const ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;
    ctx.fillStyle = "rgba(0, 0, 0, .5)";

    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);

    ctx.font = "16px Arial, Helvetica, sans-serif";
    ctx.textAlign = "center";
    ctx.fillStyle = "#eee";
    ctx.fillText("Movement: WASD", this.canvas.width / 2, this.canvas.height / 2 - 32);
    ctx.fillText("Shoot: space", this.canvas.width / 2, this.canvas.height / 2);
    ctx.font = "10px Arial, Helvetica, sans-serif";
    ctx.fillText("Press space or movement keys to unpause", this.canvas.width / 2, this.canvas.height / 2 + 28);

    for (const button of this.prevState.buttons) {
      button.render(ctx);
    }

    this.rendered = true;
  }

  public update = ({ mouse, keyboard }: OverlayUpdateState) => {
    for (const button of this.prevState.buttons) {
      button.update(mouse);
    }
    for (const key of " wasd") {
      if (keyboard.keyState[key]) {
        this.exit();
      }
    }
  }
}
