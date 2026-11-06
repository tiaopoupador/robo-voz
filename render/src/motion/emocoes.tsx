// Emocoes do canal, desenhadas em codigo no nosso traco (contorno preto grosso, cores do Tiao). Nada de emoji pronto.
// Ed (05/11): "queria que voce criasse motion graphics unicos e nossos, tipo um coracao partindo ao meio, um rosto chorando,
// com cara de espanto, outro rindo... nossos proprios emojis". Os emojis prontos ficam so de reserva.
// Uso: <Emocao e="😱" x={80} y={20} ini={0.6} />  (o emoji e so a CHAVE: o desenho e nosso)
import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola, MOLAS } from "../mola";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
const COR = { tinta: "#1F1B16", amarelo: "#F2B632", vermelho: "#D9443A", verde: "#2E9E5B", azul: "#3B6EA8", cinza: "#8A8175", branco: "#FFFDF8" };
const m = (t: number, ini: number, tipo: keyof typeof MOLAS = "cartao") => { const [w, z] = MOLAS[tipo]; return mola(t - ini, w, z); };
const T = COR.tinta, PELE = "#FFCB3D", PELE2 = "#F2A928", BOCA = "#7A2A1E", LINGUA = "#E86A5C", AGUA = "#5BB8F0", ROSA = "#F28B9B";
const L = 7; // contorno

type Olhos = "ponto" | "feliz" | "triste" | "arregalado" | "coracao" | "cifrao" | "estrela" | "lado" | "sono" | "oculos" | "cima" | "pidao";
type Boca = "sorriso" | "risao" | "O" | "o" | "triste" | "reta" | "careta" | "torta" | "ziper" | "ondulada" | "lingua";
type Sobr = "nenhuma" | "triste" | "brava" | "erguida" | "alta";
type Extra = "lagrimas" | "lagrima" | "suor" | "rubor" | "vapor" | "zzz" | "interroga" | "brilhos" | "bufada" | "tremor" | "balanca" | "susto";
type Rosto = { olhos: Olhos; boca: Boca; sobr?: Sobr; extras?: Extra[]; cor?: string };

const ROSTOS: Record<string, Rosto> = {
  "😰": { olhos: "ponto", boca: "ondulada", sobr: "triste", extras: ["suor"] },
  "😩": { olhos: "triste", boca: "triste", sobr: "triste", extras: ["suor"] },
  "😬": { olhos: "arregalado", boca: "careta", sobr: "triste", extras: ["suor"] },
  "😱": { olhos: "arregalado", boca: "O", sobr: "alta", extras: ["tremor", "susto"], cor: "#BFE3F7" },
  "😞": { olhos: "triste", boca: "triste", sobr: "triste", extras: ["lagrimas"] },
  "😔": { olhos: "triste", boca: "triste", sobr: "triste", extras: ["lagrima"] },
  "😓": { olhos: "ponto", boca: "reta", sobr: "triste", extras: ["suor"] },
  "😌": { olhos: "feliz", boca: "sorriso", extras: ["rubor"] },
  "😮‍💨": { olhos: "triste", boca: "o", sobr: "triste", extras: ["bufada"] },
  "😎": { olhos: "oculos", boca: "sorriso", extras: ["brilhos"] },
  "🤑": { olhos: "cifrao", boca: "risao", extras: ["brilhos"] },
  "😂": { olhos: "feliz", boca: "risao", extras: ["lagrimas", "balanca"] },
  "🤭": { olhos: "feliz", boca: "sorriso", extras: ["rubor", "balanca"] },
  "😏": { olhos: "lado", boca: "torta", sobr: "erguida" },
  "🤫": { olhos: "ponto", boca: "ziper", sobr: "erguida" },
  "🤔": { olhos: "cima", boca: "torta", sobr: "erguida", extras: ["interroga"] },
  "🧐": { olhos: "lado", boca: "reta", sobr: "erguida", extras: ["interroga"] },
  "🤨": { olhos: "lado", boca: "reta", sobr: "erguida" },
  "😴": { olhos: "sono", boca: "o", extras: ["zzz"] },
  "😳": { olhos: "arregalado", boca: "o", sobr: "alta", extras: ["rubor"] },
  "😒": { olhos: "lado", boca: "triste", sobr: "reta" as Sobr },
  "💪": { olhos: "ponto", boca: "sorriso", sobr: "brava", extras: ["brilhos"] },
  "😋": { olhos: "feliz", boca: "lingua" },
  "😅": { olhos: "feliz", boca: "sorriso", extras: ["suor"] },
  "😍": { olhos: "coracao", boca: "risao" },
  "🤩": { olhos: "estrela", boca: "risao", extras: ["brilhos"] },
  "🙏": { olhos: "pidao", boca: "ondulada", sobr: "triste" },
  "😮": { olhos: "arregalado", boca: "O", sobr: "alta" },
  "😄": { olhos: "feliz", boca: "risao" },
  "🥳": { olhos: "feliz", boca: "risao", extras: ["brilhos"] },
};
const ESPECIAIS = new Set(["💔", "❤️", "🤝", "💡", "🚨", "📉", "💥", "🎉", "👀"]);
export const temEmocao = (e: string) => e in ROSTOS || ESPECIAIS.has(e);

// ---------- pedacos do rosto ----------
const coracaoPath = "M0,30 C-40,0 -40,-30 -20,-38 C-8,-42 0,-32 0,-24 C0,-32 8,-42 20,-38 C40,-30 40,0 0,30 Z";
const estrelaPath = (r: number) => Array.from({ length: 10 }, (_, i) => { const a = (i * Math.PI) / 5 - Math.PI / 2, rr = i % 2 ? r * 0.45 : r; return `${i ? "L" : "M"}${(Math.cos(a) * rr).toFixed(1)},${(Math.sin(a) * rr).toFixed(1)}`; }).join(" ") + "Z";

const OlhoPar: React.FC<{ tipo: Olhos; t: number }> = ({ tipo, t }) => {
  const pisca = (t % 3.1) > 2.95 ? 0.15 : 1; // pisca de vez em quando
  const lado = (s: number) => {
    const x = 34 * s, y = -14;
    switch (tipo) {
      case "ponto": return <ellipse cx={x} cy={y} rx={10} ry={15 * pisca} fill={T} />;
      case "cima": return <g><ellipse cx={x} cy={y} rx={10} ry={15 * pisca} fill={T} /><circle cx={x + 3} cy={y - 7} r={3.5} fill="#fff" /></g>;
      case "feliz": return <path d={`M${x - 15},${y + 4} Q${x},${y - 16} ${x + 15},${y + 4}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />;
      case "triste": return <path d={`M${x - 14},${y - 2} Q${x},${y + 12} ${x + 14},${y - 2}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />;
      case "sono": return <line x1={x - 14} y1={y + 2} x2={x + 14} y2={y + 2} stroke={T} strokeWidth={L} strokeLinecap="round" />;
      case "arregalado": { const tr = Math.sin(t * 40) * 2.5; return <g><circle cx={x} cy={y} r={23} fill="#fff" stroke={T} strokeWidth={5} /><circle cx={x + tr} cy={y + 2} r={8} fill={T} /></g>; }
      case "pidao": return <g><circle cx={x} cy={y} r={21} fill={T} /><circle cx={x + 6} cy={y - 7} r={7} fill="#fff" /><circle cx={x - 6} cy={y + 6} r={3.5} fill="#fff" /></g>;
      case "lado": { const px = Math.sin(t * 1.5) > 0 ? 8 : 6; return <g><ellipse cx={x} cy={y + 2} rx={16} ry={11} fill="#fff" stroke={T} strokeWidth={5} /><circle cx={x + px} cy={y + 3} r={6} fill={T} /><line x1={x - 18} y1={y - 5} x2={x + 18} y2={y - 5} stroke={T} strokeWidth={L} strokeLinecap="round" /></g>; }
      case "coracao": { const p = 1 + 0.18 * Math.max(0, Math.sin(t * 7)); return <path d={coracaoPath} transform={`translate(${x},${y + 4}) scale(${0.55 * p})`} fill={COR.vermelho} stroke={T} strokeWidth={9} />; }
      case "estrela": return <path d={estrelaPath(20)} transform={`translate(${x},${y}) rotate(${t * 60})`} fill={COR.amarelo} stroke={T} strokeWidth={4.5} />;
      case "cifrao": return <text x={x} y={y + 14} textAnchor="middle" fontFamily={fontFamily} fontWeight={800} fontSize={44} fill={COR.verde} stroke={T} strokeWidth={2.5} transform={`scale(${1 + 0.08 * Math.sin(t * 8)})`} style={{ transformOrigin: `${x}px ${y}px` }}>$</text>;
      case "oculos": return null;
    }
  };
  return <g>{lado(-1)}{lado(1)}</g>;
};

const Oculos: React.FC<{ t: number }> = ({ t }) => {
  const desce = m(t, 0.15, "cartao"), y = -90 + 76 * desce;
  return (
    <g transform={`translate(0,${y})`}>
      <path d="M-62,-6 L62,-6" stroke={T} strokeWidth={8} />
      {[-1, 1].map((s) => <path key={s} d={`M${s * 8},-8 L${s * 58},-8 Q${s * 60},18 ${s * 34},20 Q${s * 10},18 ${s * 8},-8 Z`} fill={T} />)}
      <path d="M-46,-2 L-30,-2" stroke="#fff" strokeWidth={4} opacity={0.6 + 0.4 * Math.sin(t * 3)} strokeLinecap="round" />
    </g>
  );
};

const Sobrancelhas: React.FC<{ tipo: Sobr }> = ({ tipo }) => {
  if (tipo === "nenhuma") return null;
  const d = (s: number) => {
    const x = 34 * s, fora = x + 16 * s, dentro = x - 16 * s;
    switch (tipo) {
      case "triste": return `M${fora},-42 L${dentro},-54`;
      case "brava": return `M${fora},-54 L${dentro},-42`;
      case "alta": return `M${x - 15},-56 Q${x},-64 ${x + 15},-56`;
      case "erguida": return s < 0 ? `M${x - 15},-44 L${x + 15},-44` : `M${x - 15},-56 Q${x},-66 ${x + 15},-58`;
      default: return `M${x - 15},-46 L${x + 15},-46`;
    }
  };
  return <g>{[-1, 1].map((s) => <path key={s} d={d(s)} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />)}</g>;
};

const BocaDe: React.FC<{ tipo: Boca; t: number }> = ({ tipo, t }) => {
  const y = 34;
  switch (tipo) {
    case "sorriso": return <path d={`M-30,${y - 6} Q0,${y + 22} 30,${y - 6}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />;
    case "risao": { const a = 1 + 0.12 * Math.sin(t * 16); return <g transform={`translate(0,${y}) scale(1,${a})`}><path d="M-40,-10 Q0,-12 40,-10 Q36,34 0,36 Q-36,34 -40,-10 Z" fill={BOCA} stroke={T} strokeWidth={L} strokeLinejoin="round" /><path d="M-18,22 Q0,12 18,22 Q12,34 0,34 Q-12,34 -18,22 Z" fill={LINGUA} /><path d="M-34,-8 L34,-8 L30,2 L-30,2 Z" fill="#fff" /></g>; }
    case "O": { const a = 1 + 0.15 * Math.sin(t * 12); return <ellipse cx={0} cy={y + 6} rx={20} ry={26 * a} fill={BOCA} stroke={T} strokeWidth={L} />; }
    case "o": return <ellipse cx={0} cy={y + 2} rx={10} ry={12} fill={BOCA} stroke={T} strokeWidth={6} />;
    case "triste": return <path d={`M-28,${y + 12} Q0,${y - 12} 28,${y + 12}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />;
    case "reta": return <line x1={-24} y1={y + 4} x2={24} y2={y + 4} stroke={T} strokeWidth={L} strokeLinecap="round" />;
    case "torta": return <path d={`M-24,${y + 8} Q4,${y + 10} 28,${y - 6}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" />;
    case "careta": return <g><rect x={-38} y={y - 10} width={76} height={30} rx={8} fill="#fff" stroke={T} strokeWidth={L} />{[-19, 0, 19].map((x) => <line key={x} x1={x} y1={y - 10} x2={x} y2={y + 20} stroke={T} strokeWidth={4} />)}<line x1={-38} y1={y + 5} x2={38} y2={y + 5} stroke={T} strokeWidth={4} /></g>;
    case "ziper": return <g><line x1={-30} y1={y + 4} x2={30} y2={y + 4} stroke={T} strokeWidth={L} strokeLinecap="round" />{[-22, -11, 0, 11, 22].map((x) => <line key={x} x1={x} y1={y - 4} x2={x} y2={y + 12} stroke={T} strokeWidth={4} />)}<rect x={26} y={y - 4} width={12} height={16} rx={3} fill={COR.cinza} stroke={T} strokeWidth={3} /></g>;
    case "ondulada": { const f = Math.sin(t * 9) * 3; return <path d={`M-30,${y + 4} Q-20,${y - 6 + f} -10,${y + 4} Q0,${y + 14 - f} 10,${y + 4} Q20,${y - 6 + f} 30,${y + 4}`} fill="none" stroke={T} strokeWidth={6} strokeLinecap="round" />; }
    case "lingua": return <g><path d={`M-30,${y - 6} Q0,${y + 18} 30,${y - 6}`} fill="none" stroke={T} strokeWidth={L} strokeLinecap="round" /><path d={`M4,${y + 4} Q14,${y + 34 + 4 * Math.sin(t * 6)} 26,${y + 2}`} fill={LINGUA} stroke={T} strokeWidth={5} /></g>;
  }
};

const Extras: React.FC<{ lista: Extra[]; t: number }> = ({ lista, t }) => (
  <g>
    {lista.includes("rubor") && [-1, 1].map((s) => <ellipse key={s} cx={56 * s} cy={14} rx={16} ry={9} fill={ROSA} opacity={0.75} />)}
    {lista.includes("suor") && (() => { const p = (t * 0.7) % 1; return <path d="M0,-14 Q10,2 0,10 Q-10,2 0,-14 Z" transform={`translate(72,${-50 + p * 50}) scale(1.4)`} fill={AGUA} stroke={T} strokeWidth={3} opacity={1 - p * 0.6} />; })()}
    {(lista.includes("lagrimas") || lista.includes("lagrima")) && [-1, 1].filter((s) => lista.includes("lagrimas") || s > 0).map((s) => (
      <g key={s}>{[0, 0.33, 0.66].map((d) => { const p = (t * 1.1 + d) % 1; return <path key={d} d="M0,-10 Q8,2 0,8 Q-8,2 0,-10 Z" transform={`translate(${40 * s + s * p * 8},${4 + p * 80}) scale(1.3)`} fill={AGUA} stroke={T} strokeWidth={2.5} opacity={1 - p} />; })}
        <path d={`M${30 * s},2 Q${44 * s},40 ${38 * s},84`} fill="none" stroke={AGUA} strokeWidth={9} strokeLinecap="round" opacity={0.85} /></g>
    ))}
    {lista.includes("vapor") && [0, 0.5].map((d) => { const p = (t * 0.8 + d) % 1; return <circle key={d} cx={(d ? 40 : -40) + Math.sin(p * 6) * 6} cy={-96 - p * 50} r={12 + p * 14} fill="#fff" stroke={T} strokeWidth={4} opacity={1 - p} />; })}
    {lista.includes("zzz") && [0, 0.33, 0.66].map((d) => { const p = (t * 0.45 + d) % 1; return <text key={d} x={60 + p * 40} y={-60 - p * 70} fontFamily={fontFamily} fontWeight={800} fontSize={26 + p * 26} fill={COR.azul} stroke={T} strokeWidth={2} opacity={1 - p}>Z</text>; })}
    {lista.includes("interroga") && [0, 1].map((i) => <text key={i} x={i ? 90 : 62} y={i ? -70 : -92} fontFamily={fontFamily} fontWeight={800} fontSize={i ? 40 : 56} fill={COR.azul} stroke={T} strokeWidth={2.5} transform={`translate(0,${Math.sin(t * 3 + i * 2) * 6})`}>?</text>)}
    {lista.includes("brilhos") && [[-80, -70, 18], [86, -40, 14], [70, -96, 10]].map(([x, y, r], i) => <path key={i} d="M0,-1 C2,-0.3 0.3,-2 1,0 C0.3,2 2,0.3 0,1 C-2,0.3 -0.3,2 -1,0 C-0.3,-2 -2,-0.3 0,-1 Z" transform={`translate(${x},${y}) scale(${r * (0.6 + 0.4 * Math.abs(Math.sin(t * 4 + i)))})`} fill="#FFF3B0" stroke="#E8A800" strokeWidth={0.12} />)}
    {lista.includes("bufada") && (() => { const p = (t * 0.9) % 1; return <g opacity={1 - p}>{[0, 1, 2].map((i) => <circle key={i} cx={10 + p * 70 + i * 16} cy={44 + i * 4} r={8 + p * 10 + i * 3} fill="#fff" stroke={T} strokeWidth={3} />)}</g>; })()}
    {lista.includes("susto") && [-1, 1].map((s) => <g key={s}>{[-30, 0, 30].map((a) => <line key={a} x1={0} y1={-96} x2={0} y2={-120} stroke={T} strokeWidth={6} strokeLinecap="round" transform={`rotate(${a + s * 0})`} opacity={0.5 + 0.5 * Math.sin(t * 20)} />)}</g>)}
  </g>
);

const RostoSVG: React.FC<{ r: Rosto; t: number; tam: number }> = ({ r, t, tam }) => {
  const ex = r.extras ?? [];
  const tremX = ex.includes("tremor") ? Math.sin(t * 50) * 3 : 0, bal = ex.includes("balanca") ? Math.sin(t * 14) * 6 : 0;
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      <g transform={`translate(${tremX},0) rotate(${bal})`}>
        <circle r={90} fill={r.cor ?? PELE} stroke={T} strokeWidth={L} />
        <path d="M-78,40 Q0,112 78,40 Q60,92 0,92 Q-60,92 -78,40 Z" fill={PELE2} opacity={0.35} />
        <ellipse cx={-34} cy={-60} rx={22} ry={10} fill="#fff" opacity={0.45} transform="rotate(-20 -34 -60)" />
        <Sobrancelhas tipo={r.sobr ?? "nenhuma"} />
        <OlhoPar tipo={r.olhos} t={t} />
        {r.olhos === "oculos" && <Oculos t={t} />}
        <BocaDe tipo={r.boca} t={t} />
        <Extras lista={ex} t={t} />
      </g>
    </svg>
  );
};

// ---------- pecas especiais ----------
const CoracaoPartido: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const racha = Math.min(1, Math.max(0, (t - 0.45) / 0.25)), abre = m(t, 0.75, "cartao");
  const lado = (s: number) => (
    <g transform={`translate(${s * 34 * abre},${40 * abre * abre}) rotate(${s * 22 * abre})`}>
      <clipPath id={`m${s}`}><path d={s < 0 ? "M-60,-60 L4,-60 L-6,-30 L8,-10 L-4,10 L4,40 L-60,40 Z" : "M60,-60 L4,-60 L-6,-30 L8,-10 L-4,10 L4,40 L60,40 Z"} /></clipPath>
      <path d={coracaoPath} transform="scale(2.2)" fill={COR.vermelho} stroke={T} strokeWidth={3.2} clipPath={`url(#m${s})`} />
    </g>
  );
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      <g transform={`scale(${1 + 0.06 * Math.sin(Math.min(t, 0.45) * 20)})`}>
        {abre < 0.02 ? <path d={coracaoPath} transform="scale(2.2)" fill={COR.vermelho} stroke={T} strokeWidth={3.2} /> : <>{lado(-1)}{lado(1)}</>}
        {abre < 0.02 && racha > 0 && <polyline points="4,-60 -6,-30 8,-10 -4,10 4,40" fill="none" stroke={T} strokeWidth={7} strokeDasharray={140} strokeDashoffset={140 * (1 - racha)} transform="scale(1)" />}
        <ellipse cx={-38} cy={-46} rx={14} ry={8} fill="#fff" opacity={0.5 * (1 - abre)} />
      </g>
    </svg>
  );
};
const CoracaoBate: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const b = 1 + 0.14 * Math.max(0, Math.sin(t * 8)) * Math.max(0, Math.sin(t * 8 + 0.6));
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      {[0, 0.33, 0.66].map((d, i) => { const p = (t * 0.6 + d) % 1; return <path key={i} d={coracaoPath} transform={`translate(${(i - 1) * 60 + Math.sin(p * 8) * 8},${-40 - p * 110}) scale(${0.5 * (1 - p * 0.4)})`} fill={ROSA} stroke={T} strokeWidth={6} opacity={1 - p} />; })}
      <path d={coracaoPath} transform={`scale(${2.2 * b})`} fill={COR.vermelho} stroke={T} strokeWidth={3.2} />
      <ellipse cx={-38} cy={-46} rx={14} ry={8} fill="#fff" opacity={0.5} />
    </svg>
  );
};
const Lampada: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const acende = Math.min(1, Math.max(0, (t - 0.3) / 0.2)), pulso = 0.8 + 0.2 * Math.sin(t * 6);
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      {acende > 0 && Array.from({ length: 8 }, (_, i) => <line key={i} x1={0} y1={-96} x2={0} y2={-122} stroke={COR.amarelo} strokeWidth={9} strokeLinecap="round" transform={`rotate(${-70 + i * 20} 0 -10) scale(${pulso})`} opacity={acende} />)}
      <circle cx={0} cy={-20} r={66} fill={acende > 0 ? "#FFE680" : "#EEE"} stroke={T} strokeWidth={L} />
      {acende > 0 && <circle cx={0} cy={-20} r={90} fill="#FFE680" opacity={0.25 * acende * pulso} />}
      <path d="M-16,-8 L-6,-30 L6,-8 L16,-30" fill="none" stroke={acende > 0 ? COR.vermelho : COR.cinza} strokeWidth={5} />
      <rect x={-30} y={40} width={60} height={34} rx={6} fill={COR.cinza} stroke={T} strokeWidth={L} />
      <line x1={-30} y1={56} x2={30} y2={56} stroke={T} strokeWidth={4} />
    </svg>
  );
};
const Sirene: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const g = (t * 360 * 1.4) % 360;
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      <g transform={`rotate(${g} 0 -10)`} opacity={0.55}><path d="M0,-10 L-150,-60 L-150,40 Z" fill="#FF6B5B" /><path d="M0,-10 L150,-60 L150,40 Z" fill="#FF6B5B" /></g>
      <path d="M-56,40 L-56,-20 Q-56,-76 0,-76 Q56,-76 56,-20 L56,40 Z" fill={COR.vermelho} stroke={T} strokeWidth={L} />
      <ellipse cx={-22} cy={-40} rx={12} ry={20} fill="#fff" opacity={0.5 + 0.4 * Math.sin(t * 12)} />
      <rect x={-76} y={40} width={152} height={32} rx={8} fill={COR.cinza} stroke={T} strokeWidth={L} />
    </svg>
  );
};
const Queda: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const p = Math.min(1, Math.max(0, t / 0.8));
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      <rect x={-110} y={-100} width={220} height={200} rx={24} fill={COR.branco} stroke={T} strokeWidth={L} />
      <polyline points="-80,-60 -40,-20 -10,-40 30,20 70,60" fill="none" stroke={COR.vermelho} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" strokeDasharray={300} strokeDashoffset={300 * (1 - p)} />
      {p >= 1 && <path d="M70,60 L44,58 L68,34 Z" fill={COR.vermelho} stroke={COR.vermelho} strokeWidth={8} strokeLinejoin="round" transform={`translate(${Math.sin(t * 8) * 2},${Math.abs(Math.sin(t * 4)) * 4})`} />}
    </svg>
  );
};
const Explosao: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const e = m(t, 0, "estalo"), pts = (r1: number, r2: number) => Array.from({ length: 24 }, (_, i) => { const a = (i * Math.PI) / 12, r = i % 2 ? r2 : r1; return `${(Math.cos(a) * r).toFixed(1)},${(Math.sin(a) * r).toFixed(1)}`; }).join(" ");
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      <g transform={`scale(${e}) rotate(${t * 20})`}>
        <polygon points={pts(118, 70)} fill={COR.vermelho} stroke={T} strokeWidth={L} strokeLinejoin="round" />
        <polygon points={pts(84, 46)} fill={COR.amarelo} stroke={T} strokeWidth={5} strokeLinejoin="round" />
        <circle r={26} fill="#fff" opacity={0.85} />
      </g>
    </svg>
  );
};
const Confete: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const cores = [COR.vermelho, COR.amarelo, COR.verde, COR.azul, ROSA];
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      {Array.from({ length: 22 }, (_, i) => { const a = (i / 22) * Math.PI * 2, v = 140 + (i % 5) * 30, p = Math.min(1.6, t * 1.3); const x = Math.cos(a) * v * Math.min(1, p), y = Math.sin(a) * v * Math.min(1, p) + 60 * Math.max(0, p - 0.6) ** 2;
        return <rect key={i} x={x - 7} y={y - 4} width={14} height={8} fill={cores[i % 5]} stroke={T} strokeWidth={2} transform={`rotate(${t * 300 + i * 40} ${x} ${y})`} opacity={Math.max(0, 1 - Math.max(0, p - 1.2) * 2.5)} />; })}
      <g transform="translate(-75,-75)"><RostoSVG r={ROSTOS["🥳"]} t={t} tam={150} /></g>
    </svg>
  );
};
const OlhosGrandes: React.FC<{ t: number; tam: number }> = ({ t, tam }) => {
  const olha = Math.sin(t * 1.6) * 14, pisca = (t % 2.6) > 2.45 ? 0.1 : 1;
  return (
    <svg width={tam} height={tam} viewBox="-130 -130 260 260" style={{ overflow: "visible" }}>
      {[-1, 1].map((s) => <g key={s}><ellipse cx={s * 52} cy={0} rx={46} ry={58 * pisca} fill="#fff" stroke={T} strokeWidth={L} />{pisca > 0.5 && <><circle cx={s * 52 + olha} cy={8} r={20} fill={T} /><circle cx={s * 52 + olha + 7} cy={0} r={6} fill="#fff" /></>}</g>)}
    </svg>
  );
};

// ---------- a figura (sem posicao): usada nas reacoes e nos emojis das frases ----------
export const Figura: React.FC<{ e: string; tam: number; desde?: number }> = ({ e, tam, desde = 0 }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = Math.max(0, f / fps - desde);
  if (e === "💔") return <CoracaoPartido t={t} tam={tam} />;
  if (e === "❤️" || e === "🤝") return <CoracaoBate t={t} tam={tam} />;
  if (e === "💡") return <Lampada t={t} tam={tam} />;
  if (e === "🚨") return <Sirene t={t} tam={tam} />;
  if (e === "📉") return <Queda t={t} tam={tam} />;
  if (e === "💥") return <Explosao t={t} tam={tam} />;
  if (e === "🎉" || e === "🥳") return <Confete t={t} tam={tam} />;
  if (e === "👀") return <OlhosGrandes t={t} tam={tam} />;
  return <RostoSVG r={ROSTOS[e]} t={t} tam={tam} />;
};
