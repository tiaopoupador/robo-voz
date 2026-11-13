// A tela final NOVA, 10 s (Ed, 13/11/2026: «uma nova tela final que mostra somente 1 video, com o mesmo design da
// vinheta»; aprovou a VinhetaNova no mesmo dia). Mesma família: creme, azul, âmbar e amarelo, letra Baloo, a moeda
// que cai, quica e vira a medalha do Tião, e a onda amarela (aqui ela ENTRA e cobre a última cena).
// Lugares para o YouTube Studio (padrão 1920x1080):
//   · o quadro grande à direita (960 x 540, x 780, y 300) = o elemento "Vídeo" (o próximo, o do gancho final);
//   · a medalha à esquerda (círculo de 380, centro 350, 560) = o elemento "Inscrever-se" (mostra o ícone do canal).
// Funil do Joba (canal-dark longo.md seção 20): a fala termina no "já está aparecendo aqui, clica e vê agora"
// e o quadro já está lá. Só transform/opacity (e o traço da seta); tudo é função do tempo.
import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { mola } from "../mola";
import { AMARELO, AMBAR, AZUL, CREME, MoedaGira, Silaba, fontFamily } from "./VinhetaNova";

export const TELA_FINAL_NOVA_SEG = 10;
// os tempos (iguais no som, fabrica/tela_final_som.py)
export const TF = { onda: 0, quadro: 0.45, cai: 0.95, quica: [1.32, 1.6, 1.76], vira: 1.9, pal: [2.45, 2.62, 2.78, 2.96], botao: 3.3,
  seta: 3.0,
  // (Ed, 13/11: «achei que esta com pouco movimento! Tem que ter mais açao aqui!») do 3,9 s ao fim, sempre algo a acontecer:
  // um cursor voa e CLICA, alternando o vídeo e o INSCREVA-SE; cada clique tem resposta (onda no quadro, letras pulam,
  // sino toca, medalha gira de novo); a seta se redesenha; as listras do fundo andam e o contorno tracejado corre.
  // Tudo FORA do quadro e da medalha, porque o YouTube cobre esses dois lugares com os botões dele.
  cursor: [3.9, 5.3, 6.7, 8.1], clique: [4.5, 5.9, 7.3, 8.7], redesenha: [5.15, 7.95], giraDeNovo: 6.05 };
const DUR_VOO = 0.5;
const W = 1920, H = 1080, TINTA = "#1F1B16";
const cl = (x: number) => Math.max(0, Math.min(1, x));
const suave = (x: number) => { const c = cl(x); return c * c * (3 - 2 * c); };
const Q = { x: 780, y: 300, w: 960, h: 540 };      // o quadro do vídeo
const M = { x: 350, y: 560, r: 190 };              // a medalha (= botão de inscrever do YouTube)
const ALVO_QUADRO = { x: Q.x + Q.w + 4, y: Q.y + Q.h + 6 }, ALVO_BOTAO = { x: M.x + 110, y: 870 }, FORA = { x: 2050, y: 1200 };
const ALVOS = [ALVO_QUADRO, ALVO_BOTAO, ALVO_QUADRO, ALVO_BOTAO];
const pulinho = (t: number, em: number, dur = 0.26) => (t < em || t > em + dur ? 0 : Math.sin((Math.PI * (t - em)) / dur));
// um "toque" que passa e assenta: 0 antes, sobe, passa um fio, volta a 0
const toque = (t: number, em: number) => (t < em ? 0 : Math.sin((t - em) * 12) * Math.exp(-(t - em) * 4));

export const TelaFinalNova: React.FC<{ som?: string }> = ({ som = "marca/tela-final-nova.wav" }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;

  // 1 · a onda entra pela esquerda e cobre a última cena; atrás dela já está a tela final
  const o = cl(t / 0.8), ondaX = -2700 + (W + 2900) * suave(o), corte = Math.max(0, ondaX + 300);
  // 2 · o quadro do vídeo salta para o lugar
  const q = mola(t - TF.quadro, 11, 0.62);
  // 3 · a moeda cai do alto, quica 2 vezes e vira a medalha
  let my = -260, sq = 0;
  const [q1, q2, q3] = TF.quica;
  if (t >= TF.cai) {
    if (t < q1) { const p = (t - TF.cai) / (q1 - TF.cai); my = -260 + (M.y + 260) * p * p; }
    else if (t < q2) { const p = (t - q1) / (q2 - q1); my = M.y - 110 * 4 * p * (1 - p); }
    else if (t < q3) { const p = (t - q2) / (q3 - q2); my = M.y - 36 * 4 * p * (1 - p); }
    else my = M.y;
    for (const [k, qq] of TF.quica.entries()) if (t >= qq) sq = Math.max(sq, [0.2, 0.12, 0.06][k] * Math.exp(-(t - qq) * 22));
  }
  const giro = suave((t - TF.vira) / 0.3) * 180;
  const pulo = -60 * Math.sin(Math.PI * cl((t - TF.vira + 0.04) / 0.36));
  const balanca = -6 * (toque(t, TF.vira + 0.3) + toque(t, TF.clique[3] + 0.05));
  // a medalha gira de novo (360) quando o cursor clica no INSCREVA-SE: o visto antes de o YouTube cobrir, e um lembrete
  const giro2 = t >= TF.giraDeNovo ? suave((t - TF.giraDeNovo) / 0.5) * 360 : 0;
  const luz = cl((t - (TF.botao + 0.2)) / 0.5);
  // 4 · o botão de inscrever e a seta
  const b = mola(t - TF.botao, 24, 0.45);
  const aperta = TF.clique.filter((_, k) => k % 2 === 1).reduce((a, c) => a + 0.12 * pulinho(t, c, 0.18), 0);   // o botão afunda no clique
  const pulsa = (1 - aperta) * (1 + 0.06 * Math.max(0, toque(t, TF.clique[1] + 0.18) + toque(t, TF.clique[3] + 0.18)));
  // a seta: desenha, e a cada redesenho recolhe depressa e volta a desenhar
  let seta = suave((t - TF.seta) / 0.4);
  for (const r of TF.redesenha) if (t >= r - 0.15) seta = t < r ? 1 - suave((t - r + 0.15) / 0.15) : suave((t - r) / 0.35);
  const cutuca = t > TF.seta + 0.4 ? 10 * Math.max(0, Math.sin((t - TF.seta) * 4.2)) : 0;
  // o cursor: voa em arco de um alvo ao outro e clica (afunda e volta)
  let ck = -1; for (let k = 0; k < TF.cursor.length; k++) if (t >= TF.cursor[k]) ck = k;
  let cur = FORA;
  if (ck >= 0) {
    const de = ck === 0 ? FORA : ALVOS[ck - 1], para = ALVOS[ck], p = suave((t - TF.cursor[ck]) / DUR_VOO);
    cur = { x: de.x + (para.x - de.x) * p, y: de.y + (para.y - de.y) * p - 120 * Math.sin(Math.PI * p) };
  }
  const clicaCursor = TF.clique.reduce((a, c) => a + pulinho(t, c, 0.16), 0);
  // a resposta de cada clique no vídeo: um contorno que sai do quadro e se apaga; e as palavras pulam em fila
  const ondasQuadro = TF.clique.filter((_, k) => k % 2 === 0);
  const pulaPalavra = (k: number) => ondasQuadro.reduce((a, c) => a + pulinho(t, c + 0.05 + k * 0.07), 0);
  // o sino aparece no primeiro clique do INSCREVA-SE e toca em cada um
  const sino = mola(t - TF.clique[1], 20, 0.5), balancaSino = 22 * (toque(t, TF.clique[1]) + toque(t, TF.clique[3]));
  // o fundo: listras diagonais bem leves que andam devagar; o contorno tracejado corre em volta do quadro
  const listras = (t * 50) % 339.4, tracejado = -t * 140;
  const alto = Math.max(0, M.y - (my + pulo)) / 300;   // a sombra encolhe quando a moeda está no ar

  return (
    <AbsoluteFill style={{ overflow: "hidden" }}>
      {som && <Audio src={staticFile(som)} />}
      <AbsoluteFill style={{ clipPath: o < 1 ? `inset(0 ${Math.max(0, W - corte)}px 0 0)` : undefined, background: CREME }}>
        <div style={{ position: "absolute", left: -400, top: 0, width: W + 800, height: H, transform: `translateX(${listras}px)`,
          background: "repeating-linear-gradient(45deg, rgba(31,27,22,0) 0 120px, rgba(31,27,22,0.035) 120px 240px)" }} />
        {/* o contorno tracejado que corre em volta do quadro (fica de fora: o YouTube cobre só o quadro) */}
        {t > TF.quadro + 0.5 && (
          <svg width={W} height={H} style={{ position: "absolute", inset: 0, opacity: cl((t - TF.quadro - 0.5) / 0.3) }}>
            <rect x={Q.x - 36} y={Q.y - 36} width={Q.w + 72 + 18} height={Q.h + 72 + 18} rx={50} fill="none" stroke={AZUL} strokeWidth={6}
              strokeDasharray="34 26" strokeDashoffset={tracejado} strokeLinecap="round" />
            {ondasQuadro.map((c, k) => t >= c && t < c + 0.6 && (() => {
              const e = (t - c) / 0.6, d = 36 + 70 * e;
              return <rect key={k} x={Q.x - d} y={Q.y - d} width={Q.w + 2 * d + 18} height={Q.h + 2 * d + 18} rx={50 + d * 0.4} fill="none"
                stroke={AMBAR} strokeWidth={10 * (1 - e) + 2} opacity={1 - e} />;
            })())}
          </svg>
        )}
        {/* o quadro do vídeo: azul, contorno de tinta e a sombra chapada âmbar (a mesma das letras da vinheta) */}
        <div style={{ position: "absolute", left: Q.x, top: Q.y, width: Q.w, height: Q.h, opacity: t < TF.quadro ? 0 : 1,
          transform: `scale(${0.55 + 0.45 * q}) rotate(${-4 * (1 - q)}deg)`, transformOrigin: "50% 50%" }}>
          <div style={{ position: "absolute", left: 18, top: 18, width: Q.w, height: Q.h, borderRadius: 30, background: AMBAR }} />
          <div style={{ position: "absolute", inset: 0, borderRadius: 30, background: AZUL, border: `7px solid ${TINTA}`, boxSizing: "border-box",
            display: "flex", alignItems: "center", justifyContent: "center" }}>
            <div style={{ width: 150, height: 150, borderRadius: 999, background: AMARELO, display: "flex", alignItems: "center", justifyContent: "center" }}>
              <div style={{ width: 0, height: 0, borderTop: "34px solid transparent", borderBottom: "34px solid transparent", borderLeft: `54px solid ${AZUL}`, marginLeft: 12 }} />
            </div>
          </div>
        </div>
        {/* CLICA E VÊ AGORA, palavra por palavra no jingle */}
        <div style={{ position: "absolute", left: Q.x, top: 130, width: Q.w, textAlign: "center", whiteSpace: "nowrap" }}>
          {["CLICA", "E", "VÊ", "AGORA"].map((p, k) => <span key={k} style={{ marginRight: k < 3 ? 30 : 0, display: "inline-block", transform: `translateY(${-34 * pulaPalavra(k)}px)` }}><Silaba txt={p} em={TF.pal[k]} t={t} cor={AZUL} tam={104} /></span>)}
        </div>
        {/* a seta âmbar que aponta do botão para o vídeo, desenhada e depois cutucando */}
        <svg width={W} height={H} style={{ position: "absolute", inset: 0, transform: `translate(${cutuca * 0.6}px, ${cutuca * 0.5}px)` }}>
          <path d="M 560 420 C 610 330 700 340 752 420" fill="none" stroke={AMBAR} strokeWidth={14} strokeLinecap="round"
            strokeDasharray={260} strokeDashoffset={260 * (1 - seta)} />
          {seta > 0.9 && <path d="M 722 410 L 756 432 L 768 392" fill="none" stroke={AMBAR} strokeWidth={14} strokeLinecap="round" strokeLinejoin="round" />}
        </svg>
        {/* a sombra da moeda/medalha */}
        {t >= TF.cai && <div style={{ position: "absolute", left: M.x - M.r * 0.95, top: M.y + M.r - 14, width: M.r * 1.9, height: 34, borderRadius: "50%",
          background: "radial-gradient(ellipse at center, rgba(11,18,32,0.30) 0%, rgba(11,18,32,0.12) 45%, rgba(11,18,32,0) 70%)",
          transform: `scaleX(${1 - 0.5 * Math.min(1, alto)})`, opacity: 1 - 0.6 * Math.min(1, alto) }} />}
        {/* a moeda que vira a medalha (o YouTube põe o botão de inscrever aqui) */}
        {t >= TF.cai && (
          <div style={{ position: "absolute", left: M.x - M.r, top: my + pulo - M.r, width: M.r * 2, height: M.r * 2,
            transform: `rotate(${balanca}deg) scale(${1 + sq}, ${1 - sq})`, transformOrigin: "50% 100%" }}>
            <MoedaGira r={M.r} giro={giro2 ? ((g) => (g > 180 ? 360 - g : g))((180 + giro2) % 360) : giro} brilho={luz} />
          </div>
        )}
        {/* o botão INSCREVA-SE, colado à medalha */}
        <div style={{ position: "absolute", left: M.x - 210, top: 800, width: 420, height: 104, opacity: t < TF.botao ? 0 : 1,
          transform: `translateY(${(1 - b) * 50}px) scale(${(0.5 + 0.5 * b) * pulsa})`, transformOrigin: "50% 50%" }}>
          <div style={{ position: "absolute", left: 10, top: 10, width: 420, height: 104, borderRadius: 60, background: AMARELO }} />
          <div style={{ position: "absolute", inset: 0, borderRadius: 60, background: AZUL, border: `6px solid ${TINTA}`, boxSizing: "border-box",
            display: "flex", alignItems: "center", justifyContent: "center", fontFamily, fontWeight: 800, fontSize: 54, color: AMARELO, letterSpacing: 2 }}>
            INSCREVA-SE
          </div>
        </div>
        {/* o sino, à direita do botão */}
        {t >= TF.clique[1] && (
          <svg width={110} height={120} viewBox="-55 -60 110 120" style={{ position: "absolute", left: M.x + 230, top: 790,
            transform: `scale(${sino}) rotate(${balancaSino}deg)`, transformOrigin: "50% 10%" }}>
            <path d="M -34 26 C -30 -6 -28 -34 0 -38 C 28 -34 30 -6 34 26 L 42 34 L -42 34 Z" fill={AMARELO} stroke={TINTA} strokeWidth={6} strokeLinejoin="round" />
            <circle cx={0} cy={44} r={9} fill={AMBAR} stroke={TINTA} strokeWidth={5} />
            <circle cx={0} cy={-44} r={6} fill={TINTA} />
          </svg>
        )}
        {/* o cursor que clica */}
        {ck >= 0 && (
          <svg width={110} height={130} viewBox="-6 -6 70 96" style={{ position: "absolute", left: cur.x, top: cur.y,
            transform: `scale(${1 - 0.18 * clicaCursor})`, transformOrigin: "0 0" }}>
            <path d="M 0 0 L 0 70 L 17 55 L 29 82 L 41 77 L 29 50 L 52 50 Z" fill="#FFFFFF" stroke={TINTA} strokeWidth={5} strokeLinejoin="round" />
          </svg>
        )}
      </AbsoluteFill>
      {/* a onda que entra (a mesma da vinheta) */}
      {o > 0 && o < 1 && (
        <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
          <g transform={`translate(${ondaX}, 0)`}>
            <path d={`M 0 0 L 1250 0 C 1550 300 1050 760 1400 ${H} L 150 ${H} C -200 760 300 300 0 0 Z`} fill={AMARELO} />
            <path d={`M 1250 0 L 1330 0 C 1630 300 1130 760 1480 ${H} L 1400 ${H} C 1050 760 1550 300 1250 0 Z`} fill="#FFF0B8" />
            <path d={`M -90 0 L 0 0 C 300 300 -200 760 150 ${H} L 60 ${H} C -290 760 210 300 -90 0 Z`} fill={AMBAR} />
          </g>
        </svg>
      )}
    </AbsoluteFill>
  );
};

// só para ver antes (Ed, 13/11: «inicia com uma foto de uma pickup nada a ver»): por baixo, o azul da vinheta, nunca
// uma cena de outro vídeo. No vídeo de verdade, a onda cobre a última cena DAQUELE vídeo.
export const TelaFinalNovaProva: React.FC = () => (
  <AbsoluteFill style={{ background: AZUL }}>
    <TelaFinalNova />
  </AbsoluteFill>
);
