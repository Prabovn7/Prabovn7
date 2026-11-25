"""Builds README.md (en) and README.pt-BR.md from one structure."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GH = "https://github.com/Prabovn7"


def ic(name: str, size: int = 18, alt: str = "") -> str:
    return f'<img src="assets/icons/{name}.svg" width="{size}" height="{size}" alt="{alt}">'


def tech(*pairs: tuple[str, str]) -> str:
    return " ".join(ic(k, 20, label) for k, label in pairs)


def h2(icon: str, text: str) -> str:
    return f"<h2>{ic(icon, 24)} {text}</h2>"


STR = {
    "en": {
        "file": "README.md",
        "hero_alt": "Pablo Santos, Backend Software Engineer. APIs, Architecture, Security. Animated monochrome banner.",
        "role": "Backend Software Engineer",
        "status": "Open to junior and internship backend roles",
        "other_lang": ("README.pt-BR.md", "Português (BR)"),
        "scenes": ["About", "Featured projects", "Stack", "Activity", "Background", "Contact"],
        "word": "Scene",
        "about": "Software Engineering student focused on backend development. I build APIs with authentication, "
                 "data persistence and automated tests, using Python, FastAPI, PostgreSQL and Docker.",
        "focus": "Right now",
        "focus_items": [
            ("database", "Concurrency-safe booking with PostgreSQL and Redis"),
            ("docker", "Containerizing my projects"),
            ("shield", "Security and software architecture"),
            ("book", "Technical English"),
        ],
        "progress": "in progress",
        "cards": [
            ("bus", "Bus Ticket API", "bus-ticket-api", True,
             "Bus ticket sales with segment-based seat reservation, designed to prevent double-booking under "
             "concurrent requests."),
            ("truck", "Delivery API", "delivery-api-fastapi", False,
             "FastAPI service with JWT access and refresh tokens, order management, SQLAlchemy and automated tests."),
            ("chart", "Case Tracking Tool", "Ferramenta-de-tracking", False,
             "Python tool that distributes cases across a team, tracks them in Excel and generates reports and a "
             "manager dashboard."),
            ("weather", "Weather CLI", "api-clima", False,
             "Command-line app that fetches real-time weather data from WeatherAPI."),
        ],
        "more": "More projects",
        "more_items": [
            ("terminal", "rpg-python", "rpg-python", "Object-oriented exercise: abstraction, inheritance and polymorphism in a small RPG."),
        ],
        "stack_alt": "Animated tech stack: Python, Java, C, JavaScript, TypeScript; FastAPI, Flask, Spring, Node.js, "
                     "PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code.",
        "stack_text": "Stack as text",
        "stack_labels": ("Languages", "Backend and data", "Tools"),
        "activity_alt": "Animated grid of my recent GitHub contribution activity, updated daily.",
        "background": "Before moving into backend development I worked in corporate operations at an insurance "
                      "company, handling contracts, documentation and corporate systems. That shaped how I build: "
                      "clear rules, traceable data and well-defined processes.",
        "contact": "Let's talk",
    },
    "pt": {
        "file": "README.pt-BR.md",
        "hero_alt": "Pablo Santos, Backend Software Engineer. APIs, Arquitetura, Segurança. Banner animado monocromático.",
        "role": "Backend Software Engineer",
        "status": "Aberto a vagas de estágio e júnior em backend",
        "other_lang": ("README.md", "English"),
        "scenes": ["Sobre", "Projetos em destaque", "Stack", "Atividade", "Contexto", "Contato"],
        "word": "Cena",
        "about": "Estudante de Engenharia de Software com foco em desenvolvimento backend. Construo APIs com "
                 "autenticação, persistência de dados e testes automatizados, usando Python, FastAPI, PostgreSQL e Docker.",
        "focus": "Agora",
        "focus_items": [
            ("database", "Reserva segura contra concorrência com PostgreSQL e Redis"),
            ("docker", "Containerização dos meus projetos"),
            ("shield", "Segurança e arquitetura de software"),
            ("book", "Inglês técnico"),
        ],
        "progress": "em andamento",
        "cards": [
            ("bus", "Bus Ticket API", "bus-ticket-api", True,
             "Venda de passagens de ônibus com reserva de assento por trecho, feita para evitar reserva duplicada "
             "em requisições concorrentes."),
            ("truck", "Delivery API", "delivery-api-fastapi", False,
             "API FastAPI com tokens JWT de acesso e refresh, gerenciamento de pedidos, SQLAlchemy e testes automatizados."),
            ("chart", "Ferramenta de Tracking", "Ferramenta-de-tracking", False,
             "Ferramenta em Python que distribui cases entre a equipe, acompanha em Excel e gera relatórios e "
             "dashboard gerencial."),
            ("weather", "Weather CLI", "api-clima", False,
             "Aplicação de linha de comando que consulta o clima em tempo real pela WeatherAPI."),
        ],
        "more": "Mais projetos",
        "more_items": [
            ("terminal", "rpg-python", "rpg-python", "Exercício de orientação a objetos: abstração, herança e polimorfismo em um RPG simples."),
        ],
        "stack_alt": "Stack animada: Python, Java, C, JavaScript, TypeScript; FastAPI, Flask, Spring, Node.js, "
                     "PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code.",
        "stack_text": "Stack em texto",
        "stack_labels": ("Linguagens", "Backend e dados", "Ferramentas"),
        "activity_alt": "Grade animada da minha atividade recente de contribuições no GitHub, atualizada diariamente.",
        "background": "Antes de migrar para backend, trabalhei com operações corporativas em uma seguradora, lidando "
                      "com contratos, documentação e sistemas corporativos. Isso moldou meu jeito de construir: "
                      "regras claras, dados rastreáveis e processos bem definidos.",
        "contact": "Vamos conversar",
    },
}

STACK_LINES = (
    "Python, Java, C, JavaScript, TypeScript",
    "FastAPI, Flask, Spring, Node.js, PostgreSQL, SQLite, Redis",
    "Docker, Git, GitHub, GitHub Actions, VS Code",
)

CARD_TECH = {
    "bus-ticket-api": [("python", "Python"), ("fastapi", "FastAPI"), ("postgresql", "PostgreSQL"), ("redis", "Redis")],
    "delivery-api-fastapi": [("python", "Python"), ("fastapi", "FastAPI"), ("sqlalchemy", "SQLAlchemy"),
                             ("sqlite", "SQLite"), ("jwt", "JWT"), ("pytest", "pytest")],
    "Ferramenta-de-tracking": [("python", "Python")],
    "api-clima": [("python", "Python"), ("terminal", "CLI")],
}


def build(lang: str) -> str:
    s = STR[lang]
    sc = [f"{s['word']} 0{i + 1} — {t}" for i, t in enumerate(s["scenes"])]
    other_file, other_name = s["other_lang"]
    out: list[str] = []
    a = out.append

    a('<div align="center">\n')
    a('<picture>\n<source media="(prefers-reduced-motion: reduce)" srcset="assets/hero-static.png">\n'
      f'<img src="assets/hero.webp" alt="{s["hero_alt"]}" width="100%">\n</picture>\n')
    a("# Pablo Santos\n")
    a(f"**{s['role']}** · APIs · Architecture · Security\n")
    a(f'{ic("target", 16)} {s["status"]}\n')
    a(f'<a href="https://www.linkedin.com/in/pablov-santos-dev">{ic("linkedin", 16)} LinkedIn</a> &nbsp;·&nbsp; '
      f'<a href="{GH}">{ic("github", 16)} GitHub</a> &nbsp;·&nbsp; '
      f'<a href="{other_file}">{ic("globe", 16)} {other_name}</a>\n')
    a("</div>\n")

    a(h2("user", sc[0]) + "\n")
    a(s["about"] + "\n")
    a(f"**{s['focus']}**\n")
    for icon, text in s["focus_items"]:
        a(f"- {ic(icon, 16)} {text}")
    a("")

    a(h2("folder", sc[1]) + "\n")
    a('<table>')
    for row in (0, 2):
        a("<tr>")
        for icon, title, repo, wip, desc in s["cards"][row:row + 2]:
            badge = f" <sub>· {s['progress']}</sub>" if wip else ""
            a(f'<td width="50%" valign="top">\n'
              f'{ic(icon, 20)} <b><a href="{GH}/{repo}">{title}</a></b>{badge}<br>\n'
              f'{desc}<br><br>\n{tech(*CARD_TECH[repo])}\n</td>')
        a("</tr>")
    a("</table>\n")
    a(f"**{s['more']}**\n")
    for icon, title, repo, desc in s["more_items"]:
        name = f'<a href="{GH}/{repo}">{title}</a>' if repo else title
        a(f"- {ic(icon, 16)} **{name}**: {desc}")
    a("")

    a(h2("layers", sc[2]) + "\n")
    a('<div align="center">\n')
    a(f'<img src="assets/stack.svg" alt="{s["stack_alt"]}" width="100%">\n')
    a("</div>\n")
    lang_l, back_l, tools_l = s["stack_labels"]
    a(f"<details><summary>{s['stack_text']}</summary>\n")
    a(f"- **{lang_l}:** {STACK_LINES[0]}")
    a(f"- **{back_l}:** {STACK_LINES[1]}")
    a(f"- **{tools_l}:** {STACK_LINES[2]}\n")
    a("</details>\n")

    a(h2("activity", sc[3]) + "\n")
    a('<div align="center">\n')
    a(f'<img src="assets/activity.svg" alt="{s["activity_alt"]}" width="100%">\n')
    a("</div>\n")

    a(h2("briefcase", sc[4]) + "\n")
    a(s["background"] + "\n")

    a(h2("mail", sc[5]) + "\n")
    a(f'{ic("linkedin", 18)} <a href="https://www.linkedin.com/in/pablov-santos-dev">linkedin.com/in/pablov-santos-dev</a>  \n'
      f'{ic("github", 18)} <a href="{GH}">github.com/Prabovn7</a>\n')
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for lang in ("en", "pt"):
        (ROOT / STR[lang]["file"]).write_text(build(lang), encoding="utf-8")
    print("ok")
