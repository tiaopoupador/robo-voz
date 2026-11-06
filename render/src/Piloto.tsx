import React from "react";
import { AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola, MOLAS } from "./mola";
import { CENAS, FIM, LEGENDAS, Cena } from "./piloto-dados";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const AMARELO = "#FFD43B";
const DUR_CLIPE = 6; // os clipes do Grok tem 6 s

// Uma cena: camera lenta por cima (aproxima, afasta ou desliza) e um puxao rapido com borrao na entrada.
const Quadro: React.FC<{ c: Cena; dur: number; lado: number }> = ({ c, dur, lado }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const p = mola(t, 3.5 / dur, 1); // camera lenta: chega a ~86% do caminho no fim da cena, sem tranco
  const esc = c.mov === "entra" ? 1.0 + 0.08 * p : c.mov === "sai" ? 1.1 - 0.08 * p : 1.08;
  const dx = c.mov === "esq" ? 2.5 - 5 * p : c.mov === "dir" ? -2.5 + 5 * p : 0;
  // entrada: chicote (desliza do lado e desfoca), mola estalo
  const [ew, ez] = MOLAS.estalo;
  const e = mola(t, ew, ez);
  const entraX = (1 - e) * 9 * lado;
  const borrao = Math.max(0, (1 - e) * 22);
  const ritmo = c.tipo === "video" ? Math.min(1, (DUR_CLIPE - (c.de ?? 0)) / dur) : 1;
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#1b1b1b" }}>
      <AbsoluteFill style={{ transform: `translateX(${dx + entraX}%) scale(${esc})`, filter: `blur(${borrao}px)` }}>
        {c.tipo === "video"
          ? <OffthreadVideo src={staticFile(c.arq)} muted playbackRate={ritmo} startFrom={Math.round((c.de ?? 0) * 30)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          : <Img src={staticFile(c.arq)} style={{ width: "100%", height: "100%", objectFit: "cover" }} />}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Legenda: entra com mola de texto (sobe um fio e assenta), palavra entre *asteriscos* sai amarela.
const Legenda: React.FC<{ texto: string }> = ({ texto }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig();
  const [w, z] = MOLAS.texto; const m = mola(f / fps, w, z);
  const partes = texto.split(/(\*[^*]+\*)/g).filter(Boolean);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 92 }}>
      <div style={{
        fontFamily, fontWeight: 800, fontSize: 92, lineHeight: 1.05, color: "white", textAlign: "center", maxWidth: 1500,
        WebkitTextStroke: "14px black", paintOrder: "stroke fill",
        transform: `translateY(${(1 - m) * 26}px) scale(${0.92 + 0.08 * m})`, opacity: Math.min(1, m * 1.6),
      }}>
        {partes.map((p, i) => p.startsWith("*")
          ? <span key={i} style={{ color: AMARELO }}>{p.slice(1, -1)}</span>
          : <span key={i}>{p}</span>)}
      </div>
    </AbsoluteFill>
  );
};

export const Piloto: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ backgroundColor: "black" }}>
      {CENAS.map((c, i) => {
        const fim = i + 1 < CENAS.length ? CENAS[i + 1].ini : FIM;
        const de = Math.round(c.ini * fps), dur = Math.round(fim * fps) - de;
        return <Sequence key={i} from={de} durationInFrames={dur}><Quadro c={c} dur={dur / fps} lado={i % 2 ? -1 : 1} /></Sequence>;
      })}
      {LEGENDAS.map(([ini, txt], i) => {
        const fim = i + 1 < LEGENDAS.length ? LEGENDAS[i + 1][0] : FIM;
        const de = Math.round(ini * fps);
        return <Sequence key={"l" + i} from={de} durationInFrames={Math.round(fim * fps) - de}><Legenda texto={txt} /></Sequence>;
      })}
      <Audio src={staticFile("voz.wav")} />
    </AbsoluteFill>
  );
};
