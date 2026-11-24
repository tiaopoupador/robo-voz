// A cena da TURMA dentro do video inteiro (23/11/2026, o 05 e o 1.o longo SO MOTION: «quarta 18h longo SO MOTION», Ed 18/11).
// Junta o que ja foi aprovado nas provas (PROVA-CENA-NOITE, PROVA-VALERIA-ANDANDO, PROVA-BOCA-VALERIA): o cenario vazio
// (do meta.ai), os personagens SEMPRE nas poses oficiais (Turma.tsx: respiram, piscam, falam), o andar, o balao (opcao A:
// a voz e do Tiao contando, o balao mostra que a fala e do personagem) e a luz do lugar (noite, lampada da varanda).
// Os tempos chegam ja em segundos DENTRO da cena: o fabrica/montar.py troca os gatilhos ("g": palavra da fala) por "ini".
// Tudo e funcao do tempo (seek(t) puro).
import React from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { mola } from "../../mola";
import { Andando, Balao, brinde, aceno, Luz, Pid, Pose, Sombra, info } from "./Turma";

type PoseEm = { cod: string; ini: number };
export type Pessoa = {
  pid: Pid; x: number; y: number; alt: number; poses: PoseEm[]; espelho?: boolean; luz?: Luz; sombra?: boolean;
  fala?: [number, number][]; treme?: [number, number][]; braco?: { tipo: "aceno" | "brinde"; ini: number };
  anda?: { de: number; ini: number; dur: number; oculos?: boolean };   // chega andando de "de" ate x
  sai?: { ate: number; ini: number; dur: number; oculos?: boolean };   // vai embora andando ate "ate"
  some?: number;                                                       // some da cena a partir deste segundo
};
export type BalaoEm = { texto: string; ini: number; dur: number; x: number; y: number; larg?: number; rabo?: [number, number] };
export type Objeto = { src: string; x: number; y: number; w: number; de?: number; ini?: number; dur?: number; noite?: boolean };
export type SpecTurma = {
  fundo: string; filtro?: string; zoom?: [number, number]; fx?: number; fy?: number; luz?: Luz;
  lampada?: { x: number; y: number; r?: number }; gente: Pessoa[]; baloes?: BalaoEm[]; objetos?: Objeto[];
};

// a boca no ritmo das silabas enquanto o balao fala (a voz e do Tiao: a boca so mexe de leve)
const silabas = (t: number, faixas?: [number, number][]) => {
  for (const [a, b] of faixas ?? []) if (t >= a && t <= b) return 0.45 * Math.abs(Math.sin((t - a) * Math.PI * 4.2));
  return undefined;
};
const dentro = (t: number, faixas?: [number, number][]) => (faixas ?? []).some(([a, b]) => t >= a && t <= b);

const Gente: React.FC<{ p: Pessoa; t: number; luz?: Luz }> = ({ p, t, luz: luzCena }) => {
  const luz = p.luz ?? luzCena;
  if (p.some !== undefined && t >= p.some) return null;
  if (p.anda && t < p.anda.ini) return null;
  if (p.anda && t < p.anda.ini + p.anda.dur)
    return <Andando pid={p.pid} de={p.anda.de} ate={p.x} y={p.y} alt={p.alt} t={t - p.anda.ini} dur={p.anda.dur} luz={luz} oculosNaCabeca={p.anda.oculos} />;
  if (p.sai && t >= p.sai.ini)
    return t < p.sai.ini + p.sai.dur ? <Andando pid={p.pid} de={p.x} ate={p.sai.ate} y={p.y} alt={p.alt} t={t - p.sai.ini} dur={p.sai.dur} luz={luz} oculosNaCabeca={p.sai.oculos} /> : null;
  const ps = [...p.poses].sort((a, b) => a.ini - b.ini);
  let atual = ps[0]; for (const q of ps) if (q.ini <= t) atual = q;
  // a 1.a pose ja esta na cena; as seguintes entram com mola (e quem chegou andando entra com mola ao parar)
  const entra = atual === ps[0] ? (p.anda ? p.anda.ini + p.anda.dur : undefined) : atual.ini;
  const q = info(p.pid, atual.cod); const larg = q.tam[0] * (p.alt / q.tam[1]);
  const braco = p.braco ? (p.braco.tipo === "aceno" ? aceno(t, p.braco.ini) : brinde(t, p.braco.ini)) : undefined;
  return (
    <>
      {p.sombra !== false && <Sombra x={p.x} y={p.y - 4} larg={larg * 0.62} />}
      <Pose pid={p.pid} cod={atual.cod} x={p.x} y={p.y} alt={p.alt} t={t} entra={entra} espelho={p.espelho} luz={luz}
        fala={silabas(t, p.fala)} treme={dentro(t, p.treme) ? 1 : 0} braco={braco} acento={silabas(t, p.fala) ? 0.25 : 0} />
    </>
  );
};

export const CenaTurma: React.FC<{ c: SpecTurma; dur: number }> = ({ c, dur }) => {
  const t = useCurrentFrame() / useVideoConfig().fps;
  const [z0, z1] = c.zoom ?? [1.0, 1.06];
  const k = mola(t, 2.2 / Math.max(2, dur), 1);  // a camera anda devagar a cena inteira
  const z = z0 + (z1 - z0) * Math.min(1, t / Math.max(1, dur));
  return (
    <AbsoluteFill style={{ overflow: "hidden", background: "#0b1020" }}>
      <AbsoluteFill style={{ transformOrigin: `${c.fx ?? 50}% ${c.fy ?? 60}%`, transform: `scale(${z * (0.995 + 0.005 * k)})` }}>
        <Img src={staticFile(c.fundo)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: c.filtro }} />
        {c.lampada && <div style={{ position: "absolute", left: c.lampada.x - (c.lampada.r ?? 600), top: c.lampada.y - (c.lampada.r ?? 600), width: 2 * (c.lampada.r ?? 600), height: 2 * (c.lampada.r ?? 600), borderRadius: "50%",
          background: "radial-gradient(circle, rgba(255,190,100,0.45), rgba(255,170,80,0.1) 45%, rgba(255,170,80,0) 68%)", opacity: 0.92 + 0.08 * Math.sin(t * 13) * Math.sin(t * 7), pointerEvents: "none" }} />}
        {(c.objetos ?? []).map((o, i) => {
          const a = o.ini ?? 0, d = o.dur ?? 3; const p = o.de === undefined ? 1 : mola(t - a, 2.6 / d * 2, 1);
          const x = o.de === undefined ? o.x : o.de + (o.x - o.de) * (t < a ? 0 : p);
          const anda = o.de !== undefined && t > a && p < 0.98; const pulo = anda ? 2.5 * Math.sin(t * 22) : 0;
          return <Img key={i} src={staticFile(o.src)} style={{ position: "absolute", left: x - o.w / 2, top: o.y - o.w * 0.357 + pulo, width: o.w, filter: o.noite ? "brightness(0.42) saturate(0.6) hue-rotate(195deg)" : undefined }} />;
        })}
        {[...c.gente].sort((a, b) => a.y - b.y).map((p, i) => <Gente key={i} p={p} t={t} luz={c.luz} />)}
      </AbsoluteFill>
      {(c.baloes ?? []).map((b, i, todos) => { const prox = todos.filter((o) => o.ini > b.ini).map((o) => o.ini); return <Balao key={i} texto={b.texto} x={b.x} y={b.y} larg={b.larg ?? 900} t={t} ini={b.ini} dur={b.dur} rabo={b.rabo} fim={prox.length ? Math.min(...prox) : undefined} />; })}
    </AbsoluteFill>
  );
};
