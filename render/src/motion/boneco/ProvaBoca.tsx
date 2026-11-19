// Prova da boca que abre no proprio desenho (19/11/2026), agora lida da VOZ (fabrica/boca_voz.py):
// abre (a força), largura (redonda no «ó», esticada no «i») e acento (a sílaba forte: a cabeça acompanha).
// A voz aqui e de teste (as falas do piloto). O 3º plano mostra a opção A do Ed: a fala é DELA (balão), a voz é do Tião contando.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Pose, Balao } from "./Turma";
import { Acabamento } from "../efeitos/Acabamento";
import v0 from "../../../public/piloto-motion/fala0.boca.json";
import v1 from "../../../public/piloto-motion/fala1.boca.json";

const FPS = 30;
type Voz = { abre: number[]; largura: number[]; acento: number[] };
const VOZ: Voz[] = [v0 as Voz, v1 as Voz];
const ler = (v: Voz, t: number, forca = 1) => {
  const i = Math.floor(t * FPS); const ok = i >= 0 && i < v.abre.length;
  return { fala: ok ? v.abre[i] * forca : 0, largura: ok ? v.largura[i] : 0, acento: ok ? v.acento[i] * forca : 0 };
};
const PLANOS: { cod: string; k: 0 | 1; dur: number; balao?: string; forca?: number }[] = [
  { cod: "P10", k: 1, dur: 5.8 }, { cod: "P07", k: 0, dur: 4.6 },
  { cod: "P06", k: 0, dur: 4.6, balao: "Ai, Tião... que pobreza!", forca: 0.6 },
];
const INI = PLANOS.reduce<number[]>((a, p, i) => [...a, i ? a[i - 1] + PLANOS[i - 1].dur : 0], []);
export const FIM_PROVA_BOCA = INI[INI.length - 1] + PLANOS[PLANOS.length - 1].dur;
const VOZ_INI = 0.3;

const Plano: React.FC<{ cod: string; k: 0 | 1; balao?: string; forca?: number }> = ({ cod, k, balao, forca = 1 }) => {
  const t = useCurrentFrame() / FPS; const b = ler(VOZ[k], t - VOZ_INI, forca);
  const x = balao ? 1250 : 960;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img src={staticFile("piloto-motion/suv-casa.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", transform: "scale(1.6)", transformOrigin: "55% 65%", filter: "blur(5px)" }} />
      </AbsoluteFill>
      <Pose pid="valeria" cod={cod} x={x} y={1260} alt={1250} t={t} entra={0} fala={b.fala} largura={b.largura} acento={b.acento} />
      {balao && <Balao texto={balao} x={120} y={150} larg={820} t={t} ini={VOZ_INI} dur={VOZ[k].abre.length / FPS * 0.8} rabo={[1195, 452]} />}
      <Acabamento t={t} poeira="nada" />
    </AbsoluteFill>
  );
};

export const ProvaBoca: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    {PLANOS.map((p, i) => (
      <Sequence key={p.cod} from={Math.round(INI[i] * FPS)} durationInFrames={Math.round(p.dur * FPS)}>
        <Plano cod={p.cod} k={p.k} balao={p.balao} forca={p.forca} />
        <Sequence from={Math.round(VOZ_INI * FPS)} layout="none"><Audio src={staticFile(`piloto-motion/fala${p.k}.wav`)} /></Sequence>
      </Sequence>
    ))}
  </AbsoluteFill>
);
