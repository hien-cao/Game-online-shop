import Meteor from "../entities/Meteor";
import Game from "../Game";
import SpawnZone from "./SpawnZone";

export const getMeteorSpawns = (game: Game) => [
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 10,
      velocity: [Math.random() * 6 - 3, Math.random() * 1.5 - .75],
    }),
    getSpawnModifier: ({ player }) =>
      .2 + .8 * player.velocity[0] / player.maxVelocity[0],
    spawnRate: 3.5,

    height: game.canvas.height + 200,
    width: 150,
    x: game.canvas.width,
    y: -100,
  }),
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 10,
      velocity: [Math.random() * 1.5 - .75, Math.random() * 6 - 1.5],
    }),
    getSpawnModifier: ({ player }) =>
      .2 + .8 * Math.min(0, player.velocity[1]) / player.minVelocity[1],
    spawnRate: 1.5,

    height: 100,
    width: game.canvas.width,
    y: -200,
  }),
  new SpawnZone({
    game,

    generateSpawn: () => new Meteor({
      maxLife: 3 + Math.random() * 8,
      velocity: [Math.random() * 1.5 - .75, -Math.random() * 6 + 1.5],
    }),
    getSpawnModifier: ({ player }) =>
      .2 + .8 * Math.max(0, player.velocity[1]) / player.maxVelocity[1],
    spawnRate: 1.5,

    height: 100,
    width: game.canvas.width,
    y: game.canvas.height,
  }),
];
