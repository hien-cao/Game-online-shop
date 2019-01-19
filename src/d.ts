declare module "*.svg" { // to omit error when importing vector files
  const defaultExport: string;
  export default defaultExport;
}

type Vector = [number, number];
interface Bounds {
  r: number;
  t: number;
  l: number;
  b: number;
}
