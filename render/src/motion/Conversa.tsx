// Cena "Tião conversa" (Ed, 11/11/2026): o jeito do Prosa que Rende (524 mil views em 11 dias) com o nosso personagem.
// Fundo com zoom bem lento e escurecido, o Tião de um lado e a frase da fala grande do outro (a legenda grande, no Video.tsx).
// 18/11/2026 (Ed: «sim» para o Tião piscar e mexer a boca; «o estilo das ondas sonoras não gostei, me dê outras sugestões»;
// «teria como criarmos tipo uma etiqueta que pudesse identificar esse vídeo como uma prosa?»):
//   - o Tião pisca e fala nas poses verdadeiras (boneco/TiaoReal.tsx, TiaoPose), com a boca seguindo o volume da voz;
//   - o jeito da onda vem do props ("ondaEstilo"): barras (o antigo), linha, radio, pilulas, nada;
//   - o selo da série vem do props ("selo"): placa, fita, ou vazio.
import React, { createContext, useContext } from "react";
import { AbsoluteFill, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola } from "../mola";
import { TiaoPose, TAM_POSE, NomePose } from "./boneco/TiaoReal";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
export const ONDA_HZ = 15;                       // o montar.py mede o volume da voz 15 vezes por segundo
export const OndaCtx = createContext<number[]>([]);
export const EstiloCtx = createContext<{ onda: string; selo: string }>({ onda: "barras", selo: "" });
const BARRAS = 34;
const AMBAR = "#F2A93B", CREME = "#FFF4DC", AMARELO = "#FFD43B", MADEIRA = "#8A5A33";

// volume da voz no instante tt (0 a 1), interpolado
const useVoz = () => { const onda = useContext(OndaCtx); return (tt: number) => { const i = tt * ONDA_HZ, a = Math.floor(i), f = i - a; return (onda[a] ?? 0) * (1 - f) + (onda[a + 1] ?? 0) * f; }; };
const fixo = (k: number) => { const x = Math.sin(k * 12.9898) * 43758.5453; return x - Math.floor(x); };  // aleatório fixo

// A: barras (o jeito antigo, recusado pelo Ed a 18/11; fica como referência)
export const Ondas: React.FC<{ t: number; larg?: number; alt?: number; cor?: string }> = ({ t, larg = 620, alt = 150, cor = "white" }) => {
  const v = useVoz(); const passo = larg / BARRAS;
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: passo * 0.38, height: alt }}>
      {Array.from({ length: BARRAS }, (_, k) => {
        const r = fixo(k); const nivel = v(t - r * 0.12) * (0.45 + 0.55 * Math.abs(Math.sin(t * (5 + r * 7) + k)));
        const h = Math.max(6, Math.min(1, nivel * 1.6) * alt * (0.55 + 0.45 * Math.sin((k / BARRAS) * Math.PI)));
        return <div key={k} style={{ width: passo * 0.62, height: h, background: cor, borderRadius: 4, opacity: 0.92 }} />;
      })}
    </div>
  );
};

// B: linha de voz, duas linhas finas que ondulam juntas (como a agulha de um gravador)
const Linha: React.FC<{ t: number }> = ({ t }) => {
  const v = useVoz(); const L = 640, A = 70;
  const caminho = (fase: number, amp: number) => Array.from({ length: 81 }, (_, i) => {
    const x = (i / 80) * L, borda = Math.sin((i / 80) * Math.PI);
    const y = A + borda * amp * A * 0.9 * (Math.sin(i * 0.42 + t * 9 + fase) * 0.6 + Math.sin(i * 0.17 - t * 5 + fase) * 0.4) * v(t - i * 0.002);
    return `${i ? "L" : "M"}${x.toFixed(1)},${y.toFixed(1)}`;
  }).join(" ");
  return (
    <svg width={L} height={A * 2} style={{ overflow: "visible" }}>
      <path d={caminho(1.7, 0.6)} fill="none" stroke={CREME} strokeOpacity={0.45} strokeWidth={4} strokeLinecap="round" />
      <path d={caminho(0, 1)} fill="none" stroke={AMARELO} strokeWidth={7} strokeLinecap="round" />
    </svg>
  );
};

// C: o radinho de pilha do Tião, com o ponteiro que mexe e o alto-falante que pulsa com a voz (coisa só nossa)
const Radio: React.FC<{ t: number }> = ({ t }) => {
  const v = useVoz(); const nv = Math.min(1, v(t) * 1.3); const nlento = Math.min(1, v(t - 0.08) * 1.3);
  const ang = -38 + 76 * nlento + Math.sin(t * 23) * 2 * nv;
  return (
    <svg width={450} height={345} viewBox="0 0 300 230" style={{ overflow: "visible", filter: "drop-shadow(0 12px 22px rgba(0,0,0,0.5))" }}>
      <line x1={232} y1={40} x2={268} y2={-46} stroke="#222" strokeWidth={5} strokeLinecap="round" />
      <circle cx={268} cy={-46} r={6} fill="#222" />
      <rect x={10} y={38} width={280} height={180} rx={30} fill={MADEIRA} stroke="#111" strokeWidth={6} />
      <rect x={26} y={54} width={248} height={148} rx={20} fill="#B07A4A" stroke="#111" strokeWidth={4} />
      <g transform={`translate(94 128) scale(${1 + 0.07 * nv})`}>
        {[54, 40, 26, 12].map((r, i) => <circle key={r} r={r} fill={i % 2 ? "#3A2A1E" : "#5A4130"} stroke="#111" strokeWidth={3} />)}
      </g>
      <rect x={168} y={74} width={92} height={56} rx={10} fill={CREME} stroke="#111" strokeWidth={4} />
      {[0, 1, 2, 3, 4].map((i) => <line key={i} x1={180 + i * 17} y1={80} x2={180 + i * 17} y2={90} stroke="#111" strokeWidth={3} />)}
      <g transform={`translate(214 124) rotate(${ang})`}><line x1={0} y1={0} x2={0} y2={-40} stroke="#C62828" strokeWidth={5} strokeLinecap="round" /></g>
      <circle cx={214} cy={124} r={6} fill="#111" />
      <circle cx={190} cy={170} r={14} fill={AMBAR} stroke="#111" strokeWidth={4} />
      <circle cx={238} cy={170} r={14} fill={AMBAR} stroke="#111" strokeWidth={4} />
      <circle cx={46} cy={70} r={6} fill={nv > 0.15 ? "#FF5252" : "#5A2A2A"} stroke="#111" strokeWidth={2} />
    </svg>
  );
};

// D: pílulas grossas, poucas, crescendo do meio para cima e para baixo, nas cores do canal
const Pilulas: React.FC<{ t: number }> = ({ t }) => {
  const v = useVoz(); const N = 20, H = 230;  // Ed 18/11: «mais esticada no comprimento, maior e um pouco maior na altura»
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 15, height: H }}>
      {Array.from({ length: N }, (_, k) => {
        const r = fixo(k + 3); const meio = Math.sin(((k + 0.5) / N) * Math.PI);
        const n = Math.min(1, v(t - r * 0.1) * 1.5) * (0.5 + 0.5 * Math.abs(Math.sin(t * (4 + r * 5) + k * 1.3)));
        const h = 32 + n * (H - 32) * (0.5 + 0.5 * meio);
        return <div key={k} style={{ width: 30, height: h, borderRadius: 15, background: k % 3 === 1 ? AMARELO : k % 3 === 2 ? CREME : AMBAR, boxShadow: "0 6px 16px rgba(0,0,0,0.35)" }} />;
      })}
    </div>
  );
};

// o selo da série, no alto, do lado da frase (nunca em cima do Tião)
export const Selo: React.FC<{ tipo: string; t: number; lado: 1 | -1 }> = ({ tipo, t, lado }) => {
  if (!tipo) return null;
  const m = mola(t - 0.3, 9, 0.6);
  const pos: React.CSSProperties = { position: "absolute", top: 56, [lado > 0 ? "right" : "left"]: 70, transform: `translateY(${(1 - m) * -40}px) rotate(${tipo === "fita" ? -3 : 0}deg)`, opacity: Math.min(1, m * 1.5), transformOrigin: "50% 0%" };
  if (tipo === "placa") {  // Ed 18/11: «o tiao sentado numa cadeira de area e tomando um cafezinho e saindo fumacinha da caneca (...) como se fosse um gif»
    // e (Ed 18/11): «espelhar o tiao pra ele ficar olhando pro outro lado» e «ele levantando a xicara como se tivesse oferecendo o cafe»
    // 18/11: a 2a pose (oferecendo o cafe) foi RECUSADA («ficou muito robotico»): fica so a pose do cafe, espelhada do outro lado
    const [mx, my] = [124, 97];                                 // onde fica a boca da caneca
    const fio = (k: number) => {                                // fumacinha: 3 fios que sobem, ondulam e somem, sem parar
      const c = ((t * 0.6 + k / 3) % 1), y = -4 - c * 40, x = -c * 34 + Math.sin(c * 5 + k * 2.1) * 4;  // sobe e vai para o lado: nunca por cima do rosto
      return { d: `M0,0 C-7,-9 7,-18 0,-28`, op: Math.min(1, c * 4) * (1 - c * 0.9), tr: `translate(${x},${y}) scale(${0.7 + c * 0.7})` };
    };
    const img = (src: string, op: number) => <Img src={staticFile(src)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%", opacity: op }} />;
    return (
      <div style={{ ...pos, display: "flex", flexDirection: lado > 0 ? "row" : "row-reverse", alignItems: "flex-end", filter: "drop-shadow(0 10px 18px rgba(0,0,0,0.45))" }}>
        <div style={{ position: "relative", width: 250, height: 266, [lado > 0 ? "marginRight" : "marginLeft"]: -34, zIndex: 2,
          transform: `scaleX(${lado > 0 ? 1 : -1})` }}>
          {img("marca/selo-tiao-cafe.png", 1)}
          <svg width={60} height={140} viewBox="-30 -130 60 140" style={{ position: "absolute", left: mx - 30, top: my - 130, overflow: "visible" }}>
            {[0, 1, 2].map((k) => { const q = fio(k); return <path key={k} d={q.d} transform={q.tr} fill="none" stroke="white" strokeOpacity={q.op} strokeWidth={8} style={{ filter: "drop-shadow(0 0 3px rgba(60,40,30,0.7))" }} strokeLinecap="round" />; })}
          </svg>
        </div>
        <svg width={420} height={150} viewBox="0 0 420 150" style={{ overflow: "visible" }}>
          <line x1={110} y1={-50} x2={120} y2={22} stroke="#3A2A1E" strokeWidth={4} /><line x1={330} y1={-50} x2={320} y2={22} stroke="#3A2A1E" strokeWidth={4} />
          <rect x={6} y={20} width={408} height={124} rx={16} fill={MADEIRA} stroke="#111" strokeWidth={6} />
          <line x1={20} y1={62} x2={400} y2={62} stroke="#6E4527" strokeWidth={3} /><line x1={20} y1={102} x2={400} y2={102} stroke="#6E4527" strokeWidth={3} />
          <text x={222} y={76} textAnchor="middle" fontFamily={fontFamily} fontWeight={800} fontSize={46} fill={CREME} stroke="#111" strokeWidth={9} paintOrder="stroke">TIÃO</text>
          <text x={222} y={126} textAnchor="middle" fontFamily={fontFamily} fontWeight={800} fontSize={46} fill={AMARELO} stroke="#111" strokeWidth={9} paintOrder="stroke">CONVERSA</text>
        </svg>
      </div>
    );
  }
  return (  // fita amarela, como etiqueta colada
    <div style={{ ...pos, background: AMARELO, border: "5px solid #111", borderRadius: 10, padding: "8px 30px 6px", boxShadow: "0 10px 18px rgba(0,0,0,0.45)",
      fontFamily, fontWeight: 800, fontSize: 60, color: "#111", letterSpacing: 1, display: "flex", alignItems: "center", gap: 16 }}>
      <svg width={54} height={50} viewBox="0 0 54 50"><path d="M4 8 H38 V40 Q38 46 32 46 H10 Q4 46 4 40 Z" fill="white" stroke="#111" strokeWidth={4} />
        <path d="M38 16 Q50 16 50 26 Q50 36 38 36" fill="none" stroke="#111" strokeWidth={4} /><path d="M12 8 L16 14 L20 8" fill="#FFD43B" stroke="#111" strokeWidth={3} /></svg>
      PROSA DO TIÃO</div>
  );
};

const NOME: Record<string, NomePose> = { P1: "pensativo", P2: "explica", P3: "aponta", P4: "alerta" };
// piscar: um a cada 3 a 5 s, rápido (0,16 s)
const piscada = (t: number) => {
  const k = Math.floor(t / 4), ini = k * 4 + fixo(k + 11) * 2.4, d = t - ini;
  return d >= 0 && d < 0.16 ? 1 - Math.abs(d - 0.08) / 0.08 : 0;
};

export const Conversa: React.FC<{ fundo: string; pose: string; t0: number; dur: number; lado?: 1 | -1 }> = ({ fundo, pose, t0, dur, lado = 1 }) => {
  const f = useCurrentFrame(); const { fps, height } = useVideoConfig(); const t = f / fps; const T = t0 + t;
  const { onda, selo } = useContext(EstiloCtx); const v = useVoz();
  const z = 1.04 + 0.07 * (t / Math.max(1, dur));                     // zoom lento do fundo
  const entra = mola(t, 6, 1);
  const resp = 1 + 0.006 * Math.sin(T * 1.7);                          // respira
  const nome = NOME[(pose.match(/P\d/) ?? [""])[0]];
  const alt = height * 0.92; const [pw, ph] = nome ? TAM_POSE(nome) : [1, 1];
  const fala = Math.min(1, v(T) * 1.5);
  const boca = fala < 0.08 ? 0 : fala * (0.55 + 0.45 * Math.abs(Math.sin(T * 17)));  // abre e fecha nas sílabas
  const estilo: React.CSSProperties = { position: "absolute", bottom: 0, [lado > 0 ? "left" : "right"]: 40, height: alt,
    transform: `translateY(${(1 - entra) * 60}px) scale(${resp})`, transformOrigin: "50% 100%", filter: "drop-shadow(0 18px 40px rgba(0,0,0,0.55))" };
  const ondaPos: React.CSSProperties = { position: "absolute", bottom: 60, [lado > 0 ? "right" : "left"]: 110 };
  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#0b0f16" }}>
      <Img src={staticFile(fundo)} style={{ width: "100%", height: "100%", objectFit: "cover", transform: `scale(${z})`, filter: "saturate(1.05)" }} />
      <AbsoluteFill style={{ background: lado > 0 ? "linear-gradient(90deg, rgba(5,8,14,0.15) 0%, rgba(5,8,14,0.55) 55%, rgba(5,8,14,0.7) 100%)"
                                               : "linear-gradient(270deg, rgba(5,8,14,0.15) 0%, rgba(5,8,14,0.55) 55%, rgba(5,8,14,0.7) 100%)" }} />
      {nome ? <div style={{ ...estilo, width: alt * pw / ph }}><TiaoPose pose={nome} piscar={piscada(T)} boca={boca} sorriso={nome === "pensativo" ? 0.1 : undefined} /></div>
            : <Img src={staticFile(pose)} style={estilo} />}
      {onda === "barras" && <div style={ondaPos}><Ondas t={T} /></div>}
      {onda === "linha" && <div style={{ ...ondaPos, bottom: 40 }}><Linha t={T} /></div>}
      {onda === "pilulas" && <div style={{ ...ondaPos, bottom: 30, [lado > 0 ? "right" : "left"]: 120 }}><Pilulas t={T} /></div>}
      {onda === "radio" && <div style={{ position: "absolute", bottom: 40, [lado > 0 ? "right" : "left"]: 80 }}><Radio t={T} /></div>}
      <Selo tipo={selo} t={t} lado={lado} />
    </AbsoluteFill>
  );
};
