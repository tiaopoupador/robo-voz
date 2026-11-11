// Barra de recados estilo telejornal (Ed, 11/11/2026: «uma barra embaixo mostrando várias informações (...) umas 5 vezes
// por vídeo (...) quanto mais se pede pra se inscrever, curtir, mais a audiência faz»).
// Sobe da base com mola, o selo vermelho "PLANTÃO DO TIÃO" pisca, o texto corre da direita para a esquerda e a barra desce.
// Tudo é função do tempo (seek puro). Som: um "slide" ao subir e um "ding" leve quando o selo acende.
import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola } from "../mola";
import { Emoji, Som } from "./vivo";

const { fontFamily } = loadFont("normal", { weights: ["700", "800"] });
export const PLANTAO_ALTURA = 84;      // a legenda sobe isto quando a barra está na tela
export const PLANTAO_VEL = 210;        // px por segundo do texto correndo
export const PLANTAO_CHAR = 23;        // largura média de uma letra (px), para o montar.py calcular a duração
const AZUL = "#0E1A2B", VERMELHO = "#D62828", AMARELO = "#FFD43B";

export type Acao = "inscrever" | "like" | "comentar" | "finmoovi" | "compartilhar" | "fim" | "";
export const Plantao: React.FC<{ frases: string[]; dur: number; acoes?: Acao[] }> = ({ frases, dur, acoes = [] }) => {
  const f = useCurrentFrame(); const { fps, width } = useVideoConfig(); const t = f / fps;
  const sobe = mola(t, 11, 0.78), desce = mola(t - (dur - 0.7), 11, 1);
  const y = (1 - sobe + desce) * (PLANTAO_ALTURA + 30);
  const selo = mola(t - 0.35, 16, 0.6);                       // o selo estala depois da barra
  const pisca = 0.55 + 0.45 * Math.abs(Math.sin(t * Math.PI * 1.6));
  const x = width - Math.max(0, t - 0.9) * PLANTAO_VEL;     // o texto começa a correr quando a barra assentou
  // cada frase entra na tela em t_k; o cartão animado da ação dela vive de t_k até a próxima (Ed, 11/11: «colocar uma animação nesses pedidos»)
  const limpa = (p: string) => p.replace(/\*/g, "");
  const ent: number[] = []; let off = 0;
  frases.forEach((p, i) => { ent.push(0.9 + off / PLANTAO_VEL + 0.4); off += limpa(p).length * PLANTAO_CHAR + 90; });
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", pointerEvents: "none" }}>
      {acoes.map((a, i) => {
        const de = ent[i], ate = Math.min(i + 1 < ent.length ? ent[i + 1] : dur, dur - 0.5);
        return a && t >= de - 0.05 && t < ate + 0.5 ? <CartaoAcao key={i} acao={a} t={t - de} dur={ate - de} /> : null;
      })}
      <Som nome="slide" em={0} vol={0.28} />
      <Som nome="ding" em={0.4} vol={0.22} />
      <div style={{ height: PLANTAO_ALTURA, transform: `translateY(${y}px)`, position: "relative", overflow: "hidden",
        background: AZUL, borderTop: `5px solid ${AMARELO}`, boxShadow: "0 -8px 24px rgba(0,0,0,0.35)" }}>
        <div style={{ position: "absolute", left: 0, top: "50%", whiteSpace: "nowrap", transform: `translate(${x}px,-50%)`,
          fontFamily, fontWeight: 700, fontSize: 40, color: "white", letterSpacing: 0.3 }}>
          {frases.map((p, i) => (
            <span key={i}>
              {i > 0 && <span style={{ color: AMARELO, margin: "0 34px" }}>◆</span>}
              {p.split(/(\*[^*]+\*)/g).filter(Boolean).map((q, j) =>
                q.startsWith("*") ? <span key={j} style={{ color: AMARELO, fontWeight: 800 }}>{q.slice(1, -1)}</span> : <span key={j}>{q}</span>)}
            </span>
          ))}
        </div>
        <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, display: "flex", alignItems: "center", gap: 14, padding: "0 30px 0 26px",
          background: VERMELHO, transform: `translateX(${(selo - 1) * 420}px)`, boxShadow: `12px 0 18px ${AZUL}` }}>
          <div style={{ width: 16, height: 16, borderRadius: 8, background: "white", opacity: pisca }} />
          <div style={{ fontFamily, fontWeight: 800, fontSize: 34, color: "white", letterSpacing: 1.5 }}>PLANTÃO DO TIÃO</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- o cartão animado acima da barra, no canto direito ----------
const Cursor: React.FC<{ x: number; y: number; aperta: number }> = ({ x, y, aperta }) => (
  <svg width="54" height="64" viewBox="0 0 27 32" style={{ position: "absolute", left: x, top: y, transform: `scale(${1 - 0.18 * aperta})`, filter: "drop-shadow(0 4px 6px rgba(0,0,0,0.4))" }}>
    <path d="M2 2 L2 26 L8.5 20 L13 30 L17.5 28 L13 18.5 L22 18.5 Z" fill="white" stroke="#111" strokeWidth="2" strokeLinejoin="round" />
  </svg>
);
const CartaoAcao: React.FC<{ acao: Acao; t: number; dur: number }> = ({ acao, t, dur }) => {
  
  const entra = mola(t, 13, 0.62), sai = mola(t - dur, 13, 1), s = Math.max(0, entra - sai);
  const bate = Math.sin(t * Math.PI * 2.2) * 0.04;          // respira sempre: nada parado
  const caixa: React.CSSProperties = { position: "absolute", right: 56, bottom: PLANTAO_ALTURA + 26, transformOrigin: "100% 100%",
    transform: `scale(${s * (1 + bate)}) translateY(${(1 - s) * 40}px)`, opacity: Math.min(1, s * 1.5) };
  const clique = 1.5;                                        // o cursor chega e clica aqui
  const cx = (1 - mola(t - 0.4, 9, 0.9)) * 260, ap = t > clique && t < clique + 0.18 ? 1 : 0, feito = t >= clique;
  const bal = { background: "white", borderRadius: 26, border: "5px solid #1F1B16", boxShadow: "10px 10px 0 #1F1B16", padding: "18px 26px",
    display: "flex", alignItems: "center", gap: 18, fontFamily, fontWeight: 800 } as React.CSSProperties;
  if (acao === "inscrever") return (
    <div style={caixa}>
      <Som nome="click" em={clique} vol={0.45} /><Som nome="ding" em={clique + 0.15} vol={0.35} />
      <div style={{ ...bal, padding: "16px 20px", position: "relative" }}>
        <div style={{ background: feito ? "#E9E9E9" : "#E62117", color: feito ? "#333" : "white", borderRadius: 40, padding: "14px 30px", fontSize: 38,
          transform: `scale(${1 - 0.1 * ap})` }}>{feito ? "INSCRITO ✓" : "INSCREVER-SE"}</div>
        <div style={{ transform: `rotate(${feito ? Math.sin((t - clique) * 28) * 22 * Math.exp(-(t - clique) * 2.2) : 0}deg)`, transformOrigin: "50% 10%" }}>
          <Emoji e="🔔" tam={78} />
        </div>
        <Cursor x={150 + cx} y={52 + cx * 0.4} aperta={ap} />
      </div>
    </div>
  );
  if (acao === "like") return (
    <div style={caixa}>
      <Som nome="pop" em={0.5} vol={0.4} /><Som nome="sparkle" em={0.9} vol={0.3} />
      <div style={bal}>
        <div style={{ transform: `scale(${0.8 + 0.35 * mola(t - 0.5, 18, 0.45)}) rotate(${-12 * Math.sin(t * 5) * Math.exp(-t)}deg)` }}><Emoji e="👍" tam={110} /></div>
        <div style={{ fontSize: 44, color: "#1F1B16" }}>Deixe o<br /><span style={{ color: "#1565C0" }}>seu like</span></div>
        <div style={{ position: "absolute", right: 22, top: -44 + -40 * Math.min(1, Math.max(0, t - 0.9)), opacity: Math.max(0, 1 - Math.max(0, t - 1.6)), fontSize: 46, color: "#1565C0" }}>+1</div>
      </div>
    </div>
  );
  if (acao === "comentar") {
    const msg = "Eu já passei por isso!", n = Math.max(0, Math.min(msg.length, Math.floor((t - 0.9) * 16)));
    return (
      <div style={caixa}>
        <Som nome="keyboard" em={0.9} vol={0.25} />
        <div style={{ ...bal, flexDirection: "column", alignItems: "flex-start", gap: 8, borderRadius: "26px 26px 26px 6px" }}>
          <div style={{ fontSize: 26, color: "#8A8073" }}>💬 comentário</div>
          <div style={{ fontSize: 40, color: "#1F1B16", minWidth: 430 }}>
            {t < 0.9 ? [0, 1, 2].map((k) => <span key={k} style={{ opacity: 0.3 + 0.7 * Math.abs(Math.sin(t * 6 - k)) }}>● </span>) : msg.slice(0, n)}
            {t >= 0.9 && n < msg.length && <span style={{ opacity: Math.round(t * 3) % 2 }}>|</span>}
          </div>
        </div>
      </div>
    );
  }
  if (acao === "finmoovi") return (
    <div style={caixa}>
      <Som nome="kaching" em={0.7} vol={0.3} />
      <div style={bal}>
        <Emoji e="📈" tam={96} />
        <div><div style={{ fontSize: 50, color: "#1F1B16" }}>FinMoovi</div>
          <div style={{ fontSize: 30, color: "white", background: "#2E9E5B", borderRadius: 14, padding: "4px 14px", marginTop: 6,
            transform: `scale(${mola(t - 0.7, 18, 0.5)})`, transformOrigin: "0 50%" }}>7 dias de teste ✓</div></div>
      </div>
    </div>
  );
  if (acao === "compartilhar") {
    const voa = Math.min(1, Math.max(0, (t - 0.8) / 1.2));
    return (
      <div style={caixa}>
        <Som nome="slide" em={0.8} vol={0.35} />
        <div style={{ ...bal, position: "relative", overflow: "visible" }}>
          <div style={{ fontSize: 42, color: "#1F1B16" }}>Mande para<br /><span style={{ color: "#D62828" }}>quem precisa</span></div>
          <div style={{ transform: `translate(${voa * 160}px, ${-voa * 120}px) rotate(${-voa * 20}deg)`, opacity: 1 - Math.max(0, voa - 0.8) * 5 }}><Emoji e="✈️" tam={90} /></div>
        </div>
      </div>
    );
  }
  if (acao === "fim") return (
    <div style={caixa}>
      <Som nome="clock" em={0.4} vol={0.25} />
      <div style={bal}>
        <div style={{ transform: `rotate(${(t * 90) % 360 < 180 ? 0 : 180}deg)` }}><Emoji e="⏳" tam={90} /></div>
        <div style={{ fontSize: 42, color: "#1F1B16" }}>Fique até<br /><span style={{ color: "#D62828" }}>o fim</span></div>
      </div>
    </div>
  );
  return null;
};
