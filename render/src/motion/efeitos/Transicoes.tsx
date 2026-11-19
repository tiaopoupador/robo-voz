// As transicoes entre cenas (Ed, 18/11/2026: «eles estao usando varias transicoes de cenas diferentes, isso tambem ajuda
// muito a dar mais dinamica»). Hoje so tinhamos o chicote. Cada uma tem o seu som e o seu sentido:
//   rasgo   = muda o tempo ou o lugar («dois meses depois»): o papel rasga e a cena nova chega em preto e branco e ganha cor
//   clarao  = virada boa, ideia, descoberta
//   chicote = seguir a conversa, mesmo assunto
//   zoom    = susto, choque, numero que assusta
//   cortina = troca de capitulo (na cor da marca)
//   pagina  = lembranca, «no mes passado»
// Uso: <Cenas blocos={[{ dur, el: (t) => ..., entra: "rasgo" }, ...]} />. Cada bloco desenha-se pelo seu tempo local t.
import React from "react";
import { AbsoluteFill, Audio, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { mola } from "../../mola";

export type Trans = "rasgo" | "clarao" | "chicote" | "zoom" | "cortina" | "pagina" | "corte";
export type Bloco = { dur: number; el: (t: number) => React.ReactNode; entra?: Trans; td?: number };
export const DUR_TRANS: Record<Trans, number> = { rasgo: 0.9, clarao: 0.7, chicote: 0.45, zoom: 0.55, cortina: 0.8, pagina: 0.9, corte: 0 };
export const SOM_TRANS: Partial<Record<Trans, [string, number]>> = {
  rasgo: ["sfx/rasgo.wav", 0.55], clarao: ["sfx/sparkle.ogg", 0.3], chicote: ["sfx/slide.ogg", 0.35],
  zoom: ["sfx/boom.ogg", 0.22], cortina: ["sfx/slide.ogg", 0.3], pagina: ["sfx/card.ogg", 0.4],
};
const AZUL = "#2F5E9E", AMARELO = "#F2B632";
const ease = (p: number) => (p < 0.5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2);
const cl = (v: number) => Math.max(0, Math.min(1, v));
const h = (n: number) => { const x = Math.sin(n * 91.7 + 13.3) * 43758.5453; return x - Math.floor(x); };

// a borda do rasgo: um zigue-zague fixo (o mesmo papel do comeco ao fim)
const BORDA = Array.from({ length: 28 }, (_, i) => ({ y: (i / 27) * 1080, dx: (h(i) - 0.5) * 70 + Math.sin(i * 1.3) * 22 }));

export const Mistura: React.FC<{ tipo: Trans; p: number; a: React.ReactNode; b: React.ReactNode }> = ({ tipo, p, a, b }) => {
  const e = ease(p);
  switch (tipo) {
    case "rasgo": {
      // o rasgo atravessa da direita para a esquerda; a cena nova aparece em preto e branco e ganha cor no fim
      const x = 1920 + 160 - e * 2240;
      const pts = BORDA.map((q) => `${x + q.dx}px ${q.y}px`);
      const clipA = `polygon(0px 0px, ${pts.join(", ")}, 0px 1080px)`;
      const cinza = 1 - cl((p - 0.55) / 0.45);
      const papel = BORDA.map((q) => `${x + q.dx},${q.y}`).join(" ") + " " + [...BORDA].reverse().map((q) => `${x + q.dx + 18 + h(q.y) * 16},${q.y}`).join(" ");
      return (
        <AbsoluteFill>
          <AbsoluteFill style={{ filter: `grayscale(${cinza}) contrast(${1 + 0.1 * cinza})` }}>{b}</AbsoluteFill>
          <AbsoluteFill style={{ clipPath: clipA }}>{a}</AbsoluteFill>
          <svg width="1920" height="1080" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
            <polygon points={papel} fill="#F4EFE4" stroke="#CFC6B4" strokeWidth={2} style={{ filter: "drop-shadow(6px 0 6px rgba(0,0,0,0.35))" }} />
          </svg>
        </AbsoluteFill>
      );
    }
    case "clarao": {
      const branco = p < 0.5 ? ease(p / 0.5) : 1 - ease((p - 0.5) / 0.5);
      return (
        <AbsoluteFill>
          {p < 0.5 ? <AbsoluteFill style={{ transform: `scale(${1 + 0.05 * e})` }}>{a}</AbsoluteFill>
                   : <AbsoluteFill style={{ transform: `scale(${1.05 - 0.05 * e})` }}>{b}</AbsoluteFill>}
          <AbsoluteFill style={{ background: "radial-gradient(circle at 55% 45%, #FFFDF4 0%, #FFF3C8 55%, #FFE7A0 100%)", opacity: branco }} />
        </AbsoluteFill>
      );
    }
    case "chicote": {
      const m = mola(p * 0.6, 26, 0.6);
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          <AbsoluteFill style={{ transform: `translateX(${-m * 100}%)`, filter: `blur(${Math.sin(p * Math.PI) * 18}px)` }}>{a}</AbsoluteFill>
          <AbsoluteFill style={{ transform: `translateX(${(1 - m) * 100}%)`, filter: `blur(${Math.sin(p * Math.PI) * 18}px)` }}>{b}</AbsoluteFill>
        </AbsoluteFill>
      );
    }
    case "zoom": {
      return p < 0.45 ? (
        <AbsoluteFill style={{ transform: `scale(${1 + 0.9 * ease(p / 0.45)})`, filter: `blur(${ease(p / 0.45) * 20}px)`, opacity: 1 - 0.3 * ease(p / 0.45) }}>{a}</AbsoluteFill>
      ) : (
        <AbsoluteFill style={{ transform: `scale(${0.78 + 0.22 * mola((p - 0.45) * 0.55, 24, 0.45)})`, filter: `blur(${(1 - cl((p - 0.45) / 0.3)) * 14}px)` }}>{b}</AbsoluteFill>
      );
    }
    case "cortina": {
      // uma faixa azul da marca, com fio amarelo, varre na diagonal: cobre a cena velha e descobre a nova
      const x = -2600 + e * 5200;
      const cobre = x > -300;
      return (
        <AbsoluteFill style={{ overflow: "hidden" }}>
          {x < 960 ? a : b}
          <div style={{ position: "absolute", top: -400, left: x - 1200, width: 2400, height: 1900, background: AZUL, transform: "skewX(-18deg)", borderRight: `26px solid ${AMARELO}`, borderLeft: `26px solid ${AMARELO}`, opacity: cobre ? 1 : 1 }} />
        </AbsoluteFill>
      );
    }
    case "pagina": {
      // a cena velha vira como a folha de um caderno (dobra na esquerda)
      const ang = e * 100;
      return (
        <AbsoluteFill style={{ perspective: 2600 }}>
          <AbsoluteFill style={{ filter: `brightness(${0.75 + 0.25 * e})` }}>{b}</AbsoluteFill>
          {ang < 90 && (
            <AbsoluteFill style={{ transformOrigin: "0% 50%", transform: `rotateY(${ang}deg)`, boxShadow: `${30 * e}px 0 ${60 * e}px rgba(0,0,0,${0.45 * e})` }}>
              {a}
              <AbsoluteFill style={{ background: `linear-gradient(90deg, rgba(0,0,0,0) 40%, rgba(0,0,0,${0.35 * e}) 100%)` }} />
            </AbsoluteFill>
          )}
        </AbsoluteFill>
      );
    }
  }
  return <>{p < 0.5 ? a : b}</>;
};

export const tempos = (blocos: Bloco[]) => {
  const ini: number[] = []; let t = 0;
  blocos.forEach((b, i) => { const td = i === 0 ? 0 : (b.td ?? DUR_TRANS[b.entra ?? "corte"]); t = i === 0 ? 0 : t - td; ini.push(t); t += b.dur; });
  return { ini, fim: t };
};

export const Cenas: React.FC<{ blocos: Bloco[] }> = ({ blocos }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const { ini } = tempos(blocos);
  let atual = 0;
  for (let i = 0; i < blocos.length; i++) if (t >= ini[i]) atual = i;
  const b = blocos[atual];
  const td = atual === 0 ? 0 : (b.td ?? DUR_TRANS[b.entra ?? "corte"]);
  const dentro = t - ini[atual];
  const sons = blocos.map((x, i) => (i > 0 && x.entra && SOM_TRANS[x.entra] ? <Sequence key={i} from={Math.round(ini[i] * fps)} durationInFrames={Math.round(2 * fps)} layout="none"><Audio src={staticFile(SOM_TRANS[x.entra]![0])} volume={SOM_TRANS[x.entra]![1]} /></Sequence> : null));
  return (
    <AbsoluteFill>
      {atual > 0 && dentro < td
        ? <Mistura tipo={b.entra ?? "corte"} p={dentro / td} a={blocos[atual - 1].el(t - ini[atual - 1])} b={b.el(dentro)} />
        : b.el(dentro)}
      {sons}
    </AbsoluteFill>
  );
};
