// Prova da luz do cenario no personagem (19/11/2026): a mesma cena de noite, 3 jeitos lado a lado:
// sem luz (como era), noite (azulada) e varanda (noite + a lampada amarela da direita).
// O fundo de noite aqui e a rua da SUV escurecida (o cenario de noite de verdade o Ed ainda esta a gerar no meta.ai).
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame } from "remotion";
import { Pose, Sombra, Luz } from "./Turma";

const MODOS: (Luz | undefined)[] = [undefined, { tipo: "noite" }, { tipo: "varanda", lado: 1 }];
const NOMES = ["SEM LUZ (antes)", "NOITE", "NOITE + LÂMPADA"];

const Cena: React.FC<{ luz?: Luz; t: number }> = ({ luz, t }) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <Img src={staticFile("piloto-motion/suv-casa.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover", transform: "scale(1.5)", transformOrigin: "50% 70%", filter: "brightness(0.38) saturate(0.6) hue-rotate(195deg) blur(3px)" }} />
    {/* a lampada da varanda, na direita */}
    <div style={{ position: "absolute", right: -260, top: 120, width: 900, height: 900, borderRadius: "50%", background: "radial-gradient(circle, rgba(255,190,100,0.55), rgba(255,170,80,0) 65%)" }} />
    <Sombra x={960} y={1255} larg={520} />
    <Pose pid="valeria" cod="P09" x={960} y={1260} alt={1250} t={t} luz={luz} />
  </AbsoluteFill>
);

export const ProvaLuz: React.FC = () => {
  const t = useCurrentFrame() / 30;
  return (
    <AbsoluteFill style={{ background: "#000", flexDirection: "row" }}>
      {MODOS.map((m, i) => (
        <div key={i} style={{ position: "relative", width: 640, height: 1080, overflow: "hidden", borderRight: i < 2 ? "4px solid #000" : undefined }}>
          <div style={{ position: "absolute", left: -640, top: 0, width: 1920, height: 1080 }}><Cena luz={m} t={t} /></div>
          <div style={{ position: "absolute", left: 0, right: 0, bottom: 40, textAlign: "center", color: "#fff", font: "800 44px sans-serif", textShadow: "0 3px 8px #000" }}>{NOMES[i]}</div>
        </div>
      ))}
    </AbsoluteFill>
  );
};
