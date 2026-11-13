// A vinheta do canal, 2 s (Ed, 11/11/2026: «crie uma vinheta de 2 s, mas tem que ser muito top»).
// A moeda cai girando dentro da caneca do Tião ("tim"), a caneca dá um pulinho, e o nome entra SÍLABA POR SÍLABA,
// cada uma numa nota do jingle (TI-ÃO POU-PA-DOR, os mesmos tempos do fabrica/vinheta_som.py). No fim, um brilho corre
// pelas letras. Tudo é função do tempo; o som é o arquivo marca/vinheta-a.wav (marimba) ou -b.wav (assobio).
import React from "react";
import { AbsoluteFill, Audio, Img, OffthreadVideo, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { loadFont } from "@remotion/google-fonts/Baloo2";
import { mola } from "../mola";
import { Emoji } from "./vivo";

const { fontFamily } = loadFont("normal", { weights: ["800"] });
export const VINHETA_SEG = 2;
const SIL = [0.62, 0.78, 0.94, 1.08, 1.24];               // TI ÃO POU PA DOR
const TOM = 0.48;                                          // a moeda bate na caneca
const AMARELO = "#FFD43B";

const Silaba: React.FC<{ txt: string; em: number; t: number; cor: string; tam: number; luzEm?: number }> = ({ txt, em, t, cor, tam, luzEm = 1.38 }) => {
  const s = mola(t - em, 22, 0.42);                        // estalo: passa do tamanho e assenta
  const brilho = (t - luzEm) / 0.45, luz = cor === "#FFFFFF" ? AMARELO : "#FFFFFF";  // o brilho corre da esquerda para a direita
  return (
    <span style={{ display: "inline-block", transform: `translateY(${(1 - s) * 70}px) scale(${s}) rotate(${(1 - s) * -14}deg)`, opacity: t < em ? 0 : 1,
      fontFamily, fontWeight: 800, fontSize: tam, lineHeight: 0.92, letterSpacing: 2,
      backgroundImage: `linear-gradient(100deg, ${cor} 0%, ${cor} ${brilho * 140 - 30}%, ${luz} ${brilho * 140 - 12}%, ${cor} ${brilho * 140 + 6}%, ${cor} 100%)`,
      WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent",
      filter: `drop-shadow(0 8px 0 #05080e) drop-shadow(0 0 ${t > em ? 18 * Math.exp(-(t - em) * 4) : 0}px ${cor})` }}>{txt}</span>
  );
};

export const Vinheta: React.FC<{ som?: string }> = ({ som = "marca/vinheta-a.wav" }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  // moeda: cai de cima girando, acelerando, e some dentro da caneca no TOM
  const q = Math.min(1, t / TOM), my = -620 + 720 * q * q, giro = t * 900;
  const pulo = t > TOM ? Math.sin((t - TOM) * 26) * 0.12 * Math.exp(-(t - TOM) * 6) : 0;
  const aro = Math.max(0, Math.min(1, (t - TOM) / 0.45));
  const entra = mola(t, 9, 0.8), sai = mola(t - 1.82, 14, 1);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0B1220", overflow: "hidden" }}>
      <Audio src={staticFile(som)} />
      <AbsoluteFill style={{ background: `radial-gradient(circle at 30% 58%, rgba(255,212,59,${0.10 + 0.22 * aro * Math.exp(-(t - TOM) * 1.2)}) 0%, rgba(11,18,32,0) 46%)` }} />
      {/* raios dourados girando devagar atrás da caneca */}
      <div style={{ position: "absolute", left: "27%", top: "60%", width: 0, height: 0, transform: `rotate(${t * 18}deg) scale(${entra})`, opacity: 0.16 + 0.2 * aro * Math.exp(-(t - TOM) * 1.5) }}>
        {Array.from({ length: 12 }, (_, k) => (
          <div key={k} style={{ position: "absolute", left: -40, top: -900, width: 80, height: 900, transformOrigin: "50% 100%", transform: `rotate(${k * 30}deg)`,
            background: "linear-gradient(0deg, rgba(255,212,59,0.9), rgba(255,212,59,0))", clipPath: "polygon(35% 100%, 65% 100%, 100% 0, 0 0)" }} />
        ))}
      </div>
      {/* a caneca lascada do Tião (desenhada aqui: é a marca dele) e a moeda */}
      <div style={{ position: "absolute", left: "15%", top: "36%", width: 460, height: 440, transform: `scale(${entra * (1 - sai * 0.12)})` }}>
        {t < TOM + 0.02 && (
          <div style={{ position: "absolute", left: 150, top: my - 40, transform: `rotate(${giro * 0.4}deg) scaleX(${0.55 + 0.45 * Math.abs(Math.cos(giro * Math.PI / 180))})` }}>
            <Emoji e="🪙" tam={150} />
          </div>
        )}
        <svg viewBox="0 0 460 440" width={460} height={440} style={{ position: "absolute", inset: 0, overflow: "visible",
          transform: `scale(${1 + pulo}, ${1 - pulo})`, transformOrigin: "50% 100%" }}>
          {[0, 1].map((k) => {  // o vapor do café sobe e ondula
            const v = ((t * 0.9 + k * 0.5) % 1);
            return <path key={k} d={`M ${170 + k * 70} ${120 - v * 90} q 22 -30 0 -60 q -22 -30 0 -60`} fill="none" stroke="white" strokeWidth={12} strokeLinecap="round"
              opacity={0.45 * Math.sin(v * Math.PI)} transform={`translate(${Math.sin(t * 3 + k) * 8}, 0)`} />;
          })}
          <path d="M 330 190 C 420 190 420 330 320 330" fill="none" stroke="#1F1B16" strokeWidth={40} strokeLinecap="round" />
          <path d="M 330 190 C 420 190 420 330 320 330" fill="none" stroke="#F4EFE6" strokeWidth={22} strokeLinecap="round" />
          <path d="M 90 130 L 350 130 L 335 400 Q 333 420 313 420 L 127 420 Q 107 420 105 400 Z" fill="#F4EFE6" stroke="#1F1B16" strokeWidth={12} strokeLinejoin="round" />
          <path d="M 96 130 L 344 130" stroke="#1F1B16" strokeWidth={12} strokeLinecap="round" />
          <path d="M 268 124 L 292 124 L 281 150 Z" fill="#0B1220" stroke="#1F1B16" strokeWidth={6} strokeLinejoin="round" />
          <path d="M 130 280 Q 140 360 150 395" stroke="white" strokeWidth={14} strokeLinecap="round" opacity={0.7} fill="none" />
        </svg>
        <div style={{ position: "absolute", left: 220 - 260, top: 130 - 260, width: 520, height: 520, borderRadius: 999, border: `12px solid ${AMARELO}`,
          opacity: t > TOM ? 0.9 * (1 - aro) : 0, transform: `scale(${0.25 + 0.95 * aro})` }} />
        {t > TOM && Array.from({ length: 8 }, (_, k) => {
          const a = (k / 8) * Math.PI * 2 - Math.PI / 2, d = 70 + 280 * aro;
          return <div key={k} style={{ position: "absolute", left: 220 + Math.cos(a) * d - 18, top: 120 + Math.sin(a) * d * 0.85 - 18, width: 36, height: 36,
            background: AMARELO, clipPath: "polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)", opacity: 1 - aro, transform: `rotate(${t * 220}deg)` }} />;
        })}
      </div>
      {/* o nome, sílaba por sílaba, no ritmo do jingle */}
      <div style={{ position: "absolute", left: "43%", top: "30%", transform: `scale(${1 - sai * 0.08})`, opacity: 1 - sai * 0.0 }}>
        <div><Silaba txt="TI" em={SIL[0]} t={t} cor={AMARELO} tam={250} /><Silaba txt="ÃO" em={SIL[1]} t={t} cor={AMARELO} tam={250} /></div>
        <div style={{ marginTop: 6 }}>
          <Silaba txt="POU" em={SIL[2]} t={t} cor="#FFFFFF" tam={186} /><Silaba txt="PA" em={SIL[3]} t={t} cor="#FFFFFF" tam={186} /><Silaba txt="DOR" em={SIL[4]} t={t} cor="#FFFFFF" tam={186} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- a de 4 s, com o Tião (Ed, 11/11: «algo mais lento e talvez uns 4 s, e que apareça o Tião de alguma forma») ----------
// O Tião sobe na tela já com a caneca na mão e acenando; a moeda cai devagar, girando, DENTRO da caneca dele ("tim");
// o nome entra no jingle mais lento e, no fim, o bordão "Caneca velha, bolso cheio!" aparece num selo.
export const VINHETA4_SEG = 4;
const SIL4 = [1.60, 1.88, 2.16, 2.40, 2.66], TOM4 = 1.40;   // os mesmos do fabrica/vinheta_som.py (vinheta4)
const ALT = 860, ESC = ALT / 1300, X0 = 170, Y0 = 1040 - ALT;  // a foto marca/tiao-acenando.png tem 686 x 1300
const BOCA = { x: X0 + 215 * ESC, y: Y0 + 578 * ESC };          // a boca da caneca na foto (medida: 215, 578)
// clip = o V1 do Flow recortado (fabrica/vinheta_flow.py): quando existe, o Tião animado entra no lugar da foto parada e a moeda é a dele
export const Vinheta4: React.FC<{ som?: string; clip?: string }> = ({ som = "marca/vinheta4-a.wav", clip }) => {
  const f = useCurrentFrame(); const { fps } = useVideoConfig(); const t = f / fps;
  const sobe = mola(t - 0.1, 8, 0.62), bob = Math.sin(t * 2.4) * 6;
  const q = Math.max(0, Math.min(1, (t - 0.6) / (TOM4 - 0.6))), cy = -160 + (BOCA.y - 40 + 160) * q * q, giro = t * 700;
  const aro = Math.max(0, Math.min(1, (t - TOM4) / 0.5)), pulo = t > TOM4 ? Math.sin((t - TOM4) * 22) * 0.025 * Math.exp(-(t - TOM4) * 5) : 0;
  const selo = mola(t - 3.0, 14, 0.55), fim = Math.max(0, (t - 3.8) / 0.2);
  return (
    <AbsoluteFill style={{ backgroundColor: "#0B1220", overflow: "hidden", opacity: 1 - fim }}>
      <Audio src={staticFile(som)} />
      <div style={{ position: "absolute", left: BOCA.x, top: BOCA.y, width: 0, height: 0, transform: `rotate(${t * 14}deg)`, opacity: 0.12 + 0.22 * aro * Math.exp(-(t - TOM4) * 1.2) }}>
        {Array.from({ length: 14 }, (_, k) => (
          <div key={k} style={{ position: "absolute", left: -45, top: -1300, width: 90, height: 1300, transformOrigin: "50% 100%", transform: `rotate(${k * (360 / 14)}deg)`,
            background: "linear-gradient(0deg, rgba(255,212,59,0.9), rgba(255,212,59,0))", clipPath: "polygon(35% 100%, 65% 100%, 100% 0, 0 0)" }} />
        ))}
      </div>
      <AbsoluteFill style={{ background: `radial-gradient(circle at ${BOCA.x}px ${BOCA.y}px, rgba(255,212,59,${0.08 + 0.25 * aro * Math.exp(-(t - TOM4) * 1.4)}) 0%, rgba(11,18,32,0) 40%)` }} />
      {clip ? <OffthreadVideo src={staticFile(clip)} transparent muted style={{ position: "absolute", left: 0, top: 0, height: 1080, transform: `translateX(-180px)` }} /> :
      <Img src={staticFile("marca/tiao-acenando.png")} style={{ position: "absolute", left: X0, top: Y0, height: ALT,
        transform: `translateY(${(1 - sobe) * 700 + bob}px) scale(${1 + pulo}, ${1 - pulo})`, transformOrigin: "50% 100%", filter: "drop-shadow(0 24px 40px rgba(0,0,0,0.55))" }} />}
      {!clip && t > 0.6 && t < TOM4 + 0.02 && (
        <div style={{ position: "absolute", left: BOCA.x - 45, top: cy, transform: `rotate(${giro * 0.3}deg) scaleX(${0.55 + 0.45 * Math.abs(Math.cos(giro * Math.PI / 180))})` }}>
          <Emoji e="🪙" tam={90} />
        </div>
      )}
      <div style={{ position: "absolute", left: BOCA.x - 200, top: BOCA.y - 200 + bob, width: 400, height: 400, borderRadius: 999, border: `10px solid ${AMARELO}`,
        opacity: t > TOM4 ? 0.9 * (1 - aro) : 0, transform: `scale(${0.2 + 0.9 * aro})` }} />
      {t > TOM4 && Array.from({ length: 8 }, (_, k) => {
        const a = (k / 8) * Math.PI * 2 - Math.PI / 2, d = 50 + 230 * aro;
        return <div key={k} style={{ position: "absolute", left: BOCA.x + Math.cos(a) * d - 16, top: BOCA.y + bob + Math.sin(a) * d * 0.85 - 16, width: 32, height: 32,
          background: AMARELO, clipPath: "polygon(50% 0,62% 38%,100% 50%,62% 62%,50% 100%,38% 62%,0 50%,38% 38%)", opacity: 1 - aro, transform: `rotate(${t * 220}deg)` }} />;
      })}
      <div style={{ position: "absolute", left: 820, top: 250 }}>
        <div><Silaba txt="TI" em={SIL4[0]} t={t} cor={AMARELO} tam={270} luzEm={3.25} /><Silaba txt="ÃO" em={SIL4[1]} t={t} cor={AMARELO} tam={270} luzEm={3.25} /></div>
        <div style={{ marginTop: 4 }}>
          <Silaba txt="POU" em={SIL4[2]} t={t} cor="#FFFFFF" tam={200} luzEm={3.25} /><Silaba txt="PA" em={SIL4[3]} t={t} cor="#FFFFFF" tam={200} luzEm={3.25} /><Silaba txt="DOR" em={SIL4[4]} t={t} cor="#FFFFFF" tam={200} luzEm={3.25} />
        </div>
        <div style={{ display: "inline-block", marginTop: 34, padding: "14px 34px", borderRadius: 999, background: AMARELO, color: "#0B1220",
          fontFamily, fontWeight: 800, fontSize: 58, transform: `translateY(${(1 - selo) * 40}px) scale(${selo})`, transformOrigin: "0 50%", opacity: t < 3.0 ? 0 : 1,
          boxShadow: "0 10px 0 #05080e" }}>☕ Caneca velha, bolso cheio!</div>
      </div>
    </AbsoluteFill>
  );
};
