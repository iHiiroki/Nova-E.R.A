"""
main.py — Ponto de entrada da Nova E.R.A.

Para rodar:
    python3 main.py

Acesse:
    http://localhost:5000
"""

from mecanicas import criar_servidor, PORT
from interface import HTML


def main():
    servidor = criar_servidor(HTML)

    print(f"""
╔══════════════════════════════════════════════════════╗
║          Nova E.R.A. — Loja de Eletrônicos           ║
╠══════════════════════════════════════════════════════╣
║✓ Servidor iniciado com sucesso!                      ║
║✓ Acesse: http://localhost:{PORT:<27}║  
║✓ Pressione Ctrl+C para encerrar                      ║
╚══════════════════════════════════════════════════════╝
""")

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n✓ Servidor encerrado.")


if __name__ == "__main__":
    main()
