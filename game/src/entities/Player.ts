import Game from "../game";
import Ship, { ShipArgs } from "./Ship";

export default class Player extends Ship {
  constructor(args: ShipArgs) {
    super(args);
    // add controls
    this.onUpdate = [
      (d, game: Game) => {
        game.score += .01 * Math.sqrt(this.velocity[0] * this.velocity[0] + this.velocity[1] * this.velocity[1]);
      },
      (d, game: Game) => {
        this.acceleration[0] = 0;
        this.acceleration[1] = 0;
        if (game.keyboard.keyState.w) {
          this.acceleration[1] -= 1;
        }
        if (game.keyboard.keyState.a) {
          this.acceleration[0] -= 1;
        }
        if (game.keyboard.keyState.s) {
          this.acceleration[1] += 1;
        }
        if (game.keyboard.keyState.d) {
          this.acceleration[0] += 1;
        }
        if (this.weapon && game.keyboard.keyState[" "]) {
          this.weapon.fire(this, game);
        }
      },
    ];
  }

  public onDestroy(game: Game) {
    game.setOverlay(game.overlays.end);
  }
}
