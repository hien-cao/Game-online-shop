import Game from "./Game";
import { loadSprites } from "./Sprite";

(() => {
  loadSprites().then((sprites) => {
    const game = new Game(sprites);

    game.unmount();
    game.mount(document.getElementById("game-container") as HTMLElement);
  });
})();
