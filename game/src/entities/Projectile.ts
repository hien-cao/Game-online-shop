import GameObject, { GameObjectArgs } from "./GameObject";

export interface ProjectileArgs extends GameObjectArgs {
  source?: GameObject;
}

export default class Projectile extends GameObject {
  public source?: GameObject;

  constructor({ source, ...args }: ProjectileArgs) {
    super(args);
    this.source = source;
  }

  public collides = (obj: GameObject) => (
    this.source !== obj &&
    obj.x + obj.width > this.x && obj.x < this.x + this.width &&
    obj.y + obj.height > this.y && obj.y < this.y + this.height
  )
}
