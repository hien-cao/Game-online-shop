import GameObject, { GameObjectArgs } from "./GameObject";
import Weapon from "./Weapon";

export interface ShipArgs extends GameObjectArgs {
  weapon?: Weapon;
  shield?: number;
}

export default class Ship extends GameObject {
  public weapon?: Weapon;
  public shield: number;

  constructor({ weapon, shield = 0, ...args }: ShipArgs) {
    super(args);
    this.shield = shield;
    this.weapon = weapon;
  }
}
