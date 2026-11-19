// A turma VIVA (Ed, 19/11/2026: «vc agora tem que criar os motions, dar vida em cada personagem, todos com nota 10»).
// Cada personagem sai SEMPRE do desenho oficial dele (as poses que o Ed gerou, recortadas por
// banco/boneco-tiao/recortar_turma.py), nunca redesenhado. Por cima, so o que da vida:
//   respirar (o peito sobe, preso aos pes), balancar de leve, piscar (a palpebra desce com a cor da pele dele,
//   achada por banco/boneco-tiao/achar_rosto.py), entrar e trocar de pose com mola, tremer no susto, andar.
// Tudo e funcao do tempo (seek(t) puro).
import React from "react";
import { Img, staticFile } from "remotion";
import { mola } from "../../mola";
import TURMA from "../../../public/boneco/turma/turma.json";

export type Pid = "tiao" | "sandra" | "marcos" | "valeria" | "cida" | "jessica" | "rafa" | "lourival" | "patricia";
type Info = { nome: string; tam: [number, number]; olhos?: number[][] | null };
export const info = (pid: Pid, cod: string): Info => (TURMA as any)[pid][cod];

const cl = (v: number) => Math.max(0, Math.min(1, v));
const h = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const semente = (s: string) => [...s].reduce((a, c) => a + c.charCodeAt(0), 0);

// quando pisca: de 2,4 a 4,6 s entre uma e outra, as vezes duas seguidas (como gente)
export const piscadas = (seed: number, dur = 120): number[] => {
  const out: number[] = []; let t = 0.6 + 1.4 * h(seed);
  for (let i = 0; t < dur; i++) { out.push(t); if (h(seed + i * 3.3) > 0.82) out.push(t + 0.28); t += 2.4 + 2.2 * h(seed + i * 1.7); }
  return out;
};
const fecho = (t: number, q: number[]) => Math.max(0, ...q.map((c) => cl(1 - Math.abs(t - c) / 0.085)));

// a palpebra: desce de cima com a pele dele, a de baixo sobe um pouco, e o risco dos cilios vai na beira
const Palpebra: React.FC<{ o: number[]; p: number; esc: number }> = ({ o, p, esc }) => {
  if (p <= 0.02) return null;
  const [cx, cy, rx0, ry0, r = 220, g = 165, b = 125] = o; const rx = rx0 * 1.22, ry = ry0 * 1.25;
  const topo = cy - ry + 1.6 * ry * Math.min(1, p / 0.73);
  const baixo = cy + ry - 0.85 * ry * Math.min(1, p / 0.73);
  const linha = Math.min(topo, baixo);
  const id = `pp${Math.round(cx)}_${Math.round(cy)}`;
  const meia = (y: number) => rx * Math.sqrt(Math.max(0, 1 - ((y - cy) / ry) ** 2));
  const fechado = p >= 0.72; const yl = fechado ? cy + ry * 0.2 : linha; const w = fechado ? rx * 0.95 : meia(linha);
  const tinta = Math.max(2.5, 4 / esc);
  return (
    <g>
      <clipPath id={id}><ellipse cx={cx} cy={cy} rx={rx} ry={ry} /></clipPath>
      <g clipPath={`url(#${id})`}>
        <rect x={cx - rx} y={cy - ry - 2} width={rx * 2} height={Math.max(0, topo - (cy - ry) + 2)} fill={`rgb(${r},${g},${b})`} />
        <rect x={cx - rx} y={baixo} width={rx * 2} height={cy + ry - baixo + 2} fill={`rgb(${r},${g},${b})`} />
        {fechado && <rect x={cx - rx} y={cy - ry} width={rx * 2} height={ry * 2} fill={`rgb(${r},${g},${b})`} />}
      </g>
      <path d={`M ${cx - w} ${yl} Q ${cx} ${yl + ry * (fechado ? 0.45 : 0.25)} ${cx + w} ${yl}`} fill="none" stroke="#1B1310" strokeWidth={tinta * (fechado ? 1.2 : 1)} strokeLinecap="round" />
    </g>
  );
};

export type Vida = {
  t: number;            // tempo dentro do plano
  entra?: number;       // quando a pose aparece (mola de entrada); undefined = ja estava
  treme?: number;       // 0..1 susto
  respira?: number;     // forca da respiracao (1 = normal)
  pisca?: boolean;      // false = nao pisca (olho fechado, oculos escuros)
  espelho?: boolean;
};
// uma pose do personagem, de pe, presa pelos pes em (x, y) e com altura alt
export const Pose: React.FC<{ pid: Pid; cod: string; x: number; y: number; alt: number } & Vida> = ({ pid, cod, x, y, alt, t, entra, treme = 0, respira = 1, pisca = true, espelho }) => {
  const q = info(pid, cod); const [w, hh] = q.tam; const esc = alt / hh; const wd = w * esc; const s = semente(pid + cod);
  const e = entra === undefined ? 1 : mola(t - entra, 11, 0.55);
  if (entra !== undefined && t < entra) return null;
  const resp = Math.sin(t * 2.25 + s), bal = Math.sin(t * 1.15 + s * 0.7);
  const tx = treme * 10 * Math.sin(t * 71), ty = treme * 6 * Math.cos(t * 83);
  const tf = [
    `translate(${tx}px, ${ty + (1 - e) * 40}px)`,
    `rotate(${0.55 * bal * respira}deg)`,
    `scale(${(0.9 + 0.1 * e) * (espelho ? -1 : 1)}, ${(0.9 + 0.1 * e) * (1 + 0.009 * resp * respira)})`,
  ].join(" ");
  const p = pisca && q.olhos ? fecho(t, piscadas(s)) : 0;
  return (
    <div style={{ position: "absolute", left: x - wd / 2, top: y - alt, width: wd, height: alt, transformOrigin: "50% 100%", transform: tf, opacity: entra === undefined ? 1 : cl((t - entra) / 0.08) }}>
      <Img src={staticFile(`boneco/turma/${pid}/${cod}.png`)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }} />
      {q.olhos && p > 0 && (
        <svg viewBox={`0 0 ${w} ${hh}`} width="100%" height="100%" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
          {q.olhos.map((o, i) => <Palpebra key={i} o={o} p={p} esc={esc} />)}
        </svg>
      )}
    </div>
  );
};

// a sombra no chao, para nao boiar
export const Sombra: React.FC<{ x: number; y: number; larg: number; f?: number }> = ({ x, y, larg, f = 1 }) => (
  <div style={{ position: "absolute", left: x - larg / 2, top: y - larg * 0.07, width: larg, height: larg * 0.14, borderRadius: "50%", background: "rgba(25,15,5,0.32)", filter: "blur(7px)", transform: `scaleX(${f})` }} />
);

// andar: a pose de perfil a andar (R3), com o passo a subir e descer, o corpo a inclinar e a sombra a respirar
export const Andando: React.FC<{ pid: Pid; de: number; ate: number; y: number; alt: number; t: number; dur: number; passo?: number }> = ({ pid, de, ate, y, alt, t, dur, passo = 1.9 }) => {
  // o passo em 2 desenhos (como no desenho animado classico): a passada (R3) em baixo e as pernas juntas (R2) no alto
  const k = mola(t, 2.6 / dur * 3, 1); const x = de + (ate - de) * k; const vel = cl(1 - k * 1.03) ** 0.5;
  const fase = t * passo * Math.PI * 2;
  const alto = Math.abs(Math.sin(fase)) > 0.72 && vel > 0.15;
  // parado fica de perfil: a pose de frente (R1) da Valeria tem os oculos na cabeca e o andar no rosto (pulo de continuidade)
  const parou = false;
  const cod = parou ? "R1" : vel < 0.15 ? "R2" : alto ? "R2" : "R3";
  const q = info(pid, cod); const wd = q.tam[0] * (alt / q.tam[1]);
  const pulo = -Math.abs(Math.sin(fase)) * 14 * vel, inc = 1.4 * Math.sin(fase) * vel, amassa = 1 - 0.018 * Math.cos(fase * 2) * vel;
  const esq = ate < de && !parou;
  return (
    <>
      <Sombra x={x} y={y} larg={info(pid, "R3").tam[0] * (alt / info(pid, "R3").tam[1]) * 0.7} f={1 - 0.12 * (-pulo / 14)} />
      <div style={{ position: "absolute", left: x - wd / 2, top: y - alt + pulo, width: wd, height: alt, transformOrigin: "50% 100%", transform: `rotate(${esq ? -inc : inc}deg) scale(${esq ? -1 : 1}, ${amassa})` }}>
        <Img src={staticFile(`boneco/turma/${pid}/${cod}.png`)} style={{ width: "100%", height: "100%" }} />
      </div>
    </>
  );
};
