// 25/11/2026: o Short do «Plantão do Tião: o que muda no seu bolso» (Ed: «noticia mais quente, mais atual», «feitos com motion»,
// «quero 3 shorts por dia desse novo jeito»). Em pé (1080 x 1920), só motion: nada de imagem, tudo desenhado em código.
// De cima para baixo: a barra vermelha do PLANTÃO com a medalha do Tião · o quadro da vez (manchete, número, lista, compara,
// pergunta) · a legenda grande, 3 palavras por vez · a faixa correndo · o canto de baixo livre (botões do Instagram e do TikTok).
// Os dados vêm do props.json que o fabrica/plantao.py escreve (o texto, os tempos de cada palavra, os quadros).
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useVideoConfig } from "remotion";
import { COR, caixa, Destacado, fontFamily, m, flutua, txt, useT } from "../motion/kit";
import { Emoji, Som } from "../motion/vivo";

const AZUL = "#0E1A2B", AZUL2 = "#16263D", VERMELHO = "#D62828", AMARELO = "#FFD43B";
type Palavra = [number, number, string];
type Quadro =
  | { ini: number; tipo: "manchete"; texto: string; sobre?: string; emoji?: string }
  | { ini: number; tipo: "numero"; de?: number; ate: number; antes?: string; depois?: string; casas?: number; rotulo?: string; embaixo?: string; cor?: "verde" | "vermelho"; emoji?: string }
  | { ini: number; tipo: "lista"; titulo?: string; itens: { t: string; ok: boolean; em?: number }[]; passo?: number }
  | { ini: number; tipo: "compara"; titulo?: string; de: string; para: string; rotuloDe?: string; rotuloPara?: string; ruim?: boolean }
  | { ini: number; tipo: "pergunta"; texto: string; opcoes?: string[]; emoji?: string };
export type DadosPlantao = { voz: string; musica?: string; palavras: Palavra[]; quadros: Quadro[]; fim: number; data: string; faixa?: string; rotulo?: string };
export const PLANTAO_VAZIO: DadosPlantao = { voz: "", palavras: [], quadros: [], fim: 10, data: "" };

const Y_QUADRO = 230, H_QUADRO = 1000, Y_LEG = 1270, Y_FAIXA = 1520;  // a legenda cabe em 2 linhas antes da faixa

const Topo: React.FC<{ data: string }> = ({ data }) => {
  const t = useT(); const pisca = 0.35 + 0.65 * Math.abs(Math.sin(t * 3));
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 190, background: VERMELHO, display: "flex", alignItems: "center",
      gap: 26, padding: "40px 40px 0", boxShadow: "0 10px 30px rgba(0,0,0,0.45)", transform: `translateY(${(1 - m(t, 0, "estalo")) * -200}px)` }}>
      <Img src={staticFile("marca/tiao-medalha.png")} style={{ width: 128, height: 128, transform: `rotate(${flutua(t, 4, 2.2)}deg)` }} />
      <div style={{ display: "flex", flexDirection: "column" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
          <div style={{ width: 22, height: 22, borderRadius: 11, background: "white", opacity: pisca }} />
          <div style={{ ...txt(62, "white"), letterSpacing: 2 }}>PLANTÃO DO TIÃO</div>
        </div>
        <div style={{ ...txt(36, AMARELO, 700) }}>o que muda no seu bolso · {data}</div>
      </div>
    </div>
  );
};

// cada quadro entra com uma mola e fica vivo (flutua)
const Manchete: React.FC<{ q: Extract<Quadro, { tipo: "manchete" }> }> = ({ q }) => {
  const t = useT();
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30, padding: "0 60px", transform: `translateY(${flutua(t, 5, 1.3)}px)` }}>
      <Som nome="boom" em={0.05} vol={0.3} />
      {q.emoji && <Emoji e={q.emoji} tam={230} estilo={{ transform: `scale(${m(t, 0, "estalo")})` }} />}
      {q.sobre && <div style={{ ...txt(44, AMARELO, 700), letterSpacing: 3, textTransform: "uppercase", opacity: m(t, 0) }}>{q.sobre}</div>}
      <Destacado texto={q.texto} t={t} ini={0.1} tam={92} cor="white" marca={VERMELHO} />
    </AbsoluteFill>
  );
};
const Numero: React.FC<{ q: Extract<Quadro, { tipo: "numero" }> }> = ({ q }) => {
  const t = useT(); const dur = 1.0, de = q.de ?? 0;
  const p = Math.min(1, Math.max(0, (t - 0.25) / dur)), e = 1 - Math.pow(1 - p, 3);
  const v = de + (q.ate - de) * e;
  const num = v.toLocaleString("pt-BR", { minimumFractionDigits: q.casas ?? 0, maximumFractionDigits: q.casas ?? 0 });
  const cor = q.cor === "verde" ? COR.verde : q.cor === "vermelho" ? COR.vermelho : COR.tinta;
  const bate = t > 0.25 + dur ? 1 + 0.1 * Math.sin(Math.min(1, m(t, 0.25 + dur, "estalo")) * Math.PI) : 1;
  const texto = `${q.antes ?? ""}${num}${q.depois ?? ""}`;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34 }}>
      <Som nome="pop" em={0.05} /><Som nome="keyboard" em={0.3} vol={0.2} />
      <Som nome={q.cor === "verde" ? "kaching" : q.cor === "vermelho" ? "warning" : "ding"} em={0.25 + dur} />
      {q.emoji && <Emoji e={q.emoji} tam={200} estilo={{ transform: `scale(${m(t, 0.2 + dur, "estalo")})` }} />}
      {q.rotulo && <div style={{ ...txt(54, "white", 700), textAlign: "center", padding: "0 70px", opacity: m(t, 0), transform: `translateY(${(1 - m(t, 0)) * -30}px)` }}>{q.rotulo}</div>}
      <div style={{ ...caixa(), padding: "30px 50px", transform: `scale(${(0.7 + 0.3 * m(t, 0.05, "estalo")) * bate}) translateY(${flutua(t)}px)` }}>
        <div style={{ ...txt(Math.min(190, Math.floor(900 / (0.55 * Math.max(4, texto.length)))), cor), whiteSpace: "nowrap", fontVariantNumeric: "tabular-nums" }}>{texto}</div>
      </div>
      {q.embaixo && <div style={{ ...txt(52, AMARELO, 700), textAlign: "center", padding: "0 70px", opacity: m(t, 0.4 + dur) }}>{q.embaixo}</div>}
    </AbsoluteFill>
  );
};
const Lista: React.FC<{ q: Extract<Quadro, { tipo: "lista" }> }> = ({ q }) => {
  const t = useT(); const passo = q.passo ?? 1.2;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 26, padding: "0 60px" }}>
      {q.titulo && <div style={{ ...txt(58, AMARELO), textAlign: "center", opacity: m(t, 0) }}>{q.titulo}</div>}
      {q.itens.map((it, i) => {
        const a = it.em ?? 0.3 + i * passo, e = m(t, a, "cartao");
        return (
          <div key={i} style={{ ...caixa(), width: 940, display: "flex", alignItems: "center", gap: 26, padding: "22px 30px",
            transform: `translateX(${(1 - e) * (i % 2 ? 900 : -900)}px) rotate(${(1 - e) * (i % 2 ? 4 : -4)}deg)`, opacity: Math.min(1, e * 2) }}>
            <Som nome={it.ok ? "ding" : "warning"} em={a + 0.15} vol={0.3} />
            <div style={{ width: 84, height: 84, borderRadius: 42, flexShrink: 0, background: it.ok ? COR.verde : COR.vermelho, display: "flex",
              alignItems: "center", justifyContent: "center", ...txt(60, "white"), transform: `scale(${m(t, a + 0.2, "estalo")})` }}>{it.ok ? "✓" : "✗"}</div>
            <div style={{ ...txt(48, COR.tinta, 700) }}>{it.t}</div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
const Compara: React.FC<{ q: Extract<Quadro, { tipo: "compara" }> }> = ({ q }) => {
  const t = useT(); const cor2 = q.ruim ? COR.vermelho : COR.verde;
  const Cartao = ({ v, r, a, c }: { v: string; r?: string; a: number; c: string }) => (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 12, transform: `scale(${m(t, a, "estalo")})` }}>
      {r && <div style={{ ...txt(42, "white", 700) }}>{r}</div>}
      <div style={{ ...caixa(), padding: "24px 44px" }}><div style={{ ...txt(110, c), whiteSpace: "nowrap" }}>{v}</div></div>
    </div>);
  const seta = m(t, 0.9);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 30 }}>
      <Som nome="pop" em={0.1} /><Som nome="slide" em={0.9} vol={0.3} /><Som nome={q.ruim ? "warning" : "ding"} em={1.4} />
      {q.titulo && <div style={{ ...txt(58, AMARELO), textAlign: "center", padding: "0 60px", opacity: m(t, 0) }}>{q.titulo}</div>}
      <Cartao v={q.de} r={q.rotuloDe} a={0.1} c={COR.cinza} />
      <div style={{ ...txt(120, AMARELO), transform: `translateY(${(1 - seta) * -40}px) scaleY(${seta})` }}>↓</div>
      <Cartao v={q.para} r={q.rotuloPara} a={1.4} c={cor2} />
    </AbsoluteFill>
  );
};
const Pergunta: React.FC<{ q: Extract<Quadro, { tipo: "pergunta" }> }> = ({ q }) => {
  const t = useT();
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34, padding: "0 60px" }}>
      <Som nome="pop" em={0.1} />
      <Emoji e={q.emoji ?? "💬"} tam={200} estilo={{ transform: `scale(${m(t, 0, "estalo")}) rotate(${flutua(t, 5, 2)}deg)` }} />
      <div style={{ ...caixa(), padding: "34px 44px", transform: `scale(${0.8 + 0.2 * m(t, 0.1, "estalo")})` }}>
        <div style={{ ...txt(64, COR.tinta), textAlign: "center" }}>{q.texto}</div>
      </div>
      <div style={{ display: "flex", gap: 30 }}>
        {(q.opcoes ?? []).map((o, i) => (
          <div key={i} style={{ ...caixa(i ? COR.vermelho : COR.verde), padding: "18px 50px", ...txt(64, "white"), transform: `scale(${m(t, 0.6 + i * 0.25, "estalo")})` }}>
            <Som nome="click" em={0.6 + i * 0.25} vol={0.3} />{o}</div>))}
      </div>
    </AbsoluteFill>
  );
};

const Legenda: React.FC<{ palavras: Palavra[] }> = ({ palavras }) => {
  const t = useT();
  // blocos de até 3 palavras; um ponto fecha o bloco
  const blocos: Palavra[][] = []; let cur: Palavra[] = [];
  palavras.forEach((w) => { cur.push(w); if (cur.length === 3 || /[.!?:]$/.test(w[2])) { blocos.push(cur); cur = []; } });
  if (cur.length) blocos.push(cur);
  const b = blocos.find((x, i) => t >= x[0][0] && t < (blocos[i + 1]?.[0][0] ?? x[x.length - 1][1] + 0.6));
  if (!b) return null;
  const e = m(t, b[0][0], "estalo");
  return (
    <div style={{ position: "absolute", left: 40, right: 40, top: Y_LEG, display: "flex", justifyContent: "center", flexWrap: "wrap", gap: "0 24px",
      transform: `scale(${0.85 + 0.15 * e})` }}>
      {b.map((w, i) => {
        const fala = t >= w[0], num = /\d|R\$/.test(w[2]);
        return <span key={i} style={{ ...txt(90, num ? AMARELO : fala ? "white" : "rgba(255,255,255,0.55)"), WebkitTextStroke: "3px #0b0b0b",
          textShadow: "0 6px 0 #0b0b0b", paintOrder: "stroke fill" }}>{w[2]}</span>;
      })}
    </div>
  );
};

const Faixa: React.FC<{ texto: string; rotulo: string }> = ({ texto, rotulo }) => {
  const t = useT(); const larg = texto.length * 25; const x = -((t * 85) % larg);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: Y_FAIXA, height: 84, background: AZUL, borderTop: `6px solid ${AMARELO}`, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 270 + x, top: 14, whiteSpace: "nowrap", ...txt(44, "white", 700) }}>{texto.repeat(4)}</div>
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 260, background: VERMELHO, display: "flex", alignItems: "center", justifyContent: "center", ...txt(42, "white") }}>{rotulo}</div>
    </div>
  );
};

export const PlantaoShort: React.FC<DadosPlantao> = (d) => {
  const { fps } = useVideoConfig(); const t = useT();
  const qs = [...d.quadros].sort((a, b) => a.ini - b.ini);
  return (
    <AbsoluteFill style={{ background: AZUL, fontFamily, overflow: "hidden" }}>
      {/* fundo de noticiário: grade de pontos que anda e uma luz que respira */}
      <AbsoluteFill style={{ backgroundImage: `radial-gradient(#ffffff14 2.4px, transparent 2.8px)`, backgroundSize: "44px 44px", transform: `translate(${-t * 8}px, ${-t * 5}px) scale(1.08)` }} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 40%, ${AZUL2} 0%, transparent ${55 + 5 * Math.sin(t * 1.5)}%)` }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: Y_QUADRO, height: H_QUADRO }}>
        {qs.map((q, i) => {
          const de = Math.round(q.ini * fps), ate = Math.round((qs[i + 1]?.ini ?? d.fim + 0.5) * fps);
          return (
            <Sequence key={i} from={de} durationInFrames={Math.max(1, ate - de)} layout="none">
              <AbsoluteFill>
                {q.tipo === "manchete" && <Manchete q={q} />}{q.tipo === "numero" && <Numero q={q} />}{q.tipo === "lista" && <Lista q={q} />}
                {q.tipo === "compara" && <Compara q={q} />}{q.tipo === "pergunta" && <Pergunta q={q} />}
              </AbsoluteFill>
            </Sequence>);
        })}
      </div>
      <Topo data={d.data} />
      <Legenda palavras={d.palavras} />
      <Faixa rotulo={d.rotulo ?? "ASSISTA"} texto={d.faixa ?? "ASSISTA À HISTÓRIA INTEIRA NO CANAL TIÃO POUPADOR   •   SE INSCREVE E DEIXA O SEU LIKE!   •   "} />
      <Audio src={staticFile(d.voz)} />
      {d.musica && <Audio src={staticFile(d.musica)} volume={0.1} />}
      <Som nome="warning" em={0} vol={0.25} />
    </AbsoluteFill>
  );
};
