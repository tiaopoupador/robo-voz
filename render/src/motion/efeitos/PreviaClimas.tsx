// Previa para o Ed (18/11/2026): climas que seguem a fala (chuva, brasas, brilho, tensao) e 3 jeitos de mostrar o passado.
// Cada cena comeca 1,5 s limpa (so a luz de cinema) e depois entra o clima, para ver a diferenca.
import React from "react";
import { AbsoluteFill, Audio, Img, Sequence, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { LuzCinema, Chuva, Brasas, BrilhoDourado, Tensao, FILTRO_PASSADO, BordaPassado, Passado } from "./Acabamento";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const cl = (v: number) => Math.max(0, Math.min(1, v));
const I = (n: string) => `v02/img/${n}.jpg`;
type Cena = { img: string; rot: string; clima?: React.FC<{ t: number }>; passado?: Passado };
const CENAS: Cena[] = [
  { img: I("m18-a-sandra-cozinha-noite-sandra-seria-olhando-a-notinha"), rot: "1 · chuva fina: «naquela noite de chuva...»", clima: Chuva },
  { img: I("m06-a-sandra-supermercado-caixa-sandra-em-choque-com-o-total"), rot: "2 · brasas: coisa ruim, dinheiro queimando", clima: Brasas },
  { img: I("m08-a-tiao-cozinha-noite-flashback-tiao-assustado-com-a-conta"), rot: "3 · tensão: bordas batendo como coração", clima: Tensao },
  { img: I("m07-a-tiao-sandra-supermercado-fila-caixa-os-dois-com-cestinha-rindo-juntos"), rot: "4 · brilho dourado: coisa boa, acerto", clima: BrilhoDourado },
  { img: I("m05-a-avo-sandra-crianca-portao-de-casa-flashback-avo-da-bolacha-amarela"), rot: "5 · passado em preto e branco", passado: "pb" },
  { img: I("m05-a-avo-sandra-crianca-portao-de-casa-flashback-avo-da-bolacha-amarela"), rot: "6 · passado em sépia (foto antiga)", passado: "sepia" },
  { img: I("m05-a-avo-sandra-crianca-portao-de-casa-flashback-avo-da-bolacha-amarela"), rot: "7 · passado como lembrança (bordas claras)", passado: "memoria" },
];
const DUR = 6, LIMPA = 1.5;
export const FIM_PREVIA_CLIMAS = CENAS.length * DUR;

const UmaCena: React.FC<{ c: Cena; k: number }> = ({ c, k }) => {
  const t = useCurrentFrame() / 30, f = cl((t - LIMPA) / 0.8);
  const Clima = c.clima;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ overflow: "hidden" }}>
        <Img src={staticFile(c.img)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.04 * cl(t / DUR)})` }} />
        {c.passado && <AbsoluteFill style={{ opacity: f }}><Img src={staticFile(c.img)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.04 * cl(t / DUR)})`, filter: FILTRO_PASSADO[c.passado] }} /></AbsoluteFill>}
      </AbsoluteFill>
      <LuzCinema t={t + k * DUR} />
      {Clima && <AbsoluteFill style={{ opacity: f }}><Clima t={t} /></AbsoluteFill>}
      {c.passado && <AbsoluteFill style={{ opacity: f }}><BordaPassado tipo={c.passado} t={t} /></AbsoluteFill>}
      <div style={{ position: "absolute", left: 40, bottom: 40, padding: "10px 22px", borderRadius: 14, background: "rgba(20,16,12,0.72)", color: "#FFF6DC", fontFamily, fontSize: 36 }}>{c.rot}</div>
    </AbsoluteFill>
  );
};
export const PreviaClimas: React.FC = () => (
  <AbsoluteFill style={{ background: "#000" }}>
    {CENAS.map((c, k) => <Sequence key={k} from={k * DUR * 30} durationInFrames={DUR * 30}><UmaCena c={c} k={k} /></Sequence>)}
    <Audio src={staticFile("v02/trilha.mp3")} volume={0.12} />
  </AbsoluteFill>
);
