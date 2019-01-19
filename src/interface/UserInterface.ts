import Game from "../Game";

export default class UserInterface {
  public game: Game;

  constructor(game: Game) {
    this.game = game;
  }

  public render = (ctx: CanvasRenderingContext2D) => {
    const { player } = this.game;

    // hitpoints bar
    ctx.strokeStyle = "#555";
    ctx.rect(2, 2, 102, 14); // hp background
    ctx.stroke();
    ctx.fillStyle = "#333";
    ctx.fillRect(3, 3, 100, 12); // hp
    ctx.fillStyle = "#e05";
    ctx.fillRect(3, 3, 100 * player.life / player.maxLife, 12); // hp

    ctx.fillStyle = "#eee";
    ctx.textAlign = "center";
    ctx.fillText(`${player.life} / ${player.maxLife}`, 3 + 100 / 2, 12);

    // Score
    ctx.textAlign = "right";
    ctx.fillText(`Score: ${Math.floor(this.game.score)}`, this.game.canvas.width - 5, 12);

    // info
    ctx.fillText(
      `Coordinates: (${Math.floor(player.x)}, ${Math.floor(player.y)})`,
      this.game.canvas.width - 5,
      this.game.canvas.height - 5
    );
    // info
    ctx.fillText(
      `Velocity: (${Math.floor(player.velocity[0])}, ${Math.floor(player.velocity[1])})`,
      this.game.canvas.width - 5,
      this.game.canvas.height - 20
    );
  }
}
