module.exports = {
  "parser": "babel-eslint",
  "extends": ["google", "eslint:recommended"],
  "env": {
    "browser": true,
  },
  "ecmaFeatures": {
    "modules": true
  },
  "rules": {
    "require-jsdoc": 0,
    "valid-jsdoc": 0,
  }
};
