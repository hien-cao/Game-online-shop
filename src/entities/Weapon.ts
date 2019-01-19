import Game from "../game";
import GameObject from "./GameObject";

export interface WeaponArgs {
  fireRate: number;
  ballisticVelocity?: number;
  lastFire?: number;
  offset?: xy;
  Projectile(): GameObject;
}

export default class Weapon {
  public fireRate: number;
  public lastFire: number;
  public ballisticVelocity: number;
  public offset: xy;
  public Projectile: () => GameObject;

  constructor({
    fireRate,
    Projectile,
    ballisticVelocity = 15,
    lastFire = 0,
    offset = [0, 0],
  }: WeaponArgs) {
    this.fireRate = fireRate;
    this.lastFire = lastFire;
    this.ballisticVelocity = ballisticVelocity;
    this.Projectile = Projectile;
    this.offset = offset;
  }

  public fire = (obj: GameObject, game: Game) => {
    if (game.prevUpdate - this.lastFire > 1000 / this.fireRate) {
      this.lastFire = Date.now();
      const projectile = this.Projectile();
      projectile.x = obj.x + this.offset[0];
      projectile.y = obj.y + this.offset[1];
      projectile.velocity = [obj.velocity[0] + this.ballisticVelocity, obj.velocity[1]];

      game.addGameObject(projectile);
    }
  }
}
