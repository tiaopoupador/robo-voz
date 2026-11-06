// Vitrine das nossas emocoes (para conferir o desenho e mostrar ao Ed).
import React from "react";
import { AbsoluteFill } from "remotion";
import { Figura } from "./emocoes";
import { Fundo, txt } from "./kit";
export const LISTA_EMO = ["😱", "😰", "😬", "😞", "😔", "😩", "😓", "😮‍💨", "😳", "😒", "😏", "🤨", "🤔", "🤫", "😴", "😌", "😎", "🤑", "😂", "🤭", "😋", "😅", "😍", "🤩", "🙏", "💪", "😮", "😄", "💔", "❤️", "💡", "🚨", "📉", "💥", "🎉", "👀"];
const NOMES: Record<string, string> = { "😱": "espanto", "😰": "preocupado", "😬": "tenso", "😞": "chorando", "😔": "triste", "😩": "exausto", "😓": "suando", "😮‍💨": "bufando", "😳": "vergonha", "😒": "desdém", "😏": "deboche", "🤨": "desconfiado", "🤔": "pensando", "🤫": "segredo", "😴": "sono", "😌": "alívio", "😎": "descolado", "🤑": "dinheiro", "😂": "rindo", "🤭": "risinho", "😋": "delícia", "😅": "sem graça", "😍": "apaixonado", "🤩": "deslumbrado", "🙏": "pedindo", "💪": "confiante", "😮": "surpresa", "😄": "feliz", "💔": "coração partido", "❤️": "coração", "💡": "ideia", "🚨": "sirene", "📉": "queda", "💥": "explosão", "🎉": "festa", "👀": "olhando" };
export const GaleriaEmocoes: React.FC = () => (
  <Fundo>
    <AbsoluteFill style={{ display: "grid", gridTemplateColumns: "repeat(9, 1fr)", padding: "30px 40px", rowGap: 6 }}>
      {LISTA_EMO.map((e) => (
        <div key={e} style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <Figura e={e} tam={170} />
          <div style={{ ...txt(24, "#1F1B16", 600), marginTop: -6 }}>{NOMES[e]}</div>
        </div>
      ))}
    </AbsoluteFill>
  </Fundo>
);
