// Prova da luz numa cena que mexe (19/11/2026): 23h40, a rua apagada, só a lâmpada da varanda do Tião acesa (à direita).
// A Valéria chega andando, olha para os lados, e pede os cinquenta reais (balão, opção A). Os dois recebem a luz da lâmpada:
// o Tião, perto dela, bem aceso; a Valéria, mais longe, mais fraco. O fundo de noite é a rua da SUV escurecida (o de verdade vem do meta.ai).
import React from "react";
import { AbsoluteFill, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { Pose, Sombra, Balao } from "./Turma";

const FPS = 30;
export const FIM_CENA_NOITE = 10;
const Fundo: React.FC<{ t: number; zoom?: number; fx?: number }> = ({ t, zoom = 1, fx = 50 }) => (
  <AbsoluteFill style={{ overflow: "hidden", background: "#0b1020" }}>
    <Img src={staticFile("piloto-motion/suv-casa.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", transformOrigin: `${fx}% 70%`, transform: `scale(${zoom * (1.02 + 0.03 * Math.min(1, t / 6))})`, filter: "brightness(0.36) saturate(0.55) hue-rotate(195deg)" + (zoom > 1 ? " blur(3px)" : "") }} />
    {/* a lâmpada da varanda (à direita) e a luz que ela espalha */}
    <div style={{ position: "absolute", right: -380, top: 40, width: 1200, height: 1200, borderRadius: "50%", background: "radial-gradient(circle, rgba(255,190,100,0.5), rgba(255,170,80,0.12) 45%, rgba(255,170,80,0) 68%)", opacity: 0.92 + 0.08 * Math.sin(t * 13) * Math.sin(t * 7) }} />
  </AbsoluteFill>
);
// a boca de leve, no ritmo das palavras do balão (sem voz nesta prova)
const silabas = (t: number, ini: number, dur: number) => t < ini || t > ini + dur ? 0 : 0.45 * Math.abs(Math.sin((t - ini) * Math.PI * 4.2));

const Chega: React.FC = () => {
  const t = useCurrentFrame() / FPS;
  return (
    <AbsoluteFill>
      <Fundo t={t} />
      {/* parada ao lado do carro, com os óculos na cabeça (a pose de andar tem os óculos no rosto: pularia de um plano para o outro) */}
      <Sombra x={1010} y={1010} larg={240} />
      <Pose pid="valeria" cod="R1" x={1010} y={1015} alt={600} t={t} entra={0.3} luz={{ tipo: "varanda", lado: 1, forca: 0.55 }} />
    </AbsoluteFill>
  );
};
const Pede: React.FC = () => {
  const t = useCurrentFrame() / FPS; const pede = t > 2.0;
  return (
    <AbsoluteFill>
      <Fundo t={t} zoom={1.5} fx={58} />
      <Sombra x={1480} y={1250} larg={440} />
      <Pose pid="tiao" cod={t < 3.4 ? "P05" : "P14"} x={1480} y={1290} alt={1040} t={t} entra={t < 3.4 ? 0.2 : 3.4} luz={{ tipo: "varanda", lado: 1 }} />
      <Sombra x={600} y={1250} larg={420} />
      <Pose pid="valeria" cod={pede ? "P10" : "P04"} x={600} y={1290} alt={1060} t={t} entra={pede ? 2.0 : 0} luz={{ tipo: "varanda", lado: 1, forca: 0.7 }}
        fala={pede ? silabas(t, 2.2, 2.6) : undefined} />
      {pede && <Balao texto="Tião... você me empresta cinquenta reais até sexta?" x={330} y={28} larg={1060} t={t} ini={2.2} dur={2.6} rabo={[800, 560]} />}
    </AbsoluteFill>
  );
};

export const ProvaCenaNoite: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    <Sequence durationInFrames={Math.round(3.6 * FPS)}><Chega /></Sequence>
    <Sequence from={Math.round(3.6 * FPS)}><Pede /></Sequence>
  </AbsoluteFill>
);
