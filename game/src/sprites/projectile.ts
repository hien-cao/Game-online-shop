const projectile = document.createElement("canvas");
projectile.width = 4;
projectile.height = 3;
const ctx = projectile.getContext("2d") as CanvasRenderingContext2D;
ctx.fillStyle = "#CCC";
ctx.fillRect(0, 0, 4, 3);

export default projectile;
