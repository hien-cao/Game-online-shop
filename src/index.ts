import Game from "./Game";

(() => {
  const game = new Game();

  game.unmount();
  game.mount(document.getElementById("game-container") as HTMLElement);
})();
