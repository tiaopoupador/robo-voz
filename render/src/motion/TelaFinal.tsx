// Tela final (10 s) de todos os videos do canal: escura, dourada, com o Tiao acenando.
// Os dois quadros da direita e o circulo de inscricao sao os lugares onde o YouTube Studio poe a "tela final"
// (video recomendado, playlist, botao de inscrever). Posicoes no padrao do YouTube para 1920x1080.
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { fontFamily, m, useT } from "./kit";
import { Som } from "./vivo";

const OURO = "#F2C14E", OURO2 = "#FFE7A3", NOITE = "#0B1020";
const brilho = (t: number, ini: number, vel = 0.9) => ((t - ini) * vel) % 2.4; // posicao da faixa de luz que passa

export const TelaFinal: React.FC = () => {
  const t = useT();
  const fundo = m(t, 0, "lenta"), tiao = m(t, 0.35, "cartao"), nome = m(t, 0.9, "cartao"), sub = m(t, 1.4), q1 = m(t, 1.8, "cartao"), q2 = m(t, 2.1, "cartao"), anel = m(t, 2.5, "estalo");
  const sai = t > 9.2 ? Math.max(0, 1 - (t - 9.2) / 0.8) : 1;
  const quadro = (x: number, y: number, e: number, rotulo: string, k: number) => {
    const b = brilho(t, 2.4 + k * 0.4, 0.7);
    return (
      <div style={{ position: "absolute", left: x, top: y, width: 500, height: 281, borderRadius: 26, transform: `translateY(${(1 - e) * 120}px) scale(${0.9 + 0.1 * e})`, opacity: e,
        background: "linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02))", border: `3px solid ${OURO}`, boxShadow: `0 30px 80px rgba(0,0,0,0.55), 0 0 ${30 + 14 * Math.sin(t * 2 + k)}px rgba(242,193,78,0.25)`, overflow: "hidden" }}>
        <div style={{ position: "absolute", top: -60, bottom: -60, width: 140, left: `${-30 + b * 60}%`, background: "linear-gradient(90deg, transparent, rgba(255,231,163,0.22), transparent)", transform: "rotate(18deg)" }} />
        <div style={{ position: "absolute", left: 28, bottom: 22, fontFamily, fontWeight: 800, fontSize: 36, color: OURO2, letterSpacing: 1 }}>{rotulo}</div>
        <div style={{ position: "absolute", right: 26, top: 22, width: 66, height: 66, borderRadius: 99, border: `3px solid ${OURO}`, display: "flex", alignItems: "center", justifyContent: "center" }}>
          <div style={{ width: 0, height: 0, borderTop: "15px solid transparent", borderBottom: "15px solid transparent", borderLeft: `24px solid ${OURO}`, marginLeft: 6 }} />
        </div>
      </div>
    );
  };
  return (
    <AbsoluteFill style={{ background: NOITE, overflow: "hidden", opacity: sai }}>
      <Som nome="sparkle" em={0.3} /><Som nome="ding" em={0.95} /><Som nome="pop" em={1.85} /><Som nome="pop" em={2.15} /><Som nome="sparkle" em={2.6} />
      {/* luz de fundo que respira */}
      <AbsoluteFill style={{ background: `radial-gradient(1100px 760px at ${30 + 4 * Math.sin(t * 0.5)}% 55%, rgba(242,193,78,${0.20 * fundo}), transparent 70%), radial-gradient(900px 600px at 85% 20%, rgba(80,110,200,${0.18 * fundo}), transparent 70%)` }} />
      {/* poeira dourada subindo devagar */}
      {Array.from({ length: 36 }, (_, i) => {
        const x = (i * 137.5) % 100, vel = 18 + (i % 7) * 6, y = 110 - (((t + i * 1.7) * vel) % 130), tam = 3 + (i % 4) * 2;
        return <div key={i} style={{ position: "absolute", left: `${x}%`, top: `${y}%`, width: tam, height: tam, borderRadius: 99, background: OURO2, opacity: (0.15 + (i % 5) * 0.08) * fundo, filter: "blur(0.5px)" }} />;
      })}
      {/* linhas douradas finas que se desenham */}
      <svg style={{ position: "absolute", inset: 0 }} width={1920} height={1080}>
        <line x1={80} y1={980} x2={80 + 1760 * Math.min(1, t / 1.6)} y2={980} stroke={OURO} strokeWidth={2} opacity={0.5} />
        <line x1={1840} y1={100} x2={1840 - 1760 * Math.min(1, Math.max(0, t - 0.3) / 1.6)} y2={100} stroke={OURO} strokeWidth={2} opacity={0.5} />
      </svg>
      {/* o Tiao acenando, num pedestal de luz */}
      <div style={{ position: "absolute", left: 150, bottom: 70, width: 560, height: 240, borderRadius: "50%", background: "radial-gradient(closest-side, rgba(242,193,78,0.35), transparent)", opacity: tiao }} />
      <Img src={staticFile("marca/tiao-acenando.png")} style={{ position: "absolute", left: 210, bottom: 120, height: 820, transformOrigin: "50% 100%",
        transform: `translateY(${(1 - tiao) * 600 + Math.sin(t * 1.8) * 6}px) rotate(${Math.sin(t * 1.2) * 1.2}deg)`, filter: "drop-shadow(0 30px 40px rgba(0,0,0,0.5))" }} />
      {/* nome do canal com brilho que passa */}
      <div style={{ position: "absolute", left: 790, top: 150, transform: `translateY(${(1 - nome) * 60}px)`, opacity: nome }}>
        <div style={{ fontFamily, fontWeight: 600, fontSize: 38, color: OURO, letterSpacing: 10, textTransform: "uppercase" }}>obrigado por assistir</div>
        <div style={{ position: "relative", fontFamily, fontWeight: 800, fontSize: 132, lineHeight: 1, marginTop: 6,
          backgroundImage: `linear-gradient(100deg, ${OURO} 0%, ${OURO2} ${20 + ((t * 30) % 140)}%, ${OURO} ${40 + ((t * 30) % 140)}%)`, WebkitBackgroundClip: "text", color: "transparent" }}>Tião Poupador</div>
        <div style={{ fontFamily, fontWeight: 600, fontSize: 44, color: "#E9E4D8", marginTop: 14, opacity: sub, transform: `translateY(${(1 - sub) * 20}px)` }}>Toda semana, uma história nova sobre dinheiro.</div>
      </div>
      {quadro(790, 470, q1, "Assista agora", 0)}
      {quadro(1330, 470, q2, "Próxima história", 1)}
      {/* lugar do botao de inscrever (circulo) */}
      <div style={{ position: "absolute", left: 1225, top: 790, width: 170, height: 170, borderRadius: 999, border: `4px solid ${OURO}`, transform: `scale(${anel * (1 + 0.03 * Math.sin(t * 3))})`,
        boxShadow: `0 0 ${40 + 20 * Math.sin(t * 3)}px rgba(242,193,78,0.35)`, display: "flex", alignItems: "center", justifyContent: "center", textAlign: "center" }}>
        <div style={{ fontFamily, fontWeight: 800, fontSize: 25, color: OURO2, lineHeight: 1.1 }}>Inscreva-se</div>
      </div>
    </AbsoluteFill>
  );
};
