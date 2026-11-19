// Piloto do video SO de motion, versao 2 (Ed, 18/11/2026: «Precisa ser mais parecido com o Tiao real!»).
// O Tiao verdadeiro (pecas da ficha) anda no plano aberto; quando fala, a camera corta para o plano medio numa das
// poses verdadeiras dele, com a boca a seguir a voz e a piscar. Cenarios sem gente (Cloudflare gratis). Grao por cima.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile } from "remotion";
import { mola } from "../../mola";
import { TiaoCorpo, CORPO_BASE, PoseCorpo, TiaoPose, NomePose, TAM_POSE } from "./TiaoReal";
import { Cenas, Bloco, tempos } from "../efeitos/Transicoes";
import { Grao } from "../efeitos/Grao";
import { Reacao } from "../reacoes";
import boca from "../../../public/piloto-motion/boca.json";

const FPS = 30;
const D0 = 3.98, D1 = 5.4, IH = 3.38; // duracao das falas e o "Ih" dentro da 2a
const cl = (v: number) => Math.max(0, Math.min(1, v));
const mix = (a: number, b: number, p: number) => a + (b - a) * p;
const piscar = (t: number, q: number[]) => Math.max(0, ...q.map((c) => cl(1 - Math.abs(t - c) / 0.075)));
const falar = (t: number, k: 0 | 1, ini: number) => {
  const v = (boca as Record<string, number[]>)[String(k)]; const i = Math.floor((t - ini) * FPS);
  if (i < 0 || i >= v.length) return 0;
  return Math.min(1, 1.15 * (0.6 * v[i] + 0.4 * (v[Math.max(0, i - 1)] ?? 0)));
};
const andar = (t: number, f: number): Partial<PoseCorpo> & { pulo: number } => {
  const fase = t * 2 * Math.PI * 1.8;
  return { pernaE: 11 * Math.sin(fase) * f, pernaD: -11 * Math.sin(fase) * f, bracoE: -5 * Math.sin(fase) * f, bracoD: -5 * Math.sin(fase) * f,
           tronco: 1.4 * Math.sin(fase) * f, cabeca: 1.2 * Math.sin(fase + 0.6) * f, pulo: -16 * Math.abs(Math.sin(fase)) * f };
};

const Fundo: React.FC<{ src: string; t: number; dur: number; zoom?: number; borrao?: number; fx?: number; fy?: number }> = ({ src, t, dur, zoom = 1, borrao = 0, fx = 50, fy = 50 }) => (
  <AbsoluteFill style={{ overflow: "hidden", background: "#2a2118" }}>
    <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", transformOrigin: `${fx}% ${fy}%`, transform: `scale(${zoom * (1.02 + 0.04 * cl(t / dur))})`, filter: borrao ? `blur(${borrao}px)` : undefined }} />
  </AbsoluteFill>
);
// corpo inteiro posto pelos pes
const Corpo: React.FC<{ p: PoseCorpo; x: number; y: number; alt: number }> = ({ p, x, y, alt }) => {
  const w = alt * (1161 / 2909);
  return (
    <>
      <div style={{ position: "absolute", left: x - w * 0.5, top: y - 22, width: w, height: 44, borderRadius: "50%", background: "rgba(40,25,10,0.3)", filter: "blur(6px)" }} />
      <div style={{ position: "absolute", left: x - w / 2, top: y - alt, width: w, height: alt }}><TiaoCorpo p={p} alt={alt} /></div>
    </>
  );
};
// plano medio: a pose entra com um empurrao de camera e respira
const Medio: React.FC<{ pose: NomePose; t: number; boca: number; pisca: number; x: number; alt: number; treme?: number }> = ({ pose, t, boca: b, pisca, x, alt, treme = 0 }) => {
  const [w, h] = TAM_POSE(pose); const wd = alt * (w / h);
  const entra = mola(t, 9, 0.75), esc = 1.06 - 0.06 * entra;
  const resp = Math.sin(t * 2.3), bal = 0.7 * Math.sin(t * 1.3);
  const tx = treme * 14 * Math.sin(t * 70), ty = treme * 10 * Math.cos(t * 83);
  return (
    <div style={{ position: "absolute", left: x - wd / 2 + tx, top: 70 + ty, width: wd, height: alt, transformOrigin: "50% 100%",
      transform: `scale(${esc * (1 + 0.012 * b)}) rotate(${bal - 0.8 * b}deg) scaleY(${1 + 0.006 * resp})` }}>
      <TiaoPose pose={pose} piscar={pisca} boca={b} />
    </div>
  );
};

// ---- os planos ----
const A_DUR = 2.7;
const RuaAberta = (t: number) => {
  const chega = mola(t - 0.05, 3.0, 1), x = mix(2150, 1180, chega), f = cl(1 - chega * 1.04) ** 0.55;
  const w = andar(t, f);
  const p: PoseCorpo = { ...CORPO_BASE, ...w, piscar: piscar(t, [2.2]), respira: 0.5 + 0.5 * Math.sin(t * 2.2), sorriso: 1, olhar: mix(-0.6, 0, cl((t - 1.6) / 0.3)) };
  return <AbsoluteFill><Fundo src="piloto-motion/rua.jpg" t={t} dur={A_DUR} /><Corpo p={p} x={x} y={1050 + w.pulo} alt={640} /></AbsoluteFill>;
};
const B_FALA = 0.25, B_DUR = B_FALA + D0 + 0.55;
const RuaMedio = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/rua.jpg" t={t} dur={B_DUR} zoom={1.55} borrao={3} fx={62} fy={62} />
    <Medio pose="explica" t={t} boca={falar(t, 0, B_FALA)} pisca={piscar(t, [1.9, 4.3])} x={1150} alt={1450} />
  </AbsoluteFill>
);
const C_DUR = 2.9;
const CozAberta = (t: number) => {
  const chega = mola(t - 0.05, 3.1, 1), x = mix(-250, 640, chega), f = cl(1 - chega * 1.04) ** 0.55;
  const w = andar(t, f);
  const p: PoseCorpo = { ...CORPO_BASE, ...w, piscar: piscar(t, [0.6, 2.4]), respira: 0.5 + 0.5 * Math.sin(t * 2.2), sorriso: 0.6, olhar: mix(0.6, 0, cl((t - 1.7) / 0.3)), sobr: 0.3 * cl((t - 2) / 0.4) };
  return <AbsoluteFill><Fundo src="piloto-motion/cozinha.jpg" t={t} dur={C_DUR} zoom={1.03} /><Corpo p={p} x={x} y={1062 + w.pulo} alt={730} /></AbsoluteFill>;
};
const D_FALA = 0.25, D_DUR = D_FALA + IH + 0.2;
const CozMedio = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/cozinha.jpg" t={t} dur={D_DUR} zoom={1.45} borrao={3} fx={35} fy={55} />
    <Medio pose="aponta" t={t} boca={falar(t, 1, D_FALA)} pisca={piscar(t, [1.5])} x={820} alt={1450} />
  </AbsoluteFill>
);
// a nota de dinheiro que «criou perna» e foge pela frente
const Nota: React.FC<{ t: number }> = ({ t }) => {
  if (t < 0) return null;
  const sai = cl(t / 1.7), x = mix(-200, 2200, sai), f = Math.sin(t * 24), y = 1010 - 16 * Math.abs(Math.sin(t * 24));
  return (
    <svg width="420" height="380" viewBox="-110 -110 220 200" style={{ position: "absolute", left: x - 210, top: y - 210, overflow: "visible" }}>
      <path d={`M -22 30 L ${-30 + 18 * f} 78 L ${-44 + 18 * f} 80`} stroke="#1F1B16" strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <path d={`M 22 30 L ${30 - 18 * f} 78 L ${16 - 18 * f} 80`} stroke="#1F1B16" strokeWidth={7} fill="none" strokeLinecap="round" strokeLinejoin="round" />
      <g transform={`rotate(${-6 + 6 * f})`}>
        <rect x={-82} y={-46} width={164} height={84} rx={10} fill="#6FBF73" stroke="#1F1B16" strokeWidth={6} />
        <rect x={-66} y={-32} width={132} height={56} rx={6} fill="none" stroke="#3E8E46" strokeWidth={4} />
        <circle cx={0} cy={-4} r={22} fill="#A8DCA6" stroke="#3E8E46" strokeWidth={4} />
        <ellipse cx={-34} cy={-8} rx={9} ry={11} fill="#fff" stroke="#1F1B16" strokeWidth={3} /><circle cx={-30} cy={-6} r={4.5} fill="#1F1B16" />
        <ellipse cx={34} cy={-8} rx={9} ry={11} fill="#fff" stroke="#1F1B16" strokeWidth={3} /><circle cx={38} cy={-6} r={4.5} fill="#1F1B16" />
        <path d="M -12 18 Q 0 26 12 18" stroke="#1F1B16" strokeWidth={4} fill="none" strokeLinecap="round" />
      </g>
    </svg>
  );
};
const E_DUR = (D1 - IH) + 1.7;
const CozSusto = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/cozinha.jpg" t={t} dur={E_DUR} zoom={1.6} borrao={4} fx={40} fy={55} />
    <Medio pose="alerta" t={t + 0.5} boca={falar(t + IH - 0.1 + D_FALA, 1, D_FALA)} pisca={piscar(t, [2.6])} x={900} alt={1500} treme={cl(1 - t / 0.5)} />
    <Nota t={t - 0.45} />
  </AbsoluteFill>
);

const BLOCOS: Bloco[] = [
  { dur: A_DUR, el: RuaAberta },
  { dur: B_DUR, el: RuaMedio, entra: "corte" },
  { dur: C_DUR, el: CozAberta, entra: "rasgo" },
  { dur: D_DUR, el: CozMedio, entra: "corte" },
  { dur: E_DUR, el: CozSusto, entra: "zoom", td: 0.3 },
];
const T = tempos(BLOCOS);
export const FIM_PILOTO_MOTION = T.fim;

export const PilotoMotion: React.FC = () => {
  const [, iB, , iD, iE] = T.ini;
  const fala1 = iD + D_FALA;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Cenas blocos={BLOCOS} />
      <Reacao x={67} y={20} e="😱" ini={iE + 0.12} tam={230} />
      <Sequence from={Math.round((iB + B_FALA) * FPS)} layout="none"><Audio src={staticFile("piloto-motion/fala0.wav")} /></Sequence>
      <Sequence from={Math.round(fala1 * FPS)} layout="none"><Audio src={staticFile("piloto-motion/fala1.wav")} /></Sequence>
      <Sequence from={Math.round((iE + 0.5) * FPS)} durationInFrames={60} layout="none"><Audio src={staticFile("sfx/money.ogg")} volume={0.35} /></Sequence>
      <Audio src={staticFile("v02/trilha.mp3")} volume={0.07} />
      <Grao />
    </AbsoluteFill>
  );
};
