// Kit de motion, parte 2: pecas acrescentadas para montar o video 01 inteiro. Servem para todos os videos.
import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import { caixa, COR, Destacado, flutua, fontFamily, Fundo, LINHA, m, Pos, sombra, tempoDoDestaque, txt, useT } from "./kit";
import { Emoji, Som } from "./vivo";

// 8. ICONES em fichas (emoji + rotulo); risca = um X vermelho passa por cima
export const Icones: React.FC<{ titulo?: string; itens: { e: string; r: string; risca?: boolean }[] }> = ({ titulo, itens }) => {
  const t = useT();
  return (
    <Fundo>
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 70 }}>
        {titulo && <div style={{ ...txt(76), opacity: m(t, 0), transform: `translateY(${(1 - m(t, 0)) * -30}px)`, textAlign: "center", maxWidth: 1600 }}>{titulo}</div>}
        <div style={{ display: "flex", gap: 60 }}>
          {itens.map((it, i) => {
            const d = 0.3 + i * 0.35, e = m(t, d, "estalo"), x = it.risca ? Math.min(1, Math.max(0, (t - d - 0.7) / 0.35)) : 0;
            return (
              <div key={i} style={{ ...caixa(), width: 400, padding: "34px 20px 34px", textAlign: "center", position: "relative", transform: `scale(${e}) rotate(${(i % 2 ? 2 : -2) * e}deg) translateY(${flutua(t + i, 6)}px)` }}>
                <Som nome="pop" em={d} />
                {it.risca && <Som nome="thud" em={d + 0.75} />}
                <div style={{ position: "relative", width: 200, height: 200, margin: "0 auto" }}>
                  <Emoji e={it.e} tam={200} />
                  {x > 0 && <svg viewBox="0 0 100 100" style={{ position: "absolute", inset: -10, width: 220, height: 220 }}>
                  <line x1="8" y1="8" x2={8 + 84 * Math.min(1, x * 2)} y2={8 + 84 * Math.min(1, x * 2)} stroke={COR.vermelho} strokeWidth="9" strokeLinecap="round" />
                  {x > 0.5 && <line x1="92" y1="8" x2={92 - 84 * (x - 0.5) * 2} y2={8 + 84 * (x - 0.5) * 2} stroke={COR.vermelho} strokeWidth="9" strokeLinecap="round" />}
                  </svg>}
                </div>
                <div style={{ ...txt(50, it.risca && x > 0.5 ? COR.cinza : COR.tinta), marginTop: 14, textDecoration: it.risca && x > 0.9 ? "line-through" : "none", textDecorationColor: COR.vermelho, textDecorationThickness: 5 }}>{it.r}</div>
              </div>
            );
          })}
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 9. GRAFICO de linhas que se desenham
export const Grafico: React.FC<{ titulo?: string; series: { r: string; cor: string; pts: number[] }[]; fim?: string; eixo?: string[] }> = ({ titulo, series, fim, eixo }) => {
  const t = useT();
  const W = 1400, H = 520, max = Math.max(...series.flatMap((s) => s.pts)) * 1.12;
  const p = Math.min(1, Math.max(0, (t - 0.4) / 2.0));
  return (
    <Fundo>
      <Som nome="slide" em={0} />
      {series.map((s, k) => <Som key={k} nome={s.pts[s.pts.length - 1] >= s.pts[0] ? "growth" : "slide"} em={0.4 + k * 0.15} />)}
      {fim && <Som nome="kaching" em={2.5} />}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30 }}>
        {titulo && <div style={{ ...txt(66), opacity: m(t, 0), textAlign: "center", maxWidth: 1600 }}>{titulo}</div>}
        <div style={{ ...caixa(), padding: "50px 60px 30px", transform: `translateY(${(1 - m(t, 0)) * 300}px)` }}>
          <svg width={W} height={H} style={{ overflow: "visible" }}>
            {[0.25, 0.5, 0.75, 1].map((g) => <line key={g} x1={0} x2={W} y1={H - g * H} y2={H - g * H} stroke={`${COR.tinta}22`} strokeWidth={3} />)}
            <line x1={0} x2={W} y1={H} y2={H} stroke={COR.tinta} strokeWidth={6} />
            {series.map((s, k) => {
              const n = s.pts.length - 1, ate = p * n, ult = Math.min(n, Math.floor(ate)), fr = ate - ult;
              const xy = (i: number, v: number) => [(i / n) * W, H - (v / max) * H];
              const pts = s.pts.slice(0, ult + 1).map((v, i) => xy(i, v));
              if (ult < n) { const a = s.pts[ult], b = s.pts[ult + 1]; pts.push(xy(ult + fr, a + (b - a) * fr)); }
              const q = pts[pts.length - 1];
              return (
                <g key={k}>
                  <polyline points={pts.map((z) => z.join(",")).join(" ")} fill="none" stroke={s.cor} strokeWidth={14} strokeLinejoin="round" strokeLinecap="round" />
                  <circle cx={q[0]} cy={q[1]} r={18 + 4 * Math.sin(t * 6)} fill={s.cor} stroke={COR.tinta} strokeWidth={6} />
                  <text x={q[0] > W - 360 ? q[0] - 30 : q[0] + 30} y={q[1] - 28 + k * 76} textAnchor={q[0] > W - 360 ? "end" : "start"} fontFamily={fontFamily} fontWeight={800} fontSize={44} fill={s.cor}>{s.r}</text>
                </g>
              );
            })}
          </svg>
          {eixo && <div style={{ display: "flex", justifyContent: "space-between", marginTop: 14 }}>{eixo.map((e, i) => <span key={i} style={txt(36, COR.cinza, 600)}>{e}</span>)}</div>}
        </div>
        {fim && <div style={{ ...txt(96, COR.verde), opacity: t > 2.5 ? m(t, 2.5, "estalo") : 0 }}>{fim}</div>}
      </AbsoluteFill>
    </Fundo>
  );
};

// 10. CELULAR desenhado com uma lista (extrato); destaque = linhas que acendem; apaga = elas somem depois
export const Celular: React.FC<{ titulo?: string; linhas: { r: string; v: string; pos?: boolean }[]; destaque?: number[]; apaga?: boolean; lado?: string }> = ({ titulo, linhas, destaque = [], apaga, lado }) => {
  const t = useT();
  const acende = Math.min(1, Math.max(0, (t - 1.4) / 0.4)), some = apaga ? Math.min(1, Math.max(0, (t - 2.4) / 0.8)) : 0;
  return (
    <Fundo>
      <Som nome="slide" em={0} />
      {destaque.length > 0 && <Som nome="ding" em={1.4} />}
      {apaga && <Som nome="slide" em={2.4} />}
      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "center", gap: 90 }}>
        <div style={{ width: 560, height: 960, borderRadius: 70, background: COR.tinta, padding: 22, boxShadow: sombra(14), transform: `translateY(${(1 - m(t, 0)) * 900}px) rotate(${-3 + 3 * m(t, 0)}deg)` }}>
          <div style={{ width: "100%", height: "100%", borderRadius: 52, background: COR.branco, padding: "60px 30px", overflow: "hidden" }}>
            <div style={{ ...txt(46), marginBottom: 24 }}>{titulo ?? "Extrato"}</div>
            {linhas.map((l, i) => {
              const e = m(t, 0.4 + i * 0.12), d = destaque.includes(i);
              return (
                <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "16px 14px", borderRadius: 14, marginBottom: 6,
                  background: d ? `rgba(242,182,50,${acende * (1 - some)})` : "transparent", opacity: Math.min(1, e * 2) * (d ? 1 - 0.85 * some : 1), transform: `translateX(${(1 - e) * 60}px)` }}>
                  <span style={txt(34, COR.tinta, 600)}>{l.r}</span>
                  <span style={txt(34, l.pos ? COR.verde : COR.vermelho)}>{l.v}</span>
                </div>
              );
            })}
          </div>
        </div>
        {lado && <div style={{ maxWidth: 760 }}><Destacado texto={lado} t={t} ini={0.8} tam={84} /></div>}
      </AbsoluteFill>
    </Fundo>
  );
};

// 11. PIZZA (rosca) com uma fatia que cresce ate pct
export const Pizza: React.FC<{ pct: number; r: string; titulo?: string }> = ({ pct, r, titulo }) => {
  const t = useT();
  const p = Math.min(1, Math.max(0, (t - 0.4) / 1.3)), ease = 1 - Math.pow(1 - p, 3), a = (pct / 100) * ease;
  const R = 280, C = 2 * Math.PI * R;
  return (
    <Fundo>
      <Som nome="pop" em={0} /><Som nome="growth" em={0.4} /><Som nome="warning" em={1.7} />
      <AbsoluteFill style={{ flexDirection: "row", justifyContent: "center", alignItems: "center", gap: 110 }}>
        <svg width={760} height={760} viewBox="-380 -380 760 760" style={{ transform: `scale(${m(t, 0, "estalo")})` }}>
          <circle r={R} fill="none" stroke={COR.papel2} strokeWidth={150} />
          <circle r={R} fill="none" stroke={COR.vermelho} strokeWidth={150} strokeDasharray={`${C * a} ${C}`} transform="rotate(-90)" />
          <circle r={R + 75} fill="none" stroke={COR.tinta} strokeWidth={7} />
          <circle r={R - 75} fill="none" stroke={COR.tinta} strokeWidth={7} />
          <text textAnchor="middle" dy={50} fontFamily={fontFamily} fontWeight={800} fontSize={140} fill={COR.tinta}>{Math.round(pct * ease)}%</text>
        </svg>
        <div style={{ maxWidth: 720 }}>
          {titulo && <div style={{ ...txt(50, COR.cinza, 600), marginBottom: 18, opacity: m(t, 0.2) }}>{titulo}</div>}
          <div style={{ ...txt(84), opacity: m(t, 1.2), transform: `translateY(${(1 - m(t, 1.2)) * 40}px)` }}>{r}</div>
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 12. PESSOAS: bonequinhos; os "verm" primeiros ficam vermelhos, os "verde" ultimos ficam verdes
export const Pessoas: React.FC<{ titulo: string; total?: number; verm?: number; verde?: number }> = ({ titulo, total = 40, verm = 0, verde = 0 }) => {
  const t = useT();
  return (
    <Fundo>
      <Som nome="pop" em={0.2} /><Som nome={verm > verde ? "warning" : "ding"} em={1.4} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
        <div style={{ ...txt(78), opacity: m(t, 0), textAlign: "center", maxWidth: 1600 }}>{titulo}</div>
        <div style={{ display: "grid", gridTemplateColumns: "repeat(10, 110px)", gap: 24 }}>
          {Array.from({ length: total }, (_, i) => {
            const e = m(t, 0.2 + i * 0.025, "estalo"), pinta = t > 1.4 + i * 0.03;
            const cor = i < verm ? COR.vermelho : i >= total - verde ? COR.verde : COR.cinza;
            return (
              <svg key={i} width={110} height={140} viewBox="0 0 120 150" style={{ transform: `scale(${e}) translateY(${Math.sin(t * 3 + i * 0.7) * 4}px)` }}>
                <circle cx={60} cy={36} r={28} fill={pinta ? cor : COR.branco} stroke={COR.tinta} strokeWidth={6} />
                <path d="M14 146 Q14 76 60 76 Q106 76 106 146 Z" fill={pinta ? cor : COR.branco} stroke={COR.tinta} strokeWidth={6} />
              </svg>
            );
          })}
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 13. BALANCA: o lado mais pesado desce
export const Balanca: React.FC<{ esq: string; dir: string; pesa: "esq" | "dir"; titulo?: string }> = ({ esq, dir, pesa, titulo }) => {
  const t = useT();
  const ang = (pesa === "esq" ? -1 : 1) * (11 * m(t, 0.8, "cartao") + 1.2 * Math.sin(t * 2)), rad = (ang * Math.PI) / 180;
  const prato = (r: string, lado: number) => (
    <div style={{ position: "absolute", left: 700 + lado * 500 * Math.cos(rad) - 230, top: 420 + lado * Math.sin(rad) * 500, width: 460, textAlign: "center" }}>
      <div style={{ width: 5, height: 110, background: COR.tinta, margin: "0 auto" }} />
      <div style={{ ...caixa(lado < 0 ? COR.amarelo : COR.branco), ...txt(58), padding: "26px 20px" }}>{r}</div>
    </div>
  );
  return (
    <Fundo>
      <Som nome="slide" em={0.1} /><Som nome="thud" em={1.2} />
      {titulo && <div style={{ ...txt(76), position: "absolute", top: 90, width: "100%", textAlign: "center", opacity: m(t, 0) }}>{titulo}</div>}
      <div style={{ position: "absolute", left: 260, top: 130, width: 1400, height: 900, transform: `scale(${m(t, 0.1)})` }}>
        <div style={{ position: "absolute", left: 685, top: 420, width: 30, height: 420, background: COR.tinta, borderRadius: 10 }} />
        <div style={{ position: "absolute", left: 560, top: 820, width: 280, height: 40, background: COR.tinta, borderRadius: 14 }} />
        <div style={{ position: "absolute", left: 180, top: 404, width: 1040, height: 32, background: COR.tinta, borderRadius: 16, transform: `rotate(${ang}deg)` }} />
        <div style={{ position: "absolute", left: 670, top: 390, width: 60, height: 60, borderRadius: 99, background: COR.amarelo, border: `${LINHA}px solid ${COR.tinta}` }} />
        {prato(esq, -1)}{prato(dir, 1)}
      </div>
    </Fundo>
  );
};

// 14. TELA DIVIDIDA: duas imagens lado a lado com rotulo
export const Divide: React.FC<{ a: { src: string; r: string }; b: { src: string; r: string }; titulo?: string }> = ({ a, b, titulo }) => {
  const t = useT();
  const lado = (x: { src: string; r: string }, i: number) => {
    const e = m(t, 0.1 + i * 0.25);
    return (
      <div style={{ ...caixa(), width: 860, height: 640, overflow: "hidden", position: "relative", transform: `translateY(${(1 - e) * (i ? 700 : -700)}px) rotate(${i ? 1.5 : -1.5}deg)` }}>
        <Img src={staticFile(x.src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.04 * Math.min(1, t / 5)})` }} />
        <div style={{ ...txt(50), position: "absolute", left: 24, bottom: 24, background: COR.branco, border: `5px solid ${COR.tinta}`, borderRadius: 14, padding: "6px 22px" }}>{x.r}</div>
      </div>
    );
  };
  return (
    <Fundo>
      <Som nome="slide" em={0.1} /><Som nome="slide" em={0.35} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 }}>
        {titulo && <div style={{ ...txt(72), opacity: m(t, 0.5) }}>{titulo}</div>}
        <div style={{ display: "flex", gap: 60 }}>{lado(a, 0)}{lado(b, 1)}</div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 15. BOTAO de like ou inscrever, com o dedo que clica
export const Botao: React.FC<{ tipo: "like" | "inscrever"; texto?: string }> = ({ tipo, texto }) => {
  const t = useT();
  const chega = m(t, 0.3, "cartao"), ligado = t > 1.25, pulo = t > 1.2 ? 1 + 0.18 * Math.sin(Math.min(1, (t - 1.2) / 0.3) * Math.PI) : 1;
  const nome = tipo === "like" ? (ligado ? "Curtido" : "Curtir") : ligado ? "Inscrito" : "Inscrever-se";
  return (
    <Fundo>
      <Som nome="pop" em={0} /><Som nome="click" em={1.2} /><Som nome="sparkle" em={1.3} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 70 }}>
        <div style={{ ...caixa(ligado ? (tipo === "like" ? COR.azul : COR.vermelho) : COR.branco), ...txt(110, ligado ? COR.branco : COR.tinta), padding: "30px 80px", display: "flex", alignItems: "center", gap: 36, transform: `scale(${m(t, 0, "estalo") * pulo})` }}>
          <Emoji e={tipo === "like" ? "👍" : "🔔"} tam={140} />{nome}
        </div>
        {texto && <div style={{ maxWidth: 1500, opacity: m(t, 1.4) }}><Destacado texto={texto} t={t} ini={1.4} tam={66} /></div>}
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 1180 + (1 - chega) * 500, top: 470 + (1 - chega) * 400, transform: `scale(${t > 1.2 && t < 1.45 ? 0.85 : 1})` }}><Emoji e="👆" tam={150} /></div>
    </Fundo>
  );
};

// 16. TORRE de parcelas: blocos caem um em cima do outro e a torre balanca
export const Torre: React.FC<{ itens: string[]; titulo?: string }> = ({ itens, titulo }) => {
  const t = useT();
  const bal = Math.sin(t * 3) * Math.min(4, Math.max(0, t - 0.5 - itens.length * 0.45) * 3);
  return (
    <Fundo>
      {itens.map((_, i) => <Som key={i} nome="thud" em={0.4 + i * 0.45 + 0.15} />)}
      <Som nome="warning" em={0.6 + itens.length * 0.45} />
      {titulo && <div style={{ ...txt(76), position: "absolute", top: 80, width: "100%", textAlign: "center", opacity: m(t, 0) }}>{titulo}</div>}
      <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 80 }}>
        <div style={{ display: "flex", flexDirection: "column-reverse", alignItems: "center", transformOrigin: "50% 100%", transform: `rotate(${bal}deg)` }}>
          {itens.map((r, i) => {
            const e = m(t, 0.4 + i * 0.45, "estalo");
            return <div key={i} style={{ ...caixa(i % 2 ? COR.vermelho : COR.amarelo), ...txt(54, i % 2 ? COR.branco : COR.tinta), width: 720 - i * 30, padding: "22px 0", textAlign: "center", marginTop: -4,
              transform: `translateY(${(1 - e) * -900}px) rotate(${i % 2 ? 1.5 : -1.5}deg)`, opacity: t < 0.4 + i * 0.45 ? 0 : 1 }}>{r}</div>;
          })}
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 17. GRADE de quadradinhos que enchem (parcelas, meses, dias); ate = para no meio
export const Grade: React.FC<{ total: number; cols?: number; titulo?: string; ate?: number; cor?: string; rotuloFim?: string; corFim?: string }> = ({ total, cols = 12, titulo, ate, cor = COR.vermelho, rotuloFim, corFim = COR.tinta }) => {
  const t = useT();
  const lim = ate ?? total, dur = 2.0, cheio = Math.floor(Math.min(1, Math.max(0, (t - 0.4) / dur)) * lim);
  const tam = Math.min(110, Math.floor(1500 / cols) - 14);
  return (
    <Fundo>
      {Array.from({ length: 10 }, (_, i) => <Som key={i} nome="clock" em={0.4 + (i * dur) / 10} vol={0.22} />)}
      {rotuloFim && <Som nome={corFim === COR.vermelho ? "warning" : corFim === COR.verde ? "kaching" : "ding"} em={0.4 + dur} />}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 46 }}>
        {titulo && <div style={{ ...txt(70), opacity: m(t, 0), textAlign: "center", maxWidth: 1600 }}>{titulo}</div>}
        <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, ${tam}px)`, gap: 14 }}>
          {Array.from({ length: total }, (_, i) => (
            <div key={i} style={{ height: tam * 0.8, borderRadius: 12, border: `5px solid ${COR.tinta}`, background: i < cheio ? cor : COR.branco, transform: `scale(${i === cheio - 1 ? 1.15 : 1})` }} />
          ))}
        </div>
        {rotuloFim && <div style={{ ...txt(66, corFim), opacity: t > 0.4 + dur ? m(t, 0.4 + dur, "estalo") : 0 }}>{rotuloFim}</div>}
      </AbsoluteFill>
    </Fundo>
  );
};

// ---------- mais coisas por cima de imagem ----------
// Placa: caixa com texto que salta (numero, rotulo)
export const Placa: React.FC<Pos & { texto: string; cor?: string; fundo?: string; ini?: number; tam?: number }> = ({ x, y, texto, cor = COR.tinta, fundo = COR.branco, ini = 0.5, tam = 92 }) => {
  const t = useT(); const e = m(t, ini, "estalo");
  const som = cor === COR.verde ? "kaching" : cor === COR.vermelho ? "card" : "pop";
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) scale(${e}) rotate(${-2 * e}deg) translateY(${flutua(t, 3)}px)` }}>
      <Som nome={som} em={ini} />
      <div style={{ ...caixa(fundo), ...txt(tam, cor), padding: "14px 42px", whiteSpace: "nowrap" }}>{texto}</div>
    </div>
  );
};
// Frase no alto da imagem, numa faixa
export const FraseTopo: React.FC<{ texto: string; ini?: number; pos?: "topo" | "esq" | "dir" }> = ({ texto, ini = 0.4, pos = "topo" }) => {
  const t = useT(); const e = m(t, ini); const td = tempoDoDestaque(texto, ini + 0.15);
  const lado = pos !== "topo";
  const onde: React.CSSProperties = lado
    ? { position: "absolute", top: "14%", [pos === "esq" ? "left" : "right"]: 60, width: 640, transform: `translateX(${(1 - e) * (pos === "esq" ? -800 : 800)}px) translateY(${flutua(t, 3)}px)` }
    : { position: "absolute", top: 56, left: 0, right: 0, display: "flex", justifyContent: "center", transform: `translateY(${(1 - e) * -260}px)` };
  return (
    <div style={onde}>
      <Som nome="pop" em={ini} />{td !== null && <Som nome="sparkle" em={td} vol={0.25} />}
      <div style={{ ...caixa(), padding: lado ? "26px 34px" : "22px 54px", maxWidth: 1700 }}><Destacado texto={texto} t={t} ini={ini + 0.15} tam={lado ? 64 : 76} /></div>
    </div>
  );
};
// Lista: papeizinhos que entram um a um; riscar = risca o ultimo
export const Lista: React.FC<Pos & { itens: string[]; riscar?: boolean; ini?: number }> = ({ x, y, itens, riscar, ini = 0.4 }) => {
  const t = useT();
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: "translate(-50%,-50%)", display: "flex", flexDirection: "column", gap: 18, alignItems: "flex-start" }}>
      {itens.map((r, i) => {
        const d = ini + i * 0.45, e = m(t, d, "estalo"), rs = riscar && i === itens.length - 1 ? Math.min(1, Math.max(0, (t - d - 0.7) / 0.4)) : 0;
        return (
          <div key={i} style={{ ...caixa(i % 2 ? COR.amarelo : COR.branco), ...txt(56), padding: "10px 34px", position: "relative", whiteSpace: "nowrap", transform: `translateX(${(1 - e) * 300}px) rotate(${i % 2 ? 1.5 : -1.5}deg) translateY(${flutua(t + i, 3)}px)`, opacity: t < d ? 0 : 1 }}>
            <Som nome="pop" em={d} />{riscar && i === itens.length - 1 && <Som nome="card" em={d + 0.7} />}
            {r}
            {rs > 0 && <div style={{ position: "absolute", left: 20, top: "48%", height: 10, width: `calc(${rs * 100}% - 40px)`, background: COR.vermelho, borderRadius: 5 }} />}
          </div>
        );
      })}
    </div>
  );
};
// Trinca no vidro: linhas que correm do ponto de impacto
export const Trinca: React.FC<Pos & { ini?: number }> = ({ x, y, ini = 1.2 }) => {
  const t = useT(); const p = Math.min(1, Math.max(0, (t - ini) / 0.35));
  const raios = [[-60, -30], [40, -70], [90, 10], [50, 80], [-40, 90], [-100, 30], [10, -100]];
  const x0 = (x / 100) * 1920, y0 = (y / 100) * 1080;
  return (
    <svg style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }} viewBox="0 0 1920 1080">
      <Som nome="boom" em={ini} />
      {raios.map(([dx, dy], i) => (
        <polyline key={i} fill="none" stroke="#fff" strokeWidth={7} strokeLinejoin="round"
          points={`${x0},${y0} ${x0 + dx * 2 * p},${y0 + dy * 2 * p} ${x0 + dx * 4 * p + dy * 0.6 * p},${y0 + dy * 4 * p - dx * 0.4 * p} ${x0 + dx * 6.5 * p},${y0 + dy * 6.5 * p}`} />
      ))}
    </svg>
  );
};
