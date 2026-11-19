// Piloto da turma viva (19/11/2026): um gostinho do video 04 (a Valeria da SUV), so com as poses que o Ed gerou.
// A Valeria chega a andar, mostra a chave da SUV, o Tiao comenta (boca a seguir a voz), a fatura chega no celular,
// ela fica sem graca e o Tiao brinda com a caneca. Prova de piscar, respirar, mola, tremer e andar.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile } from "remotion";
import { mola } from "../../mola";
import { Pose, Andando, Sombra, aceno, brinde } from "./Turma";
import { Cenas, Bloco, tempos } from "../efeitos/Transicoes";
import { Acabamento, BrilhoDourado, Tensao } from "../efeitos/Acabamento";
import { Reacao } from "../reacoes";
import boca from "../../../public/piloto-motion/boca.json";

const FPS = 30, D0 = 3.98;
const cl = (v: number) => Math.max(0, Math.min(1, v));
const falar = (t: number, k: 0 | 1, ini: number) => {
  const v = (boca as Record<string, number[]>)[String(k)]; const i = Math.floor((t - ini) * FPS);
  if (i < 0 || i >= v.length) return 0;
  return Math.min(1, 1.15 * (0.6 * v[i] + 0.4 * (v[Math.max(0, i - 1)] ?? 0)));
};

const Fundo: React.FC<{ src: string; t: number; dur: number; zoom?: number; borrao?: number; fx?: number; fy?: number }> = ({ src, t, dur, zoom = 1, borrao = 0, fx = 50, fy = 50 }) => (
  <AbsoluteFill style={{ overflow: "hidden", background: "#2a2118" }}>
    <Img src={staticFile(src)} style={{ width: "100%", height: "100%", objectFit: "cover", transformOrigin: `${fx}% ${fy}%`, transform: `scale(${zoom * (1.02 + 0.04 * cl(t / dur))})`, filter: borrao ? `blur(${borrao}px)` : undefined }} />
  </AbsoluteFill>
);
// camera que respira: um empurrao lento para dentro do plano
const Camera: React.FC<{ t: number; dur: number; de?: number; ate?: number; fx?: number; fy?: number; children: React.ReactNode }> = ({ t, dur, de = 1, ate = 1.05, fx = 50, fy = 60, children }) => (
  <AbsoluteFill style={{ transformOrigin: `${fx}% ${fy}%`, transform: `scale(${de + (ate - de) * cl(t / dur)})` }}>{children}</AbsoluteFill>
);

// A · a Valeria chega a andar pela calcada e para ao lado da SUV dela (o cenario dela: a casa de vitrine)
const A_DUR = 3.3;
const Chega = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/suv-casa.jpg" t={t} dur={A_DUR} />
    <Andando pid="valeria" de={2250} ate={1660} y={1040} alt={700} t={t} dur={A_DUR} />
    <Acabamento t={t} poeira="lenta" />
  </AbsoluteFill>
);
// B · plano medio: a chave da SUV, cheia de si
const B_DUR = 3.0;
const Chave = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/suv-casa.jpg" t={t} dur={B_DUR} zoom={1.6} borrao={4} fx={52} fy={68} />
    <Camera t={t} dur={B_DUR}>
      <Pose pid="valeria" cod="P07" x={980} y={1120} alt={1080} t={t} entra={0.05} pisca={false} />
    </Camera>
    <BrilhoDourado t={t} />
    <Acabamento t={t} poeira="nada" />
  </AbsoluteFill>
);
// C · o Tiao comenta, com o caderno na mao (pose nova P09, a boca a seguir a voz)
const C_FALA = 0.2, C_DUR = C_FALA + D0 + 0.45;
const Comenta = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/cozinha.jpg" t={t} dur={C_DUR} zoom={1.45} borrao={4} fx={40} fy={55} />
    <Camera t={t} dur={C_DUR} de={1.0} ate={1.04} fx={45} fy={30}>
      <Pose pid="tiao" cod="P09" x={720} y={1150} alt={1150} t={t} entra={0.0} fala={falar(t, 0, C_FALA)} />
    </Camera>
    <Acabamento t={t} poeira="luz" />
  </AbsoluteFill>
);
// D · a fatura chega: susto, treme, pisca depressa
const D_DUR = 3.0;
const Fatura = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/suv-casa.jpg" t={t} dur={D_DUR} zoom={1.7} borrao={5} fx={45} fy={65} />
    <Camera t={t} dur={D_DUR} de={1.0} ate={1.09} fx={50} fy={35}>
      <Pose pid="valeria" cod="P08" x={960} y={1130} alt={1100} t={t} entra={0.0} treme={cl(1 - Math.abs(t - 0.55) / 0.5)} />
    </Camera>
    <Tensao t={t} />
    <Acabamento t={t} poeira="nada" />
  </AbsoluteFill>
);
// E · sem graca, com vergonha (oculos escuros: nao pisca, o corpo encolhe)
const E_DUR = 2.6;
const Vergonha = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/suv-casa.jpg" t={t} dur={E_DUR} zoom={1.6} borrao={5} fx={62} fy={62} />
    <Pose pid="valeria" cod="P11" x={1180} y={1110} alt={1060 - 25 * cl(t / E_DUR)} t={t} entra={0.0} pisca={false} respira={1.6} />
    <Acabamento t={t} poeira="lenta" />
  </AbsoluteFill>
);
// F · o Tiao brinda com a caneca velha: o braco sobe no "tchim"
const F_DUR = 3.2, F_TCHIM = 0.55;
const Brinde = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/cozinha.jpg" t={t} dur={F_DUR} zoom={1.4} borrao={4} fx={50} fy={55} />
    <Camera t={t} dur={F_DUR} de={1.0} ate={1.06}>
      <Sombra x={960} y={1075} larg={520} />
      <Pose pid="tiao" cod="P08" x={960} y={1130} alt={1120} t={t} entra={0.1} braco={brinde(t, F_TCHIM - 0.2)} />
    </Camera>
    <BrilhoDourado t={t} />
    <Acabamento t={t} poeira="luz" />
  </AbsoluteFill>
);

// G · o Tiao acena tchau (o braco abana no ombro)
const G_DUR = 2.4;
const Tchau = (t: number) => (
  <AbsoluteFill>
    <Fundo src="piloto-motion/cozinha.jpg" t={t} dur={G_DUR} zoom={1.4} borrao={4} fx={55} fy={55} />
    <Camera t={t} dur={G_DUR} de={1.0} ate={1.04}>
      <Pose pid="tiao" cod="P12" x={900} y={1130} alt={1120} t={t} entra={0.0} braco={aceno(t, 0.25)} />
    </Camera>
    <Acabamento t={t} poeira="luz" />
  </AbsoluteFill>
);

const BLOCOS: Bloco[] = [
  { dur: A_DUR, el: Chega },
  { dur: B_DUR, el: Chave, entra: "corte" },
  { dur: C_DUR, el: Comenta, entra: "chicote" },
  { dur: D_DUR, el: Fatura, entra: "zoom", td: 0.3 },
  { dur: E_DUR, el: Vergonha, entra: "corte" },
  { dur: F_DUR, el: Brinde, entra: "pagina" },
  { dur: G_DUR, el: Tchau, entra: "corte" },
];
const T = tempos(BLOCOS);
export const FIM_PILOTO_TURMA = T.fim;

export const PilotoTurma: React.FC = () => {
  const [, iB, iC, iD, iE, iF] = T.ini;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Cenas blocos={BLOCOS} />
      {/* cada emoji vive so na sua cena */}
      <Sequence from={Math.round(iB * FPS)} durationInFrames={Math.round(B_DUR * FPS)} layout="none"><Reacao x={70} y={22} e="😎" ini={0.45} tam={200} /></Sequence>
      <Sequence from={Math.round(iD * FPS)} durationInFrames={Math.round(D_DUR * FPS)} layout="none"><Reacao x={72} y={20} e="😱" ini={0.25} tam={230} /></Sequence>
      <Sequence from={Math.round(iF * FPS)} durationInFrames={Math.round(F_DUR * FPS)} layout="none"><Reacao x={30} y={22} e="✨" ini={0.5} tam={200} /></Sequence>
      <Sequence from={Math.round((iB + 0.35) * FPS)} durationInFrames={45} layout="none"><Audio src={staticFile("sfx/card.ogg")} volume={0.4} /></Sequence>
      <Sequence from={Math.round((iC + C_FALA) * FPS)} layout="none"><Audio src={staticFile("piloto-motion/fala0.wav")} /></Sequence>
      <Sequence from={Math.round((iD + 0.1) * FPS)} durationInFrames={45} layout="none"><Audio src={staticFile("sfx/warning.ogg")} volume={0.35} /></Sequence>
      <Sequence from={Math.round((iF + F_TCHIM) * FPS)} durationInFrames={60} layout="none"><Audio src={staticFile("sfx/ding.ogg")} volume={0.4} /></Sequence>
      <Audio src={staticFile("v02/trilha.mp3")} volume={0.07} />
    </AbsoluteFill>
  );
};
