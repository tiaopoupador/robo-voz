// Entrada do robo (nuvem): so a composicao "Video", que recebe os dados com --props=public/vNN/props.json.
import React from "react";
import { Composition, registerRoot } from "remotion";
import { Video, VAZIO, Dados } from "./geral/Video";

const Raiz: React.FC = () =>
  React.createElement(Composition, {
    id: "Video", component: Video as React.FC<any>, fps: 30, width: 1920, height: 1080, durationInFrames: 300, defaultProps: VAZIO,
    calculateMetadata: ({ props }: { props: Dados }) => ({ durationInFrames: Math.max(30, Math.round((props.fim + (props.tela ?? 0)) * 30)) }),
  });
registerRoot(Raiz);
