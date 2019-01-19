
declare module "*.svg" { // to omit error when importing vector files
  const defaultExport: string;
  export default defaultExport;
}

type xy = [number, number];
type vector = [number, number];
interface Bounds {
  r: number;
  t: number;
  l: number;
  b: number;
}
interface Trackable {
  x: number;
  y: number;
  velocity: vector;
}
