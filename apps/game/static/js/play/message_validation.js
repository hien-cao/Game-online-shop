/**
 * Validation methods for incoming messages.
 */

/**
 * Validators for different message types incoming from child.
 */
const messageValidators = {
	SCORE: [
 		data => data.hasOwnProperty("score"),
    ],
    SAVE: [
        data => data.hasOwnProperty("gameState"),
    ],
    SETTING: [
        data => data.hasOwnProperty("options"),
    ]
}

/**
 * 
 * @param {Object} data; MessageEvent, data attribute.
 */
const validateMessage = data => {
    try {
        if (!Object.prototype.hasOwnProperty.call(data, "messageType")) {
            throw new Error("Invalid messageType.");
        }
        console.log("data:", data)
        for (const validator of messageValidators[data.messageType]) {
            if (!validator(data)) {
                throw new Error(`Validator ${validator} failed for ${data}.`);
            }
        }
        return true;
    } catch (e) {
        console.log("Message validation error:", e);
        return false;
    }
}
