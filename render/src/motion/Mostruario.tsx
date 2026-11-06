// Vitrine do kit de motion com exemplos reais do video 01 (para o Ed aprovar o estilo antes do video inteiro).
import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { Balao, Barras, Calendario, Carimbo, Cita, Conta, COR, Etiqueta, Frase, Hibrida, LinhaTempo, Numero } from "./kit";

const D = 4.5; // segundos por exemplo
export const ITENS: { dur: number; el: (dur: number) => React.ReactNode }[] = [
  { dur: D, el: () => <Frase sobre="o dinheiro do Tião" texto="Ele não sabia para onde ia. Simplesmente *sumia*." /> },
  { dur: D, el: () => <Calendario mes="Um mês qualquer" ate={20} marcados={{ 5: { cor: COR.verde, rotulo: "salário" }, 20: { cor: COR.vermelho, rotulo: "R$ 0" } }} /> },
  { dur: D, el: () => <Barras titulo="Quanto entra por mês" itens={[{ rotulo: "Tião", valor: 3800 }, { rotulo: "Marcos e Sandra", valor: 12000, cor: COR.vermelho }]} /> },
  { dur: D, el: (d) => <Hibrida img="v01/picape-salao.jpg" dur={d}><Etiqueta x={70} y={30} texto="R$ 220.000" /></Hibrida> },
  { dur: D, el: () => <Numero rotulo="A parcela da picape" valor={5714} embaixo="todo mês, por 5 anos" cor={COR.vermelho} /> },
  { dur: 9, el: () => <Conta titulo="O mês da casa do Marcos" passo={0.95} linhas={[
    { rotulo: "Entram", valor: 12000 }, { rotulo: "Parcela da picape", valor: -5714 }, { rotulo: "Aluguel", valor: -2200 },
    { rotulo: "Mercado", valor: -1500 }, { rotulo: "Luz, água, internet", valor: -600 }, { rotulo: "Gasolina", valor: -600 },
    { rotulo: "Seguro", valor: -700 }, { rotulo: "IPVA (por mês)", valor: -730 }]} /> },
  { dur: 5.5, el: () => <Cita nome="Thorstein Veblen" ano="1899" onde="economista americano" achado="A gente compra pelo que a coisa *mostra*, não pelo que ela faz." fonte="A Teoria da Classe Ociosa (1899)" /> },
  { dur: D, el: () => <LinhaTempo titulo="A vida do Marcos" marcos={["Ano 1", "Ano 2", "Ano 3", "Ano 4", "Ano 5"]} ativo={2} /> },
  { dur: D, el: (d) => <Hibrida img="v01/carro-2001.jpg" dur={d} mov="dir"><Carimbo x={50} y={42} texto="QUITADO" /></Hibrida> },
  { dur: D, el: (d) => <Hibrida img="v01/marcos-porta.jpg" dur={d} mov="sai"><Balao x={66} y={26} lado="esq" texto="Tião, eu preciso de *R$ 2.000* emprestados." /></Hibrida> },
];
export const FIM_MOSTRUARIO = ITENS.reduce((s, i) => s + i.dur, 0);

export const Mostruario: React.FC = () => {
  let ini = 0;
  return (
    <AbsoluteFill style={{ background: COR.tinta }}>
      {ITENS.map((it, i) => {
        const de = Math.round(ini * 30), n = Math.round(it.dur * 30); ini += it.dur;
        return <Sequence key={i} from={de} durationInFrames={n}>{it.el(it.dur)}</Sequence>;
      })}
    </AbsoluteFill>
  );
};
