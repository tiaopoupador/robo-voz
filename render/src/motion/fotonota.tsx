// Captura por FOTO da notinha (Ed, 08/11/2026: «fala que tira uma foto da notinha, mas mostra uma captura por voz (...)
// se nao tiver a imagem da captura tem que ser feito, faca!»). No mesmo jeito escuro da tela "Capturar por voz" do FinMoovi:
// o celular enquadra a notinha, bate a foto (flash e clique), a linha verde le de cima a baixo, e do lado aparece
// item por item, o total e o lancamento em "Mercado".
import React from "react";
import { AbsoluteFill } from "remotion";
import { flutua, fontFamily, m, reais, useT } from "./kit";
import { Som } from "./vivo";

const ROXO = "#8B5CF6", VERDE = "#22C55E", LARANJA = "#F97316", CINZA = "#9CA3AF";
const f = (tam: number, cor = "#FFFFFF", peso = 800): React.CSSProperties => ({ fontFamily, fontWeight: peso, fontSize: tam, color: cor, lineHeight: 1.1 });

export const FotoNota: React.FC<{ itens: [string, number][]; total: number; categoria?: string }> = ({ itens, total, categoria = "Mercado" }) => {
  const t = useT();
  const FOTO = 1.0, LER = 1.25, PASSO = 0.38;
  const fimItens = LER + 0.5 + itens.length * PASSO, TOT = fimItens + 0.2, LANCA = TOT + 0.7;
  const eCel = m(t, 0.05, "cartao"), flash = Math.max(0, 1 - Math.abs(t - FOTO - 0.06) / 0.18);
  const scan = Math.min(1, Math.max(0, (t - LER) / (itens.length * PASSO + 0.4)));
  const pontos = Array.from({ length: 26 }, (_, i) => ({ x: (i * 397) % 1920, y: (i * 233) % 1080, r: 2 + (i % 3), v: 0.4 + (i % 5) * 0.15 }));
  return (
    <AbsoluteFill style={{ background: "#0B0C16", overflow: "hidden" }}>
      <AbsoluteFill style={{ background: "radial-gradient(circle at 12% 40%, #0E4A4A88, transparent 45%), radial-gradient(circle at 88% 60%, #4A1E5A88, transparent 45%)" }} />
      {pontos.map((p, i) => <div key={i} style={{ position: "absolute", left: p.x, top: (p.y - t * 18 * p.v + 1080) % 1080, width: p.r * 2, height: p.r * 2, borderRadius: 9, background: i % 2 ? "#2DD4BF55" : "#F472B655" }} />)}
      <Som nome="slide" em={0.05} />
      {/* titulo */}
      <div style={{ position: "absolute", top: 60, left: 0, right: 0, textAlign: "center", opacity: Math.min(1, m(t, 0.1) * 1.5) }}>
        <div style={f(84)}>Capturar por foto</div>
        <div style={{ ...f(38, CINZA, 600), marginTop: 6 }}>FinMoovi Quick</div>
      </div>
      {/* celular com a camera */}
      <div style={{ position: "absolute", left: 300, top: 250, width: 440, height: 780, borderRadius: 56, background: "#111827", border: "10px solid #1F2937",
        boxShadow: "0 0 80px #8B5CF655", transform: `translateY(${(1 - eCel) * 500 + flutua(t, 4)}px) rotate(${-2 + flutua(t, 0.6, 0.8)}deg)`, overflow: "hidden" }}>
        <div style={{ position: "absolute", inset: 0, background: "linear-gradient(180deg, #5B4636, #3E2F24)" }} />
        {/* a notinha */}
        <div style={{ position: "absolute", left: 70, top: 90, width: 280, height: 560, background: "#FFFDF5", transform: "rotate(-3deg)", boxShadow: "0 18px 30px #0008",
          clipPath: "polygon(0 0,100% 0,100% 97%,92% 100%,84% 97%,76% 100%,68% 97%,60% 100%,52% 97%,44% 100%,36% 97%,28% 100%,20% 97%,12% 100%,4% 97%,0 100%)" }}>
          <div style={{ margin: "26px auto 18px", width: 150, height: 14, borderRadius: 7, background: "#D1D5DB" }} />
          {itens.map((_, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", margin: "0 24px 22px" }}>
              <div style={{ width: 120 + (i * 37) % 50, height: 11, borderRadius: 6, background: "#9CA3AF" }} />
              <div style={{ width: 52, height: 11, borderRadius: 6, background: "#6B7280" }} />
            </div>
          ))}
          <div style={{ margin: "30px 24px 0", height: 4, background: "#D1D5DB" }} />
          <div style={{ display: "flex", justifyContent: "space-between", margin: "20px 24px" }}>
            <div style={{ width: 90, height: 16, borderRadius: 8, background: "#374151" }} />
            <div style={{ width: 70, height: 16, borderRadius: 8, background: "#374151" }} />
          </div>
        </div>
        {/* moldura da camera */}
        {[[40, 60, "0 0"], [360, 60, "0 1"], [40, 660, "1 0"], [360, 660, "1 1"]].map(([x, y, q], i) => {
          const [b, r] = String(q).split(" ").map(Number);
          return <div key={i} style={{ position: "absolute", left: x as number, top: y as number, width: 40, height: 40, borderColor: "#FFFFFF", borderStyle: "solid",
            borderWidth: `${b ? 0 : 6}px ${r ? 6 : 0}px ${b ? 6 : 0}px ${r ? 0 : 6}px`, borderRadius: 6 }} />;
        })}
        {/* a linha que le */}
        {t > LER && scan < 1 && <div style={{ position: "absolute", left: 50, right: 50, top: 90 + scan * 560, height: 6, borderRadius: 3, background: VERDE, boxShadow: `0 0 30px ${VERDE}` }} />}
        {/* botao da camera */}
        <div style={{ position: "absolute", left: 175, bottom: 28, width: 70, height: 70, borderRadius: 99, background: LARANJA, border: "6px solid #fff",
          transform: `scale(${t > FOTO - 0.1 && t < FOTO + 0.2 ? 0.82 : 1})` }} />
        <AbsoluteFill style={{ background: "#FFFFFF", opacity: flash }} />
      </div>
      <Som nome="click" em={FOTO} />
      {/* o que ele leu */}
      <div style={{ position: "absolute", left: 860, top: 250, width: 820 }}>
        <div style={{ ...f(40, "#A78BFA", 700), opacity: t > LER ? 1 : 0, marginBottom: 18 }}>{scan < 1 ? "Lendo a notinha..." : "Notinha lida, item por item"}</div>
        {itens.map(([nome, v], i) => {
          const d = LER + 0.5 + i * PASSO, e = m(t, d, "estalo");
          return (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", alignItems: "center", background: "#161827", border: "2px solid #2A2D45", borderRadius: 18,
              padding: "12px 26px", marginBottom: 12, opacity: t < d ? 0 : 1, transform: `translateX(${(1 - e) * 160}px)` }}>
              <Som nome="pop" em={d} vol={0.25} />
              <span style={f(40, "#E5E7EB", 700)}>{nome}</span><span style={f(40, "#FFFFFF")}>{reais(v, 2)}</span>
            </div>
          );
        })}
        <div style={{ display: "flex", justifyContent: "space-between", padding: "14px 26px", marginTop: 6, borderTop: `3px solid ${ROXO}`,
          opacity: t < TOT ? 0 : 1, transform: `scale(${0.8 + 0.2 * m(t, TOT, "estalo")})`, transformOrigin: "left" }}>
          <span style={f(52)}>Total</span><span style={f(52, "#FFFFFF")}>{reais(total, 2)}</span>
        </div>
        <div style={{ display: "inline-flex", alignItems: "center", gap: 14, marginTop: 18, background: "#0F2A1C", border: `3px solid ${VERDE}`, borderRadius: 99, padding: "10px 30px",
          opacity: t < LANCA ? 0 : 1, transform: `scale(${m(t, LANCA, "estalo")})`, transformOrigin: "left" }}>
          <Som nome="kaching" em={LANCA} />
          <span style={f(42, VERDE)}>✓ lançado em {categoria}</span>
        </div>
      </div>
    </AbsoluteFill>
  );
};
