// Cena "Tião conversa" (Ed, 11/11/2026): o jeito do Prosa que Rende (524 mil views em 11 dias) com o nosso personagem.
// Fundo de paisagem com zoom bem lento e escurecido, o Tião PARADO de um lado (só respira), as ondas do som da voz
// subindo e descendo embaixo e a frase da fala grande do outro lado (a legenda, em modo grande, no Video.tsx).
// Serve para a playlist "Tião Conversa" inteira e, no vídeo longo, para trocar algumas imagens nos trechos de conselho.
import React, { createContext, useContext } from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { mola } from "../mola";

export const ONDA_HZ = 15;                       // o montar.py mede o volume da voz 15 vezes por segundo
export const OndaCtx = createContext<number[]>([]);
const BARRAS = 34;

// barras que seguem o volume da voz: cada barra tem a sua fase, para parecer um espectro de verdade
export const Ondas: React.FC<{ t: number; larg?: number; alt?: number; cor?: string }> = ({ t, larg = 620, alt = 150, cor = "white" }) => {
  const onda = useContext(OndaCtx);
  const v = (tt: number) => { const i = tt * ONDA_HZ, a = Math.floor(i), b = a + 1, f = i - a; return (onda[a] ?? 0) * (1 - f) + (onda[b] ?? 0) * f; };
  const passo = larg / BARRAS;
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: passo * 0.38, height: alt }}>
      {Array.from({ length: BARRAS }, (_, k) => {
        const fase = Math.sin(k * 12.9898) * 43758.5453, r = fase - Math.floor(fase);            // aleatório fixo por barra
        const nivel = v(t - r * 0.12) * (0.45 + 0.55 * Math.abs(Math.sin(t * (5 + r * 7) + k)));
        const h = Math.max(6, Math.min(1, nivel * 1.6) * alt * (0.55 + 0.45 * Math.sin((k / BARRAS) * Math.PI)));
        return <div key={k} style={{ width: passo * 0.62, height: h, background: cor, borderRadius: 4, opacity: 0.92 }} />;
      })}
    </div>
  );
};

export const Conversa: React.FC<{ fundo: string; pose: string; t0: number; dur: number; lado?: 1 | -1 }> = ({ fundo, pose, t0, dur, lado = 1 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const z = 1.04 + 0.07 * (t / Math.max(1, dur));                     // zoom lento do fundo
  const entra = mola(t, 6, 1);
  const resp = 1 + 0.006 * Math.sin(t * 1.7);                          // o Tião só respira
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#0b0f16" }}>
      <Img src={staticFile(fundo)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${z})`, filter: "saturate(1.05)" }} />
      <AbsoluteFill style={{ background: lado > 0 ? "linear-gradient(90deg, rgba(5,8,14,0.15) 0%, rgba(5,8,14,0.55) 55%, rgba(5,8,14,0.7) 100%)"
                                               : "linear-gradient(270deg, rgba(5,8,14,0.15) 0%, rgba(5,8,14,0.55) 55%, rgba(5,8,14,0.7) 100%)" }} />
      <Img src={staticFile(pose)} style={{ position: "absolute", bottom: 0, [lado > 0 ? "left" : "right"]: 40, height: "92%",
        transform: `translateY(${(1 - entra) * 60}px) scale(${resp})`, transformOrigin: "50% 100%", filter: "drop-shadow(0 18px 40px rgba(0,0,0,0.55))" }} />
      <div style={{ position: "absolute", bottom: 60, [lado > 0 ? "right" : "left"]: 110 }}><Ondas t={t0 + t} /></div>
    </AbsoluteFill>
  );
};
