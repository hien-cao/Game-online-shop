import Game from "../Game";
import Sprite from "../sprites/Sprite";
import GameObject, { GameObjectArgs } from "./GameObject";

export interface MeteorArgs extends GameObjectArgs {
  radius?: number;
}

export default class Meteor extends GameObject {
  public static generateSprite(radius: number) {
    const n = 3 + Math.random() * Math.sqrt(radius); // number of verices
    const sprite = document.createElement("canvas");
    sprite.width = radius * 2;
    sprite.height = radius * 2;
    const ctx = sprite.getContext("2d") as CanvasRenderingContext2D;

    const step = 2 * Math.PI / n;

    ctx.beginPath();
    ctx.moveTo(
      Math.random() * .1 * radius + radius * 2,
      Math.random() * .1 * radius + radius
    );
    for (let i = 0; i < n; i++) {
      ctx.lineTo(
        (Math.random() * .1 * radius) + (radius + Math.cos(i * step) * radius),
        (Math.random() * .1 * radius) + (radius + Math.sin(i * step) * radius)
      );
    }
    ctx.closePath();
    ctx.fillStyle = "#CCC";
    ctx.fill();
    ctx.rotate(Math.random() * Math.PI);

    return sprite;
  }

  public radius: number;

  constructor({ radius, ...args }: MeteorArgs) {
    super(args);
    this.radius = this.maxLife * 2.5;
    this.sprite = new Sprite(Meteor.generateSprite(this.radius));
  }

  public getDistance = (obj: Trackable): number => Math.sqrt(obj instanceof Meteor ?
    (
      Math.pow(this.x + this.radius - (obj.x + obj.radius), 2) +
      Math.pow(this.y + this.radius - (obj.y + obj.radius), 2)
    ) : (
      Math.pow(this.x - obj.x, 2) +
      Math.pow(this.y - obj.y, 2)
    )
  )

  public collides = (obj: GameObject): boolean => obj instanceof Meteor ?
    (
      this.getDistance(obj) < obj.radius + this.radius
    ) : (
      obj.x + obj.width > this.x && obj.x < this.x + this.width &&
      obj.y + obj.height > this.y && obj.y < this.y + this.height
    )

  protected onDestroy(game: Game) {
    if (this.maxLife < 5) {
      return;
    }
    const m1 = new Meteor({
      maxLife: this.maxLife / 2,
      velocity: [this.velocity[0] + .5 - Math.random(), Math.min(this.velocity[1], 0) - 2 * Math.random()],
      x: this.x + this.radius,
      y: this.y + this.radius - 5,
    });
    const m2 = new Meteor({
      maxLife: this.maxLife / 2,
      velocity: [this.velocity[0] + .5 - Math.random(), Math.max(this.velocity[1], 0) + 2 * Math.random()],
      x: this.x + this.radius,
      y: this.y + this.radius + 5,
    });

    // splitted meteors should not be able to destroy eachother
    m1.immuneTo = [m2];
    m2.immuneTo = [m1];

    game.addGameObject(m1);
    game.addGameObject(m2);
  }
}
