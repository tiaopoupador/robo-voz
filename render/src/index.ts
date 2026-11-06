import React from "react";
import { Composition, registerRoot } from "remotion";
import { Piloto } from "./Piloto";
import { FIM } from "./piloto-dados";
import { Mostruario, FIM_MOSTRUARIO } from "./motion/Mostruario";
import { Video01, FIM_V01 } from "./v01/Video01";
import { GaleriaEmocoes } from "./motion/GaleriaEmocoes";

const comp = (id: string, component: React.FC, seg: number) =>
  React.createElement(Composition, { key: id, id, component, durationInFrames: Math.round(seg * 30), fps: 30, width: 1920, height: 1080 });
const Raiz: React.FC = () =>
  React.createElement(React.Fragment, null, comp("Piloto", Piloto, FIM), comp("Mostruario", Mostruario, FIM_MOSTRUARIO), comp("Video01", Video01, FIM_V01), comp("GaleriaEmocoes", GaleriaEmocoes, 6));
registerRoot(Raiz);
