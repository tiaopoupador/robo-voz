import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { TiaoCorpo, CORPO_BASE, TiaoPose } from "./TiaoReal";
const caixa = (l: number, t: number, w: number, h: number): React.CSSProperties => ({ position: "absolute", left: l, top: t, width: w, height: h });
export const ProvaBoneco: React.FC = () => (
  <AbsoluteFill>
    <Img src={staticFile("piloto-motion/cozinha.jpg")} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
    <div style={caixa(40, 330, 290, 727)}><TiaoCorpo alt={727} p={CORPO_BASE} /></div>
    <div style={caixa(340, 330, 290, 727)}><TiaoCorpo alt={727} p={{ ...CORPO_BASE, boca: 0.8, espanto: 1, sobr: 1, bracoE: 25, bracoD: -25 }} /></div>
    <div style={caixa(640, 330, 290, 727)}><TiaoCorpo alt={727} p={{ ...CORPO_BASE, piscar: 1, pernaE: 12, pernaD: -12, bracoE: -10, bracoD: -10, cabeca: 5, boca: 0.4 }} /></div>
    <div style={caixa(940, 300, 420, 607)}><TiaoPose pose="explica" piscar={0} boca={0.5} /></div>
    <div style={caixa(1300, 300, 350, 602)}><TiaoPose pose="aponta" piscar={0} boca={0} /></div>
    <div style={caixa(1560, 300, 450, 605)}><TiaoPose pose="alerta" piscar={1} boca={0.7} /></div>
  </AbsoluteFill>
);
