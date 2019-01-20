import { globalSpeedModifier } from "../entities/GameObject";
import Overlay, { OverlayArgs } from "./Overlay";

export interface GameState {
  x: number;
  y: number;
  velocity: vector;
  life: number;
  maxLife: number;
  score: number;
}

export default class UserInterface extends Overlay {
  constructor(args: OverlayArgs) {
    super(args);
  }

  public render = (state: GameState) => {
    if (JSON.stringify(this.prevState) === JSON.stringify(state)) {
      return; // no need to re-render if no updates
    }
    const ctx = this.canvas.getContext("2d") as CanvasRenderingContext2D;

    ctx.font = "12 Arial, Helvetica, sans-serif";

    // hitpoints bar
    if (!this.prevState || this.prevState.life !== state.life || this.prevState.maxLife !== state.maxLife) {
      ctx.strokeStyle = "#555";
      ctx.rect(2, 2, 102, 14); // hp background
      ctx.stroke();
      ctx.fillStyle = "#333";
      ctx.fillRect(3, 3, 100, 12); // hp
      ctx.fillStyle = "#e05";
      ctx.fillRect(3, 3, 100 * state.life / state.maxLife, 12); // hp

      ctx.fillStyle = "#eee";
      ctx.textAlign = "center";
      ctx.fillText(`${state.life} / ${state.maxLife}`, 3 + 100 / 2, 12);
    }

    // Score
    const score = `Score: ${Math.floor(state.score)}`;
    let w = ctx.measureText(score).width;
    ctx.clearRect(this.canvas.width - 5 - w, 0, w, 12);
    ctx.textAlign = "right";
    ctx.fillText(score, this.canvas.width - 5, 12);

    // info
    const coordinates = `Coordinates: (${
      Math.floor(state.x / globalSpeedModifier)
      }, ${
      Math.floor(state.y / globalSpeedModifier)
      })`;
    const velocity = `Velocity: (${Math.floor(state.velocity[0])}, ${Math.floor(state.velocity[1])})`;
    w = Math.max(ctx.measureText(coordinates).width, ctx.measureText(velocity).width);
    ctx.clearRect(this.canvas.width - 10 - w, this.canvas.height - 32, w + 10, 32);
    ctx.fillText(
      coordinates,
      this.canvas.width - 5,
      this.canvas.height - 5
    );
    ctx.fillText(
      velocity,
      this.canvas.width - 5,
      this.canvas.height - 20
    );

    this.prevState = state;
  }

}
