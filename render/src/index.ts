import React from "react";
import { Composition, registerRoot } from "remotion";
import { Piloto } from "./Piloto";
import { FIM } from "./piloto-dados";
import { Mostruario, FIM_MOSTRUARIO } from "./motion/Mostruario";
import { Video01, FIM_V01 } from "./v01/Video01";
import { GaleriaEmocoes } from "./motion/GaleriaEmocoes";
import { ProvaBoneco } from "./motion/boneco/Prova";
import { PilotoMotion, FIM_PILOTO_MOTION } from "./motion/boneco/PilotoMotion";
import { PreviaTransicoes, FIM_PREVIA_TRANS } from "./motion/efeitos/PreviaTransicoes";
import { PreviaTexturas, FIM_PREVIA_TEXTURAS } from "./motion/efeitos/PreviaTexturas";
import { PreviaPoeiras, FIM_PREVIA_POEIRAS } from "./motion/efeitos/PreviaPoeiras";
import { PreviaClimas, FIM_PREVIA_CLIMAS } from "./motion/efeitos/PreviaClimas";
import { PilotoTurma, FIM_PILOTO_TURMA } from "./motion/boneco/PilotoTurma";
import { ProvaBoca, FIM_PROVA_BOCA } from "./motion/boneco/ProvaBoca";
import { ProvaLuz } from "./motion/boneco/ProvaLuz";
import { ProvaCenaNoite, FIM_CENA_NOITE } from "./motion/boneco/ProvaCenaNoite";

const comp = (id: string, component: React.FC, seg: number) =>
  React.createElement(Composition, { key: id, id, component, durationInFrames: Math.round(seg * 30), fps: 30, width: 1920, height: 1080 });
const Raiz: React.FC = () =>
  React.createElement(React.Fragment, null, comp("Piloto", Piloto, FIM), comp("Mostruario", Mostruario, FIM_MOSTRUARIO), comp("Video01", Video01, FIM_V01), comp("GaleriaEmocoes", GaleriaEmocoes, 6), comp("ProvaBoneco", ProvaBoneco, 1), comp("PilotoMotion", PilotoMotion, FIM_PILOTO_MOTION), comp("PreviaTransicoes", PreviaTransicoes, FIM_PREVIA_TRANS), comp("PreviaTexturas", PreviaTexturas, FIM_PREVIA_TEXTURAS), comp("PreviaPoeiras", PreviaPoeiras, FIM_PREVIA_POEIRAS), comp("PreviaClimas", PreviaClimas, FIM_PREVIA_CLIMAS), comp("PilotoTurma", PilotoTurma, FIM_PILOTO_TURMA), comp("ProvaBoca", ProvaBoca, FIM_PROVA_BOCA), comp("ProvaLuz", ProvaLuz, 2), comp("ProvaCenaNoite", ProvaCenaNoite, FIM_CENA_NOITE));
registerRoot(Raiz);
