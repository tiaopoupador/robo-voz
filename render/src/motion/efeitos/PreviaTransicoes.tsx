// Previa para o Ed (18/11/2026): as 6 transicoes novas e o grao de filme, com imagens do video 02.
import React from "react";
import { AbsoluteFill, Audio, Img, staticFile, useCurrentFrame } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { Cenas, Bloco, tempos, Trans } from "./Transicoes";
import { Grao } from "./Grao";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const cl = (v: number) => Math.max(0, Math.min(1, v));
const IMGS: [string, Trans | undefined, string][] = [
  ["m03-a-tiao-sandra-supermercado-fila-caixa-cestinha-x-carrinho-lotado.jpg", undefined, "sem grão nos 2 primeiros segundos, depois com grão"],
  ["m08-a-tiao-cozinha-noite-flashback-tiao-assustado-com-a-conta.jpg", "rasgo", "1 · papel rasgado: mudou o tempo ou o lugar"],
  ["m07-a-tiao-sandra-supermercado-fila-caixa-os-dois-com-cestinha-rindo-juntos.jpg", "clarao", "2 · clarão: virada boa, descoberta"],
  ["m09-a-sandra-supermercado-corredor-bolachas-sandra-le-o-peso-e-devolve.jpg", "chicote", "3 · chicote: segue a conversa (a que já temos)"],
  ["m06-a-sandra-supermercado-caixa-sandra-em-choque-com-o-total.jpg", "zoom", "4 · soco de zoom: susto, choque"],
  ["m16-a-tiao-sandra-rua-portao-tarde-sandra-pergunta-rindo-tiao-rega-as-plantas.jpg", "cortina", "5 · cortina da marca: troca de capítulo"],
  ["m05-a-avo-sandra-crianca-portao-de-casa-flashback-avo-da-bolacha-amarela.jpg", "pagina", "6 · página que vira: lembrança"],
];
const Foto = (src: string, k: number) => (t: number) => (
  <AbsoluteFill style={{ overflow: "hidden" }}>
    <Img src={staticFile("v02/img/" + src)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${1.04 + 0.05 * cl(t / 4.6)}) translateX(${(k % 2 ? 1 : -1) * 1.2 * cl(t / 4.6)}%)` }} />
  </AbsoluteFill>
);
const BLOCOS: Bloco[] = IMGS.map(([src, entra], k) => ({ dur: 4.4, el: Foto(src, k), entra }));
const T = tempos(BLOCOS);
export const FIM_PREVIA_TRANS = T.fim;
export const PreviaTransicoes: React.FC = () => {
  const t = useCurrentFrame() / 30;
  let i = 0; for (let k = 0; k < T.ini.length; k++) if (t >= T.ini[k]) i = k;
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      <Cenas blocos={BLOCOS} />
      <Grao forca={cl((t - 2) / 0.6)} />
      <div style={{ position: "absolute", left: 40, bottom: 40, padding: "10px 22px", borderRadius: 14, background: "rgba(20,16,12,0.72)", color: "#FFF6DC", fontFamily, fontSize: 34 }}>{IMGS[i][2]}</div>
      <Audio src={staticFile("v02/trilha.mp3")} volume={0.12} />
    </AbsoluteFill>
  );
};
