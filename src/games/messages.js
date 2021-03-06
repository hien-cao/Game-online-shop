/**
 * Validation methods for incoming messages.
 */

/**
 * Validators for different message types incoming from child.
 */
export const messageValidators = {
  SCORE: [
    (data) => data.hasOwnProperty('score'),
  ],
  SAVE: [
    (data) => data.hasOwnProperty('gameState'),
  ],
  SETTING: [
    (data) => data.hasOwnProperty('options'),
  ],
};

/**
 *
 * @param {Object} data; MessageEvent, data attribute.
 */
export const validateMessage = (data) => {
  try {
    if (!Object.prototype.hasOwnProperty.call(data, 'messageType')) {
      throw new Error('Invalid messageType.');
    }
    if (Array.isArray(messageValidators[data.messageType])) {
      for (const validator of messageValidators[data.messageType]) {
        if (!validator(data)) {
          throw new Error(`Validator ${validator} failed for ${data}.`);
        }
      }
    }
    return true;
  } catch (e) {
    return false;
  }
};
