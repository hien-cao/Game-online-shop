import GameObject, { GameObjectArgs } from "./GameObject";

export interface ShipArgs extends GameObjectArgs {
  shield: number;
}

export default class Ship extends GameObject {

}
