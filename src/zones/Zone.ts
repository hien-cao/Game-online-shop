import GameObject from "../entities/GameObject";
import Game from "../Game";
import Viewport from "../ViewPort";

export interface ZoneArgs {
  x: number;
  y: number;
  width: number;
  height: number;
  game: Game;
  absolutePosition: boolean;
}

export default class Zone {
  public x: number;
  public y: number;
  public width: number;
  public height: number;
  public game: Game;
  public absolutePosition: boolean;

  constructor({ game, x, y, width, height, absolutePosition = false }: ZoneArgs) {
    this.game = game;

    this.absolutePosition = absolutePosition;
    this.x = x;
    this.y = y;
    this.width = width;
    this.height = height;
  }

  public remove = (): any => true;

  public contains = (obj: GameObject) => this.absolutePosition ?
    (
      obj.x + obj.width > this.x + this.game.viewport.x && obj.x < this.game.viewport.x + this.x + this.width &&
      obj.y + obj.height > this.y + this.game.viewport.y && obj.y < this.game.viewport.y + this.y + this.height
    ) : (
      obj.x + obj.width > this.x && obj.x < this.x + this.width &&
      obj.y + obj.height > this.y && obj.y < this.y + this.height
    )
}
