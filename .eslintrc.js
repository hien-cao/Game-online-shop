module.exports = {
  "parser": "babel-eslint",
  "extends": ["eslint:recommended", "google"],
  "env": {
    "browser": true,
  },
  "ecmaFeatures": {
    "modules": true
  },
  "rules": {
    "require-jsdoc": 0,
    "valid-jsdoc": 0,
    "no-console": 0,
  }
};
