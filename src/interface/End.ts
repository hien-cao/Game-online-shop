import { Button } from "../controls/Button";
import Game from "../Game";
import Overlay, { OverlayUpdateState } from "./Overlay";

export interface EndArgs {
  game: Game;
}

export default class End extends Overlay {
  public prevState: {
    buttons: Button[]
  };

  constructor({ game, ...args }: EndArgs) {
    super({
      ...args,
      height: game.canvas.height,
      width: game.canvas.width,
    });

    const restartButton = new Button({
      font: "16px Arial, Helvetica, sans-serif",
      label: "Restart Game",
      onClick: () => game.reset(),
      x: 0,
      y: this.canvas.height / 2,
    });
    restartButton.x = this.canvas.width / 2 - restartButton.width / 2;
    const highScoreButton = new Button({
      font: "18px Arial, Helvetica, sans-serif",
      label: "Submit score",
      onClick: () => console.log("jej"),
      x: 0,
      y: this.canvas.height - 40,
    });
    highScoreButton.x = this.canvas.width / 2 - highScoreButton.width / 2;

    this.prevState = {
      buttons: [
        restartButton,
        highScoreButton,
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

    ctx.font = "10px Arial, Helvetica, sans-serif";
    ctx.textAlign = "center";
    ctx.fillStyle = "#eee";
    ctx.fillText(
      "Your journey ended in the vast space,",
      this.canvas.width / 2,
      this.canvas.height / 2 - 48
    );
    ctx.fillText(
      "where the fragments of your ship fill float until the end of the time.",
      this.canvas.width / 2,
      this.canvas.height / 2 - 30
    );
    ctx.fillText(
      "You can only hope that your journey was not made in vain, and someone will hear of your heroic exploits",
      this.canvas.width / 2,
      this.canvas.height - 60
    );

    for (const button of this.prevState.buttons) {
      button.render(ctx);
    }

    this.rendered = true;
  }

  public update = ({ mouse, keyboard }: OverlayUpdateState) => {
    for (const button of this.prevState.buttons) {
      button.update(mouse);
    }
  }
}
