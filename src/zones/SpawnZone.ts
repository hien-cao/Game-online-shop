import GameObject from "../entities/GameObject";
import Game from "../Game";
import Zone, { ZoneArgs } from "./Zone";

type spawnable = GameObject | GameObject[];

export interface SpawnZoneArgs extends Pick<ZoneArgs, Exclude<keyof ZoneArgs, "absolutePosition">> {
  spawnRate: number;
  getSpawnModifier?(game: Game): number;
  generateSpawn(zone: SpawnZone): spawnable;
}

export default class SpawnZone extends Zone {
  public spawnRate: number;
  public prevSpawn = 0;
  public getSpawnModifier: (game: Game) => number;
  public generateSpawn: (zone: SpawnZone) => spawnable;

  constructor({ spawnRate, generateSpawn, getSpawnModifier = () => 1, ...args }: SpawnZoneArgs) {
    super({
      ...args,
      absolutePosition: true,
    });
    this.getSpawnModifier = getSpawnModifier;
    this.spawnRate = spawnRate;
    this.generateSpawn = generateSpawn;
  }

  public update = () => {
    if (this.game.prevLoop - this.prevSpawn < 1000 / (this.getSpawnModifier(this.game) * this.spawnRate)) {
      return;
    }
    const spawn = this.generateSpawn(this);
    if (Array.isArray(spawn)) {
      for (const obj of spawn) {
        this.spawn(obj);
      }
    } else {
      this.spawn(spawn);
    }
    this.prevSpawn = Date.now();
  }

  private spawn = (obj: GameObject) => {
    if (this.contains(obj)) {
      return;
    }
    obj.x = this.x + Math.random() * this.width;
    obj.y = this.y + Math.random() * this.height;

    if (this.absolutePosition) {
      obj.x += this.game.viewport.x;
      obj.y += this.game.viewport.y;
    }

    this.game.addGameObject(obj);
  }
}
