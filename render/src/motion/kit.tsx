// Kit de motion graphics do Tiao Poupador. Serve para TODOS os videos do canal.
// Cada peca enche a tela (1920x1080), comeca no quadro 0 da sua Sequence e anima sozinha.
// Estilo: papel creme, contorno preto grosso e sombra dura (igual ao desenho), mola em tudo.
// Cada animacao toca o seu som no mesmo instante (Som) e pode levar um emoji animado (Emoji).
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola, MOLAS } from "../mola";
import { Emoji, Som } from "./vivo";

export const { fontFamily } = loadFont("normal", { weights: ["600", "800"] });
export const COR = {
  papel: "#F4EBDD", papel2: "#EADFCB", tinta: "#1F1B16", amarelo: "#F2B632", vermelho: "#D9443A",
  verde: "#2E9E5B", azul: "#3B6EA8", cinza: "#8A8175", branco: "#FFFDF8",
};
export const LINHA = 7; // espessura do contorno
export const sombra = (n = 12) => `${n}px ${n}px 0 ${COR.tinta}`;
export const caixa = (fundo: string = COR.branco): React.CSSProperties => ({
  background: fundo, border: `${LINHA}px solid ${COR.tinta}`, borderRadius: 26, boxShadow: sombra(),
});
export const txt = (tam: number, cor: string = COR.tinta, peso = 800): React.CSSProperties => ({ fontFamily, fontWeight: peso, fontSize: tam, color: cor, lineHeight: 1.05 });

export const useT = () => { const f = useCurrentFrame(); const { fps } = useVideoConfig(); return f / fps; };
export const m = (t: number, ini: number, tipo: keyof typeof MOLAS = "cartao") => { const [w, z] = MOLAS[tipo]; return mola(t - ini, w, z); };
export const flutua = (t: number, amp = 6, vel = 1.6) => Math.sin(t * vel) * amp; // movimento leve continuo (nada fica parado)
export const reais = (v: number, casas = 0) =>
  (v < 0 ? "-" : "") + "R$ " + Math.abs(v).toLocaleString("pt-BR", { minimumFractionDigits: casas, maximumFractionDigits: casas });

// Fundo de papel com pontinhos (nunca liso)
export const Fundo: React.FC<{ cor?: string; children?: React.ReactNode }> = ({ cor = COR.papel, children }) => {
  const t = useT();
  return (
    <AbsoluteFill style={{ background: cor, overflow: "hidden" }}>
      <AbsoluteFill style={{
        backgroundImage: `radial-gradient(${COR.tinta}22 2.2px, transparent 2.6px)`, backgroundSize: "46px 46px",
        transform: `translate(${-t * 6}px, ${-t * 4}px) scale(1.06)`,
      }} />
      {children}
    </AbsoluteFill>
  );
};

// Texto com *destaque*: o destaque ganha marca-texto que corre por tras. Pontuacao fica colada na palavra.
const SEP = "§§";
export const Destacado: React.FC<{ texto: string; t: number; ini: number; tam: number; cor?: string; marca?: string }> = ({ texto, t, ini, tam, cor = COR.tinta, marca = COR.amarelo }) => {
  const brutas = texto.split(/(\*[^*]+\*|\s+)/g).filter((p) => p && !/^\s+$/.test(p));
  const palavras: string[] = [];
  brutas.forEach((p) => { if (/^[.,!?:;]+$/.test(p) && palavras.length) palavras[palavras.length - 1] += SEP + p; else palavras.push(p); });
  return (
    <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: `0 ${tam * 0.28}px`, maxWidth: 1600 }}>
      {palavras.map((p, i) => {
        const [pal, pont = ""] = p.split(SEP); const d = ini + i * 0.11, e = m(t, d, "estalo"), forte = pal.startsWith("*");
        const corre = Math.min(1, Math.max(0, (t - d - 0.18) / 0.35));
        return (
          <span key={i} style={{ position: "relative", display: "inline-block", transform: `translateY(${(1 - e) * 40}px) scale(${0.6 + 0.4 * e})`, opacity: Math.min(1, e * 2) }}>
            {forte && <span style={{ position: "absolute", left: -10, right: -10, top: "34%", bottom: "4%", background: marca, borderRadius: 10, transform: `scaleX(${corre})`, transformOrigin: "left", zIndex: 0 }} />}
            <span style={{ ...txt(tam, cor), position: "relative" }}>{forte ? pal.slice(1, -1) : pal}</span>{pont && <span style={{ ...txt(tam, cor), position: "relative" }}>{pont}</span>}
          </span>
        );
      })}
    </div>
  );
};
export const tempoDoDestaque = (texto: string, ini: number) => {
  const pal = texto.split(/(\*[^*]+\*|\s+)/g).filter((p) => p && !/^\s+$/.test(p) && !/^[.,!?:;]+$/.test(p));
  const i = pal.findIndex((p) => p.startsWith("*")); return i < 0 ? null : ini + i * 0.11 + 0.2;
};

// 1. FRASE grande, palavra por palavra (com emoji animado opcional)
export const Frase: React.FC<{ texto: string; sobre?: string; escuro?: boolean; emoji?: string }> = ({ texto, sobre, escuro, emoji }) => {
  const t = useT(); const td = tempoDoDestaque(texto, 0.15);
  return (
    <Fundo cor={escuro ? COR.tinta : COR.papel}>
      <Som nome={escuro ? "boom" : "pop"} em={0.12} />
      {td !== null && <Som nome="sparkle" em={td} vol={0.25} />}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30, padding: 120, transform: `translateY(${flutua(t, 4, 1.2)}px)` }}>
        {emoji && <Emoji e={emoji} tam={210} estilo={{ transform: `scale(${m(t, 0, "estalo")}) rotate(${flutua(t, 4, 2)}deg)` }} />}
        {sobre && <div style={{ ...txt(44, escuro ? COR.amarelo : COR.cinza, 600), opacity: m(t, 0), letterSpacing: 2, textTransform: "uppercase" }}>{sobre}</div>}
        <Destacado texto={texto} t={t} ini={0.15} tam={emoji ? 112 : 128} cor={escuro ? COR.branco : COR.tinta} marca={escuro ? COR.vermelho : COR.amarelo} />
      </AbsoluteFill>
    </Fundo>
  );
};

// 2. NUMERO que conta e bate na tela (som de contagem e batida: verde = caixa registradora, vermelho = alerta)
export const Numero: React.FC<{ valor: number; rotulo?: string; embaixo?: string; de?: number; cor?: string; formato?: (v: number) => string; dur?: number; emoji?: string }> = (
  { valor, rotulo, embaixo, de = 0, cor = COR.tinta, formato = reais, dur = 1.1, emoji }) => {
  const t = useT();
  const p = Math.min(1, Math.max(0, (t - 0.25) / dur)), ease = 1 - Math.pow(1 - p, 3);
  const bate = m(t, 0.25 + dur, "estalo"), pancada = t > 0.25 + dur ? 1 + 0.12 * Math.sin(Math.min(1, bate) * Math.PI) : 1;
  const batida = cor === COR.verde ? "kaching" : cor === COR.vermelho ? "warning" : "ding";
  return (
    <Fundo>
      <Som nome="pop" em={0.05} />
      {de !== valor && <Som nome="keyboard" em={0.3} vol={0.2} />}
      <Som nome={batida} em={0.25 + dur} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 24 }}>
        {rotulo && <div style={{ ...txt(64, COR.cinza, 600), transform: `translateY(${(1 - m(t, 0)) * -40}px)`, opacity: m(t, 0) }}>{rotulo}</div>}
        <div style={{ display: "flex", alignItems: "center", gap: 40, transform: `translateY(${flutua(t)}px)` }}>
          <div style={{ ...caixa(), padding: "26px 70px", transform: `scale(${(0.7 + 0.3 * m(t, 0.05, "estalo")) * pancada}) rotate(${(1 - m(t, 0.05)) * -4}deg)` }}>
            <div style={{ ...txt(230, cor), fontVariantNumeric: "tabular-nums" }}>{formato(de + (valor - de) * ease)}</div>
          </div>
          {emoji && <Emoji e={emoji} tam={240} estilo={{ transform: `scale(${m(t, 0.25 + dur, "estalo")})` }} />}
        </div>
        {embaixo && <div style={{ ...txt(58, COR.tinta, 600), opacity: m(t, 0.4 + dur), transform: `translateY(${(1 - m(t, 0.4 + dur)) * 30}px)` }}>{embaixo}</div>}
      </AbsoluteFill>
    </Fundo>
  );
};

// 3. CONTA: nota de papel, linha por linha, com o total correndo embaixo
export type LinhaConta = { rotulo: string; valor: number };
export const Conta: React.FC<{ titulo: string; linhas: LinhaConta[]; passo?: number; total?: string; ja?: number; neutro?: boolean }> = ({ titulo, linhas, passo = 0.9, total = "Sobra", ja = 0, neutro }) => {
  const t = useT();
  const ini = 0.5; let soma = 0, somaFim = 0;
  const quando = (i: number) => (i < ja ? -9 : ini + (i - ja) * passo);
  const vis = linhas.map((l, i) => ({ ...l, e: i < ja ? 1 : m(t, quando(i), "estalo") }));
  vis.forEach((l, i) => { somaFim += l.valor; if (t >= quando(i)) soma += l.valor; });
  const neg = !neutro && soma < 0, pisca = neg ? 0.75 + 0.25 * Math.sin(t * 9) : 1;
  const fimNovas = ini + (linhas.length - ja - 1) * passo;
  return (
    <Fundo>
      <Som nome="slide" em={0} />
      {linhas.map((l, i) => i >= ja && <Som key={i} nome={neutro ? "typewriter" : l.valor < 0 ? "card" : "coins"} em={quando(i)} />)}
      {!neutro && somaFim < 0 && <Som nome="warning" em={fimNovas + 0.45} />}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ ...caixa(), width: 1180, padding: "40px 64px", transform: `translateY(${(1 - m(t, 0)) * 300 + flutua(t, 4)}px) rotate(-1.5deg)` }}>
          <div style={{ ...txt(62), borderBottom: `5px dashed ${COR.tinta}55`, paddingBottom: 14, marginBottom: 10 }}>{titulo}</div>
          {vis.map((l, i) => (
            <div key={i} style={{ display: "flex", justifyContent: "space-between", padding: "8px 0", opacity: Math.min(1, l.e * 2), transform: `translateX(${(1 - l.e) * 80}px)` }}>
              <span style={txt(50, COR.tinta, 600)}>{l.rotulo}</span>
              <span style={{ ...txt(54, neutro ? COR.tinta : l.valor < 0 ? COR.vermelho : COR.verde), fontVariantNumeric: "tabular-nums" }}>{(neutro ? "" : l.valor < 0 ? "- " : "+ ") + reais(Math.abs(l.valor))}</span>
            </div>
          ))}
          <div style={{ display: "flex", justifyContent: "space-between", borderTop: `${LINHA}px solid ${COR.tinta}`, marginTop: 16, paddingTop: 16 }}>
            <span style={txt(62)}>{total}</span>
            <span style={{ ...txt(76, neg ? COR.vermelho : COR.tinta), opacity: pisca, fontVariantNumeric: "tabular-nums" }}>{reais(neutro ? Math.abs(soma) : soma)}</span>
          </div>
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 4. CITA: ficha de pesquisa presa com tachinha (sem rosto de gente real)
export const Cita: React.FC<{ nome: string; ano: string; onde?: string; achado: string; fonte?: string; emoji?: string }> = ({ nome, ano, onde, achado, fonte, emoji }) => {
  const t = useT();
  const e = m(t, 0), selo = m(t, 0.55, "estalo"); const td = tempoDoDestaque(achado, 0.8);
  return (
    <Fundo cor={COR.papel2}>
      <Som nome="card" em={0} /><Som nome="thud" em={0.6} />
      {td !== null && <Som nome="sparkle" em={td} vol={0.25} />}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ ...caixa(), width: 1380, padding: "64px 80px 52px", position: "relative", transform: `translateY(${(1 - e) * -500 + flutua(t, 4)}px) rotate(${-2 + (1 - e) * 10}deg)` }}>
          <div style={{ position: "absolute", top: -26, left: "50%", width: 52, height: 52, marginLeft: -26, borderRadius: 99, background: COR.vermelho, border: `${LINHA}px solid ${COR.tinta}` }} />
          <div style={{ position: "absolute", top: -40, right: -40, width: 210, height: 210, borderRadius: 999, background: COR.amarelo, border: `${LINHA}px solid ${COR.tinta}`, display: "flex", alignItems: "center", justifyContent: "center", transform: `scale(${selo}) rotate(${(1 - selo) * 90 + 8}deg)`, boxShadow: sombra(8) }}>
            <span style={txt(ano.length > 5 ? 56 : 76)}>{ano}</span>
          </div>
          {emoji && <div style={{ position: "absolute", left: -70, bottom: -70 }}><Emoji e={emoji} tam={180} estilo={{ transform: `scale(${m(t, 0.9, "estalo")})` }} /></div>}
          <div style={{ ...txt(40, COR.cinza, 600), letterSpacing: 3, textTransform: "uppercase" }}>pesquisa</div>
          <div style={{ ...txt(96), marginTop: 6, maxWidth: 1000 }}>{nome}</div>
          {onde && <div style={{ ...txt(46, COR.azul, 600), marginTop: 8 }}>{onde}</div>}
          <div style={{ borderTop: `5px dashed ${COR.tinta}44`, margin: "30px 0 24px" }} />
          <Destacado texto={achado} t={t} ini={0.8} tam={66} />
          {fonte && <div style={{ ...txt(30, COR.cinza, 600), marginTop: 28, opacity: m(t, 1.4), textAlign: "right" }}>Fonte: {fonte}</div>}
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 5. BARRAS que crescem e comparam (som de subida em cada barra)
export const Barras: React.FC<{ titulo?: string; itens: { rotulo: string; valor: number; cor?: string }[]; formato?: (v: number) => string }> = ({ titulo, itens, formato = reais }) => {
  const t = useT();
  const max = Math.max(...itens.map((i) => i.valor));
  return (
    <Fundo>
      <Som nome="pop" em={0} />
      {itens.map((it, i) => <Som key={i} nome={it.cor === COR.vermelho ? "slide" : "growth"} em={0.3 + i * 0.45} />)}
      <AbsoluteFill style={{ justifyContent: "center", padding: "0 170px", gap: 46 }}>
        {titulo && <div style={{ ...txt(70), opacity: m(t, 0), marginBottom: 10 }}>{titulo}</div>}
        {itens.map((it, i) => {
          const d = 0.3 + i * 0.45, cresce = m(t, d, "cartao"), p = Math.min(1, Math.max(0, (t - d) / 0.9));
          return (
            <div key={i}>
              <div style={{ ...txt(50, COR.tinta, 600), marginBottom: 10, opacity: Math.min(1, cresce * 2) }}>{it.rotulo}</div>
              <div style={{ display: "flex", alignItems: "center", gap: 30 }}>
                <div style={{ ...caixa(it.cor ?? COR.amarelo), height: 120, width: `${(it.valor / max) * 1020 * cresce * (1 + 0.006 * Math.sin(t * 3 + i))}px`, minWidth: 30, borderRadius: 20 }} />
                <span style={{ ...txt(80), whiteSpace: "nowrap", opacity: Math.min(1, cresce * 2), fontVariantNumeric: "tabular-nums" }}>{formato(it.valor * (1 - Math.pow(1 - p, 3)))}</span>
              </div>
            </div>
          );
        })}
      </AbsoluteFill>
    </Fundo>
  );
};

// 6. LINHA DO TEMPO: a bolinha corre ate o marco atual (tique do relogio e sino na chegada)
export const LinhaTempo: React.FC<{ marcos: string[]; ativo: number; titulo?: string }> = ({ marcos, ativo, titulo }) => {
  const t = useT();
  const desenha = Math.min(1, t / 0.8), anda = m(t, 0.7, "cartao"), pos = anda * ativo;
  const larg = 1500, passo = larg / (marcos.length - 1);
  return (
    <Fundo>
      <Som nome="slide" em={0.05} />
      {Array.from({ length: ativo + 1 }, (_, i) => <Som key={i} nome="clock" em={0.75 + i * 0.12} vol={0.3} />)}
      <Som nome="ding" em={0.75 + ativo * 0.12 + 0.25} />
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        {titulo && <div style={{ ...txt(84), position: "absolute", top: 230, opacity: m(t, 0) }}>{titulo}</div>}
        <div style={{ position: "relative", width: larg, height: 300 }}>
          <div style={{ position: "absolute", top: 140, left: 0, height: 16, width: larg * desenha, background: COR.tinta, borderRadius: 9 }} />
          {marcos.map((r, i) => {
            const e = m(t, 0.1 + i * 0.12, "estalo"), feito = i <= pos + 0.01, atual = i === ativo;
            return (
              <div key={i} style={{ position: "absolute", left: i * passo - 60, top: 88, width: 120, textAlign: "center", transform: `scale(${e * (atual ? 1 + 0.06 * Math.sin(t * 4) : 1)})` }}>
                <div style={{ width: 120, height: 120, borderRadius: 99, background: feito ? (atual ? COR.amarelo : COR.verde) : COR.branco, border: `${LINHA}px solid ${COR.tinta}`, boxShadow: sombra(6) }} />
                <div style={{ ...txt(atual ? 64 : 46, atual ? COR.tinta : COR.cinza, atual ? 800 : 600), marginTop: 24, whiteSpace: "nowrap", marginLeft: -100, marginRight: -100 }}>{r}</div>
              </div>
            );
          })}
          <div style={{ position: "absolute", left: pos * passo - 40, top: 30, fontSize: 70, transform: `translateY(${Math.sin(t * 6) * 6}px)` }}>▼</div>
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// 7. CALENDARIO: os dias vao passando (tique), dias marcados saltam com etiqueta (sino ou alerta)
export const Calendario: React.FC<{ mes?: string; marcados: Record<number, { cor: string; rotulo: string }>; ate?: number }> = ({ mes = "", marcados, ate = 30 }) => {
  const t = useT();
  const hoje = Math.min(ate, Math.floor(1 + Math.max(0, t - 0.4) * 9));
  return (
    <Fundo>
      <Som nome="slide" em={0} />
      {Array.from({ length: ate }, (_, i) => i + 1).map((d) => {
        const mk = marcados[d], em = 0.4 + (d - 1) / 9;
        if (mk) return <Som key={d} nome={mk.cor === COR.vermelho ? "warning" : "ding"} em={em} />;
        return d % 2 ? <Som key={d} nome="clock" em={em} vol={0.18} /> : null;
      })}
      <AbsoluteFill style={{ justifyContent: "center", alignItems: "center" }}>
        <div style={{ ...caixa(), padding: 40, transform: `translateY(${(1 - m(t, 0)) * 400 + flutua(t, 3)}px)` }}>
          {mes && <div style={{ ...txt(60), textAlign: "center", marginBottom: 20 }}>{mes}</div>}
          <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 150px)", columnGap: 14, rowGap: 58 }}>
            {Array.from({ length: 30 }, (_, i) => i + 1).map((d) => {
              const mk = marcados[d], passou = d <= hoje, pop = mk && passou ? m(t, 0.4 + (d - 1) / 9, "estalo") : 0;
              return (
                <div key={d} style={{ height: 104, borderRadius: 16, border: `5px solid ${COR.tinta}`, position: "relative",
                  background: mk && passou ? mk.cor : passou ? COR.papel2 : COR.branco, transform: `scale(${1 + 0.25 * Math.sin(Math.min(1, pop) * Math.PI)})`, zIndex: mk ? 2 : 1 }}>
                  <span style={{ ...txt(44, mk && passou ? COR.branco : COR.tinta), position: "absolute", left: 14, top: 8 }}>{d}</span>
                  {mk && passou && <div style={{ ...txt(34, COR.tinta), position: "absolute", bottom: -54, left: -40, right: -40, textAlign: "center", background: COR.branco, border: `5px solid ${COR.tinta}`, borderRadius: 14, padding: "4px 8px", opacity: Math.min(1, pop * 2) }}>{mk.rotulo}</div>}
                </div>
              );
            })}
          </div>
        </div>
      </AbsoluteFill>
    </Fundo>
  );
};

// ---------- Cena hibrida: imagem com camera + uma coisa animada por cima ----------
export const Hibrida: React.FC<{ img: string; mov?: "entra" | "sai" | "esq" | "dir"; dur: number; children?: React.ReactNode }> = ({ img, mov = "entra", dur, children }) => {
  const t = useT();
  const p = mola(t, 3.5 / dur, 1);
  const esc = mov === "entra" ? 1 + 0.08 * p : mov === "sai" ? 1.1 - 0.08 * p : 1.08;
  const dx = mov === "esq" ? 2.5 - 5 * p : mov === "dir" ? -2.5 + 5 * p : 0;
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: COR.tinta }}>
      <AbsoluteFill style={{ transform: `translateX(${dx}%) scale(${esc})` }}>
        <Img src={staticFile(img)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
      </AbsoluteFill>
      {children}
    </AbsoluteFill>
  );
};

export type Pos = { x: number; y: number }; // em % da tela
// Carimbo que bate e treme (som de pancada)
export const Carimbo: React.FC<Pos & { texto: string; cor?: string; ini?: number }> = ({ x, y, texto, cor = COR.verde, ini = 0.6 }) => {
  const t = useT(); const e = m(t, ini, "estalo");
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) scale(${2.2 - 1.2 * e}) rotate(-12deg)`, opacity: t < ini ? 0 : Math.min(1, e * 3) }}>
      <Som nome="thud" em={ini + 0.08} />
      <div style={{ ...txt(110, cor), border: `12px solid ${cor}`, borderRadius: 22, padding: "4px 40px", background: `${COR.branco}cc`, letterSpacing: 6, whiteSpace: "nowrap" }}>{texto}</div>
    </div>
  );
};
// Etiqueta de preco pendurada, balancando
export const Etiqueta: React.FC<Pos & { texto: string; ini?: number; cor?: string }> = ({ x, y, texto, ini = 0.4, cor = COR.amarelo }) => {
  const t = useT(); const e = m(t, ini, "estalo"), balanco = Math.sin((t - ini) * 3.2) * 4 * Math.exp(-(t - ini) * 0.6) + Math.sin(t * 1.5) * 1;
  const fio = (y / 100) * 1080 + 20; // o fio sai do TOPO DA TELA (Ed, 05/11: "esses ganchos teriam que sair do topo da tela")
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transformOrigin: `50% -${fio}px`, transform: `translate(-50%, ${(1 - e) * -300}px) rotate(${t > ini ? balanco : 0}deg)` }}>
      <Som nome="pop" em={ini} />
      <div style={{ position: "absolute", left: "50%", top: -fio, width: 5, height: fio, marginLeft: -2, background: COR.tinta }} />
      <div style={{ position: "absolute", left: "50%", top: -14, width: 18, height: 18, marginLeft: -9, borderRadius: 99, background: COR.cinza, border: `4px solid ${COR.tinta}` }} />
      <div style={{ ...caixa(cor), ...txt(84), padding: "14px 46px", whiteSpace: "nowrap" }}>{texto}</div>
    </div>
  );
};
// Balao de fala
export const Balao: React.FC<Pos & { texto: string; ini?: number; lado?: "esq" | "dir" }> = ({ x, y, texto, ini = 0.4, lado = "esq" }) => {
  const t = useT(); const e = m(t, ini, "estalo");
  return (
    <div style={{ position: "absolute", left: `${x}%`, top: `${y}%`, transform: `translate(-50%,-50%) scale(${e}) translateY(${flutua(t, 3)}px)`, transformOrigin: lado === "esq" ? "0% 100%" : "100% 100%" }}>
      <Som nome="pop" em={ini} />
      <div style={{ ...caixa(), padding: "24px 40px", maxWidth: 680, position: "relative" }}>
        <Destacado texto={texto} t={t} ini={ini + 0.15} tam={58} />
        <div style={{ position: "absolute", bottom: -46, [lado === "esq" ? "left" : "right"]: 70, width: 0, height: 0, borderLeft: "30px solid transparent", borderRight: "30px solid transparent", borderTop: `50px solid ${COR.tinta}` } as React.CSSProperties} />
      </div>
    </div>
  );
};
