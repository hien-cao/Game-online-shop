"use strict";
/**
 * JS for `games/:id/play`
 * Global variables in this view:
 * @var {String} rawGameURL; The full URL of the game.
 * @var {URL} gameURL; URL object that may be parsed.
 */

/**
 * Loosely validates if the message object received is correct.
 *
 * @param {Event} e; Message Event from child
 * @param {URL} url; URL of the game
 */
const messageIsValid = (e, url) => (
  e.origin === url.origin &&
  validateMessage(e.data)
);

/**
 * Attach message listener for incoming messages.
 */
const attachMessageListener = () => {
  window.addEventListener("message", (e) => {
    if (messageIsValid(e, gameURL)) {
      console.log('message received is valid and from the right game url');
      const { data } = e;

      switch (data.messageType) {
        case "SCORE":
          console.log("Update score for player");
          const payload = {
            score: data.score,
          }
          defaultFetch(
            `/games/${gameID}/save-score/`,
            payload
          )
            .then(response => response.json())
            .then(console.log);
          break;
        case "SAVE":
          const { gameState } = data;
          defaultFetch(
            `/games/${gameID}/state/`,
            gameState
          ).then(response => {
            console.log(response);
            if (response.ok) {
              window.alert("Game saved succesfully")
            } else {
              window.alert("Attempting to save the game failed")
            }
          })
          break;
        case "SETTING":
          if (data.hasOwnProperty("options")) {
            const game = document.getElementById("game");
            if (data.options.hasOwnProperty("width")) {
              game.style.width = data.options.width + "px";
            }
            if (data.options.hasOwnProperty("height")) {
              game.style.height = data.options.height + "px";
            }
          }
          break;
        case "LOAD_REQUEST":
          fetch(`/games/${gameID}/state`)
            .then(response => response.json())
            .then(gameState => {
              document.getElementById("game").contentWindow.postMessage(
                {
                  messageType: "LOAD",
                  gameState
                },
                gameURL.origin
              )
            })
            .catch((e) => {
              console.log(e);
              document.getElementById("game").contentWindow.postMessage(
                {
                  messageType: "ERROR",
                  info: "Gamestate could not be loaded",
                },
                gameURL.origin
              )
            })
          console.log("Do something with load request");
          break;
        default:
          throw new Error("Invalid message type");
      }
    }
  });
};

/**
 * Attach listeners when DOM fully loaded.
 */
const onLoad = () => {
  attachMessageListener();
};

/**
 * Trigger onLoad when window fully loaded.
*/
(() => onLoad())();
