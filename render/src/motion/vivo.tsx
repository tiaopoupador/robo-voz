// Coisas que dao vida ao motion: emoji animado (Noto, Google, licenca livre) e som sincronizado com a animacao.
// Sons: os mesmos do FinMoovi (Kenney, CC0), em public/sfx. Cada peca toca o som NO MESMO instante da sua animacao.
import React, { useEffect, useState } from "react";
import { Audio, continueRender, delayRender, Sequence, staticFile, useVideoConfig } from "remotion";
import { Lottie, LottieAnimationData } from "@remotion/lottie";
import lista from "./emojis.json";
import { Figura, temEmocao } from "./emocoes";

const TEM = new Set(lista as string[]);
export const codigo = (e: string) => Array.from(e).map((c) => c.codePointAt(0)!.toString(16)).join("_");

// Emoji animado quando existe a versao animada; senao, o emoji parado (com um leve balanco)
// Emoji: se temos a NOSSA emocao desenhada, usa ela; senao, o emoji animado do Google (reserva)
export const Emoji: React.FC<{ e: string; tam: number; estilo?: React.CSSProperties; desde?: number }> = ({ e, tam, estilo, desde }) => {
  if (temEmocao(e)) return <div style={{ width: tam, height: tam, ...estilo }}><Figura e={e} tam={tam} desde={desde} /></div>;
  return <EmojiPronto e={e} tam={tam} estilo={estilo} />;
};
const EmojiPronto: React.FC<{ e: string; tam: number; estilo?: React.CSSProperties }> = ({ e, tam, estilo }) => {
  const cod = codigo(e), cod2 = cod.replace(/_fe0f/g, "");
  const nome = TEM.has(cod) ? cod : TEM.has(cod2) ? cod2 : null;
  const [dados, setDados] = useState<LottieAnimationData | null>(null);
  const [h] = useState(() => (nome ? delayRender("emoji " + nome) : null));
  useEffect(() => {
    if (!nome || h === null) return;
    fetch(staticFile(`emoji/${nome}.json`)).then((r) => r.json()).then((j) => { setDados(j); continueRender(h); }).catch(() => continueRender(h));
  }, [nome, h]);
  if (nome && dados) return <div style={{ width: tam, height: tam, ...estilo }}><Lottie animationData={dados} loop style={{ width: tam, height: tam }} /></div>;
  return <div style={{ fontSize: tam * 0.86, lineHeight: 1, width: tam, height: tam, textAlign: "center", ...estilo }}>{e}</div>;
};

// Som: toca o arquivo "nome" (public/sfx/nome.ogg) no segundo "em" da cena
export type NomeSom = "pop" | "boom" | "money" | "coins" | "growth" | "clock" | "card" | "warning" | "kaching" | "typewriter" | "keyboard" | "click" | "ding" | "thud" | "sparkle" | "slide";
const VOL: Partial<Record<NomeSom, number>> = { pop: 0.35, click: 0.4, clock: 0.25, keyboard: 0.25, typewriter: 0.3, warning: 0.3, boom: 0.35, thud: 0.45, kaching: 0.4, money: 0.35, coins: 0.35, growth: 0.3, card: 0.35, ding: 0.35, sparkle: 0.35, slide: 0.3 };
export const Som: React.FC<{ nome: NomeSom; em: number; vol?: number }> = ({ nome, em, vol }) => {
  const { fps } = useVideoConfig();
  return <Sequence from={Math.max(0, Math.round(em * fps))} durationInFrames={Math.round(2 * fps)} layout="none"><Audio src={staticFile(`sfx/${nome}.ogg`)} volume={vol ?? VOL[nome] ?? 0.35} /></Sequence>;
};

const NEG_FORTE = new Set(["😱", "💥", "🤯"]);
const NEG = new Set(["😰", "😩", "😬", "😞", "😔", "😓", "😒", "😮‍💨", "😳", "🤨", "😤", "🚨", "⚠️", "📉"]);
const POS = new Set(["😌", "😎", "🤑", "😍", "🥳", "🤩", "😋", "😄", "💪", "🤝", "🎉", "❤️", "✅", "🙏", "😂", "🤭", "😏"]);
export const somDoEmoji = (e: string): NomeSom =>
  e === "💔" ? "slide" : e === "💡" ? "ding" : e === "🤑" ? "kaching" : NEG_FORTE.has(e) ? "boom" : NEG.has(e) ? "warning" : POS.has(e) ? "sparkle" : "pop";
