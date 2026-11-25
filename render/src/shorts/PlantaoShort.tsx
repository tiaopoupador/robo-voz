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
  | { ini: number; tipo: "pergunta"; texto: string; opcoes?: string[]; emoji?: string }
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

const Lista: React.FC<{ q: Extract<Quadro, { tipo: "lista" }> }> = ({ q }) => {
  const t = useT(); const passo = q.passo ?? 1.2;
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 28, padding: "0 50px" }}>
      {q.titulo && <div style={{ ...txt(64, AMARELO), textAlign: "center", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      {q.itens.map((it, i) => {
        const a = it.em ?? 0.3 + i * passo, e = m(t, a, "estalo"), anel = cl((t - a - 0.2) / 0.45);
        return (
          <div key={i} style={{ ...caixa(), width: 960, display: "flex", alignItems: "center", gap: 26, padding: "24px 30px",
            transform: `translateX(${(1 - e) * (i % 2 ? 1100 : -1100)}px) rotate(${(1 - e) * (i % 2 ? 9 : -9)}deg) scale(${t > a + 0.2 ? 1 + 0.05 * Math.sin(cl((t - a - 0.2) / 0.25) * Math.PI) : 1})` }}>
            <Som nome="slide" em={a} vol={0.25} /><Som nome={it.ok ? "ding" : "warning"} em={a + 0.2} vol={0.3} />
            <div style={{ position: "relative", flexShrink: 0 }}>
              {anel > 0 && anel < 1 && <div style={{ position: "absolute", inset: -10 - 40 * anel, borderRadius: "50%", border: `6px solid ${it.ok ? COR.verde : COR.vermelho}`, opacity: 1 - anel }} />}
              <div style={{ width: 90, height: 90, borderRadius: 45, background: it.ok ? COR.verde : COR.vermelho, display: "flex", alignItems: "center", justifyContent: "center",
                ...txt(64, "white"), transform: `scale(${m(t, a + 0.2, "estalo")}) rotate(${(1 - m(t, a + 0.2)) * -90}deg)` }}>{it.ok ? "✓" : "✗"}</div>
            </div>
            <div style={{ ...txt(50, COR.tinta, 700) }}>{it.t}</div>
          </div>);
      })}
    </AbsoluteFill>
  );
};

const Compara: React.FC<{ q: Extract<Quadro, { tipo: "compara" }> }> = ({ q }) => {
  const t = useT(); const cor2 = q.ruim ? COR.vermelho : COR.verde; const b = 1.4;
  const risco = cl((t - 1.0) / 0.3), seta = m(t, 0.9, "estalo");
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 26 }}>
      <Som nome="pop" em={0.1} /><Som nome="slide" em={1.0} vol={0.3} /><Som nome={q.ruim ? "warning" : "kaching"} em={b} />
      {q.titulo && <div style={{ ...txt(60, AMARELO), textAlign: "center", padding: "0 60px", transform: `scale(${m(t, 0, "estalo")})` }}>{q.titulo}</div>}
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, transform: `scale(${m(t, 0.1, "estalo") * (1 - 0.18 * risco)})`, filter: `grayscale(${risco})`, opacity: 1 - 0.35 * risco }}>
        {q.rotuloDe && <div style={{ ...txt(44, "white", 700) }}>{q.rotuloDe}</div>}
        <div style={{ ...caixa(), padding: "22px 46px", position: "relative" }}>
          <div style={{ ...txt(110, COR.cinza), whiteSpace: "nowrap" }}>{q.de}</div>
          <div style={{ position: "absolute", left: 20, top: "50%", height: 12, width: `calc(${risco * 100}% - 40px)`, background: VERMELHO, borderRadius: 6, transform: "rotate(-8deg)" }} />
        </div>
      </div>
      <div style={{ ...txt(140, AMARELO), transform: `translateY(${(1 - seta) * -60 + Math.abs(Math.sin(t * 5)) * 12}px) scale(${seta})`, textShadow: "6px 6px 0 #000" }}>⬇</div>
      <div style={{ position: "relative", display: "flex", flexDirection: "column", alignItems: "center", gap: 10, transform: `scale(${(2 - m(t, b, "estalo")) * (t > b ? 1 : 0)}) rotate(${(1 - m(t, b)) * 10}deg)` }}>
        <Raios em={b + 0.1} cor={cor2} />
        {q.rotuloPara && <div style={{ ...txt(44, "white", 700) }}>{q.rotuloPara}</div>}
        <div style={{ ...caixa(), padding: "26px 54px" }}><div style={{ ...txt(130, cor2), whiteSpace: "nowrap" }}>{q.para}</div></div>
      </div>
    </AbsoluteFill>
  );
};

const Mao: React.FC<{ x: number; y: number; toque: number }> = ({ x, y, toque }) => {
  const t = useT(); const aperta = t > toque && t < toque + 0.2 ? 0.85 : 1;
  return <div style={{ position: "absolute", left: x, top: y, fontSize: 120, transform: `scale(${aperta})`, filter: "drop-shadow(4px 6px 0 #000)" }}>👆</div>;
};
const Pergunta: React.FC<{ q: Extract<Quadro, { tipo: "pergunta" }> }> = ({ q }) => {
  const t = useT(); const ops = q.opcoes ?? [];
  const alvo = Math.floor(Math.max(0, t - 1.2) / 0.9) % Math.max(1, ops.length);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 36, padding: "0 50px" }}>
      <Som nome="pop" em={0.1} />
      <Emoji e={q.emoji ?? "💬"} tam={220} estilo={{ transform: `scale(${m(t, 0, "estalo")}) rotate(${flutua(t, 8, 3)}deg) translateY(${Math.abs(Math.sin(t * 4)) * -16}px)` }} />
      <div style={{ ...caixa(), padding: "34px 44px", position: "relative", transform: `scale(${0.6 + 0.4 * m(t, 0.1, "estalo")}) rotate(${flutua(t, 1.2, 2)}deg)` }}>
        <div style={{ ...txt(66, COR.tinta), textAlign: "center" }}>{q.texto}</div>
        <div style={{ position: "absolute", left: 80, bottom: -44, width: 0, height: 0, borderLeft: "30px solid transparent", borderRight: "30px solid transparent", borderTop: `44px solid ${COR.tinta}` }} />
      </div>
      {ops.length > 0 && <div style={{ display: "flex", gap: 34, position: "relative" }}>
        {ops.map((o, i) => (
          <div key={i} style={{ ...caixa(i ? COR.vermelho : COR.verde), padding: "20px 56px", ...txt(70, "white"),
            transform: `scale(${m(t, 0.6 + i * 0.25, "estalo") * (t > 1.2 && alvo === i ? 1.12 : 1)})` }}>
            <Som nome="click" em={0.6 + i * 0.25} vol={0.3} />{o}</div>))}
        {t > 1.2 && <Mao x={alvo * 300 + 90} y={60} toque={1.2 + Math.floor((t - 1.2) / 0.9) * 0.9} />}
      </div>}
      {/* 25/11 (Ed: «tem que pedir para se inscrever, deixar comentario»): o lembrete que a resposta vai nos comentários */}
      <div style={{ ...txt(48, AMARELO, 700), opacity: m(t, 1.0), transform: `translateY(${(1 - m(t, 1.0)) * 30}px)` }}>👇 responde nos comentários</div>
    </AbsoluteFill>
  );
};

const Inscrever: React.FC<{ q: Extract<Quadro, { tipo: "inscrever" }> }> = ({ q }) => {
  const t = useT(); const clique = 1.1, feito = t > clique; const sino = feito ? Math.sin((t - clique) * 25) * 22 * Math.max(0, 1 - (t - clique) / 1.2) : 0;
  const maoX = 140 + 300 * cl((t - 0.3) / 0.7);
  return (
    <AbsoluteFill style={{ justifyContent: "center", alignItems: "center", gap: 40 }}>
      <Som nome="pop" em={0.05} /><Som nome="click" em={clique} /><Som nome="ding" em={clique + 0.15} />
      <div style={{ ...txt(64, "white"), textAlign: "center", padding: "0 60px", transform: `scale(${m(t, 0, "estalo")})` }}>{q.texto ?? "Todo dia tem Plantão do Tião!"}</div>
      <div style={{ display: "flex", alignItems: "center", gap: 30, position: "relative" }}>
        <div style={{ ...caixa(feito ? "#E9E9E9" : "#E62117"), padding: "26px 54px", ...txt(70, feito ? "#333" : "white"),
          transform: `scale(${m(t, 0.1, "estalo") * (t > clique && t < clique + 0.15 ? 0.9 : 1)})` }}>{feito ? "INSCRITO ✓" : "INSCREVA-SE"}</div>
        <div style={{ fontSize: 120, transform: `scale(${m(t, 0.3, "estalo")}) rotate(${sino}deg)`, transformOrigin: "50% 10%" }}>🔔</div>
        <div style={{ position: "absolute", right: -60, top: -60, ...txt(70, AMARELO), opacity: feito ? cl(1.6 - (t - clique)) : 0, transform: `translateY(${-(t - clique) * 60}px)` }}>+1</div>
        {t < clique + 0.6 && <Mao x={maoX} y={70} toque={clique} />}
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
