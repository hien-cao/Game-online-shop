import GameObject from "../entities/GameObject";
import Zone, { ZoneArgs } from "./Zone";

type spawnable = GameObject | GameObject[];

export interface SpawnZoneArgs extends ZoneArgs {
  spawnRate: number;
  generateSpawn(zone: SpawnZone): spawnable;
}

export default class SpawnZone extends Zone {
  public spawnHandle?: number;
  public spawnRate: number;
  public generateSpawn: (zone: SpawnZone) => spawnable;

  constructor({ spawnRate, generateSpawn, ...args }: SpawnZoneArgs) {
    super(args);

    this.spawnRate = spawnRate;
    this.generateSpawn = generateSpawn;
    this.spawnHandle = window.setInterval(
      this.spawnObjects,
      1000 / this.spawnRate
    );
  }

  public remove = () => window.clearInterval(this.spawnHandle);

  private spawnObjects = () => {
    const spawn = this.generateSpawn(this);
    if (Array.isArray(spawn)) {
      for (const obj of spawn) {
        this.spawn(obj);
      }
    } else {
      this.spawn(spawn);
    }
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
