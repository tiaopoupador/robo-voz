// Previa para o Ed (18/11/2026): «o grao (...) pra mim ainda esta muito forte! (...) essas bolinhas (...) quero ver outras opcoes!»
// A mesma imagem 7 vezes, cada uma com um acabamento diferente por cima, para comparar lado a lado.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { Grao } from "./Grao";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const cl = (v: number) => Math.max(0, Math.min(1, v));
const h = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const DUR = 5;

// grao de filme bem fino e fraco, sem poeira
const GraoFino: React.FC = () => {
  const s = Math.floor(useCurrentFrame() / 2);
  return (
    <svg width="1920" height="1080" style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity: 0.28 }}>
      <filter id={`f${s}`} x="0" y="0" width="100%" height="100%">
        <feTurbulence type="fractalNoise" baseFrequency="0.95" numOctaves={1} seed={s % 997} />
        <feColorMatrix type="saturate" values="0" />
      </filter>
      <rect width="1920" height="1080" filter={`url(#f${s})`} />
    </svg>
  );
};
// textura de papel de desenho: PARADA (nao mexe), como se a imagem estivesse impressa em papel
const Papel: React.FC<{ forca?: number }> = ({ forca = 1 }) => (
  <svg width="1920" height="1080" style={{ position: "absolute", inset: 0, mixBlendMode: "soft-light", opacity: 0.9 * forca }}>
    <filter id="papel" x="0" y="0" width="100%" height="100%">
      <feTurbulence type="fractalNoise" baseFrequency="0.035 0.05" numOctaves={4} seed={7} result="manchas" />
      <feTurbulence type="fractalNoise" baseFrequency="0.7 0.9" numOctaves={2} seed={3} result="fibra" />
      <feBlend in="manchas" in2="fibra" mode="multiply" />
      <feColorMatrix type="saturate" values="0" />
    </filter>
    <rect width="1920" height="1080" filter="url(#papel)" />
  </svg>
);
// luz de cinema: brilho que respira devagar, uma luz quente que passa pela borda, vinheta
const Luz: React.FC = () => {
  const t = useCurrentFrame() / 30;
  const x = 50 + 55 * Math.sin(t * 0.35), y = 20 + 15 * Math.cos(t * 0.27);
  return (
    <>
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${x}% ${y}%, rgba(255,170,80,0.7) 0%, rgba(255,140,60,0) 42%)`, mixBlendMode: "screen", opacity: 0.32 + 0.08 * Math.sin(t * 1.1) }} />
      <AbsoluteFill style={{ background: "#FFF3D6", mixBlendMode: "soft-light", opacity: 0.06 + 0.03 * Math.sin(t * 3.1) }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(20,14,8,0.38) 100%)" }} />
    </>
  );
};
// filme antigo: grao fino + um risco vertical fino que aparece de vez em quando (sem bolinhas)
const Riscos: React.FC = () => {
  const s = Math.floor(useCurrentFrame() / 2);
  const riscos = [0, 1].map((i) => ({ on: h(s * 5 + i * 11) > 0.62, x: h(Math.floor(s / 6) * 3 + i * 17) * 1920 + 6 * Math.sin(s * 1.7 + i), a: 0.18 + 0.22 * h(s * 7 + i) }));
  return (
    <>
      <GraoFino />
      <svg width="1920" height="1080" style={{ position: "absolute", inset: 0 }}>
        {riscos.filter((r) => r.on).map((r, i) => <line key={i} x1={r.x} y1={0} x2={r.x + 4} y2={1080} stroke="#FFF8E8" strokeWidth={1.6} opacity={r.a} />)}
      </svg>
      <AbsoluteFill style={{ background: "#FFF3D6", mixBlendMode: "soft-light", opacity: 0.05 + 0.06 * h(s * 3) }} />
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 62%, rgba(20,14,8,0.32) 100%)" }} />
    </>
  );
};

const OPCOES: [string, React.FC][] = [
  ["0 · limpa: sem nada por cima (só para comparar)", () => null],
  ["1 · a de agora: grão + bolinhas de poeira", () => <Grao />],
  ["2 · grão bem fino e fraco, sem bolinhas", GraoFino],
  ["3 · papel de desenho: textura parada, não mexe", () => <Papel />],
  ["4 · luz de cinema: luz quente que passa devagar", Luz],
  ["5 · filme antigo: grão fino + riscos finos de vez em quando", Riscos],
  ["6 · papel + luz de cinema (a minha aposta)", () => <><Papel forca={0.8} /><Luz /></>],
];
export const FIM_PREVIA_TEXTURAS = OPCOES.length * DUR;
const IMG = "v02/img/m07-a-tiao-sandra-supermercado-fila-caixa-os-dois-com-cestinha-rindo-juntos.jpg";

export const PreviaTexturas: React.FC = () => {
  const t = useCurrentFrame() / 30;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {OPCOES.map(([rot, Efeito], k) => (
        <Sequence key={k} from={k * DUR * 30} durationInFrames={DUR * 30}>
          <AbsoluteFill style={{ overflow: "hidden" }}>
            <Img src={staticFile(IMG)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.04 * cl((t - k * DUR) / DUR)})` }} />
          </AbsoluteFill>
          <Efeito />
          <div style={{ position: "absolute", left: 40, bottom: 40, padding: "10px 22px", borderRadius: 14, background: "rgba(20,16,12,0.72)", color: "#FFF6DC", fontFamily, fontSize: 36 }}>{rot}</div>
        </Sequence>
      ))}
      <Audio src={staticFile("v02/trilha.mp3")} volume={0.12} />
    </AbsoluteFill>
  );
};
