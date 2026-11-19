// Previa para o Ed (18/11/2026): a luz de cinema (opcao 4) com 3 tipos de poeira, e no fim como fica num video de verdade,
// com cenas que tem poeira e cenas sem nada.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { Acabamento, Poeira } from "./Acabamento";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const cl = (v: number) => Math.max(0, Math.min(1, v));
const I = (n: string) => `v02/img/${n}.jpg`;
const M07 = I("m07-a-tiao-sandra-supermercado-fila-caixa-os-dois-com-cestinha-rindo-juntos");
const CENAS: { img: string; poeira: Poeira; rot: string; dur: number }[] = [
  { img: M07, poeira: "lenta", rot: "A · poeira lenta e sutil, flutuando na luz", dur: 6 },
  { img: M07, poeira: "neve", rot: "B · neve grossa: cai um pouco e para", dur: 6 },
  { img: M07, poeira: "luz", rot: "C · pontos de luz grandes, subindo devagar", dur: 6 },
  { img: M07, poeira: "nada", rot: "D · só a luz de cinema, sem poeira", dur: 5 },
  { img: I("m08-a-tiao-cozinha-noite-flashback-tiao-assustado-com-a-conta"), poeira: "neve", rot: "E · num vídeo de verdade: cena com neve...", dur: 5 },
  { img: I("m09-a-sandra-supermercado-corredor-bolachas-sandra-le-o-peso-e-devolve"), poeira: "nada", rot: "...cena sem nada...", dur: 4 },
  { img: I("m16-a-tiao-sandra-rua-portao-tarde-sandra-pergunta-rindo-tiao-rega-as-plantas"), poeira: "lenta", rot: "...cena com poeira lenta...", dur: 5 },
  { img: I("m06-a-sandra-supermercado-caixa-sandra-em-choque-com-o-total"), poeira: "nada", rot: "...e outra sem nada", dur: 4 },
];
const INI = CENAS.reduce<number[]>((a, c, i) => [...a, i ? a[i - 1] + CENAS[i - 1].dur : 0], []);
export const FIM_PREVIA_POEIRAS = INI[INI.length - 1] + CENAS[CENAS.length - 1].dur;

export const PreviaPoeiras: React.FC = () => {
  const t = useCurrentFrame() / 30;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {CENAS.map((c, k) => (
        <Sequence key={k} from={Math.round(INI[k] * 30)} durationInFrames={Math.round(c.dur * 30)}>
          <AbsoluteFill style={{ overflow: "hidden" }}>
            <Img src={staticFile(c.img)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.04 * cl((t - INI[k]) / c.dur)})` }} />
          </AbsoluteFill>
          <Acabamento t={t} poeira={c.poeira} tc={t - INI[k]} />
          <div style={{ position: "absolute", left: 40, bottom: 40, padding: "10px 22px", borderRadius: 14, background: "rgba(20,16,12,0.72)", color: "#FFF6DC", fontFamily, fontSize: 36 }}>{c.rot}</div>
        </Sequence>
      ))}
      <Audio src={staticFile("v02/trilha.mp3")} volume={0.12} />
    </AbsoluteFill>
  );
};
