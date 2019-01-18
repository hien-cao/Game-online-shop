import spriteSRC from "../../static/images/ship.svg";
import Sprite from "../Sprite";
import GameObject from "./GameObject";

const sprite = new Image();
sprite.src = spriteSRC;

export default class Ship extends GameObject {
  constructor() {
    super(new Sprite(sprite, .15));
  }

  public update = () => {
    //
  }
}
