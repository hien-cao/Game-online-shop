"use strict";
/**
 * JS for `games/:id/play`
 * Global variables in this view:
 * @var {String} raw_game_url; The full URL of the game.
 * @var {URL} game_url; URL object that may be parsed.
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
        if (messageIsValid(e, game_url)) {
            console.log('message received is valid and from the right game url');
            const { data } = e;

            switch (data.messageType) {
                case "SCORE":
                    console.log("Update score for player");
                    const payload = {
                        score: data.score,
                    }
                    postData(
                        "save-score",
                        payload
                    ).then(data => {
                        console.log(data);
                    });
                    break;
                case "SAVE":
                    console.log("Save score somewhere");
                    break;
                case "SETTING":
                    console.log("Set settings somewhere");
                    break;
                default: // LOAD_REQUEST
                    console.log("Do something with load request");
                    break;
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