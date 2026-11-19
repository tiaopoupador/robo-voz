// O Tiao VERDADEIRO a mexer-se (Ed, 18/11/2026: «Precisa ser mais parecido com o Tiao real!»).
// Corpo inteiro: as pecas recortadas da ficha (banco/boneco-tiao/montar_pecas.py), cada uma a rodar no seu eixo.
// Plano medio: as poses verdadeiras da playlist Conversa (montar_poses.py). Nos dois, os olhos, as sobrancelhas
// (so no corpo inteiro) e a boca sao desenhados por cima, no mesmo traco, para piscar, falar e mudar de emocao.
import React from "react";
import { Img, staticFile } from "remotion";
import PECAS from "../../../public/boneco/tiao/pecas.json";
import POSES from "../../../public/boneco/tiao/poses.json";

export type PoseCorpo = {
  bracoE: number; bracoD: number; pernaE: number; pernaD: number; cabeca: number; tronco: number;
  piscar: number; boca: number; sorriso: number; sobr: number; espanto: number; olhar: number; respira: number;
};
export const CORPO_BASE: PoseCorpo = { bracoE: 0, bracoD: 0, pernaE: 0, pernaD: 0, cabeca: 0, tronco: 0, piscar: 0, boca: 0, sorriso: 1, sobr: 0, espanto: 0, olhar: 0, respira: 0 };

const TINTA = "#1B1310", SOBR = "#231712", BOCA_DENTRO = "#6E2219", LINGUA = "#D5645A", LABIO = "#4A2018";
const P = PECAS as any;
const [W, H] = P.tam as [number, number];

// cada peca: uma camada do tamanho da folha inteira, que roda no seu eixo. <Img> faz o Remotion esperar a imagem.
const FOLHA: React.CSSProperties = { position: "absolute", left: 0, top: 0, width: W, height: H };
const Camada: React.FC<{ rot?: number; eixo?: [number, number]; dy?: number; children?: React.ReactNode }> = ({ rot = 0, eixo = [0, 0], dy = 0, children }) => (
  <div style={{ ...FOLHA, transformOrigin: `${eixo[0]}px ${eixo[1]}px`, transform: `translateY(${dy}px) rotate(${rot}deg)` }}>{children}</div>
);
const Peca: React.FC<{ n: string; rot?: number; eixo?: [number, number]; children?: React.ReactNode }> = ({ n, rot = 0, eixo, children }) => {
  const c = P.pecas[n];
  return (
    <Camada rot={rot} eixo={eixo ?? P.eixos[n] ?? [0, 0]}>
      <Img src={staticFile(`boneco/tiao/${n}.png`)} style={{ position: "absolute", left: c.x, top: c.y, width: c.w, height: c.h }} />
      {children && <svg width={W} height={H} viewBox={`0 0 ${W} ${H}`} style={{ position: "absolute", left: 0, top: 0, overflow: "visible" }}>{children}</svg>}
    </Camada>
  );
};

// boca desenhada: fechada = sorriso fino; aberta = labio de cima fixo, o de baixo desce com a voz
export const Boca: React.FC<{ cx: number; cy: number; mw: number; aberta: number; sorriso: number; esc?: number }> = ({ cx, cy, mw, aberta, sorriso, esc = 1 }) => {
  const sx = cx - mw, dx = cx + mw, canto = cy - 14 * sorriso * esc;
  if (aberta < 0.07) {
    return <path d={`M ${sx} ${canto} Q ${cx} ${cy + 26 * sorriso * esc} ${dx} ${canto}`} fill="none" stroke={LABIO} strokeWidth={8 * esc} strokeLinecap="round" />;
  }
  const cima = cy + 6 * sorriso * esc, baixo = cy + (14 + 62 * aberta) * esc + 10 * sorriso * esc;
  const mw2 = mw * (0.86 + 0.1 * sorriso - 0.12 * aberta);
  const d = `M ${cx - mw2} ${canto} Q ${cx} ${cima} ${cx + mw2} ${canto} Q ${cx + mw2 * 0.8} ${baixo} ${cx} ${baixo} Q ${cx - mw2 * 0.8} ${baixo} ${cx - mw2} ${canto} Z`;
  return (
    <g>
      <path d={d} fill={BOCA_DENTRO} />
      <clipPath id={`b${Math.round(cx)}${Math.round(cy)}`}><path d={d} /></clipPath>
      <g clipPath={`url(#b${Math.round(cx)}${Math.round(cy)})`}>
        <ellipse cx={cx} cy={baixo + 4 * esc} rx={mw2 * 0.62} ry={(10 + 26 * aberta) * esc} fill={LINGUA} />
        <rect x={cx - mw2} y={cima - 30 * esc} width={mw2 * 2} height={(30 + 12 * Math.min(1, aberta * 2)) * esc} fill="#FBF6EE" />
      </g>
      <path d={d} fill="none" stroke={LABIO} strokeWidth={7 * esc} strokeLinejoin="round" />
    </g>
  );
};

// olho: o ponto preto do desenho; ao piscar vira um risco curvo; no espanto ganha branco em volta
export const Olho: React.FC<{ cx: number; cy: number; rx: number; ry: number; piscar: number; espanto?: number; olhar?: number }> = ({ cx, cy, rx, ry, piscar, espanto = 0, olhar = 0 }) => {
  const abre = 1 - piscar;
  if (abre < 0.18) return <path d={`M ${cx - rx * 1.5} ${cy + 4} Q ${cx} ${cy + ry * 0.55} ${cx + rx * 1.5} ${cy + 4}`} fill="none" stroke={TINTA} strokeWidth={9} strokeLinecap="round" />;
  const e = espanto;
  return (
    <g>
      {e > 0.05 && <ellipse cx={cx} cy={cy} rx={rx * (1 + 1.1 * e)} ry={ry * (1 + 0.45 * e) * abre} fill="#FFFDF7" stroke={TINTA} strokeWidth={6 * e} opacity={Math.min(1, e * 2)} />}
      <ellipse cx={cx + olhar * rx * 0.5} cy={cy} rx={rx * (1 - 0.2 * e)} ry={ry * abre * (1 - 0.25 * e)} fill={TINTA} />
    </g>
  );
};

// o Tiao de corpo inteiro (pes em baixo ao centro da imagem 1161 x 2909)
export const TiaoCorpo: React.FC<{ p: PoseCorpo; alt: number }> = ({ p, alt }) => {
  const r = P.rosto; const [oex, oey, oerx, oery] = r.olhoE; const [odx, ody, odrx, odry] = r.olhoD;
  const sb = -26 * p.sobr - 20 * p.espanto;
  const sob = (pts: number[][], lado: number) => {
    const [a, m, b] = pts; const inc = 14 * Math.min(0, p.sobr) * lado; // bravo: as pontas de dentro descem
    return `M ${a[0]} ${a[1] + sb - (lado > 0 ? inc : -inc)} Q ${m[0]} ${m[1] + sb - 6 * p.espanto} ${b[0]} ${b[1] + sb + (lado > 0 ? inc : -inc)}`;
  };
  const sobe = -10 * p.respira;
  const [bx, by, bw] = r.boca;
  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <div style={{ ...FOLHA, transformOrigin: "0 0", transform: `scale(${alt / H})` }}>
        <Camada rot={p.tronco} eixo={[W / 2, 1990]}>
          <Peca n="perna_e" rot={p.pernaE} />
          <Peca n="perna_d" rot={p.pernaD} />
          <Camada dy={sobe * 0.3}>
            <Peca n="braco_e" rot={p.bracoE} />
            <Peca n="braco_d" rot={p.bracoD} />
            <Camada dy={sobe * 0.4}><Peca n="tronco" /></Camada>
            <Peca n="manga_e" rot={p.bracoE * 0.35} eixo={P.eixos.braco_e} />
            <Peca n="manga_d" rot={p.bracoD * 0.35} eixo={P.eixos.braco_d} />
            <Camada dy={sobe}>
              <Peca n="cabeca" rot={p.cabeca}>
                <path d={sob(r.sobrE, 1)} fill="none" stroke={SOBR} strokeWidth={30} strokeLinecap="round" />
                <path d={sob(r.sobrD, -1)} fill="none" stroke={SOBR} strokeWidth={30} strokeLinecap="round" />
                <Olho cx={oex} cy={oey} rx={oerx} ry={oery} piscar={p.piscar} espanto={p.espanto} olhar={p.olhar} />
                <Olho cx={odx} cy={ody} rx={odrx} ry={odry} piscar={p.piscar} espanto={p.espanto} olhar={p.olhar} />
                <Boca cx={bx} cy={by + 4} mw={bw} aberta={Math.max(p.boca, 0.45 * p.espanto)} sorriso={p.sorriso} />
              </Peca>
            </Camada>
          </Camada>
        </Camada>
      </div>
    </div>
  );
};

// o Tiao em plano medio, numa das poses verdadeiras
export type NomePose = "pensativo" | "explica" | "aponta" | "alerta";
export const TiaoPose: React.FC<{ pose: NomePose; piscar: number; boca: number; sorriso?: number }> = ({ pose, piscar, boca, sorriso }) => {
  const q = (POSES as any)[pose]; const [w, h] = q.tam; const [bx, by, bw, base] = q.boca;
  const sor = sorriso ?? (pose === "explica" ? 0.9 : pose === "aponta" ? -0.1 : -0.3);
  return (
    <div style={{ position: "relative", width: "100%", height: "100%" }}>
      <Img src={staticFile(`boneco/tiao/pose_${pose}.png`)} style={{ position: "absolute", inset: 0, width: "100%", height: "100%" }} />
      <svg viewBox={`0 0 ${w} ${h}`} width="100%" height="100%" style={{ position: "absolute", inset: 0, overflow: "visible" }}>
        {q.olhos.map((o: number[], i: number) => <Olho key={i} cx={o[0]} cy={o[1]} rx={o[2]} ry={o[3]} piscar={piscar} />)}
        <Boca cx={bx} cy={by} mw={bw} aberta={Math.max(boca, base * 0.35)} sorriso={sor} esc={0.85} />
      </svg>
    </div>
  );
};
export const TAM_POSE = (pose: NomePose) => (POSES as any)[pose].tam as [number, number];
export const TAM_CORPO = [W, H] as const;
