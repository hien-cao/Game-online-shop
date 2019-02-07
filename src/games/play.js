import {validateMessage} from './messages';
import {defaultFetch} from '../util';
/* global gameID */
/**
 * Loosely validates if the message object received is correct.
 *
 * @param {Event} e; Message Event from child
 * @param {URL} url; URL of the game
 */
export const messageIsValid = (e, url) => (
  e.origin === url.origin &&
  validateMessage(e.data)
);

/**
 * Attach message listener for incoming messages.
 */
export const attachMessageListener = () => {
  window.addEventListener('message', (e) => {
    const game = document.getElementById('game');
    if (messageIsValid(e, game.contentWindow.location)) {
      const {data} = e;

      switch (data.messageType) {
        case 'SCORE':
          defaultFetch(
              `/games/${gameID}/save-score/`,
              {score: data.score}
          )
              .then((response) => response.json())
              .then(() => alert('score submitted'));
          break;
        case 'SAVE':
          defaultFetch(
              `/games/${gameID}/state/`,
              data.gameState
          ).then((response) => {
            if (response.ok) {
              window.alert('Game saved succesfully');
            } else {
              window.alert('Attempting to save the game failed');
            }
          });
          break;
        case 'SETTING':
          if (data.hasOwnProperty('options')) {
            const game = document.getElementById('game');
            if (data.options.hasOwnProperty('width')) {
              game.style.width = data.options.width + 'px';
            }
            if (data.options.hasOwnProperty('height')) {
              game.style.height = data.options.height + 'px';
            }
          }
          break;
        case 'LOAD_REQUEST':
          fetch(`/games/${gameID}/state`)
              .then((response) => response.json())
              .then((gameState) => {
                document.getElementById('game').contentWindow.postMessage(
                    {
                      messageType: 'LOAD',
                      gameState,
                    },
                    game.contentWindow.location.href
                );
              })
              .catch((e) => {
                document.getElementById('game').contentWindow.postMessage(
                    {
                      messageType: 'ERROR',
                      info: 'Gamestate could not be loaded',
                    },
                    game.contentWindow.location.href
                );
              });
          break;
        default:
          throw new Error('Invalid message type');
      }
    }
  });
};

/**
 * Attach evenlisteners when DOM fully loaded.
*/
(() => attachMessageListener())();