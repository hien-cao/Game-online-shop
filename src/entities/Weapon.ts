import Game from "../game";
import Sprite from "../sprites/Sprite";
import GameObject from "./GameObject";
import Projectile from "./Projectile";
import Ship from "./Ship";

export interface WeaponArgs {
  fireRate: number;
  ballisticVelocity?: number;
  lastFire?: number;
  offset?: xy;
  ship?: Ship;
  projectileSettings: ProjectileSettings;
}

export interface ProjectileSettings {
  damage: number;
  sprite: Sprite;
}

export default class Weapon {
  public fireRate: number;
  public lastFire: number;
  public ballisticVelocity: number;
  public offset: xy;
  public ship?: Ship;
  public projectileSettings: ProjectileSettings;

  constructor({
    fireRate,
    projectileSettings,
    ballisticVelocity = 25,
    lastFire = 0,
    ship,
    offset = [0, 0],
  }: WeaponArgs) {
    this.fireRate = fireRate;
    this.lastFire = lastFire;
    this.ballisticVelocity = ballisticVelocity;
    this.projectileSettings = projectileSettings;
    this.offset = offset;
    this.ship = ship;
  }

  public fire = (obj: GameObject, game: Game) => {
    if (this.ship && game.prevLoop - this.lastFire > 1000 / this.fireRate) {
      this.lastFire = Date.now();
      const projectile = new Projectile({
        maxLife: this.projectileSettings.damage,
        source: this.ship,
        sprite: this.projectileSettings.sprite,
      });
      projectile.x = obj.x + this.offset[0] - obj.velocity[0];
      projectile.y = obj.y + this.offset[1] - obj.velocity[1];
      projectile.velocity = [obj.velocity[0] + this.ballisticVelocity, obj.velocity[1]];

      game.addGameObject(projectile);
    }
  }
}
