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

  constructor(args: MeteorArgs) {
    super({
      ...args,
      sprite: new Sprite(Meteor.generateSprite(15)),
    });
  }

  protected onDestroy(game: Game) {
    if (this.life < 5) {
      return;
    }
  }
}
