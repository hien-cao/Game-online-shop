import Meteor from "../entities/Meteor";
import Game from "../Game";
import SpawnZone from "./SpawnZone";

export const getMeteorSpawns = (game: Game) => [
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 10,
      velocity: [Math.random() * 2 - 1, Math.random() * .5 - .25],
    }),
    spawnRate: 3,

    absolutePosition: true,
    height: game.canvas.height + 400,
    width: 200,
    x: game.canvas.width,
    y: -200,
  }),
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 10,
      velocity: [Math.random() * .5 - .25, Math.random() * 2 - .5],
    }),
    spawnRate: .5,

    absolutePosition: true,
    height: 180,
    width: game.canvas.width,
    y: -200,
  }),
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 10,
      velocity: [Math.random() * .5 - .25, -Math.random() * 2 + .5],
    }),
    spawnRate: .5,

    absolutePosition: true,
    height: 180,
    width: game.canvas.width,
    y: game.canvas.height,
  }),
];
