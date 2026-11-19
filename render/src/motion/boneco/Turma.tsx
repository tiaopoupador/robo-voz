// A turma VIVA (Ed, 19/11/2026: «vc agora tem que criar os motions, dar vida em cada personagem, todos com nota 10»).
// Cada personagem sai SEMPRE do desenho oficial dele (as poses que o Ed gerou, recortadas por
// banco/boneco-tiao/recortar_turma.py), nunca redesenhado. Por cima, so o que da vida:
//   respirar (o peito sobe, preso aos pes), balancar de leve, piscar (a palpebra desce com a cor da pele dele,
//   achada por banco/boneco-tiao/achar_rosto.py), entrar e trocar de pose com mola, tremer no susto, andar.
// Tudo e funcao do tempo (seek(t) puro).
import React from "react";
import { Img, staticFile } from "remotion";
import { mola } from "../../mola";
import TURMA from "../../../public/boneco/turma/turma.json";
import { Boca } from "./TiaoReal";
import { loadFont } from "@remotion/google-fonts/Baloo2";
const { fontFamily: FONTE } = loadFont("normal", { weights: ["800"] });

export type Pid = "tiao" | "sandra" | "marcos" | "valeria" | "cida" | "jessica" | "rafa" | "lourival" | "patricia";
// boca: [cx, y do labio de cima, meia largura, aberta no desenho, sorriso]; braco: o ombro onde o braco roda
// boca2: a boca do proprio desenho que abre (banco/boneco-tiao/boca_labio.py): o pedaco da boca em n aberturas
type Boca2 = { x: number; y: number; w: number; h: number; n: number; larg?: string[] };
type Info = { nome: string; tam: [number, number]; olhos?: number[][] | null; boca?: number[]; boca2?: Boca2 | null; sobr?: Boca2 | null; braco?: { eixo: [number, number] } };
export const info = (pid: Pid, cod: string): Info => (TURMA as any)[pid][cod];

const cl = (v: number) => Math.max(0, Math.min(1, v));
const h = (n: number) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const semente = (s: string) => [...s].reduce((a, c) => a + c.charCodeAt(0), 0);

// quando pisca: de 2,4 a 4,6 s entre uma e outra, as vezes duas seguidas (como gente)
export const piscadas = (seed: number, dur = 120): number[] => {
  const out: number[] = []; let t = 0.6 + 1.4 * h(seed);
  for (let i = 0; t < dur; i++) { out.push(t); if (h(seed + i * 3.3) > 0.82) out.push(t + 0.28); t += 2.4 + 2.2 * h(seed + i * 1.7); }
  return out;
};
const fecho = (t: number, q: number[]) => Math.max(0, ...q.map((c) => cl(1 - Math.abs(t - c) / 0.085)));

// a palpebra: desce de cima com a pele dele, a de baixo sobe um pouco, e o risco dos cilios vai na beira
const Palpebra: React.FC<{ o: number[]; p: number; esc: number }> = ({ o, p, esc }) => {
  if (p <= 0.02) return null;
  const [cx, cy, rx0, ry0, r = 220, g = 165, b = 125] = o; const rx = rx0 * 1.22, ry = ry0 * 1.25;
  const topo = cy - ry + 1.6 * ry * Math.min(1, p / 0.73);
  const baixo = cy + ry - 0.85 * ry * Math.min(1, p / 0.73);
  const linha = Math.min(topo, baixo);
  const id = `pp${Math.round(cx)}_${Math.round(cy)}`;
  const meia = (y: number) => rx * Math.sqrt(Math.max(0, 1 - ((y - cy) / ry) ** 2));
  const fechado = p >= 0.72; const yl = fechado ? cy + ry * 0.2 : linha; const w = fechado ? rx * 0.95 : meia(linha);
  const tinta = Math.max(2.5, 4 / esc);
  return (
    <g>
      <clipPath id={id}><ellipse cx={cx} cy={cy} rx={rx} ry={ry} /></clipPath>
      <g clipPath={`url(#${id})`}>
        <rect x={cx - rx} y={cy - ry - 2} width={rx * 2} height={Math.max(0, topo - (cy - ry) + 2)} fill={`rgb(${r},${g},${b})`} />
        <rect x={cx - rx} y={baixo} width={rx * 2} height={cy + ry - baixo + 2} fill={`rgb(${r},${g},${b})`} />
        {fechado && <rect x={cx - rx} y={cy - ry} width={rx * 2} height={ry * 2} fill={`rgb(${r},${g},${b})`} />}
      </g>
      <path d={`M ${cx - w} ${yl} Q ${cx} ${yl + ry * (fechado ? 0.45 : 0.25)} ${cx + w} ${yl}`} fill="none" stroke="#1B1310" strokeWidth={tinta * (fechado ? 1.2 : 1)} strokeLinecap="round" />
    </g>
  );
};

export type Vida = {
  t: number;            // tempo dentro do plano
  entra?: number;       // quando a pose aparece (mola de entrada); undefined = ja estava
  treme?: number;       // 0..1 susto
  respira?: number;     // forca da respiracao (1 = normal)
  pisca?: boolean;      // false = nao pisca (olho fechado, oculos escuros)
  espelho?: boolean;
  fala?: number;        // 0..1 a boca a abrir com a voz; undefined = a boca do desenho
  largura?: number;     // -1..1 boca redonda («ó») ou esticada («i»), lida da voz (fabrica/boca_voz.py)
  acento?: number;      // 0..1 a sílaba forte: a cabeça acompanha
  braco?: number;       // graus que o braco roda no ombro (so nas poses com braco separado)
  luz?: Luz;            // a luz do cenario no personagem (noite azulada, a lampada da varanda de um lado)
};
// A luz do cenario (Ed, 19/11: dar vida; sem isto, de noite o personagem parece recortado e colado).
// noite: o corpo escurece e puxa para o azul; varanda: a noite + a luz amarela da lampada batendo de um lado.
export type Luz = { tipo: "dia" | "noite" | "varanda"; lado?: 1 | -1; forca?: number };
// uma pose do personagem, de pe, presa pelos pes em (x, y) e com altura alt
export const Pose: React.FC<{ pid: Pid; cod: string; x: number; y: number; alt: number } & Vida> = ({ pid, cod, x, y, alt, t, entra, treme = 0, respira = 1, pisca = true, espelho, fala, braco, largura = 0, acento = 0, luz }) => {
  const q = info(pid, cod); const [w, hh] = q.tam; const esc = alt / hh; const wd = w * esc; const s = semente(pid + cod);
  const e = entra === undefined ? 1 : mola(t - entra, 11, 0.55);
  if (entra !== undefined && t < entra) return null;
  const resp = Math.sin(t * 2.25 + s), bal = Math.sin(t * 1.15 + s * 0.7);
  const tx = treme * 10 * Math.sin(t * 71), ty = treme * 6 * Math.cos(t * 83);
  const tf = [
    `translate(${tx}px, ${ty + (1 - e) * 40}px)`,
    `translateY(${-2 * (fala ?? 0) - 5 * acento}px) rotate(${0.55 * bal * respira + 0.7 * acento * (s % 2 ? 1 : -1) + 0.2 * Math.sin(t * 4.3 + s) * Math.min(1, (fala ?? 0) * 2)}deg)`,  // falando, a cabeça e o corpo batem nas sílabas fortes
    `scale(${(0.9 + 0.1 * e) * (espelho ? -1 : 1)}, ${(0.9 + 0.1 * e) * (1 + 0.009 * resp * respira)})`,
  ].join(" ");
  const p = pisca && q.olhos ? fecho(t, piscadas(s)) : 0;
  const falando = fala !== undefined && !!q.boca; const mexe = braco !== undefined && !!q.braco;
  const base = `boneco/turma/${pid}/${cod}${mexe ? "_corpo" : ""}${falando ? "_sb" : ""}.png`;
  const cheio: React.CSSProperties = { position: "absolute", inset: 0, width: "100%", height: "100%" };
  return (
    <div style={{ position: "absolute", left: x - wd / 2, top: y - alt, width: wd, height: alt, transformOrigin: "50% 100%", transform: tf, opacity: entra === undefined ? 1 : cl((t - entra) / 0.08) }}>
      <div style={{ position: "absolute", inset: 0, filter: filtroLuz(luz) }}>
      {mexe && <Img src={staticFile(`boneco/turma/${pid}/${cod}_braco.png`)} style={{ ...cheio, transformOrigin: `${(q.braco!.eixo[0] / w) * 100}% ${(q.braco!.eixo[1] / hh) * 100}%`, transform: `rotate(${braco}deg)` }} />}
      <Img src={staticFile(base)} style={cheio} />
      {acento > 0.2 && q.sobr && (() => {  // a sobrancelha sobe na sílaba forte (banco/boneco-tiao/sobrancelha.py)
        const b = q.sobr!; const lv = Math.min(b.n, Math.round(acento * b.n));
        if (lv < 1) return null;
        return <Img src={staticFile(`boneco/turma/${pid}/${cod}_s${lv}.png`)} style={{ position: "absolute", left: `${(b.x / w) * 100}%`, top: `${(b.y / hh) * 100}%`, width: `${(b.w / w) * 100}%`, height: `${(b.h / hh) * 100}%` }} />;
      })()}
      {((q.olhos && p > 0) || falando) && (
        <svg viewBox={`0 0 ${w} ${hh}`} width="100%" height="100%" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
          {q.olhos && p > 0 && q.olhos.map((o, i) => <Palpebra key={i} o={o} p={p} esc={esc} />)}
          {falando && (() => { const [bx, by, bw, ab, sor] = q.boca!; return <Boca cx={bx} cy={by + 0.09 * bw} mw={bw} aberta={Math.max(fala!, ab * 0.4)} sorriso={sor} esc={bw / 80} />; })()}
        </svg>
      )}
      {falando && pid === "tiao" && <Img src={staticFile(`boneco/turma/tiao/${cod}_bigode.png`)} style={cheio} />}
      {fala !== undefined && !q.boca && q.boca2 && (() => {
        const b = q.boca2!; const lv = Math.min(b.n, Math.round(Math.max(0, fala) * b.n * 1.1));
        if (lv < 1) return null;
        const lg = b.larg ? (largura < -0.35 ? "n" : largura > 0.35 ? "w" : "m") : "";
        return <Img src={staticFile(`boneco/turma/${pid}/${cod}_b${lv}${lg}.png`)} style={{ position: "absolute", left: `${(b.x / w) * 100}%`, top: `${(b.y / hh) * 100}%`, width: `${(b.w / w) * 100}%`, height: `${(b.h / hh) * 100}%` }} />;
      })()}
      </div>
      {luz && luz.tipo !== "dia" && <CorDaLuz luz={luz} src={staticFile(base)} />}
      {luz && luz.tipo !== "dia" && mexe && <CorDaLuz luz={luz} src={staticFile(`boneco/turma/${pid}/${cod}_braco.png`)} gira={{ eixo: q.braco!.eixo, w, hh, graus: braco! }} />}
    </div>
  );
};

// o braco a acenar (tchau) e a subir no brinde: so funcoes do tempo
export const aceno = (t: number, ini = 0, forca = 9) => (t < ini ? 0 : forca * Math.sin((t - ini) * 2 * Math.PI * 1.7) * Math.min(1, (t - ini) / 0.25));
export const brinde = (t: number, ini = 0, forca = 7) => {
  if (t < ini) return 0; const k = t - ini;
  return forca * (mola(k, 9, 0.45) - 0.35 * Math.max(0, Math.sin(Math.max(0, k - 0.5) * 9)) * Math.exp(-Math.max(0, k - 0.5) * 3));
};

const filtroLuz = (l?: Luz) => !l || l.tipo === "dia" ? undefined : `brightness(${1 - 0.36 * (l.forca ?? 1)}) contrast(${1 + 0.14 * (l.forca ?? 1)}) saturate(${1 - 0.12 * (l.forca ?? 1)})`;
// a cor da luz, so onde o personagem esta desenhado (a propria pose serve de mascara)
const CorDaLuz: React.FC<{ luz: Luz; src: string; gira?: { eixo: [number, number]; w: number; hh: number; graus: number } }> = ({ luz, src, gira }) => {
  const f = luz.forca ?? 1; const lado = luz.lado ?? 1;
  const base: React.CSSProperties = { position: "absolute", inset: 0,
    ...(gira ? { transformOrigin: `${(gira.eixo[0] / gira.w) * 100}% ${(gira.eixo[1] / gira.hh) * 100}%`, transform: `rotate(${gira.graus}deg)` } : {}) };
  const um = (m: string): React.CSSProperties => ({ WebkitMaskImage: m, maskImage: m, WebkitMaskSize: "100% 100%", maskSize: "100% 100%", WebkitMaskRepeat: "no-repeat", maskRepeat: "no-repeat" });
  // o contorno de luz: a pose menos ela mesma empurrada para longe da lampada = so a borda do lado da lampada
  const borda = (dx: number): React.CSSProperties => ({
    WebkitMaskImage: `url(${src}), url(${src})`, maskImage: `url(${src}), url(${src})`,
    WebkitMaskSize: "100% 100%, 100% 100%", maskSize: "100% 100%, 100% 100%", WebkitMaskRepeat: "no-repeat", maskRepeat: "no-repeat",
    WebkitMaskPosition: `0px 0px, ${-lado * dx}px 0px`, maskPosition: `0px 0px, ${-lado * dx}px 0px`,
    WebkitMaskComposite: "source-out", maskComposite: "subtract" } as React.CSSProperties);
  return (
    <>
      <div style={{ ...base, ...um(`url(${src})`), background: "#2F4FA8", mixBlendMode: "multiply", opacity: 0.38 * f }} />
      {luz.tipo === "varanda" && <>
        <div style={{ ...base, ...um(`url(${src})`), mixBlendMode: "soft-light", opacity: 0.7 * f,
          background: `linear-gradient(${lado > 0 ? "270deg" : "90deg"}, rgba(255,176,80,1) 0%, rgba(255,170,80,0.4) 22%, rgba(255,160,70,0) 45%)` }} />
        <div style={{ ...base, ...borda(30), background: "#FFB860", mixBlendMode: "overlay", opacity: 0.9 * f }} />
        <div style={{ ...base, ...borda(12), background: "#FFD08A", mixBlendMode: "overlay", opacity: 0.8 * f }} />
      </>}
    </>
  );
};

// a sombra no chao, para nao boiar
export const Sombra: React.FC<{ x: number; y: number; larg: number; f?: number }> = ({ x, y, larg, f = 1 }) => (
  <div style={{ position: "absolute", left: x - larg / 2, top: y - larg * 0.07, width: larg, height: larg * 0.14, borderRadius: "50%", background: "rgba(25,15,5,0.32)", filter: "blur(7px)", transform: `scaleX(${f})` }} />
);

// andar: a pose de perfil a andar (R3), com o passo a subir e descer, o corpo a inclinar e a sombra a respirar
export const Andando: React.FC<{ pid: Pid; de: number; ate: number; y: number; alt: number; t: number; dur: number; passo?: number; luz?: Luz }> = ({ pid, de, ate, y, alt, t, dur, passo = 1.9, luz }) => {
  // o passo em 2 desenhos (como no desenho animado classico): a passada (R3) em baixo e as pernas juntas (R2) no alto
  const k = mola(t, 2.6 / dur * 3, 1); const x = de + (ate - de) * k; const vel = cl(1 - k * 1.03) ** 0.5;
  const fase = t * passo * Math.PI * 2;
  const alto = Math.abs(Math.sin(fase)) > 0.72 && vel > 0.15;
  // parado fica de perfil: a pose de frente (R1) da Valeria tem os oculos na cabeca e o andar no rosto (pulo de continuidade)
  const parou = false;
  const cod = parou ? "R1" : vel < 0.15 ? "R2" : alto ? "R2" : "R3";
  const q = info(pid, cod); const wd = q.tam[0] * (alt / q.tam[1]);
  const pulo = -Math.abs(Math.sin(fase)) * 14 * vel, inc = 1.4 * Math.sin(fase) * vel, amassa = 1 - 0.018 * Math.cos(fase * 2) * vel;
  const esq = ate < de && !parou;
  return (
    <>
      <Sombra x={x} y={y} larg={info(pid, "R3").tam[0] * (alt / info(pid, "R3").tam[1]) * 0.7} f={1 - 0.12 * (-pulo / 14)} />
      <div style={{ position: "absolute", left: x - wd / 2, top: y - alt + pulo, width: wd, height: alt, transformOrigin: "50% 100%", transform: `rotate(${esq ? -inc : inc}deg) scale(${esq ? -1 : 1}, ${amassa})` }}>
        <Img src={staticFile(`boneco/turma/${pid}/${cod}.png`)} style={{ width: "100%", height: "100%", filter: filtroLuz(luz) }} />
        {luz && luz.tipo !== "dia" && <CorDaLuz luz={{ ...luz, lado: ((luz.lado ?? 1) * (esq ? -1 : 1)) as 1 | -1 }} src={staticFile(`boneco/turma/${pid}/${cod}.png`)} />}
      </div>
    </>
  );
};

// o balão de fala (Ed, 19/11, opção A: a voz é do Tião contando, o balão mostra que a fala é DELA).
// As palavras entram uma a uma no tempo da voz; o rabinho aponta para a boca de quem fala. Nunca por cima de rosto.
export const Balao: React.FC<{ texto: string; x: number; y: number; larg?: number; t: number; ini: number; dur: number; rabo?: [number, number] }> = ({ texto, x, y, larg = 620, t, ini, dur, rabo }) => {
  if (t < ini - 0.15) return null;
  const e = mola(t - ini + 0.15, 12, 0.55); const pal = texto.split(" ");
  const vis = Math.min(pal.length, Math.floor(((t - ini) / Math.max(0.3, dur)) * pal.length) + 1);
  return (
    <div style={{ position: "absolute", left: x, top: y, width: larg, transform: `scale(${0.6 + 0.4 * e})`, transformOrigin: rabo ? `${rabo[0] - x}px ${rabo[1] - y}px` : "50% 100%", opacity: cl((t - ini + 0.15) / 0.12) }}>
      {rabo && <svg style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }} width={1} height={1}>
        <path d={`M ${larg - 30} 52 Q ${(larg + rabo[0] - x) / 2} ${(rabo[1] - y) * 0.55 + 40} ${rabo[0] - x} ${rabo[1] - y} Q ${(larg + rabo[0] - x) / 2 - 10} ${(rabo[1] - y) * 0.6 + 70} ${larg - 30} 128 Z`} fill="#FFFDF7" stroke="#1B1310" strokeWidth={6} strokeLinejoin="round" />
      </svg>}
      <div style={{ position: "relative", background: "#FFFDF7", border: "6px solid #1B1310", borderRadius: 46, padding: "26px 40px", boxShadow: "0 10px 0 rgba(27,19,16,0.25)",
        fontFamily: FONTE, fontWeight: 800, fontSize: 66, lineHeight: 1.05, color: "#1B1310", textAlign: "center" }}>
        {pal.map((w, i) => <span key={i} style={{ opacity: i < vis ? 1 : 0, display: "inline-block", marginRight: 16, transform: `translateY(${i === vis - 1 ? -6 * (1 - cl(((t - ini) / dur * pal.length) % 1 * 3)) : 0}px)` }}>{w}</span>)}
      </div>
    </div>
  );
};
