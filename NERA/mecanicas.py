"""
mecanicas.py — Lógica do servidor e configurações da Nova E.R.A.

Responsável por:
  - Porta do servidor
  - Favicon SVG
  - Handler HTTP (rotas e respostas)
  - Função para criar o servidor
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler

# ─── Porta do servidor ────────────────────────────────────────────────────────
PORT = int(os.environ.get("PORT", 5000))

# ─── Ícone da aba do navegador (SVG com raio roxo) ───────────────────────────
FAVICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
      <stop offset="0%" stop-color="#7c3aed"/>
      <stop offset="100%" stop-color="#8b5cf6"/>
    </linearGradient>
  </defs>
  <rect width="64" height="64" rx="14" fill="url(#g)"/>
  <path d="M37 9L17 37h16l-6 18L51 27H35L37 9z" fill="white"/>
</svg>"""


# ─── Handler HTTP — processa cada requisição do navegador ─────────────────────

def criar_handler(html: str, favicon: str):
    """
    Cria a classe Handler com o HTML e favicon injetados.
    Usamos uma função de fábrica para poder passar o HTML como dependência
    sem poluir o escopo global.
    """

    class Handler(BaseHTTPRequestHandler):

        def do_GET(self):
            """Responde todas as rotas com o HTML da SPA, exceto /favicon.svg."""

            if self.path == "/favicon.svg":
                dados = favicon.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "image/svg+xml")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

            else:
                # Qualquer outra rota entrega o app React (SPA com hash routing)
                dados = html.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Cache-Control", "no-cache")
                self.send_header("Content-Length", str(len(dados)))
                self.end_headers()
                self.wfile.write(dados)

        def log_message(self, format, *args):
            # Silencia os logs de acesso no terminal
            pass

    return Handler


def criar_servidor(html: str):
    """Cria e retorna o servidor HTTP já configurado."""
    handler = criar_handler(html, FAVICON_SVG)
    return HTTPServer(("0.0.0.0", PORT), handler)
