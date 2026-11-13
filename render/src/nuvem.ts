// Entrada do robo (nuvem): so a composicao "Video", que recebe os dados com --props=public/vNN/props.json.
import React from "react";
import { Composition, registerRoot } from "remotion";
import { Video, VAZIO, Dados } from "./geral/Video";
import { Vinheta, Vinheta4 } from "./motion/Vinheta";
import { VinhetaNova } from "./motion/VinhetaNova";
import { TelaFinalNova, TelaFinalNovaProva } from "./motion/TelaFinalNova";

const Raiz: React.FC = () => React.createElement(React.Fragment, null,
  React.createElement(Composition, { id: "TelaFinalNova", component: TelaFinalNova as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 300 }),
  React.createElement(Composition, { id: "TelaFinalNovaProva", component: TelaFinalNovaProva as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 300 }),
  React.createElement(Composition, { id: "VinhetaNova", component: VinhetaNova as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 135, defaultProps: { som: "marca/vinheta-nova.wav" } }),
  React.createElement(Composition, { id: "Vinheta4", component: Vinheta4 as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 120, defaultProps: { som: "marca/vinheta4-a.wav" } }),
  React.createElement(Composition, { id: "Vinheta", component: Vinheta as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 60, defaultProps: { som: "marca/vinheta-a.wav" } }),
  React.createElement(Composition, {
    id: "Video", component: Video as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 300, defaultProps: VAZIO,
    calculateMetadata: ({ props }: { props: Dados }) => ({ durationInFrames: Math.max(30, Math.round((props.fim + (props.tela ?? 0)) * 30)) }),
  }));
registerRoot(Raiz);
