import GameObject, { UpdateArgs } from "./GameObject";

export default class Player extends GameObject {
  public update = ({ keyState }: UpdateArgs) => {
    if (keyState.w) {
      this.velocity[1] -= 1;
    }
    if (keyState.a) {
      this.velocity[0] -= 1;
    }
    if (keyState.s) {
      this.velocity[1] += 1;
    }
    if (keyState.d) {
      this.velocity[0] += 1;
    }

    this.updatePosition();
  }
}
