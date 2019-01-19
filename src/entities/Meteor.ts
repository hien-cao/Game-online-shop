import Game from "../Game";
import Sprite from "../sprites/Sprite";
import GameObject, { GameObjectArgs } from "./GameObject";

export type MeteorArgs = Pick<GameObjectArgs, Exclude<keyof GameObjectArgs, "sprite">>;

export default class Meteor extends GameObject {
  public static generateSprite(radius: number, n: number = 3 + (Math.random() * 5)) {
    const sprite = document.createElement("canvas");
    sprite.width = radius * 2;
    sprite.height = radius * 2;
    const ctx = sprite.getContext("2d") as CanvasRenderingContext2D;

    const step = 2 * Math.PI / n;

    ctx.beginPath();
    const startX = (Math.random() * .1 * radius) + radius * 2;
    const startY = (Math.random() * .1 * radius) + radius;
    for (let i = 0; i < n; i++) {
      ctx.lineTo(
        (Math.random() * .1 * radius) + (radius + Math.cos(i * step) * radius),
        (Math.random() * .1 * radius) + (radius + Math.sin(i * step) * radius)
      );
    }
    ctx.lineTo(startX, startY);
    ctx.fillStyle = "#CCC";
    ctx.fill();
    ctx.rotate(Math.random() * Math.PI);

    return sprite;
  }

  constructor({ maxLife = 1 + Math.random() * 14, ...args }: MeteorArgs) {
    super({
      ...args,
      maxLife,
      sprite: new Sprite(Meteor.generateSprite(5 + maxLife, 3 + Math.random() * Math.sqrt(maxLife))),
    });
  }

  protected onDestroy(game: Game) {
    if (this.maxLife < 5) {
      return;
    }
    const m1 = new Meteor({
      maxLife: this.maxLife / 2,
      velocity: [this.velocity[0] + .5 - Math.random(), this.velocity[1] - Math.random()],
      x: this.x,
      y: this.y - 5,
    });
    const m2 = new Meteor({
      maxLife: this.maxLife / 2,
      velocity: [this.velocity[0] + .5 - Math.random(), this.velocity[1] + Math.random()],
      x: this.x,
      y: this.y - 5,
    });
    m1.immuneTo = [m2];
    m2.immuneTo = [m1];
    game.addGameObject(m1);
    game.addGameObject(m2);
  }
}
