import Game from "../game";
import GameObject from "./GameObject";

export default class Weapon {
  public fireRate: number;
  public lastFire: number;
  public ballisticVelocity: number;
  public Projectile: () => GameObject;

  constructor(fireRate: number, Projectile: () => GameObject, ballisticVelocity = 15, lastFire: number = 0) {
    this.fireRate = fireRate;
    this.lastFire = lastFire;
    this.ballisticVelocity = ballisticVelocity;
    this.Projectile = Projectile;
  }

  public fire = (obj: GameObject, game: Game) => {
    if (game.prevUpdate - this.lastFire > 1000 / this.fireRate) {
      this.lastFire = Date.now();
      const projectile = this.Projectile();
      projectile.x = obj.x;
      projectile.y = obj.y;
      projectile.velocity = [obj.velocity[0] + this.ballisticVelocity, obj.velocity[1]];

      game.addGameObject(projectile);
    }
  }
}
