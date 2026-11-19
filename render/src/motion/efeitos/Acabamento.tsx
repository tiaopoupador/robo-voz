// Acabamento por cima das cenas (Ed, 18/11/2026): «gostei da 4 sem graos mas com uma poeira passando mais lentamente e mais
// sutil (...) no do tuco parece uma neve mais grossa caindo de vez em quando e tem slide q nao tem nada».
// Luz de cinema (sempre) + um tipo de poeira por cena, ou nenhum. Tudo e funcao do tempo (seek(t) puro).
import React from "react";
import { AbsoluteFill } from "remotion";

const h = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const cl = (v: number) => Math.max(0, Math.min(1, v));
const W = 1920, H = 1080;

// luz de cinema: uma luz quente que passa devagar, o brilho que respira, as bordas um pouco mais escuras
export const LuzCinema: React.FC<{ t: number }> = ({ t }) => {
  const x = 50 + 55 * Math.sin(t * 0.35), y = 20 + 15 * Math.cos(t * 0.27);
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${x}% ${y}%, rgba(255,170,80,0.7) 0%, rgba(255,140,60,0) 42%)`, mixBlendMode: "screen", opacity: 0.32 + 0.08 * Math.sin(t * 1.1) }} />
      <AbsoluteFill style={{ background: "#FFF3D6", mixBlendMode: "soft-light", opacity: 0.06 + 0.03 * Math.sin(t * 3.1) }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(20,14,8,0.38) 100%)" }} />
    </AbsoluteFill>
  );
};

type Particula = { x: number; y: number; r: number; a: number };
// cada particula da a volta na tela no seu proprio tempo; entra e sai a desvanecer
const campo = (t: number, n: number, sem: number, o: { vx: number; vy: number; r: [number, number]; a: number; balanco: number }): Particula[] =>
  Array.from({ length: n }, (_, i) => {
    const k = sem * 100 + i * 7, vel = 0.6 + 0.8 * h(k + 1);
    const vida = (H + 200) / (Math.abs(o.vy) * vel + 1e-6); // segundos para cruzar a tela
    const p = ((t / vida) + h(k + 2)) % 1;                    // 0..1 ao longo do caminho
    const y0 = o.vy >= 0 ? -100 + p * (H + 200) : H + 100 - p * (H + 200);
    const x = (h(k + 3) * W + o.vx * vel * t + o.balanco * Math.sin(t * (0.5 + h(k + 4)) + i)) % W;
    const funde = cl(Math.min(p, 1 - p) * 6);
    return { x: x < 0 ? x + W : x, y: y0, r: o.r[0] + (o.r[1] - o.r[0]) * h(k + 5), a: o.a * funde * (0.5 + 0.5 * h(k + 6)) };
  });

// A) poeira lenta e sutil, a flutuar na luz
export const PoeiraLenta: React.FC<{ t: number }> = ({ t }) => (
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, pointerEvents: "none" }}>
    <filter id="pl"><feGaussianBlur stdDeviation="1.2" /></filter>
    <g filter="url(#pl)">{campo(t, 26, 1, { vx: 9, vy: 14, r: [1.8, 4], a: 0.55, balanco: 30 }).map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={p.r} fill="#FFF6E0" opacity={p.a} />)}</g>
  </svg>
);
// B) neve grossa que cai de vez em quando (rajadas), e depois nada
export const NeveGrossa: React.FC<{ t: number; rajadas?: [number, number][] }> = ({ t, rajadas = [[0.6, 4.6]] }) => {
  const forca = Math.max(0, ...rajadas.map(([a, b]) => cl((t - a) / 0.8) * cl((b - t) / 0.8)));
  if (forca <= 0) return null;
  return (
    <svg width={W} height={H} style={{ position: "absolute", inset: 0, pointerEvents: "none", opacity: forca }}>
      <filter id="ng"><feGaussianBlur stdDeviation="2.2" /></filter>
      <g filter="url(#ng)">{campo(t, 60, 2, { vx: -14, vy: 150, r: [4.5, 10], a: 0.75, balanco: 40 }).map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={p.r} fill="#FFFFFF" opacity={p.a} />)}</g>
    </svg>
  );
};
// C) pontos de luz grandes e desfocados que sobem devagar (como poeira contra o sol)
export const PontosDeLuz: React.FC<{ t: number }> = ({ t }) => (
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, pointerEvents: "none", mixBlendMode: "screen" }}>
    <filter id="pz"><feGaussianBlur stdDeviation="7" /></filter>
    <g filter="url(#pz)">{campo(t, 14, 3, { vx: 6, vy: -18, r: [14, 30], a: 0.55, balanco: 50 }).map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={p.r} fill="#FFE2B0" opacity={p.a} />)}</g>
  </svg>
);

// ---- climas que seguem a fala (Ed, 18/11: «quando falar noite chuvosa, ai cai uma chuva (...) algo ruim (...) poeira como de fogo, mas bem sutil») ----
// chuva fina: riscos finos e apagados, um pouco de azul escuro por cima
export const Chuva: React.FC<{ t: number }> = ({ t }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <AbsoluteFill style={{ background: "rgba(30,45,75,0.22)", mixBlendMode: "multiply" }} />
    <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
      {campo(t, 80, 4, { vx: -120, vy: 1500, r: [0.9, 1.6], a: 0.22, balanco: 0 }).map((p, i) => (
        <line key={i} x1={p.x} y1={p.y} x2={p.x + 9} y2={p.y - 46 - 30 * p.r} stroke="#DCE6F2" strokeWidth={p.r} strokeLinecap="round" opacity={p.a} />
      ))}
    </svg>
  </AbsoluteFill>
);
// brasas: faiscas laranja pequenas que sobem devagar e piscam, um calor leve vindo de baixo (coisa ruim, dinheiro a queimar)
export const Brasas: React.FC<{ t: number }> = ({ t }) => {
  const ps = campo(t, 18, 5, { vx: 10, vy: -60, r: [1.8, 3.4], a: 0.5, balanco: 45 });
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <AbsoluteFill style={{ background: "linear-gradient(to top, rgba(255,90,30,0.12), rgba(255,90,30,0) 40%)", mixBlendMode: "screen" }} />
      <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
        <filter id="br"><feGaussianBlur stdDeviation="3.5" /></filter>
        {ps.map((p, i) => {
          const pisca = 0.55 + 0.45 * Math.sin(t * (6 + i % 5) + i * 2);
          return (
            <g key={i} opacity={p.a * pisca}>
              <circle cx={p.x} cy={p.y} r={p.r * 2.8} fill="#FF5A14" opacity={0.5} filter="url(#br)" />
              <circle cx={p.x} cy={p.y} r={p.r} fill="#FFB347" />
            </g>
          );
        })}
      </svg>
    </AbsoluteFill>
  );
};
// brilho dourado: coisa boa, descoberta, dinheiro guardado
export const BrilhoDourado: React.FC<{ t: number }> = ({ t }) => (
  <svg width={W} height={H} style={{ position: "absolute", inset: 0, pointerEvents: "none", mixBlendMode: "screen" }}>
    <filter id="bd"><feGaussianBlur stdDeviation="2" /></filter>
    <g filter="url(#bd)">{campo(t, 24, 6, { vx: 5, vy: -22, r: [2, 5], a: 0.7, balanco: 35 }).map((p, i) => (
      <circle key={i} cx={p.x} cy={p.y} r={p.r * (0.8 + 0.3 * Math.sin(t * 3 + i))} fill="#FFD36B" opacity={p.a * (0.6 + 0.4 * Math.sin(t * 2.4 + i))} />
    ))}</g>
  </svg>
);
// tensao: as bordas escurecem a bater como um coracao
export const Tensao: React.FC<{ t: number }> = ({ t }) => {
  const f = (t * 1.25) % 1, bate = Math.exp(-f * 9) + 0.6 * Math.exp(-Math.max(0, f - 0.22) * 9) * (f > 0.22 ? 1 : 0);
  return <AbsoluteFill style={{ pointerEvents: "none", background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 45%, rgba(40,0,0,0.65) 100%)", opacity: 0.35 + 0.4 * bate }} />;
};
// o passado: filtro na IMAGEM (fica por baixo da luz) e um acabamento por cima
export type Passado = "pb" | "sepia" | "memoria";
export const FILTRO_PASSADO: Record<Passado, string> = {
  pb: "grayscale(1) contrast(1.06) brightness(1.02)",
  sepia: "sepia(0.85) saturate(0.75) contrast(0.95) brightness(1.03)",
  memoria: "sepia(0.45) saturate(0.6) brightness(1.06) contrast(0.92)",
};
export const BordaPassado: React.FC<{ tipo: Passado; t: number }> = ({ tipo, t }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    {tipo === "sepia" && <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 50%, rgba(60,35,10,0.55) 100%)" }} />}
    {tipo === "memoria" && <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(255,250,235,0) 45%, rgba(255,248,230,0.75) 100%)", opacity: 0.85 + 0.1 * Math.sin(t * 1.5) }} />}
    {tipo === "pb" && <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,0.45) 100%)" }} />}
  </AbsoluteFill>
);

export type Poeira = "nada" | "lenta" | "neve" | "luz";
export const Acabamento: React.FC<{ t: number; poeira: Poeira; tc?: number }> = ({ t, poeira, tc = t }) => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <LuzCinema t={t} />
    {poeira === "lenta" && <PoeiraLenta t={tc} />}
    {poeira === "neve" && <NeveGrossa t={tc} />}
    {poeira === "luz" && <PontosDeLuz t={tc} />}
  </AbsoluteFill>
);
