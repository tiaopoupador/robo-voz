// Video de QUALQUER numero: recebe os dados de fora (--props=public/vNN/props.json, feito pelo fabrica/montar.py).
import React from "react";
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola, MOLAS } from "../mola";
import { Balao, Barras, Calendario, Carimbo, Cita, Conta, COR, Etiqueta, Frase, LinhaTempo, Numero, reais } from "../motion/kit";
import { Balanca, Botao, Celular, Divide, FraseTopo, Grade, Grafico, Icones, Lista, Pessoas, Pizza, Placa, Torre, Trinca } from "../motion/kit2";
import { TelaFinal } from "../motion/TelaFinal";
import { FotoNota } from "../motion/fotonota";
import { Brilho, Check, Reacao, tremor, Voa, Xis } from "../motion/reacoes";
import { Acao, Plantao, PLANTAO_ALTURA } from "../motion/Plantao";
import { Conversa, OndaCtx } from "../motion/Conversa";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
type Cena = { ini: number; k: string; [x: string]: any };
type Efeito = { src: string; ini: number; dur: number; vol: number; fi: number; fo: number };
type Barra = { ini: number; dur: number; frases: string[]; acoes?: Acao[] };
export type Dados = { pasta: string; fim: number; tela: number; cenas: Cena[]; legendas: [number, number, string][]; efeitos: Efeito[]; barras?: Barra[]; onda?: number[] };
export const VAZIO: Dados = { pasta: "v02", fim: 10, tela: 0, cenas: [], legendas: [], efeitos: [] };

const formato = (c: Cena) => {
  const suf = c.suf ?? "";
  if (c.fmt === "int") return (v: number) => Math.round(v) + suf;
  if (c.fmt === "num") return (v: number) => v.toLocaleString("pt-BR", { minimumFractionDigits: c.casas, maximumFractionDigits: c.casas }) + suf;
  if (c.fmt === "pct") return (v: number) => v.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 }) + "%";
  if (c.fmt === "nada") return () => "";
  return (v: number) => reais(v, c.casas ?? 0);
};

// imagem ou video com camera lenta e entrada em chicote (como no piloto aprovado)
const Camera: React.FC<{ c: Cena; dur: number; lado: number; children?: React.ReactNode }> = ({ c, dur, lado, children }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const p = mola(t, 3.5 / dur, 1);
  const esc = c.mov === "entra" ? 1.0 + 0.08 * p : c.mov === "sai" ? 1.1 - 0.08 * p : 1.08;
  const dx = c.mov === "esq" ? 2.5 - 5 * p : c.mov === "dir" ? -2.5 + 5 * p : 0;
  const [ew, ez] = MOLAS.estalo; const e = mola(t, ew, ez);
  const entraX = (1 - e) * 9 * lado, borrao = Math.max(0, (1 - e) * 22);
  const sustos = (c.ov ?? []).filter((o: any) => o.t === "xis" || (o.t === "reacao" && ["😱", "💥", "🤯"].includes(o.e))).map((o: any) => o.ini ?? 0.6);
  const [tx, ty] = tremor(t, sustos);
  const resto = (c.clip ?? 6) - (c.de ?? 0), ritmo = c.k === "vid" ? Math.max(0.5, Math.min(1, resto / dur)) : 1;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#1b1b1b" }}>
      <AbsoluteFill style={{ transform: `translate(${tx}px, ${ty}px) translateX(${dx + entraX}%) scale(${esc})`, filter: `blur(${borrao}px)` }}>
        {c.k === "vid"
          ? <OffthreadVideo src={staticFile(c.src)} muted playbackRate={ritmo} startFrom={Math.round((c.de ?? 0) * 30)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          : <Img src={staticFile(c.src)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
      </AbsoluteFill>
      {children}
    </AbsoluteFill>
  );
};

const PorCima: React.FC<{ o: any }> = ({ o }) => {
  switch (o.t) {
    case "placa": return <Placa x={o.x} y={o.y} texto={o.texto} cor={o.cor} fundo={o.fundo} tam={o.tam} ini={o.ini} />;
    case "etiqueta": return <Etiqueta x={o.x} y={o.y} texto={o.texto} cor={o.cor} ini={o.ini} />;
    case "carimbo": return <Carimbo x={o.x} y={o.y} texto={o.texto} cor={o.cor} ini={o.ini} />;
    case "balao": return <Balao x={o.x} y={o.y} texto={o.texto} lado={o.lado} ini={o.ini} />;
    case "frasetopo": return <FraseTopo texto={o.texto} pos={o.pos} ini={o.ini} />;
    case "lista": return <Lista x={o.x} y={o.y} itens={o.itens} riscar={o.riscar} ini={o.ini} />;
    case "trinca": return <Trinca x={o.x} y={o.y} />;
    case "reacao": return <Reacao x={o.x} y={o.y} e={o.e} ini={o.ini} />;
    case "brilho": return <Brilho x={o.x} y={o.y} ini={o.ini} />;
    case "xis": return <Xis x={o.x} y={o.y} ini={o.ini} />;
    case "check": return <Check x={o.x} y={o.y} ini={o.ini} />;
    case "voa": return <Voa x={o.x} y={o.y} ini={o.ini} />;
  }
  return null;
};

const Peca: React.FC<{ c: Cena; dur: number; lado: number }> = ({ c, dur, lado }) => {
  switch (c.k) {
    case "img": case "vid":
    case "hib": return <Camera c={c} dur={dur} lado={lado}>{(c.ov ?? []).map((o: any, i: number) => <PorCima key={i} o={o} />)}</Camera>;
    case "conversa": return <Conversa fundo={c.src} pose={c.pose} t0={c.ini} dur={dur} lado={c.lado ?? 1} />;
    case "frase": return <Frase texto={c.texto} sobre={c.sobre ?? undefined} escuro={c.escuro} emoji={c.emoji ?? undefined} />;
    case "num": return <Numero valor={c.valor} rotulo={c.rotulo ?? undefined} embaixo={c.embaixo ?? undefined} de={c.de} cor={c.cor} formato={formato(c)} emoji={c.emoji ?? undefined} />;
    case "conta": return <Conta titulo={c.titulo} linhas={c.linhas} ja={c.ja} total={c.total} neutro={c.neutro} passo={c.passo} />;
    case "cita": return <Cita nome={c.nome} ano={c.ano} onde={c.onde ?? undefined} achado={c.achado} fonte={c.fonte ?? undefined} emoji={c.emoji ?? undefined} />;
    case "barras": return <Barras titulo={c.titulo ?? undefined} itens={c.itens} formato={formato(c)} />;
    case "linha": return <LinhaTempo marcos={c.marcos} ativo={c.ativo} titulo={c.titulo ?? undefined} />;
    case "cal": return <Calendario mes={c.mes} ate={c.ate} marcados={Object.fromEntries(Object.entries(c.marcados).map(([d, v]) => [Number(d), v as any]))} />;
    case "icones": return <Icones titulo={c.titulo ?? undefined} itens={c.itens} />;
    case "graf": return <Grafico titulo={c.titulo} series={c.series} eixo={c.eixo} fim={c.fim} />;
    case "celular": return <Celular titulo={c.titulo} linhas={c.linhas} destaque={c.destaque} apaga={c.apaga} lado={c.lado} />;
    case "pizza": return <Pizza pct={c.pct} r={c.r} titulo={c.titulo} />;
    case "pessoas": return <Pessoas titulo={c.titulo} total={c.total} verm={c.verm} verde={c.verde} />;
    case "balanca": return <Balanca esq={c.esq} dir={c.dir} pesa={c.pesa} titulo={c.titulo} />;
    case "divide": return <Divide a={c.a} b={c.b} titulo={c.titulo} />;
    case "botao": return <Botao tipo={c.tipo} texto={c.texto} />;
    case "torre": return <Torre itens={c.itens} titulo={c.titulo} />;
    case "fotonota": return <FotoNota itens={c.itens} total={c.total} categoria={c.categoria} />;
    case "final": return <TelaFinal />;
    case "montagem": return <Montagem imgs={c.imgs} seg={c.seg ?? 0.45} />;
    case "grade": return <Grade total={c.total} cols={c.cols} titulo={c.titulo} ate={c.ate} cor={c.cor} rotuloFim={c.rotuloFim} corFim={c.corFim} />;
  }
  return <AbsoluteFill style={{ background: "red" }} />;
};

// montagem de tensao (Ed, 05/11): varias imagens muito rapidas, corte seco, um soco de zoom em cada uma
const Montagem: React.FC<{ imgs: string[]; seg: number }> = ({ imgs, seg }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const i = Math.floor(t / seg) % imgs.length, dentro = (t % seg) / seg;
  const [tx, ty] = tremor(t, [0.05]);
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#000" }}>
      <Img src={staticFile(imgs[i])} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `translate(${tx}px,${ty}px) scale(${1.12 - 0.08 * dentro})` }} />
      <AbsoluteFill style={{ background: "radial-gradient(circle, transparent 55%, rgba(0,0,0,0.55))" }} />
    </AbsoluteFill>
  );
};

// legenda (igual a do piloto): mola de texto, *palavra* em amarelo
const AMARELO = "#FFD43B";
const Legenda: React.FC<{ texto: string; acima?: number; grande?: number }> = ({ texto, acima = 0, grande = 0 }) => {
  const lado = acima ? -230 : 0;  // com a barra na tela, a legenda vai para a esquerda: o cartão animado fica no canto direito
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const [w, z] = MOLAS.texto; const m = mola(f / fps, w, z);
  const partes = texto.split(/(\*[^*]+\*)/g).filter(Boolean);
  if (grande) return (  // cena "Tião conversa": a frase grande do lado oposto ao Tião, como no Prosa que Rende
    <AbsoluteFill style={{ justifyContent: "center", alignItems: grande > 0 ? "flex-end" : "flex-start", padding: "0 110px 120px" }}>
      <div style={{ fontFamily, fontWeight: 800, fontSize: 112, lineHeight: 1.02, color: "white", textAlign: "center", width: 900,
        textShadow: "0 6px 30px rgba(0,0,0,0.6)", transform: `translateY(${(1 - m) * 30}px) scale(${0.94 + 0.06 * m})`, opacity: Math.min(1, m * 1.6) }}>
        {partes.map((p, i) => p.startsWith("*") ? <span key={i} style={{ color: AMARELO }}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}
      </div>
    </AbsoluteFill>
  );
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 92 + acima }}>
      <div style={{ fontFamily, fontWeight: 800, fontSize: 92, lineHeight: 1.05, color: "white", textAlign: "center", maxWidth: acima ? 1100 : 1500, marginLeft: lado * 2,
        WebkitTextStroke: "14px black", paintOrder: "stroke fill", transform: `translateY(${(1 - m) * 26}px) scale(${0.92 + 0.08 * m})`, opacity: Math.min(1, m * 1.6) }}>
        {partes.map((p, i) => p.startsWith("*") ? <span key={i} style={{ color: AMARELO }}>{p.slice(1, -1)}</span> : <span key={i}>{p}</span>)}
      </div>
    </AbsoluteFill>
  );
};

export const Video: React.FC<Dados> = (dados) => {
  const { fps } = useVideoConfig();
  const CENAS = dados.cenas, FALA = dados.fim, FIM = FALA + (dados.tela ?? 0);
  const leg = dados.legendas, barras = dados.barras ?? [];
  const cenaEm = (t: number) => { let k: Cena | null = null; for (const c of CENAS) { if (c.ini <= t + 0.05) k = c; else break; } return k; };
  const sobBarra = (a: number, b: number) => barras.some((x) => a < x.ini + x.dur && b > x.ini);  // a legenda sobe por cima da barra
  return (
    <OndaCtx.Provider value={dados.onda ?? []}>
    <AbsoluteFill style={{ backgroundColor: COR.tinta }}>
      {CENAS.map((c, i) => {
        const fim = i + 1 < CENAS.length ? CENAS[i + 1].ini : FIM;
        const de = Math.round(c.ini * fps), n = Math.max(1, Math.round(fim * fps) - de);
        return <Sequence key={i} from={de} durationInFrames={n}><Peca c={c} dur={n / fps} lado={i % 2 ? -1 : 1} /></Sequence>;
      })}
      {leg.map(([ini, fim, txt], i) => {
        const prox = i + 1 < leg.length ? leg[i + 1][0] : FALA;
        const de = Math.round(ini * fps), ate = Math.round(Math.min(fim + 0.25, prox) * fps);
        return <Sequence key={"l" + i} from={de} durationInFrames={Math.max(1, ate - de)}><Legenda texto={txt} acima={sobBarra(ini, fim) ? PLANTAO_ALTURA : 0} grande={cenaEm(ini)?.k === "conversa" ? (cenaEm(ini)?.lado ?? 1) : 0} /></Sequence>;
      })}
      {barras.map((b, i) => (
        <Sequence key={"b" + i} from={Math.round(b.ini * fps)} durationInFrames={Math.round(b.dur * fps)}><Plantao frases={b.frases} dur={b.dur} acoes={b.acoes} /></Sequence>
      ))}
      <Audio src={staticFile(dados.pasta + "/narracao.mp3")} />
      <Audio src={staticFile(dados.pasta + "/trilha.mp3")} volume={1} />
      {dados.efeitos.map((e, i) => {
        const n = Math.round(e.dur * fps);
        return (
          <Sequence key={"e" + i} from={Math.round(e.ini * fps)} durationInFrames={n} layout="none">
            <Audio src={staticFile(e.src)} loop volume={(f) => e.vol * Math.min(1, f / Math.max(1, e.fi * fps), (n - f) / Math.max(1, e.fo * fps))} />
          </Sequence>
        );
      })}
    </AbsoluteFill>
    </OndaCtx.Provider>
  );
};
