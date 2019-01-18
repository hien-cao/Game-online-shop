import Game from "./game";

const game = new Game();

(() => {
  game.mount(document.getElementById("game-container") as HTMLElement);
})();
