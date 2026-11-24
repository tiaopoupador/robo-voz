// Video de QUALQUER numero: recebe os dados de fora (--props=public/vNN/props.json, feito pelo fabrica/montar.py).
import React from "react";
import { Mistura, DUR_TRANS, SOM_TRANS, Trans } from "../motion/efeitos/Transicoes";
import { LuzCinema, PoeiraLenta, PontosDeLuz, Chuva, Brasas, BrilhoDourado, Tensao, FILTRO_PASSADO, BordaPassado } from "../motion/efeitos/Acabamento";
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola, MOLAS } from "../mola";
import { Balao, Barras, Calendario, Carimbo, Cita, Conta, COR, Etiqueta, Frase, LinhaTempo, Numero, reais } from "../motion/kit";
import { Balanca, Botao, Celular, Divide, FraseTopo, Grade, Grafico, Icones, Lista, Pessoas, Pizza, Placa, Torre, Trinca } from "../motion/kit2";
import { TelaFinalNova } from "../motion/TelaFinalNova";
import { VinhetaNova } from "../motion/VinhetaNova";  // 19/11: entra no meio do video, depois do "Vamos começar?" (VINHETA no cenas.py)  // Ed 13/11: «pode» (a TelaFinal antiga fica no arquivo, fora de uso)
import { FotoNota } from "../motion/fotonota";
import { Brilho, Check, Reacao, tremor, Voa, Xis } from "../motion/reacoes";
import { Acao, Plantao, PLANTAO_ALTURA } from "../motion/Plantao";
import { Conversa, OndaCtx, EstiloCtx } from "../motion/Conversa";
import { CenaTurma } from "../motion/boneco/CenaTurma";  // 23/11: o longo so motion (05): a turma viva no cenario

const { fontFamily } = loadFont("normal", { weights: ["800"] });
type Cena = { ini: number; k: string; [x: string]: any };
type Efeito = { src: string; ini: number; dur: number; vol: number; fi: number; fo: number };
type Barra = { ini: number; dur: number; frases: string[]; acoes?: Acao[] };
export type Dados = { pasta: string; fim: number; tela: number; cenas: Cena[]; legendas: [number, number, string][]; efeitos: Efeito[]; barras?: Barra[]; onda?: number[]; acabamento?: boolean; ondaEstilo?: string; selo?: string };
export const VAZIO: Dados = { pasta: "v02", fim: 10, tela: 0, cenas: [], legendas: [], efeitos: [] };

const formato = (c: Cena) => {
  const suf = c.suf ?? "";
  // 21/11: 50000 virava «50000»; de 10 mil para cima leva o ponto (os anos, como 1990, ficam sem ponto)
  if (c.fmt === "int") return (v: number) => (Math.abs(c.valor ?? v) >= 10000 ? Math.round(v).toLocaleString("pt-BR") : String(Math.round(v))) + suf;
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
  const [ew, ez] = MOLAS.estalo; const e = c.entra ? 1 : mola(t, ew, ez);  // com transicao propria, sem o chicote
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
    case "turma": return <CenaTurma c={c as any} dur={dur} />;
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
    case "final": return <TelaFinalNova />;
    case "vinheta": return <VinhetaNova />;
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

// clima da cena (Ed, 18/11/2026), sempre sutil: entra em 0,6 s; o passado e «lembranca» (cor apagada, bordas claras)
const ComClima: React.FC<{ clima: string; t0: number; children: React.ReactNode }> = ({ clima, t0, children }) => {
  const t = useCurrentFrame() / useVideoConfig().fps, f = Math.min(1, t / 0.6);
  const Efeito = ({ lenta: PoeiraLenta, luz: PontosDeLuz, chuva: Chuva, brasas: Brasas, brilho: BrilhoDourado, tensao: Tensao } as Record<string, React.FC<{ t: number }>>)[clima];
  return (
    <AbsoluteFill>
      <AbsoluteFill style={clima === "passado" ? { filter: FILTRO_PASSADO.memoria } : undefined}>{children}</AbsoluteFill>
      {clima === "passado" && <AbsoluteFill style={{ opacity: f }}><BordaPassado tipo="memoria" t={t} /></AbsoluteFill>}
      {Efeito && <AbsoluteFill style={{ opacity: f, pointerEvents: "none" }}><Efeito t={t + t0} /></AbsoluteFill>}
    </AbsoluteFill>
  );
};
// a entrada da cena com uma das 6 transicoes: nos primeiros instantes mistura a cena de antes (a) com a nova (b)
const Entrada: React.FC<{ tipo: Trans; a: React.ReactNode; b: React.ReactNode }> = ({ tipo, a, b }) => {
  const t = useCurrentFrame() / useVideoConfig().fps, td = DUR_TRANS[tipo];
  return t < td ? <Mistura tipo={tipo} p={t / td} a={a} b={b} /> : <>{b}</>;
};
const LuzGeral: React.FC = () => <LuzCinema t={useCurrentFrame() / useVideoConfig().fps} />;

export const Video: React.FC<Dados> = (dados) => {
  const { fps } = useVideoConfig();
  const CENAS = dados.cenas, FALA = dados.fim, FIM = FALA + (dados.tela ?? 0);
  const leg = dados.legendas, barras = dados.barras ?? [];
  const cenaEm = (t: number) => { let k: Cena | null = null; for (const c of CENAS) { if (c.ini <= t + 0.05) k = c; else break; } return k; };
  const sobBarra = (a: number, b: number) => barras.some((x) => a < x.ini + x.dur && b > x.ini);  // a legenda sobe por cima da barra
  return (
    <OndaCtx.Provider value={dados.onda ?? []}><EstiloCtx.Provider value={{ onda: dados.ondaEstilo ?? "barras", selo: dados.selo ?? "" }}>
    <AbsoluteFill style={{ backgroundColor: COR.tinta }}>
      {CENAS.map((c, i) => {
        // a cena antes da tela final dura mais 0,8 s: é ela que a onda amarela cobre ao entrar (por baixo, nunca um fundo vazio)
        const fim = i + 1 < CENAS.length ? CENAS[i + 1].ini + (CENAS[i + 1].k === "final" ? 0.8 : 0) : FIM;
        const de = Math.round(c.ini * fps), n = Math.max(1, Math.round(fim * fps) - de);
        const no = (j: number, nn: number) => { const x = CENAS[j]; const p = <Peca c={x} dur={nn / fps} lado={j % 2 ? -1 : 1} />; const cl = x.k === "conversa" && x.clima === "passado" ? "" : x.clima;  // 19/11: o Tião falando é sempre hoje; o passado só pinta a imagem da lembrança
        return cl ? <ComClima clima={cl} t0={x.ini}>{p}</ComClima> : p; };
        const atual = no(i, n);
        if (!c.entra || i === 0) return <Sequence key={i} from={de} durationInFrames={n}>{atual}</Sequence>;
        const dp = Math.round(CENAS[i - 1].ini * fps), np = de - dp + Math.round(DUR_TRANS[c.entra as Trans] * fps);
        const antes = <Sequence from={dp - de} durationInFrames={np}>{no(i - 1, de - dp)}</Sequence>;
        const som = SOM_TRANS[c.entra as Trans];
        return (
          <Sequence key={i} from={de} durationInFrames={n}>
            <Entrada tipo={c.entra} a={antes} b={atual} />
            {som && <Sequence durationInFrames={60} layout="none"><Audio src={staticFile(som[0])} volume={som[1]} /></Sequence>}
          </Sequence>
        );
      })}
      {dados.acabamento && <Sequence durationInFrames={Math.round(FALA * fps)} layout="none"><LuzGeral /></Sequence>}
      {leg.map(([ini, fim, txt], i) => {
        const prox = i + 1 < leg.length ? leg[i + 1][0] : FALA;
        const de = Math.round(ini * fps), ate = Math.round(Math.min(fim + 0.25, prox) * fps);
        // 18/11 (Ed: «o texto sobressai por cima do outro»): se a cena troca no meio da frase, a frase troca de jeito na mesma hora
        // (grande ao lado do Tião na conversa, embaixo nas outras cenas), para nunca ficar por cima de um número ou cartão
        const jeito = (t: number) => (cenaEm(t)?.k === "conversa" ? (cenaEm(t)?.lado ?? 1) : 0);
        // 20/11 (Ed: «a legenda da imagem anterior continua sendo mostrada na imagem seguinte»): nunca passa da troca de cena
        const troca = CENAS.find((c) => c.ini > ini + 0.02)?.ini ?? 1e9;
        const ac = Math.min(fim + 0.25, prox, Math.max(fim, troca - 0.04)); const corte = CENAS.find((c) => c.ini > ini && c.ini < ac && jeito(c.ini + 0.01) !== jeito(ini))?.ini;
        const peca = (a: number, b: number, g: number, k: string) => <Sequence key={k} from={Math.round(a * fps)} durationInFrames={Math.max(1, Math.round(b * fps) - Math.round(a * fps))}><Legenda texto={txt} acima={sobBarra(ini, fim) ? PLANTAO_ALTURA : 0} grande={g} /></Sequence>;
        if (corte === undefined) return peca(ini, ac, jeito(ini), "l" + i);
        return <React.Fragment key={"l" + i}>{peca(ini, corte, jeito(ini), "a")}{peca(corte, ac, jeito(corte + 0.01), "b")}</React.Fragment>;
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
    </EstiloCtx.Provider></OndaCtx.Provider>
  );
};
