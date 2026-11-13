// A vinheta NOVA do canal, 4,5 s (Ed, 13/11/2026: «nao gostei daquele estilo (...) veja o inicio desse video», modelo RoboNuggets
// youtu.be/csOEsfiBfvo aos 33 s). Entra logo depois do "Vamos começar?" (canal-dark longo.md secoes 20 e 21).
// O gesto é nosso: um raio amarelo desce, abre um leque com as cores do canal, o leque fecha numa linha fina que segura
// a MOEDA do Tião; a linha solta, a moeda cai, quica três vezes, cresce, VIRA e do outro lado está o rosto do Tião
// (uma medalha). A medalha vai para a esquerda e o nome entra sílaba por sílaba no jingle TI-ÃO POU-PA-DOR.
// Uma onda amarela varre a tela e devolve ao vídeo. Tudo é função do tempo (seek puro); só transform/opacity.
// O som é marca/vinheta-nova.wav (fabrica/vinheta_nova_som.py, com os MESMOS tempos de T abaixo).
import React from "react";
import { AbsoluteFill, Audio, Img, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola } from "../mola";

export const { fontFamily } = loadFont("normal", { weights: ["800"] });
export const VINHETA_NOVA_SEG = 4.5;
export const AMARELO = "#FFD43B", AMBAR = "#F59F00", AZUL = "#0B1220", CREME = "#F6F1E7";
// os tempos (iguais no som): raio, leque abre, leque fecha, solta, 3 quiques, vira, sílabas, onda
export const T = { raio: 0, abre: 0.32, fecha: 0.82, solta: 1.28, quica: [1.62, 1.9, 2.06], vira: 2.28, sil: [2.62, 2.78, 2.96, 3.1, 3.24], onda: 3.78 };
const W = 1920, H = 1080, CX = W / 2;
const cl = (x: number) => Math.max(0, Math.min(1, x));
const suave = (x: number) => { const c = cl(x); return c * c * (3 - 2 * c); };

// a moeda do Tião: ouro, aro, e uma caneca gravada no meio (a marca dele)
export const Moeda: React.FC<{ r: number }> = ({ r }) => (
  <svg width={r * 2} height={r * 2} viewBox="-100 -100 200 200" style={{ display: "block" }}>
    <defs>
      <radialGradient id="ouro" cx="35%" cy="30%" r="80%"><stop offset="0" stopColor="#FFF3B0" /><stop offset="0.45" stopColor={AMARELO} /><stop offset="1" stopColor="#D98A00" /></radialGradient>
    </defs>
    <circle r="96" fill="url(#ouro)" stroke="#1F1B16" strokeWidth="7" />
    <circle r="74" fill="none" stroke="#B87400" strokeWidth="5" strokeDasharray="3 7" />
    <g transform="translate(-6,4)" stroke="#8A5600" strokeWidth="9" strokeLinejoin="round" strokeLinecap="round" fill="none">
      <path d="M -34 -30 L 30 -30 L 26 34 Q 25 40 19 40 L -23 40 Q -29 40 -30 34 Z" />
      <path d="M 30 -16 C 52 -16 52 20 28 20" />
      <path d="M -14 -46 q 6 -8 0 -16 M 6 -46 q 6 -8 0 -16" strokeWidth="6" />
    </g>
    <ellipse cx="-38" cy="-46" rx="22" ry="10" fill="white" opacity="0.45" transform="rotate(-30 -38 -46)" />
  </svg>
);

// a medalha: marca/tiao-medalha.png (1000 x 1000), a cabeça INTEIRA do Tião com folga, aumentada 4x no Real-ESRGAN
// (Ed, 13/11: «o rosto do Tiao (...) ficou um pouco deformado»: o recorte antigo cortava o cabelo e esticava a foto pequena).
// brilho = 0..1: uma faixa de luz atravessa a medalha na diagonal (reflexo de metal, nunca brilho em volta).
export const Medalha: React.FC<{ r: number; brilho?: number }> = ({ r, brilho = 0 }) => {
  const aro = Math.max(5, r * 0.045);
  return (
    <div style={{ width: r * 2, height: r * 2, borderRadius: 999, overflow: "hidden", position: "relative", background: AMARELO }}>
      <Img src={staticFile("marca/tiao-medalha.png")} style={{ position: "absolute", left: aro, top: aro, width: r * 2 - aro * 2, height: r * 2 - aro * 2 }} />
      {brilho > 0 && brilho < 1 && (
        <div style={{ position: "absolute", top: -r, left: -r * 1.2 + brilho * r * 4.4, width: r * 0.32, height: r * 4, transform: "rotate(24deg)",
          background: "linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.55), rgba(255,255,255,0))" }} />
      )}
      <div style={{ position: "absolute", inset: 0, borderRadius: 999, border: `${aro}px solid #1F1B16` }} />
    </div>
  );
};

// a moeda girando em Y (giro 0..180): até 90 mostra a moeda, depois a medalha; de lado aparece a borda dourada serrilhada
// (ideia copiada do Flow a 13/11: 14 camadas da mesma moeda deslocadas para o lado que se afasta)
export const MoedaGira: React.FC<{ r: number; giro: number; brilho?: number }> = ({ r, giro, brilho = 0 }) => {
  const escX = Math.max(Math.abs(Math.cos((giro * Math.PI) / 180)), 0.02);
  const lateral = Math.abs(Math.sin((giro * Math.PI) / 180)), grossura = r * 0.16, lado = giro < 90 ? -1 : 1;
  return (
    <div style={{ position: "absolute", inset: 0 }}>
      {lateral > 0.04 && Array.from({ length: 14 }, (_, k) => 14 - k).map((k) => (
        <div key={k} style={{ position: "absolute", inset: 0, borderRadius: "50%", background: k % 2 ? "#C98500" : "#E9A814",
          boxShadow: k === 14 ? "inset 0 0 0 4px #1F1B16" : undefined, transform: `translateX(${lado * grossura * lateral * (k / 14)}px) scaleX(${escX})` }} />
      ))}
      <div style={{ position: "absolute", inset: 0, transform: `scaleX(${escX})` }}>
        {giro < 90 ? <Moeda r={r} /> : <Medalha r={r} brilho={brilho} />}
      </div>
    </div>
  );
};

export const Silaba: React.FC<{ txt: string; em: number; t: number; cor: string; tam: number }> = ({ txt, em, t, cor, tam }) => {
  const s = mola(t - em, 24, 0.45);
  return (
    <span style={{ display: "inline-block", fontFamily, fontWeight: 800, fontSize: tam, lineHeight: 0.9, color: cor, letterSpacing: 1,
      opacity: t < em ? 0 : 1, transform: `translateY(${(1 - s) * 60}px) scale(${0.4 + 0.6 * s})`, transformOrigin: "50% 100%",
      textShadow: `0 7px 0 ${cor === AZUL ? AMARELO : AZUL}` }}>{txt}</span>
  );
};

export const VinhetaNova: React.FC<{ som?: string; semFundo?: boolean }> = ({ som = "marca/vinheta-nova.wav", semFundo }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;

  // 1 · o raio desce do alto até o meio da tela
  const raio = suave((t - T.raio) / (T.abre - T.raio));
  const linhaY = 520;                                  // onde a linha segura a moeda
  // 2 · o leque abre (3 cunhas presas no alto, no meio) e cobre a tela; 3 · fecha numa linha fina
  // (Ed, 13/11: «copie da do flow o que achar necessario»: no Flow o leque lê-se como LEQUE: fatias com o arco redondo
  //  e uma fresta entre elas, abrindo uma depois da outra. O nosso cobria a tela e virava só manchas de cor.)
  const fecha = suave((t - T.fecha) / (T.solta - T.fecha));
  const abreDe = (atraso: number) => mola(t - T.abre - atraso, 9, 0.72);
  const fatia = (cor: string, centro: number, meia: number, raioF: number) => {   // graus a partir do "para baixo"
    const pt = (g: number) => { const a = (g * Math.PI) / 180; return `${CX + raioF * Math.sin(a)} ${raioF * Math.cos(a)}`; };
    const a0 = centro - meia, a1 = centro + meia;
    return <path d={`M ${CX} 0 L ${pt(a0)} A ${raioF} ${raioF} 0 0 0 ${pt(a1)} Z`} fill={cor} />;
  };
  const leque = (atraso: number) => abreDe(atraso) * (1 - fecha);                // 0 = fechado, 1 = aberto
  const raioLeque = (k: number) => (560 + 520 * abreDe(k)) * (1 - fecha) + linhaY * fecha;  // fechado = do alto até a moeda
  // a cortina azul sobe enquanto o leque fecha e mostra o creme por baixo (no Flow o azul recua para cima)
  const cortina = suave((t - T.fecha - 0.1) / 0.36);
  // 4 · a linha sobe e solta a moeda; ela cai e quica 3 vezes até assentar no chão (y = 640)
  const CHAO = 640, R = 100;
  let my = linhaY + R, sq = 0;                          // centro da moeda, e o achatamento no quique
  if (t >= T.solta) {
    const [q1, q2, q3] = T.quica;
    if (t < q1) { const p = (t - T.solta) / (q1 - T.solta); my = linhaY + R + (CHAO - linhaY - R) * p * p; }
    else if (t < q2) { const p = (t - q1) / (q2 - q1); my = CHAO - 150 * 4 * p * (1 - p); }
    else if (t < q3) { const p = (t - q2) / (q3 - q2); my = CHAO - 50 * 4 * p * (1 - p); }
    else my = CHAO;
    for (const q of T.quica) if (t >= q) sq = Math.max(sq, 0.22 * Math.exp(-(t - q) * 22) * (q === q1 ? 1 : q === q2 ? 0.6 : 0.35));
  }
  const sobeLinha = suave((t - T.solta) / 0.3);
  // 5 · cresce e vira: a moeda gira em Y; passou de 90 graus, mostra a medalha do Tião
  const cresce = mola(t - (T.vira - 0.12), 11, 0.62);
  const giro = suave((t - T.vira) / 0.28) * 180;       // 0 a 180 graus
  const r = R * (1 + 1.2 * cresce);                     // raio final ~ 220 px
  const pulo = -80 * Math.sin(Math.PI * cl((t - T.vira + 0.04) / 0.36));
  // 6 · a medalha anda para a esquerda e o nome entra à direita
  const anda = mola(t - (T.vira + 0.1), 10, 0.8);  // começa ainda girando: quando o TI entra, a medalha já saiu do caminho
  const mx = CX + (-430) * anda, myF = my + (H / 2 - 20 - CHAO) * cresce + pulo;
  // brilho que corre pelo aro quando o nome fecha
  const luz = cl((t - (T.sil[4] + 0.15)) / 0.5);
  // a medalha chega à esquerda e balança um fio, como quem cumprimenta (mola que passa e assenta)
  const balanca = t > T.sil[0] ? -7 * Math.sin((t - T.sil[0]) * 11) * Math.exp(-(t - T.sil[0]) * 3.2) : 0;
  // 7 · a onda amarela: uma faixa de borda curva atravessa a tela; atrás dela, o vídeo volta
  const o = (t - T.onda) / (VINHETA_NOVA_SEG - T.onda);
  const ondaX = -2700 + (W + 2900) * suave(o);
  const atrasDaOnda = ondaX + 1250 > 0 && o > 0;        // a borda de trás da onda já passou: dali para a esquerda é vídeo
  const corte = Math.max(0, ondaX + 300);               // até onde a vinheta já foi coberta e trocada

  return (
    <AbsoluteFill style={{ backgroundColor: semFundo ? "transparent" : AZUL, overflow: "hidden" }}>
      {som && <Audio src={staticFile(som)} />}
      {/* a vinheta inteira, recortada pela onda (o que a onda já cobriu volta a ser vídeo) */}
      <AbsoluteFill style={{ clipPath: o > 0 && atrasDaOnda ? `inset(0 0 0 ${Math.min(W, corte)}px)` : undefined }}>
        <AbsoluteFill style={{ background: t < T.abre ? "transparent" : CREME }} />
        {/* a borda de baixo da cortina é curva, a mesma família da onda do fim (nunca um corte reto) */}
        {t >= T.abre && cortina < 1 && (
          <svg width={W} height={H + 260} style={{ position: "absolute", left: 0, top: 0, transform: `translateY(${-cortina * (H + 260)}px)` }}>
            <path d={`M 0 0 L ${W} 0 L ${W} ${H} C ${W * 0.7} ${H + 260} ${W * 0.3} ${H + 260} 0 ${H} Z`} fill={AZUL} />
          </svg>
        )}
        {/* o raio: três fios afinados que descem (amarelo, âmbar, azul) */}
        {t < T.abre + 0.3 && [[-26, AMBAR, 26], [0, AMARELO, 34], [26, AZUL, 20]].map(([dx, cor, lg], k) => (
          <div key={k} style={{ position: "absolute", left: CX + (dx as number) - (lg as number) / 2, top: 0, width: lg as number, height: (linhaY + 40) * raio,
            background: cor as string, clipPath: "polygon(0 0, 100% 0, 55% 100%, 45% 100%)" }} />
        ))}
        {/* o leque */}
        {t >= T.abre && t < T.solta + 0.05 && <>
          <svg width={W} height={H} style={{ position: "absolute", inset: 0 }}>
            {fatia(AMBAR, -50 * leque(0.06), Math.max(0.3, 24 * leque(0.06)), raioLeque(0.06))}
            {fatia(CREME, 50 * leque(0.11), Math.max(0.3, 24 * leque(0.11)), raioLeque(0.11))}
            {fatia(AMARELO, 0, Math.max(0.4, 24 * leque(0)), raioLeque(0))}
          </svg>
        </>}
        {/* a linha que segura a moeda */}
        {t >= T.fecha + 0.2 && t < T.solta + 0.3 && (
          <>
            <div style={{ position: "absolute", left: CX - 4, top: 0, width: 8, height: Math.max(0, linhaY * (1 - sobeLinha) - 14), background: AMBAR, borderRadius: 4 }} />
            <div style={{ position: "absolute", left: CX - 11, top: linhaY * (1 - sobeLinha) - 20, width: 22, height: 26, borderRadius: "50%",
              border: "5px solid #1F1B16", boxSizing: "border-box" }} />
          </>
        )}
        {/* a sombra no chão: fica no chão quando a moeda pula (encolhe e clareia), e sob a medalha depois */}
        {t >= T.fecha + 0.2 && (() => {
          const chao = (CHAO + R) * (1 - cresce) + (myF + r) * cresce, alto = Math.max(0, chao - (myF + r * (1 - sq)) ) / 200;
          const ls = r * 1.9, as = Math.max(16, r * 0.2);
          return <div style={{ position: "absolute", left: mx - ls / 2, top: chao - as * 0.55, width: ls, height: as, borderRadius: "50%",
            background: "radial-gradient(ellipse at center, rgba(11,18,32,0.30) 0%, rgba(11,18,32,0.12) 45%, rgba(11,18,32,0) 70%)",
            transform: `scaleX(${1 - 0.45 * Math.min(1, alto)})`, opacity: 1 - 0.5 * Math.min(1, alto) }} />;
        })()}
        {/* a moeda / a medalha */}
        {t >= T.fecha + 0.2 && (
          <div style={{ position: "absolute", left: mx - r, top: myF - r, width: r * 2, height: r * 2,
            transform: `rotate(${balanca}deg) scale(${1 + sq}, ${1 - sq})`, transformOrigin: "50% 100%" }}>
            <MoedaGira r={r} giro={giro} brilho={luz} />
          </div>
        )}
        {/* o nome */}
        <div style={{ position: "absolute", left: CX - 160, top: H / 2 - 235 }}>
          <div><Silaba txt="TI" em={T.sil[0]} t={t} cor={AZUL} tam={230} /><Silaba txt="ÃO" em={T.sil[1]} t={t} cor={AZUL} tam={230} /></div>
          <div style={{ marginTop: -6 }}>
            <Silaba txt="POU" em={T.sil[2]} t={t} cor={AMBAR} tam={168} /><Silaba txt="PA" em={T.sil[3]} t={t} cor={AMBAR} tam={168} /><Silaba txt="DOR" em={T.sil[4]} t={t} cor={AMBAR} tam={168} />
          </div>
        </div>
      </AbsoluteFill>
      {/* a onda: faixa amarela com uma faixa creme na frente, bordas curvas */}
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
