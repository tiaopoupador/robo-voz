# Peca do robo: manda um e-mail da conta do canal (Gmail) para o Ed. O texto vem em Markdown simples e vira HTML.
# Uso: python fabrica/correio.py "assunto" arquivo.md [para]
import base64, html, os, re, sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/..")
from fabrica.google import api
PARA = "tiaopoupador@gmail.com"
def md_html(md):
    out, cod = [], None
    for l in md.splitlines():
        if l.startswith("```"):
            if cod is None: cod = []
            else:
                out.append('<pre style="white-space:pre-wrap;background:#f4f1ea;border:1px solid #d9d2c3;border-radius:8px;padding:12px;font-size:13px;line-height:1.45">' + html.escape("\n".join(cod)) + "</pre>"); cod = None
            continue
        if cod is not None: cod.append(l); continue
        t = html.escape(l)
        t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t); t = re.sub(r"`(.+?)`", r"<code>\1</code>", t)
        t = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', t)
        if l.startswith("### "): out.append(f'<h3 style="margin:22px 0 6px;color:#1F1B16">{t[4:]}</h3>')
        elif l.startswith("## "): out.append(f'<h2 style="margin:28px 0 8px;color:#B8860B;border-bottom:2px solid #F2B632">{t[3:]}</h2>')
        elif l.startswith("# "): out.append(f'<h1 style="color:#1F1B16">{t[2:]}</h1>')
        elif l.startswith("- "): out.append(f"<li>{t[2:]}</li>")
        elif l.strip(): out.append(f"<p style='margin:6px 0'>{t}</p>")
    return '<div style="font-family:Arial,sans-serif;font-size:15px;max-width:760px;color:#222">' + "\n".join(out) + "</div>"
def enviar(assunto, md, para=PARA):
    m = MIMEMultipart("alternative"); m["To"] = para; m["From"] = "Robo do Tiao Poupador <tiaopoupador@gmail.com>"; m["Subject"] = assunto
    m.attach(MIMEText(md, "plain", "utf-8")); m.attach(MIMEText(md_html(md), "html", "utf-8"))
    r = api("https://gmail.googleapis.com/gmail/v1/users/me/messages/send", {"raw": base64.urlsafe_b64encode(m.as_bytes()).decode()})
    print("e-mail enviado:", r.get("id")); return r
if __name__ == "__main__":
    enviar(sys.argv[1], open(sys.argv[2], encoding="utf-8").read(), *(sys.argv[3:4]))
