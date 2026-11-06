// Reacoes "de filme" por cima de imagem e video: emocao do personagem, brilho, X vermelho, check verde, dinheiro voando.
// Ed (05/11): "quando se fala que a picape aparece brilhando, aparece uma estrelinha e o som de estrela... sons e icones de
// sentimentos e emocoes, isso gera muito engajamento. Quero que seja igual um filme de Hollywood."
// Cada reacao toca o seu som no instante em que aparece. Posicao x,y em % da tela (sempre longe do rosto).
import React from "react";
import { COR, flutua, m, Pos, useT } from "./kit";
import { Emoji, Som, somDoEmoji } from "./vivo";

const NEG = new Set(["😰", "😩", "😬", "😞", "😔", "😓", "😒", "😮‍💨", "😳", "🤨", "😤", "🚨", "⚠️", "💔", "📉", "😱", "💥"]);

// emocao: emoji grande que salta, balanca e tem um aro que pulsa atras
export const Reacao: React.FC<Pos & { e: string; ini?: number; tam?: number }> = ({ x, y, e, ini = 0.6, tam = 300 }) => {
  const t = useT(); const s = m(t, ini, "estalo");
  if (t < ini) return null;
  const aro = Math.min(1, (t - ini) / 0.6);
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) scale(${s}) rotate(${flutua(t, 6, 2.2)}deg) translateY(${flutua(t, 8, 1.8)}px)` }}>
      <Som nome={somDoEmoji(e)} em={ini} />
      <div style={{ position: "absolute", left: "50%", top: "50%", width: tam * 1.3, height: tam * 1.3, marginLeft: -tam * 0.65, marginTop: -tam * 0.65, borderRadius: 999,
        border: `8px solid ${NEG.has(e) ? COR.vermelho : COR.amarelo}`, opacity: 0.8 * (1 - aro), transform: `scale(${0.6 + 0.7 * aro})` }} />
      {e === "💔" && <Som nome="thud" em={ini + 0.75} />}
      <div style={{ filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.35))" }}><Emoji e={e} tam={tam} desde={ini} /></div>
    </div>
  );
};

// brilho: 4 estrelinhas de 4 pontas que piscam em volta de um ponto (som de estrela)
const Estrela: React.FC<{ tam: number; cor?: string }> = ({ tam, cor = "#FFF6C8" }) => (
  <svg width={tam} height={tam} viewBox="-50 -50 100 100" style={{ filter: "drop-shadow(0 0 18px rgba(255,230,140,1)) drop-shadow(0 0 6px rgba(255,255,255,0.9))" }}>
    <path d="M0,-50 C6,-10 10,-6 50,0 C10,6 6,10 0,50 C-6,10 -10,6 -50,0 C-10,-6 -6,-10 0,-50 Z" fill={cor} stroke="#E8A800" strokeWidth={3} />
  </svg>
);
export const Brilho: React.FC<Pos & { ini?: number }> = ({ x, y, ini = 0.6 }) => {
  const t = useT(); if (t < ini) return null;
  const pts = [[0, 0, 230, 0], [-150, -120, 140, 0.18], [150, -150, 110, 0.33], [130, 110, 160, 0.5], [-130, 120, 90, 0.62]];
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%` }}>
      <Som nome="sparkle" em={ini} vol={0.45} /><Som nome="sparkle" em={ini + 0.45} vol={0.3} />
      {pts.map(([dx, dy, tam, atraso], i) => {
        const tt = t - ini - atraso; if (tt < 0) return null;
        const entra = Math.min(1, tt / 0.2), pisca = entra * (0.75 + 0.25 * Math.sin(tt * 7 + i * 1.3));
        return <div key={i} style={{ position: "absolute", left: dx, top: dy, transform: `translate(-50%,-50%) scale(${pisca}) rotate(${tt * 70}deg)` }}><Estrela tam={tam} /></div>;
      })}
    </div>
  );
};

// X vermelho que se desenha, com tremida e som de alerta
export const Xis: React.FC<Pos & { ini?: number; tam?: number }> = ({ x, y, ini = 0.6, tam = 240 }) => {
  const t = useT(); if (t < ini) return null;
  const a = Math.min(1, (t - ini) / 0.16), b = Math.min(1, Math.max(0, (t - ini - 0.14) / 0.16)), treme = (t - ini) < 0.4 ? Math.sin((t - ini) * 80) * 6 * (1 - (t - ini) / 0.4) : 0;
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) translateX(${treme}px) scale(${1 + 0.15 * (1 - a)})` }}>
      <Som nome="warning" em={ini} vol={0.4} /><Som nome="thud" em={ini + 0.14} />
      <svg width={tam} height={tam} viewBox="0 0 100 100" style={{ filter: "drop-shadow(0 8px 14px rgba(0,0,0,0.4))" }}>
        <circle cx={50} cy={50} r={46} fill="#FFFDF8" stroke="#1F1B16" strokeWidth={6} opacity={a} />
        <line x1={28} y1={28} x2={28 + 44 * a} y2={28 + 44 * a} stroke={COR.vermelho} strokeWidth={13} strokeLinecap="round" />
        {b > 0 && <line x1={72} y1={28} x2={72 - 44 * b} y2={28 + 44 * b} stroke={COR.vermelho} strokeWidth={13} strokeLinecap="round" />}
      </svg>
    </div>
  );
};

// check verde que se desenha, com sino
export const Check: React.FC<Pos & { ini?: number; tam?: number }> = ({ x, y, ini = 0.6, tam = 220 }) => {
  const t = useT(); if (t < ini) return null;
  const e = m(t, ini, "estalo"), d = Math.min(1, Math.max(0, (t - ini - 0.1) / 0.3));
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) scale(${e}) translateY(${flutua(t, 5)}px)` }}>
      <Som nome="ding" em={ini} vol={0.45} /><Som nome="sparkle" em={ini + 0.25} vol={0.25} />
      <svg width={tam} height={tam} viewBox="0 0 100 100" style={{ filter: "drop-shadow(0 8px 14px rgba(0,0,0,0.35))" }}>
        <circle cx={50} cy={50} r={46} fill={COR.verde} stroke="#1F1B16" strokeWidth={6} />
        <polyline points="27,52 43,67 74,34" fill="none" stroke="#FFFDF8" strokeWidth={12} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={80} strokeDashoffset={80 * (1 - d)} />
      </svg>
    </div>
  );
};

// dinheiro voando embora (3 notas que sobem e somem)
export const Voa: React.FC<Pos & { ini?: number }> = ({ x, y, ini = 0.6 }) => {
  const t = useT(); if (t < ini) return null;
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%` }}>
      <Som nome="money" em={ini} /><Som nome="slide" em={ini + 0.3} vol={0.25} />
      {[0, 0.25, 0.5].map((atraso, i) => {
        const tt = t - ini - atraso; if (tt < 0) return null;
        const p = Math.min(1, tt / 1.6);
        return <div key={i} style={{ position: "absolute", transform: `translate(${-80 + i * 70 + p * (180 + i * 60)}px, ${-p * (420 + i * 80)}px) rotate(${p * (40 - i * 30)}deg)`, opacity: 1 - p * p }}><Emoji e="💸" tam={150} /></div>;
      })}
    </div>
  );
};

// tremida de camera (para os sustos): deslocamento em px no instante t
export const tremor = (t: number, quando: number[]) => {
  let dx = 0, dy = 0;
  for (const q of quando) { const tt = t - q; if (tt >= 0 && tt < 0.45) { const f = 1 - tt / 0.45; dx += Math.sin(tt * 90) * 14 * f; dy += Math.cos(tt * 70) * 10 * f; } }
  return [dx, dy];
};
