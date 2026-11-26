// 25/11/2026: o Short do «Plantão do Tião: o que muda no seu bolso» (Ed: «noticia mais quente, mais atual», «feitos com motion»,
// «quero 3 shorts por dia desse novo jeito»). Em pé (1080 x 1920), só motion: nada de imagem, tudo desenhado em código.
// De cima para baixo: a barra vermelha do PLANTÃO com a medalha do Tião e a barra de progresso · o quadro da vez · a legenda
// grande (a palavra falada pula) · a faixa correndo · o canto de baixo livre (botões do Instagram e do TikTok).
// 2.ª versão, no mesmo dia (Ed: «achei os motion muito simples, tem que ser mais dinamico», «nao precisa colocar data»):
//  - cada quadro entra com um golpe de câmera (zoom de 1,18 com desfoque e clarão branco) e um «vush»;
//  - a câmera nunca para (zoom lento) e treme no impacto do número;
//  - fundo de plantão: faixas diagonais que correm, um brilho que varre a tela, a borda vermelha que pulsa no alerta;
//  - manchete: as palavras batem uma a uma, tortas, e a palavra forte treme dentro da caixa vermelha; carimbo URGENTE no 1.º;
//  - número: rola, bate, solta raios e uma seta que sobe ou desce; compara: o antigo é riscado, o novo bate com carimbo;
//  - pergunta: os botões SIM e NÃO pulsam e a mãozinha toca; inscrever: o botão vermelho é clicado, vira INSCRITO e o sino toca.
// 3.ª versão, 26/11 (Ed: «mais motion, mais graficos, cards, o mouse se mexendo, clicando»): o mouse anda e clica em tudo, cada
// clique muda a cor ou põe um check; quadros novos: gráfico (barras ou linha) e cards.
// Os dados vêm do props.json que o fabrica/plantao.py escreve (o texto, os tempos de cada palavra, os quadros).
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useVideoConfig } from "remotion";
import { COR, caixa, fontFamily, m, flutua, txt, useT } from "../motion/kit";
import { Emoji, Som } from "../motion/vivo";

const AZUL = "#0E1A2B", AZUL2 = "#1B2F4D", VERMELHO = "#D62828", AMARELO = "#FFD43B";
type Palavra = [number, number, string];
type Quadro =
  | { ini: number; tipo: "manchete"; texto: string; sobre?: string; emoji?: string }
  | { ini: number; tipo: "numero"; de?: number; ate: number; antes?: string; depois?: string; casas?: number; rotulo?: string; embaixo?: string; cor?: "verde" | "vermelho"; emoji?: string }
  | { ini: number; tipo: "lista"; titulo?: string; itens: { t: string; ok: boolean; em?: number }[]; passo?: number }
  | { ini: number; tipo: "compara"; titulo?: string; de: string; para: string; rotuloDe?: string; rotuloPara?: string; ruim?: boolean }
  | { ini: number; tipo: "pergunta"; texto: string; opcoes?: string[]; emoji?: string; resposta?: string }
  | { ini: number; tipo: "grafico"; titulo?: string; modo?: "barras" | "linha"; barras: { rotulo: string; valor: number; txt?: string }[]; destaque?: number; nota?: string; cor?: "verde" | "vermelho" }
  | { ini: number; tipo: "cards"; titulo?: string; cards: { emoji?: string; t: string; valor?: string; ok?: boolean; em?: number }[]; passo?: number }
  | { ini: number; tipo: "inscrever"; texto?: string };
export type DadosPlantao = { voz: string; musica?: string; volMusica?: number; palavras: Palavra[]; quadros: Quadro[]; fim: number; cauda?: number; data?: string; faixa?: string; rotulo?: string };
export const PLANTAO_VAZIO: DadosPlantao = { voz: "", palavras: [], quadros: [], fim: 10 };

const Y_QUADRO = 250, H_QUADRO = 1000, Y_LEG = 1270, Y_FAIXA = 1520;
const cl = (x: number) => Math.min(1, Math.max(0, x));
const rnd = (i: number) => (Math.sin(i * 91.7 + 13.3) * 43758.5) % 1; // sorteio fixo (o mesmo em todo quadro do render)

const Topo: React.FC<{ fim: number; batidas: number[] }> = ({ fim, batidas }) => {
  const t = useT(); const pisca = 0.35 + 0.65 * Math.abs(Math.sin(t * 3));
  const ultima = Math.max(-9, ...batidas.filter((b) => b <= t)); const pulo = Math.sin(cl((t - ultima) / 0.35) * Math.PI) * 0.18;
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: 0, height: 200, transform: `translateY(${(1 - m(t, 0, "estalo")) * -220}px)` }}>
      <div style={{ position: "absolute", inset: 0, background: VERMELHO, boxShadow: "0 10px 30px rgba(0,0,0,0.45)", overflow: "hidden" }}>
        {/* brilho que corre na barra */}
        <div style={{ position: "absolute", top: 0, bottom: 0, width: 260, left: ((t * 520) % 1800) - 400, background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.28), transparent)", transform: "skewX(-20deg)" }} />
      </div>
      <div style={{ position: "absolute", left: 40, top: 46, display: "flex", alignItems: "center", gap: 26 }}>
        <Img src={staticFile("marca/tiao-medalha.png")} style={{ width: 128, height: 128, transform: `scale(${1 + pulo}) rotate(${flutua(t, 5, 2.2)}deg)` }} />
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 16 }}>
            <div style={{ width: 22, height: 22, borderRadius: 11, background: "white", opacity: pisca, boxShadow: `0 0 ${18 * pisca}px white` }} />
            <div style={{ ...txt(64, "white"), letterSpacing: 2 }}>PLANTÃO DO TIÃO</div>
          </div>
          <div style={{ ...txt(38, AMARELO, 700) }}>o que muda no seu bolso</div>
        </div>
      </div>
      {/* barra de progresso: quem vê quanto falta fica até o fim */}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: -12, height: 12, background: "rgba(0,0,0,0.35)" }}>
        <div style={{ height: "100%", width: `${cl(t / fim) * 100}%`, background: AMARELO }} />
      </div>
    </div>
  );
};

// Fundo de plantão: faixas diagonais, varredura de luz, borda vermelha que pulsa a cada quadro
const Fundo: React.FC<{ batidas: number[] }> = ({ batidas }) => {
  const t = useT(); const ultima = Math.max(-9, ...batidas.filter((b) => b <= t)); const alarme = Math.max(0, 1 - (t - ultima) / 0.7);
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 38%, ${AZUL2} 0%, ${AZUL} ${58 + 6 * Math.sin(t * 1.4)}%)` }} />
      <AbsoluteFill style={{ backgroundImage: `repeating-linear-gradient(-35deg, rgba(255,255,255,0.035) 0 38px, transparent 38px 96px)`, backgroundPosition: `${t * 60}px 0` }} />
      <AbsoluteFill style={{ backgroundImage: `radial-gradient(#ffffff16 2.4px, transparent 2.8px)`, backgroundSize: "44px 44px", transform: `translate(${-t * 10}px, ${-t * 6}px) scale(1.08)` }} />
      <div style={{ position: "absolute", top: -300, bottom: -300, width: 380, left: ((t * 300) % 2400) - 700, background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.07), transparent)", transform: "rotate(18deg)" }} />
      <AbsoluteFill style={{ boxShadow: `inset 0 0 ${120 + 80 * alarme}px rgba(214,40,40,${0.25 + 0.45 * alarme})` }} />
    </AbsoluteFill>
  );
};

// o golpe de câmera da entrada de cada quadro (e o tremor do impacto)
const Golpe: React.FC<{ children: React.ReactNode; treme?: number }> = ({ children, treme }) => {
  const t = useT(); const e = m(t, 0, "estalo"); const z = 1.18 - 0.18 * e + 0.035 * t / 6;
  const tr = treme !== undefined && t > treme ? Math.max(0, 1 - (t - treme) / 0.4) : 0;
  const sx = Math.sin(t * 90) * 14 * tr, sy = Math.cos(t * 77) * 10 * tr;
  return (
    <AbsoluteFill style={{ transform: `translate(${sx}px, ${sy}px) scale(${z})`, filter: `blur(${(1 - cl(e * 1.4)) * 10}px)`, opacity: cl(e * 3) }}>
      {children}
    </AbsoluteFill>
  );
};
const Clarao: React.FC = () => { const t = useT(); const o = Math.max(0, 0.75 - t / 0.16); return o > 0 ? <AbsoluteFill style={{ background: "white", opacity: o }} /> : null; };

const Raios: React.FC<{ em: number; cor: string }> = ({ em, cor }) => {
  const t = useT(); const p = cl((t - em) / 0.6); if (p <= 0 || p >= 1) return null;
  return (<div style={{ position: "absolute", left: "50%", top: "50%" }}>
    {Array.from({ length: 14 }, (_, i) => (
      <div key={i} style={{ position: "absolute", width: 16, height: 120, background: cor, borderRadius: 8, opacity: 1 - p,
        transform: `rotate(${i * (360 / 14)}deg) translateY(${-200 - 260 * p}px) scaleY(${1 - p * 0.6})`, transformOrigin: "50% 0" }} />))}
  </div>);
};

const Manchete: React.FC<{ q: Extract<Quadro, { tipo: "manchete" }>; primeiro: boolean }> = ({ q, primeiro }) => {
  const t = useT();
  const partes = q.texto.split(/(\*[^*]+\*|\s+)/g).filter((p) => p && !/^\s+$/.test(p));
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34, padding: "0 50px" }}>
      <Som nome="boom" em={0.02} vol={0.35} />
      {q.emoji && <Emoji e={q.emoji} tam={260} estilo={{ transform: `scale(${m(t, 0.05, "estalo")}) translateY(${Math.abs(Math.sin(t * 4)) * -18}px) rotate(${flutua(t, 8, 3)}deg)` }} />}
      {q.sobre && <div style={{ ...txt(46, AMARELO, 700), letterSpacing: 3, textTransform: "uppercase", opacity: m(t, 0) }}>{q.sobre}</div>}
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "8px 22px" }}>
        {partes.map((p, i) => {
          const forte = p.startsWith("*"), w = forte ? p.slice(1, -1) : p, d = 0.12 + i * 0.09, e = m(t, d, "estalo"), r = (rnd(i) - 0.5) * 16;
          const tre = forte && t > d + 0.3 ? Math.sin(t * 40) * 3 * Math.max(0, 1 - (t - d - 0.3) / 0.6) : 0;
          return (
            <span key={i} style={{ display: "inline-block", opacity: cl(e * 2), transform: `scale(${2.2 - 1.2 * e}) rotate(${r * (1 - e) + tre}deg)`,
              ...(forte ? { background: VERMELHO, padding: "0 18px", borderRadius: 14, boxShadow: `8px 8px 0 #000` } : {}), ...txt(forte ? 100 : 94, "white") }}>
              {w}{i === 0 && <Som nome="pop" em={d} vol={0.2} />}
            </span>);
        })}
      </div>
      {primeiro && <div style={{ position: "absolute", right: 60, top: 40, ...txt(54, "white"), border: `8px solid ${AMARELO}`, color: AMARELO, padding: "6px 22px",
        borderRadius: 12, transform: `rotate(${-12 + (1 - m(t, 0.6, "estalo")) * 30}deg) scale(${2 - m(t, 0.6, "estalo")})`, opacity: cl((t - 0.6) * 5) }}>
        <Som nome="thud" em={0.6} />URGENTE</div>}
    </AbsoluteFill>
  );
};

const Numero: React.FC<{ q: Extract<Quadro, { tipo: "numero" }> }> = ({ q }) => {
  const t = useT(); const dur = 1.1, de = q.de ?? 0, bate = 0.25 + dur;
  const p = cl((t - 0.25) / dur), e = 1 - Math.pow(1 - p, 3), v = de + (q.ate - de) * e;
  const num = v.toLocaleString("pt-BR", { minimumFractionDigits: q.casas ?? 0, maximumFractionDigits: q.casas ?? 0 });
  const cor = q.cor === "verde" ? COR.verde : q.cor === "vermelho" ? COR.vermelho : COR.tinta;
  const pul = t > bate ? 1 + 0.16 * Math.sin(cl((t - bate) / 0.3) * Math.PI) : 1;
  const texto = `${q.antes ?? ""}${num}${q.depois ?? ""}`, sobe = q.ate >= de;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 34 }}>
      <Som nome="pop" em={0.05} /><Som nome="keyboard" em={0.3} vol={0.25} />
      <Som nome={q.cor === "verde" ? "kaching" : q.cor === "vermelho" ? "warning" : "ding"} em={bate} />
      {q.rotulo && <div style={{ ...txt(58, "white", 700), textAlign: "center", padding: "0 70px", opacity: m(t, 0), transform: `translateY(${(1 - m(t, 0)) * -40}px)` }}>{q.rotulo}</div>}
      <div style={{ position: "relative" }}>
        <Raios em={bate} cor={q.cor === "verde" ? COR.verde : AMARELO} />
        <div style={{ ...caixa(), padding: "34px 54px", transform: `scale(${(0.6 + 0.4 * m(t, 0.05, "estalo")) * pul}) rotate(${(1 - m(t, 0.05)) * -8}deg)` }}>
          <div style={{ ...txt(Math.min(200, Math.floor(880 / (0.55 * Math.max(4, texto.length)))), cor), whiteSpace: "nowrap", fontVariantNumeric: "tabular-nums" }}>{texto}</div>
        </div>
        {/* a seta que sobe ou desce */}
        <div style={{ position: "absolute", right: -30, top: -70, ...txt(130, sobe ? (q.cor === "verde" ? COR.verde : VERMELHO) : COR.verde),
          transform: `scale(${m(t, bate, "estalo")}) translateY(${(sobe ? -1 : 1) * Math.abs(Math.sin(t * 5)) * 16}px)`, textShadow: "6px 6px 0 #000" }}>{sobe ? "▲" : "▼"}</div>
      </div>
      {q.emoji && <Emoji e={q.emoji} tam={190} estilo={{ transform: `scale(${m(t, bate, "estalo")}) rotate(${flutua(t, 8, 3)}deg)` }} />}
      {q.embaixo && <div style={{ ...txt(54, AMARELO, 700), textAlign: "center", padding: "0 70px", opacity: m(t, bate + 0.15), transform: `translateY(${(1 - m(t, bate + 0.15)) * 40}px)` }}>{q.embaixo}</div>}
    </AbsoluteFill>
  );
};

// ===== 26/11 (Ed: «queria q tivesse mais motion, mais graficos, cards, o mouse se mexendo, clicando, o botao ficando de outra
// cor, a cada clique um check quando possivel»). O MOUSE: uma seta de computador que voa de alvo em alvo (curva com arco e
// aceleração suave), aperta no clique (encolhe, solta um anel e faz «clique»), e cada clique MUDA algo na tela: o botão troca de
// cor, aparece um check, o sino toca, o like fica azul. As coordenadas são as do quadro (1080 x 1000).
type Pt = { t: number; x: number; y: number; c?: boolean };
const suave = (x: number) => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
const Cursor: React.FC<{ pts: Pt[] }> = ({ pts }) => {
  const t = useT(); if (!pts.length) return null;
  let x = pts[0].x, y = pts[0].y;
  for (let i = 0; i < pts.length; i++) {
    const a = pts[i], b = pts[i + 1];
    if (!b || t < b.t) {
      if (b && t > a.t) { const p = suave(cl((t - a.t) / (b.t - a.t))); x = a.x + (b.x - a.x) * p; y = a.y + (b.y - a.y) * p - Math.sin(p * Math.PI) * 50; }
      else { x = a.x; y = a.y; }
      break;
    }
  }
  const fim = pts[pts.length - 1];
  if (t > fim.t + 0.3) { x += Math.sin((t - fim.t) * 2.2) * 10; y += Math.cos((t - fim.t) * 1.7) * 7; } // nunca parado
  const cliques = pts.filter((p) => p.c);
  const aperta = cliques.some((c) => t >= c.t && t < c.t + 0.13) ? 0.78 : 1;
  return (
    <>
      {cliques.map((c, i) => {
        const p = cl((t - c.t) / 0.5);
        return (<React.Fragment key={i}>
          <Som nome="click" em={c.t} vol={0.5} />
          {p > 0 && p < 1 && <div style={{ position: "absolute", left: c.x - 20 - 60 * p, top: c.y - 20 - 60 * p, width: 40 + 120 * p, height: 40 + 120 * p,
            borderRadius: "50%", border: `${8 * (1 - p) + 2}px solid ${AMARELO}`, opacity: 1 - p }} />}
        </React.Fragment>);
      })}
      <svg width={90} height={110} viewBox="-4 -4 54 74" style={{ position: "absolute", left: x, top: y, transform: `scale(${aperta})`, transformOrigin: "0 0",
        filter: "drop-shadow(5px 7px 0 rgba(0,0,0,0.55))", zIndex: 50 }}>
        <path d="M0 0 L0 56 L14 43 L24 66 L35 61 L25 39 L44 39 Z" fill="white" stroke="#0b0b0b" strokeWidth={4.5} strokeLinejoin="round" />
      </svg>
    </>
  );
};
// a marca que aparece no clique: um selo redondo com ✓ (verde) ou ✗ (vermelho) que salta
const Selo: React.FC<{ em: number; ok: boolean; tam?: number; estilo?: React.CSSProperties }> = ({ em, ok, tam = 84, estilo }) => {
  const t = useT(); if (t < em) return null; const e = m(t, em, "estalo");
  return <div style={{ position: "absolute", width: tam, height: tam, borderRadius: tam / 2, background: ok ? COR.verde : COR.vermelho, border: "5px solid white",
    display: "flex", alignItems: "center", justifyContent: "center", ...txt(tam * 0.62, "white"), boxShadow: "4px 5px 0 #000",
    transform: `scale(${e}) rotate(${(1 - e) * -120}deg)`, ...estilo }}>{ok ? "✓" : "✗"}</div>;
};

const Lista: React.FC<{ q: Extract<Quadro, { tipo: "lista" }> }> = ({ q }) => {
  const t = useT(); const passo = q.passo ?? 1.2; const n = q.itens.length;
  const TIT = q.titulo ? 130 : 0, H = 140, G = 24, top0 = (H_QUADRO - (TIT + n * H + (n - 1) * G)) / 2;
  // cada item: entra (a) e o mouse clica na caixinha dele (ck), sempre em ordem
  const tempos: { a: number; ck: number }[] = [];
  q.itens.forEach((it, i) => { const a = it.em ?? 0.3 + i * passo; const ck = Math.max(a + 0.45, (tempos[i - 1]?.ck ?? 0) + 0.42); tempos.push({ a, ck }); });
  const pts: Pt[] = [{ t: tempos[0] ? tempos[0].a : 0.3, x: 1000, y: 980 }, ...tempos.map((tp, i) => ({ t: tp.ck, x: 128, y: top0 + TIT + i * (H + G) + 74, c: true }))];
  return (
    <AbsoluteFill>
      {q.titulo && <div style={{ position: "absolute", left: 40, right: 40, top: top0, height: TIT - 20, display: "flex", alignItems: "center", justifyContent: "center",
        ...txt(64, AMARELO), textAlign: "center", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      {q.itens.map((it, i) => {
        const { a, ck } = tempos[i], e = m(t, a, "estalo"), feito = t >= ck, top = top0 + TIT + i * (H + G);
        const cor = it.ok ? COR.verde : COR.vermelho, pulso = feito ? 1 + 0.05 * Math.sin(cl((t - ck) / 0.25) * Math.PI) : 1;
        return (
          <div key={i} style={{ position: "absolute", left: 60, top, width: 960, height: H, ...caixa(feito ? (it.ok ? "#E8F7EE" : "#FCE9E7") : COR.branco),
            display: "flex", alignItems: "center", gap: 26, padding: "0 26px", boxSizing: "border-box", borderColor: feito ? cor : COR.tinta,
            transform: `translateX(${(1 - e) * (i % 2 ? 1100 : -1100)}px) rotate(${(1 - e) * (i % 2 ? 9 : -9)}deg) scale(${pulso})` }}>
            <Som nome="slide" em={a} vol={0.25} /><Som nome={it.ok ? "ding" : "warning"} em={ck + 0.05} vol={0.32} />
            <div style={{ position: "relative", width: 90, height: 90, flexShrink: 0, borderRadius: 20, border: `6px solid ${feito ? cor : COR.tinta}`,
              background: feito ? cor : "white", display: "flex", alignItems: "center", justifyContent: "center" }}>
              {feito && <div style={{ ...txt(70, "white"), transform: `scale(${m(t, ck, "estalo")}) rotate(${(1 - m(t, ck)) * -90}deg)` }}>{it.ok ? "✓" : "✗"}</div>}
            </div>
            <div style={{ ...txt(50, COR.tinta, 700), textDecoration: feito && !it.ok ? "line-through" : "none", textDecorationColor: COR.vermelho }}>{it.t}</div>
          </div>);
      })}
      <Cursor pts={pts} />
    </AbsoluteFill>
  );
};

const Compara: React.FC<{ q: Extract<Quadro, { tipo: "compara" }> }> = ({ q }) => {
  const t = useT(); const cor2 = q.ruim ? COR.vermelho : COR.verde; const b = 1.4, ck1 = 0.95, ck2 = b + 0.6;
  const risco = cl((t - 1.0) / 0.3), seta = m(t, 0.9, "estalo"), brilho = t > ck2 ? 1 + 0.08 * Math.sin(cl((t - ck2) / 0.3) * Math.PI) : 1;
  const pts: Pt[] = [{ t: 0.35, x: 1000, y: 980 }, { t: ck1, x: 640, y: 330, c: true }, { t: ck2, x: 650, y: 760, c: true }];
  return (
    <AbsoluteFill>
      <Som nome="pop" em={0.1} /><Som nome="slide" em={1.0} vol={0.3} /><Som nome={q.ruim ? "warning" : "kaching"} em={b} /><Som nome="sparkle" em={ck2 + 0.05} vol={0.3} />
      {q.titulo && <div style={{ position: "absolute", left: 50, right: 50, top: 20, height: 160, display: "flex", alignItems: "flex-end", justifyContent: "center",
        ...txt(60, AMARELO), textAlign: "center", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      <div style={{ position: "absolute", left: 0, right: 0, top: 200, display: "flex", flexDirection: "column", alignItems: "center", gap: 10,
        transform: `scale(${m(t, 0.1, "estalo") * (1 - 0.18 * risco)})`, filter: `grayscale(${risco})`, opacity: 1 - 0.35 * risco }}>
        {q.rotuloDe && <div style={{ ...txt(44, "white", 700) }}>{q.rotuloDe}</div>}
        <div style={{ ...caixa(), padding: "22px 46px", position: "relative" }}>
          <div style={{ ...txt(110, COR.cinza), whiteSpace: "nowrap" }}>{q.de}</div>
          <div style={{ position: "absolute", left: 20, top: "50%", height: 12, width: `calc(${risco * 100}% - 40px)`, background: VERMELHO, borderRadius: 6, transform: "rotate(-8deg)" }} />
        </div>
      </div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 440, textAlign: "center", ...txt(140, AMARELO), transform: `translateY(${(1 - seta) * -60 + Math.abs(Math.sin(t * 5)) * 12}px) scale(${seta})`, textShadow: "6px 6px 0 #000" }}>⬇</div>
      <div style={{ position: "absolute", left: 0, right: 0, top: 600, display: "flex", flexDirection: "column", alignItems: "center", gap: 10,
        transform: `scale(${(2 - m(t, b, "estalo")) * (t > b ? 1 : 0) * brilho}) rotate(${(1 - m(t, b)) * 10}deg)` }}>
        <Raios em={b + 0.1} cor={cor2} />
        {q.rotuloPara && <div style={{ ...txt(44, "white", 700) }}>{q.rotuloPara}</div>}
        <div style={{ ...caixa(t > ck2 ? AMARELO : COR.branco), padding: "26px 54px", position: "relative" }}>
          <div style={{ ...txt(130, t > ck2 ? COR.tinta : cor2), whiteSpace: "nowrap" }}>{q.para}</div>
          <Selo em={ck2} ok={!q.ruim} tam={90} estilo={{ right: -40, top: -40 }} />
        </div>
      </div>
      <Cursor pts={pts} />
    </AbsoluteFill>
  );
};

// 26/11: o GRÁFICO. Barras que crescem uma a uma (ou uma linha que se desenha), o valor em cima de cada uma, e o mouse
// clica na barra que importa: ela acende em amarelo e abre um balão com a explicação.
const Grafico: React.FC<{ q: Extract<Quadro, { tipo: "grafico" }> }> = ({ q }) => {
  const t = useT(); const n = q.barras.length, X0 = 110, X1 = 970, BASE = 800, TOPO = 330;
  const max = Math.max(...q.barras.map((b) => b.valor)) * 1.12 || 1, slot = (X1 - X0) / n, larg = slot * 0.58;
  const ini = (i: number) => 0.35 + i * 0.32, pronto = ini(n - 1) + 0.6, d = q.destaque ?? n - 1, ck = pronto + 0.55;
  const cor = q.cor === "verde" ? COR.verde : q.cor === "vermelho" ? VERMELHO : AMARELO;
  const cx = (i: number) => X0 + slot * i + slot / 2, alt = (i: number) => (q.barras[i].valor / max) * (BASE - TOPO);
  const rot = (b: { valor: number; txt?: string }) => b.txt ?? b.valor.toLocaleString("pt-BR");
  const linha = q.modo === "linha", desenho = cl((t - 0.35) / (0.4 + 0.32 * n));
  const pontos = q.barras.map((_, i) => `${cx(i)},${BASE - alt(i)}`).join(" ");
  const pts: Pt[] = [{ t: pronto, x: 1060, y: 990 }, { t: ck, x: cx(d) + 10, y: BASE - alt(d) * (linha ? 1 : 0.6) + 10, c: true }];
  return (
    <AbsoluteFill>
      <Som nome="growth" em={0.35} vol={0.3} /><Som nome={q.cor === "vermelho" ? "warning" : "sparkle"} em={ck + 0.05} vol={0.35} />
      {q.titulo && <div style={{ position: "absolute", left: 50, right: 50, top: 40, height: 200, display: "flex", alignItems: "center", justifyContent: "center",
        ...txt(62, AMARELO), textAlign: "center", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      {/* as linhas de fundo do gráfico se desenham */}
      {[0, 1, 2, 3].map((k) => <div key={k} style={{ position: "absolute", left: X0 - 20, top: TOPO + k * (BASE - TOPO) / 4, height: 3, width: (X1 - X0 + 40) * cl((t - 0.1 - k * 0.06) / 0.4),
        background: "rgba(255,255,255,0.16)" }} />)}
      <div style={{ position: "absolute", left: X0 - 30, top: BASE, height: 8, borderRadius: 4, background: "white", width: (X1 - X0 + 60) * cl((t - 0.05) / 0.35) }} />
      {!linha && q.barras.map((b, i) => {
        const e = m(t, ini(i), "estalo"), h = alt(i) * e, acesa = i === d && t > ck;
        return (<React.Fragment key={i}>
          <Som nome="pop" em={ini(i)} vol={0.22} />
          <div style={{ position: "absolute", left: cx(i) - larg / 2, top: BASE - h, width: larg, height: h, borderRadius: "16px 16px 0 0",
            background: acesa ? AMARELO : i === d ? cor : "#5B8FD6", border: `5px solid ${acesa ? "white" : "#0b0b0b"}`, borderBottom: "none", boxSizing: "border-box",
            boxShadow: acesa ? `0 0 ${30 + 14 * Math.sin(t * 8)}px ${AMARELO}` : "6px 0 0 rgba(0,0,0,0.35)" }} />
          <div style={{ position: "absolute", left: cx(i) - 160, width: 320, top: BASE - h - 78, textAlign: "center", ...txt(54, "white"), opacity: cl((t - ini(i) - 0.25) * 4) }}>{rot(b)}</div>
          <div style={{ position: "absolute", left: cx(i) - slot / 2, width: slot, top: BASE + 22, textAlign: "center", ...txt(36, "rgba(255,255,255,0.85)", 700), opacity: cl((t - ini(i)) * 4) }}>{b.rotulo}</div>
        </React.Fragment>);
      })}
      {linha && <>
        <svg width={1080} height={1000} style={{ position: "absolute", left: 0, top: 0 }}>
          <polyline points={pontos} fill="none" stroke={cor} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - desenho} />
        </svg>
        {q.barras.map((b, i) => {
          const chega = 0.35 + (0.4 + 0.32 * n) * (i / Math.max(1, n - 1)), e = m(t, chega, "estalo");
          return (<React.Fragment key={i}>
            <Som nome="pop" em={chega} vol={0.2} />
            <div style={{ position: "absolute", left: cx(i) - 22, top: BASE - alt(i) - 22, width: 44, height: 44, borderRadius: 22, background: i === d && t > ck ? AMARELO : "white",
              border: "6px solid #0b0b0b", transform: `scale(${e * (i === d && t > ck ? 1.3 + 0.1 * Math.sin(t * 8) : 1)})` }} />
            <div style={{ position: "absolute", left: cx(i) - 160, width: 320, top: BASE - alt(i) - 96, textAlign: "center", ...txt(48, "white"), opacity: cl((t - chega - 0.1) * 4) }}>{rot(b)}</div>
            <div style={{ position: "absolute", left: cx(i) - slot / 2, width: slot, top: BASE + 22, textAlign: "center", ...txt(36, "rgba(255,255,255,0.85)", 700), opacity: cl((t - chega) * 4) }}>{b.rotulo}</div>
          </React.Fragment>);
        })}
      </>}
      {/* o balão que o clique abre */}
      {q.nota && t > ck && <div style={{ position: "absolute", left: Math.min(Math.max(cx(d) - 300, 30), 450), top: Math.max(TOPO - 150, BASE - alt(d) - 260), width: 600,
        ...caixa(AMARELO), padding: "18px 24px", ...txt(46, COR.tinta), textAlign: "center", transform: `scale(${m(t, ck + 0.05, "estalo")})`, transformOrigin: "50% 100%" }}>{q.nota}</div>}
      <Cursor pts={pts} />
    </AbsoluteFill>
  );
};

// 26/11: os CARDS. Até 4 cartões que giram para dentro (1 a 3 em coluna, 4 em grade), cada um com ícone, título e valor;
// o mouse clica em cada um e ele ganha a cor e o selo ✓ (bom) ou ✗ (ruim), ou acende em amarelo (neutro).
const Cards: React.FC<{ q: Extract<Quadro, { tipo: "cards" }> }> = ({ q }) => {
  const t = useT(); const n = Math.min(4, q.cards.length), grade = n === 4, passo = q.passo ?? 1.0;
  const W = grade ? 450 : 940, H = grade ? 300 : 190, G = grade ? 50 : 28, TIT = q.titulo ? 130 : 0;
  const linhas = grade ? 2 : n, top0 = (H_QUADRO - (TIT + linhas * H + (linhas - 1) * G)) / 2;
  const pos = (i: number) => ({ x: grade ? 60 + (i % 2) * (W + 60) : 70, y: top0 + TIT + (grade ? Math.floor(i / 2) : i) * (H + G) });
  const tempos: { a: number; ck: number }[] = [];
  q.cards.slice(0, n).forEach((c, i) => { const a = c.em ?? 0.3 + i * passo; tempos.push({ a, ck: Math.max(a + 0.55, (tempos[i - 1]?.ck ?? 0) + 0.45) }); });
  const pts: Pt[] = [{ t: tempos[0]?.a ?? 0.3, x: 1060, y: 990 }, ...tempos.map((tp, i) => ({ t: tp.ck, x: pos(i).x + W - 120, y: pos(i).y + H - 70, c: true }))];
  return (
    <AbsoluteFill>
      {q.titulo && <div style={{ position: "absolute", left: 40, right: 40, top: top0, height: TIT - 20, display: "flex", alignItems: "center", justifyContent: "center",
        ...txt(64, AMARELO), textAlign: "center", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      {q.cards.slice(0, n).map((c, i) => {
        const { a, ck } = tempos[i], e = m(t, a, "estalo"), feito = t >= ck, { x, y } = pos(i);
        const cor = c.ok === undefined ? AMARELO : c.ok ? COR.verde : COR.vermelho;
        const pulso = feito ? 1 + 0.06 * Math.sin(cl((t - ck) / 0.25) * Math.PI) : 1 + 0.012 * Math.sin(t * 3 + i);
        return (
          <div key={i} style={{ position: "absolute", left: x, top: y, width: W, height: H, perspective: 1200 }}>
            <Som nome="card" em={a} vol={0.3} /><Som nome={c.ok === undefined ? "sparkle" : c.ok ? "ding" : "warning"} em={ck + 0.05} vol={0.32} />
            <div style={{ width: "100%", height: "100%", ...caixa(COR.branco), borderColor: feito ? cor : COR.tinta, borderWidth: feito ? 10 : 7, boxSizing: "border-box",
              display: "flex", flexDirection: grade ? "column" : "row", alignItems: "center", justifyContent: grade ? "center" : "flex-start", gap: grade ? 8 : 28,
              padding: grade ? 16 : "0 30px", opacity: cl(e * 2), transform: `rotateY(${(1 - e) * 95}deg) translateY(${(1 - e) * 80}px) scale(${pulso})`,
              boxShadow: feito ? `0 0 28px ${cor}, 12px 12px 0 #000` : "12px 12px 0 #000" }}>
              {c.emoji && <div style={{ width: grade ? 96 : 130, height: grade ? 96 : 130, borderRadius: 26, background: feito ? cor : "#FFE9A8", flexShrink: 0,
                display: "flex", alignItems: "center", justifyContent: "center" }}><Emoji e={c.emoji} tam={grade ? 70 : 96} estilo={{ transform: `rotate(${flutua(t, 6, 2.4 + i)}deg)` }} /></div>}
              <div style={{ display: "flex", flexDirection: "column", alignItems: grade ? "center" : "flex-start", gap: 4, textAlign: grade ? "center" : "left" }}>
                <div style={{ ...txt(grade ? 40 : 46, COR.tinta, 700) }}>{c.t}</div>
                {c.valor && <div style={{ ...txt(grade ? 58 : 70, c.ok === false ? COR.vermelho : c.ok ? COR.verde : COR.tinta), whiteSpace: "nowrap" }}>{c.valor}</div>}
              </div>
            </div>
            {c.ok !== undefined && <Selo em={ck} ok={c.ok} tam={86} estilo={{ right: -26, top: -30 }} />}
          </div>);
      })}
      <Cursor pts={pts} />
    </AbsoluteFill>
  );
};

// a pergunta: o mouse clica na resposta (o botão acende com ✓), vai à caixa de comentário, a resposta se digita sozinha e o
// mouse clica em enviar (o botão fica verde com ✓ e sobe um +1). É o convite a comentar mostrado, não só dito.
const Pergunta: React.FC<{ q: Extract<Quadro, { tipo: "pergunta" }> }> = ({ q }) => {
  const t = useT(); const ops = q.opcoes ?? [], n = ops.length;
  const BW = n === 1 ? 440 : 300, BG = 40, rowW = n * BW + Math.max(0, n - 1) * BG, L0 = (960 - rowW) / 2;
  const escolhe = 1.6, caixaC = n ? 2.35 : 1.4, resp = q.resposta ?? ops[0] ?? "QUERO", digita = caixaC + 0.15, fimDig = digita + 0.09 * resp.length, envia = fimDig + 0.55;
  const pts: Pt[] = [{ t: 0.9, x: 1000, y: 520 }, ...(n ? [{ t: escolhe, x: L0 + BW / 2 + 20, y: 80, c: true }] : []), { t: caixaC, x: 330, y: 280, c: true }, { t: envia, x: 870, y: 280, c: true }];
  const escrito = resp.slice(0, Math.floor(cl((t - digita) / Math.max(0.01, fimDig - digita)) * resp.length + 0.0001));
  const enviado = t >= envia;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 46, padding: "0 50px" }}>
      <Som nome="pop" em={0.1} />{n > 0 && <Som nome="ding" em={escolhe + 0.05} vol={0.3} />}
      <Som nome="keyboard" em={digita} vol={0.3} /><Som nome="kaching" em={envia + 0.05} vol={0.3} />
      <Emoji e={q.emoji ?? "💬"} tam={200} estilo={{ transform: `scale(${m(t, 0, "estalo")}) rotate(${flutua(t, 8, 3)}deg) translateY(${Math.abs(Math.sin(t * 4)) * -16}px)` }} />
      <div style={{ ...caixa(), padding: "30px 44px", position: "relative", transform: `scale(${0.6 + 0.4 * m(t, 0.1, "estalo")}) rotate(${flutua(t, 1.2, 2)}deg)` }}>
        <div style={{ ...txt(64, COR.tinta), textAlign: "center" }}>{q.texto}</div>
        <div style={{ position: "absolute", left: 80, bottom: -44, width: 0, height: 0, borderLeft: "30px solid transparent", borderRight: "30px solid transparent", borderTop: `44px solid ${COR.tinta}` }} />
      </div>
      <div style={{ position: "relative", width: 960, height: 340 }}>
        {ops.map((o, i) => {
          const marcado = i === 0 && t >= escolhe, apagado = i > 0 && t >= escolhe;
          return (<div key={i} style={{ position: "absolute", left: L0 + i * (BW + BG), top: 10, width: BW, height: 130, boxSizing: "border-box",
            ...caixa(marcado ? AMARELO : i ? COR.vermelho : COR.verde), display: "flex", alignItems: "center", justifyContent: "center", ...txt(70, marcado ? COR.tinta : "white"),
            opacity: apagado ? 0.45 : 1, transform: `scale(${m(t, 0.6 + i * 0.25, "estalo") * (marcado ? 1 + 0.08 * Math.sin(cl((t - escolhe) / 0.3) * Math.PI) : 1)})` }}>
            <Som nome="pop" em={0.6 + i * 0.25} vol={0.25} />{o}
            {marcado && <Selo em={escolhe} ok tam={80} estilo={{ right: -30, top: -34 }} />}
          </div>);
        })}
        {/* a caixa de comentário */}
        <div style={{ position: "absolute", left: 40, top: 210, width: 880, height: 110, borderRadius: 55, background: "white", border: `6px solid ${t >= caixaC ? AMARELO : "#0b0b0b"}`,
          boxSizing: "border-box", display: "flex", alignItems: "center", padding: "0 34px", opacity: m(t, n ? 1.0 : 0.4), transform: `translateY(${(1 - m(t, n ? 1.0 : 0.4)) * 60}px)` }}>
          <div style={{ ...txt(50, escrito ? COR.tinta : "#9A9A9A", escrito ? 800 : 600), whiteSpace: "nowrap" }}>
            {escrito || (t < caixaC ? "Adicione um comentário..." : "")}
            {t >= caixaC && !enviado && Math.floor(t * 3) % 2 === 0 && <span style={{ color: COR.azul }}>|</span>}
          </div>
          <div style={{ position: "absolute", right: 14, top: 9, width: 80, height: 80, borderRadius: 40, background: enviado ? COR.verde : "#C9C9C9",
            display: "flex", alignItems: "center", justifyContent: "center", ...txt(enviado ? 54 : 44, "white"), transform: `scale(${enviado ? m(t, envia, "estalo") : 1})` }}>{enviado ? "✓" : "➤"}</div>
          {enviado && <div style={{ position: "absolute", right: -10, top: -70, ...txt(66, AMARELO), opacity: cl(1.6 - (t - envia)), transform: `translateY(${-(t - envia) * 60}px)`, textShadow: "4px 4px 0 #000" }}>+1</div>}
        </div>
        <div style={{ position: "absolute", left: 0, right: 0, top: 150, textAlign: "center", ...txt(44, AMARELO, 700), opacity: m(t, 1.0) }}>👇 responde nos comentários</div>
        <Cursor pts={pts} />
      </div>
    </AbsoluteFill>
  );
};

// inscrever: o mouse clica em INSCREVA-SE (fica cinza, INSCRITO ✓), depois no sino (toca e acende) e no like (fica azul, +1)
const Inscrever: React.FC<{ q: Extract<Quadro, { tipo: "inscrever" }> }> = ({ q }) => {
  const t = useT(); const c1 = 1.0, c2 = 1.65, c3 = 2.3;
  const sino = t > c2 ? Math.sin((t - c2) * 25) * 24 * Math.max(0, 1 - (t - c2) / 1.2) : 0;
  const pts: Pt[] = [{ t: 0.35, x: 1000, y: 420 }, { t: c1, x: 300, y: 110, c: true }, { t: c2, x: 640, y: 110, c: true }, { t: c3, x: 810, y: 110, c: true }];
  const bola = (x: number, on: boolean, cor: string): React.CSSProperties => ({ position: "absolute", left: x, top: 30, width: 130, height: 130, borderRadius: 65,
    background: on ? cor : "rgba(255,255,255,0.12)", border: `6px solid ${on ? "white" : "rgba(255,255,255,0.5)"}`, boxSizing: "border-box",
    display: "flex", alignItems: "center", justifyContent: "center", fontSize: 74 });
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 50 }}>
      <Som nome="pop" em={0.05} /><Som nome="ding" em={c1 + 0.08} /><Som nome="sparkle" em={c2 + 0.05} /><Som nome="pop" em={c3 + 0.05} />
      <div style={{ ...txt(64, "white"), textAlign: "center", padding: "0 60px", transform: `scale(${m(t, 0, "estalo")})` }}>{q.texto ?? "Todo dia tem Plantão do Tião!"}</div>
      <div style={{ position: "relative", width: 900, height: 200, transform: `scale(${m(t, 0.1, "estalo")})` }}>
        <div style={{ position: "absolute", left: 40, top: 30, width: 480, height: 130, boxSizing: "border-box", ...caixa(t > c1 ? "#E9E9E9" : "#E62117"),
          display: "flex", alignItems: "center", justifyContent: "center", ...txt(64, t > c1 ? "#333" : "white"),
          transform: `scale(${t > c1 && t < c1 + 0.15 ? 0.9 : 1})` }}>{t > c1 ? "INSCRITO ✓" : "INSCREVA-SE"}</div>
        <div style={bola(560, t > c2, AMARELO)}><span style={{ display: "inline-block", transform: `rotate(${sino}deg)`, transformOrigin: "50% 10%" }}>🔔</span></div>
        <div style={bola(730, t > c3, "#1E88E5")}><span style={{ display: "inline-block", transform: `scale(${t > c3 ? 1 + 0.35 * Math.sin(cl((t - c3) / 0.35) * Math.PI) : 1})` }}>👍</span></div>
        {t > c3 && <div style={{ position: "absolute", left: 760, top: -60, ...txt(70, AMARELO), opacity: cl(1.6 - (t - c3)), transform: `translateY(${-(t - c3) * 60}px)`, textShadow: "4px 4px 0 #000" }}>+1</div>}
        <Cursor pts={pts} />
      </div>
    </AbsoluteFill>
  );
};

const Legenda: React.FC<{ palavras: Palavra[] }> = ({ palavras }) => {
  const t = useT();
  const blocos: Palavra[][] = []; let cur: Palavra[] = [];
  palavras.forEach((w) => { cur.push(w); if (cur.length === 3 || /[.!?:]$/.test(w[2])) { blocos.push(cur); cur = []; } });
  if (cur.length) blocos.push(cur);
  const b = blocos.find((x, i) => t >= x[0][0] && t < (blocos[i + 1]?.[0][0] ?? x[x.length - 1][1] + 0.6));
  if (!b) return null;
  const e = m(t, b[0][0], "estalo");
  return (
    <div style={{ position: "absolute", left: 30, right: 30, top: Y_LEG, display: "flex", justifyContent: "center", flexWrap: "wrap", gap: "0 22px",
      transform: `scale(${0.8 + 0.2 * e})` }}>
      {b.map((w, i) => {
        const agora = t >= w[0] && t < w[1] + 0.05, fala = t >= w[0], num = /\d|R\$|%/.test(w[2]);
        const pulo = agora ? 1 + 0.14 * Math.sin(cl((t - w[0]) / 0.18) * Math.PI / 2) : 1;
        return <span key={i} style={{ display: "inline-block", ...txt(90, num ? AMARELO : fala ? "white" : "rgba(255,255,255,0.5)"), WebkitTextStroke: "3px #0b0b0b",
          textShadow: "0 6px 0 #0b0b0b", paintOrder: "stroke fill", transform: `scale(${pulo}) translateY(${agora ? -6 : 0}px)`,
          background: agora ? "rgba(214,40,40,0.9)" : "transparent", borderRadius: 14, padding: "0 10px" }}>{w[2]}</span>;
      })}
    </div>
  );
};

// 26/11 (Ed viu no TikTok a faixa cortada na capa, «ANAL TIÃO POUPADOR»): o TikTok escolhe sozinho o quadro da capa, então a
// faixa não corre mais. Mostra um pedaço inteiro de cada vez (até 30 letras), que entra deslizando e fica parado: qualquer
// quadro que vire capa mostra uma frase completa.
const pedacos = (texto: string) => {
  const out: string[] = [];
  for (const frase of texto.split("•").map((f) => f.trim()).filter(Boolean)) {
    let atual = "";
    for (const p of frase.split(/\s+/)) {
      if (atual && (atual + " " + p).length > 30) { out.push(atual); atual = p; } else atual = atual ? atual + " " + p : p;
    }
    if (atual) out.push(atual);
  }
  return out.length ? out : [texto];
};
const Faixa: React.FC<{ texto: string; rotulo: string }> = ({ texto, rotulo }) => {
  const t = useT(); const ps = pedacos(texto); const CADA = 2.6;
  const i = Math.floor(t / CADA) % ps.length, dentro = (t % CADA) / 0.3;
  const x = dentro >= 1 ? 0 : 60 * (1 - dentro) * (1 - dentro), op = Math.min(1, 0.4 + dentro);
  return (
    <div style={{ position: "absolute", left: 0, right: 0, top: Y_FAIXA, height: 84, background: AZUL, borderTop: `6px solid ${AMARELO}`, overflow: "hidden" }}>
      <div style={{ position: "absolute", left: 260, right: 0, top: 0, bottom: 0, display: "flex", alignItems: "center", justifyContent: "center",
        whiteSpace: "nowrap", transform: `translateX(${x}px)`, opacity: op, ...txt(Math.min(44, Math.floor(1500 / ps[i].length)), "white", 700) }}>{ps[i]}</div>
      <div style={{ position: "absolute", left: 0, top: 0, bottom: 0, width: 260, background: VERMELHO, display: "flex", alignItems: "center", justifyContent: "center", ...txt(42, "white") }}>{rotulo}</div>
    </div>
  );
};

export const PlantaoShort: React.FC<DadosPlantao> = (d) => {
  const { fps } = useVideoConfig();
  const qs = [...d.quadros].sort((a, b) => a.ini - b.ini); const batidas = qs.map((q) => q.ini);
  return (
    <AbsoluteFill style={{ background: AZUL, fontFamily, overflow: "hidden" }}>
      <Fundo batidas={batidas} />
      <div style={{ position: "absolute", left: 0, right: 0, top: Y_QUADRO, height: H_QUADRO }}>
        {qs.map((q, i) => {
          const de = Math.round(q.ini * fps), ate = Math.round((qs[i + 1]?.ini ?? d.fim + 0.6) * fps);
          return (
            <Sequence key={i} from={de} durationInFrames={Math.max(1, ate - de)} layout="none">
              <Som nome="slide" em={0} vol={0.22} />
              <Golpe treme={q.tipo === "numero" ? 1.35 : q.tipo === "compara" ? 1.4 : undefined}>
                {q.tipo === "manchete" && <Manchete q={q} primeiro={i === 0} />}{q.tipo === "numero" && <Numero q={q} />}{q.tipo === "lista" && <Lista q={q} />}
                {q.tipo === "compara" && <Compara q={q} />}{q.tipo === "pergunta" && <Pergunta q={q} />}{q.tipo === "inscrever" && <Inscrever q={q} />}
                {q.tipo === "grafico" && <Grafico q={q} />}{q.tipo === "cards" && <Cards q={q} />}
              </Golpe>
            </Sequence>);
        })}
      </div>
      {qs.map((q, i) => <Sequence key={"c" + i} from={Math.round(q.ini * fps)} durationInFrames={6} layout="none"><Clarao /></Sequence>)}
      <Topo fim={d.fim} batidas={batidas} />
      <Legenda palavras={d.palavras} />
      <Faixa rotulo={d.rotulo ?? "ASSISTA"} texto={d.faixa ?? "ASSISTA À HISTÓRIA INTEIRA NO CANAL TIÃO POUPADOR   •   SE INSCREVE E DEIXA O SEU LIKE!   •   "} />
      <Audio src={staticFile(d.voz)} />
      {/* a música de alerta do Tião Conversa (Interloper), presente como num plantão de jornal */}
      {d.musica && <Audio src={staticFile(d.musica)} volume={d.volMusica ?? 0.3} />}
      <Som nome="warning" em={0} vol={0.3} />
    </AbsoluteFill>
  );
};
