// Mola amortecida (copiada da skill /designer): acelera, passa um fio e assenta.
export const mola = (t: number, w: number, z: number): number => {
  if (t <= 0) return 0;
  if (z >= 1) return 1 - Math.exp(-w * t) * (1 + w * t);
  const wd = w * Math.sqrt(1 - z * z);
  return 1 - Math.exp(-z * w * t) * (Math.cos(wd * t) + ((z * w) / wd) * Math.sin(wd * t));
};
export const MOLAS = { texto: [15, 1], cartao: [13, 0.72], estalo: [26, 0.5], lenta: [4.2, 1] } as const;
