// Piloto do video 01 (abertura, 49 s). Tempos em segundos, medidos com o Whisper na narracao v4.
// tipo "video" = cena animada no Grok; "imagem" = imagem parada com camera em codigo.
// mov: para onde a camera anda (entra = aproxima, sai = afasta, esq/dir = desliza).
// de: em que segundo do clipe a cena comeca (para voltar a um clipe ja usado).
export type Cena = { ini: number; arq: string; tipo: "video" | "imagem"; mov: "entra" | "sai" | "esq" | "dir"; de?: number };
export const CENAS: Cena[] = [
  { ini: 0.0, arq: "cenas/01-rua-manha.png", tipo: "imagem", mov: "entra" },
  { ini: 2.74, arq: "animadas/02-tiao-lavando.mp4", tipo: "video", mov: "entra" },
  { ini: 5.04, arq: "cenas/02b-caneca.png", tipo: "imagem", mov: "entra" },
  { ini: 7.36, arq: "animadas/02-tiao-lavando.mp4", tipo: "video", mov: "sai", de: 2.4 },
  { ini: 10.12, arq: "cenas/03-parachoque.png", tipo: "imagem", mov: "dir" },
  { ini: 13.56, arq: "cenas/04-banco-rasgado.png", tipo: "imagem", mov: "entra" },
  { ini: 17.86, arq: "animadas/05-marcos-sai.mp4", tipo: "video", mov: "sai" },
  { ini: 23.78, arq: "cenas/06-picape.png", tipo: "imagem", mov: "esq" },
  { ini: 29.56, arq: "animadas/07-marcos-botao.mp4", tipo: "video", mov: "entra" },
  { ini: 34.78, arq: "animadas/08-marcos-ri.mp4", tipo: "video", mov: "entra" },
  { ini: 37.7, arq: "animadas/09-sandra-janela.mp4", tipo: "video", mov: "sai" },
  { ini: 40.88, arq: "animadas/10-tiao-caneca.mp4", tipo: "video", mov: "entra" },
  { ini: 44.78, arq: "animadas/11-tiao-rosto.mp4", tipo: "video", mov: "entra" },
];
export const FIM = 49.4;

// Legenda: 2 a 4 palavras. *palavra* = amarela.
export const LEGENDAS: [number, string][] = [
  [0.0, "*Sábado*,"], [1.0, "*7h40* da manhã."],
  [2.74, "O Tião está"], [3.36, "na *calçada*,"], [4.08, "de *chinelo*,"], [5.04, "com a *caneca*"], [5.88, "de café lascada"],
  [6.72, "na mão,"], [7.36, "lavando um carro"], [8.12, "branco de *2001*."],
  [10.12, "O para-choque"], [10.96, "tem um *arranhão*"], [11.64, "que ninguém consertou."],
  [13.56, "O banco do motorista"], [15.18, "tem um *rasgo*"], [15.94, "coberto com uma capa."],
  [17.86, "Do outro lado"], [18.5, "da rua,"], [19.46, "o *Marcos*"], [19.86, "sai de casa"], [20.56, "com a *chave* na mão."],
  [23.78, "Na garagem dele,"], [25.58, "uma *picape* preta,"], [27.04, "*zero* quilômetro,"], [27.72, "*brilhando*."],
  [29.56, "Ele aperta o botão,"], [31.38, "o farol *pisca*"], [32.08, "e ele olha"], [33.02, "para o carro do Tião"], [34.06, "e *ri*."],
  [34.78, "\"Ô Tião,"], [35.7, "esse aí ainda"], [36.36, "pega no *tranco*?\""],
  [37.7, "A *Sandra*,"], [38.46, "mulher do Marcos,"], [39.48, "*ri* junto, da janela."],
  [40.88, "O Tião *sorri*,"], [41.9, "levanta a caneca"], [42.74, "e *não responde*."],
  [44.78, "*Ninguém* naquela rua"], [46.18, "sabia o que"], [47.12, "o Tião *sabia*."],
];
