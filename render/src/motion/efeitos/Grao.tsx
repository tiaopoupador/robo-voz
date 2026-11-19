// Camada de grao de filme + poeira por cima das cenas desenhadas (Ed, 18/11/2026, visto no Tuco Investe: «uma camada tipo
// uns chuviscos em toda a tela, isso da mais dinamica»). Tudo sai do quadro (seek(t) puro): o mesmo quadro da sempre o mesmo grao.
import React from "react";
import { AbsoluteFill, useCurrentFrame } from "remotion";

const h = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };

export const Grao: React.FC<{ forca?: number }> = ({ forca = 1 }) => {
  const f = useCurrentFrame();
  const semente = Math.floor(f / 2); // o grao troca a cada 2 quadros (15 por segundo), como pelicula
  const pontos = Array.from({ length: 26 }, (_, i) => {
    const k = semente * 31 + i * 7;
    return { x: h(k) * 1920, y: h(k + 1) * 1080, r: 1.5 + h(k + 2) * 4.2, claro: h(k + 3) > 0.45, vis: h(k + 4) > 0.25 };
  });
  const fio = h(semente * 13) > 0.6 ? { x: h(semente * 17) * 1920, y: h(semente * 19) * 1080, a: h(semente * 23) * 180 } : null;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <svg width="1920" height="1080" style={{ position: "absolute", inset: 0, mixBlendMode: "overlay", opacity: 0.74 * forca }}>
        <filter id={`g${semente}`} x="0" y="0" width="100%" height="100%">
          <feTurbulence type="fractalNoise" baseFrequency="0.55" numOctaves={2} seed={semente % 997} stitchTiles="stitch" />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="1920" height="1080" filter={`url(#g${semente})`} />
      </svg>
      <svg width="1920" height="1080" style={{ position: "absolute", inset: 0, opacity: 0.8 * forca }}>
        {pontos.filter((p) => p.vis).map((p, i) => <circle key={i} cx={p.x} cy={p.y} r={p.r} fill={p.claro ? "#FFF8E8" : "#2A241D"} opacity={0.7} />)}
        {fio && <path d={`M ${fio.x} ${fio.y} q 14 -10 30 -2 t 26 8`} transform={`rotate(${fio.a} ${fio.x} ${fio.y})`} stroke="#FFF8E8" strokeWidth={1.4} fill="none" opacity={0.6} />}
      </svg>
      {/* luz de projetor: o brilho oscila de leve a cada 2 quadros */}
      <AbsoluteFill style={{ background: "#FFF3D6", mixBlendMode: "soft-light", opacity: (0.05 + 0.07 * h(semente * 3)) * forca }} />
      {/* vinheta suave nas bordas */}
      <AbsoluteFill style={{ background: "radial-gradient(ellipse at center, rgba(0,0,0,0) 62%, rgba(20,14,8,0.34) 100%)", opacity: forca }} />
    </AbsoluteFill>
  );
};
