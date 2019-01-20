import Game from "./Game";

(() => {
  const game = new Game();

  window.removeEventListener("message", game.load); // for development
  window.addEventListener("message", game.load, false);

  game.unmount(); // for development
  game.mount(document.getElementById("game-container") as HTMLElement);
})();
