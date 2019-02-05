import GameObject, { GameObjectArgs } from "./GameObject";
import Weapon from "./Weapon";

export interface ShipArgs extends GameObjectArgs {
  weapon?: Weapon;
  shield?: number;
  maxVelocity?: vector;
  minVelocity?: vector;
}

export default class Ship extends GameObject {
  public weapon?: Weapon;
  public maxVelocity: vector;
  public minVelocity: vector;
  public shield: number;

  constructor({ weapon, minVelocity = [10, 10], maxVelocity = [10, 10], shield = 0, ...args }: ShipArgs) {
    super(args);
    this.minVelocity = minVelocity;
    this.maxVelocity = maxVelocity;
    this.shield = shield;
    this.weapon = weapon;
  }
}
