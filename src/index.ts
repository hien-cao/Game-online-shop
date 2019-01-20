import Game from "./Game";

(() => {
  const game = new Game();

  document.removeEventListener("message", game.load); // for development
  document.addEventListener("message", game.load, false);

  game.unmount(); // for development
  game.mount(document.getElementById("game-container") as HTMLElement);
})();
