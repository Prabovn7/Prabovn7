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
        "hero_alt": "Pablo Santos, Backend Software Engineer. APIs, Architecture, Security. Animated navy banner.",
        "role": "Backend Software Engineer",
        "status": "Open to junior and internship backend roles",
        "other_lang": ("README.pt-BR.md", "Português (BR)"),
        "roles_alt": "Building APIs, architecture and security (animated line cycling through the three words).",
        "overview_alt": "GitHub overview: public repositories, stars received, followers and languages.",
        "languages_alt": "Most used languages across my public repositories, by bytes of code.",
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
                     "PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code, IntelliJ IDEA.",
        "stack_text": "Stack as text",
        "stack_labels": ("Languages", "Backend and data", "Tools"),
        "activity_alt": "Animated bar chart of my GitHub contributions over the last 30 days, updated daily.",
        "background": "Before moving into backend development I worked in corporate operations at an insurance "
                      "company, handling contracts, documentation and corporate systems. That shaped how I build: "
                      "clear rules, traceable data and well-defined processes.",
        "contact": "Let's talk",
    },
    "pt": {
        "file": "README.pt-BR.md",
        "hero_alt": "Pablo Santos, Backend Software Engineer. APIs, Arquitetura, Segurança. Banner animado em azul marinho.",
        "role": "Backend Software Engineer",
        "status": "Aberto a vagas de estágio e júnior em backend",
        "other_lang": ("README.md", "English"),
        "roles_alt": "Construindo APIs, arquitetura e segurança (linha animada alternando as três palavras).",
        "overview_alt": "Resumo do GitHub: repositórios públicos, estrelas recebidas, seguidores e linguagens.",
        "languages_alt": "Linguagens mais usadas nos meus repositórios públicos, por bytes de código.",
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
                     "PostgreSQL, SQLite, Redis; Docker, Git, GitHub, GitHub Actions, VS Code, IntelliJ IDEA.",
        "stack_text": "Stack em texto",
        "stack_labels": ("Linguagens", "Backend e dados", "Ferramentas"),
        "activity_alt": "Gráfico animado das minhas contribuições no GitHub nos últimos 30 dias, atualizado diariamente.",
        "background": "Antes de migrar para backend, trabalhei com operações corporativas em uma seguradora, lidando "
                      "com contratos, documentação e sistemas corporativos. Isso moldou meu jeito de construir: "
                      "regras claras, dados rastreáveis e processos bem definidos.",
        "contact": "Vamos conversar",
    },
}

STACK_LINES = (
    "Python, Java, C, JavaScript, TypeScript",
    "FastAPI, Flask, Spring, Node.js, PostgreSQL, SQLite, Redis",
    "Docker, Git, GitHub, GitHub Actions, VS Code, IntelliJ IDEA",
)

CARD_TECH = {
    "bus-ticket-api": [("python", "Python"), ("fastapi", "FastAPI"), ("postgresql", "PostgreSQL"), ("redis", "Redis")],
    "delivery-api-fastapi": [("python", "Python"), ("fastapi", "FastAPI"), ("sqlalchemy", "SQLAlchemy"),
                             ("sqlite", "SQLite"), ("jwt", "JWT"), ("pytest", "pytest")],
    "Ferramenta-de-tracking": [("python", "Python")],
    "api-clima": [("python", "Python"), ("terminal", "CLI")],
}


def deco(name: str, width: str = "100%", height: str = "") -> str:
    h = f' height="{height}"' if height else ""
    return f'<img src="assets/{name}" width="{width}"{h} alt="">'


def build(lang: str) -> str:
    s = STR[lang]
    sc = list(s["scenes"])
    other_file, other_name = s["other_lang"]
    right_now = "right-now-pt.svg" if lang == "pt" else "right-now.svg"
    focus_alt = s["focus"] + ": " + "; ".join(t for _, t in s["focus_items"])
    out: list[str] = []
    a = out.append
    divider = f'<div align="center">{deco("scene-divider.svg")}</div>\n'

    a('<div align="center">\n')
    a('<picture>\n<source media="(prefers-reduced-motion: reduce)" srcset="assets/hero-static.png">\n'
      f'<img src="assets/hero.webp" alt="{s["hero_alt"]}" width="100%">\n</picture>\n')
    a(f'<img src="assets/roles.svg" alt="{s["roles_alt"]}" width="380">\n')
    a(f'{ic("target", 16)} {s["status"]}\n')
    a(f'<a href="https://www.linkedin.com/in/pablov-santos-dev"><img src="assets/btn-linkedin.svg" height="44" alt="LinkedIn"></a> '
      f'<a href="{GH}"><img src="assets/btn-github.svg" height="44" alt="GitHub"></a>\n')
    a(f'<a href="{other_file}">{ic("globe", 20, other_name)}</a> {other_name}\n')
    a("</div>\n")

    a(divider)
    a(h2("user", sc[0]) + "\n")
    a(s["about"] + "\n")
    a('<div align="center">\n')
    a(f'<img src="assets/{right_now}" alt="{focus_alt}" width="100%">\n')
    a("</div>\n")

    a(divider)
    a(h2("folder", sc[1]) + "\n")
    a("<table>")
    for row in (0, 2):
        a("<tr>")
        for k, (icon, title, repo, wip, desc) in enumerate(s["cards"][row:row + 2]):
            badge = f" <sub>· {s['progress']}</sub>" if wip else ""
            a(f'<td width="50%" valign="top">\n'
              f'<a href="{GH}/{repo}">{ic(icon, 24, title)}</a> <b>{title}</b>{badge}<br>\n'
              f'{deco(f"bar-{row + k + 1}.svg", "100%", "6")}<br>\n'
              f'{desc}<br><br>\n{tech(*CARD_TECH[repo])} &nbsp; <a href="{GH}/{repo}">{ic("github", 20, "GitHub: " + title)}</a>\n</td>')
        a("</tr>")
    a("</table>\n")
    a(f"**{s['more']}**\n")
    for icon, title, repo, desc in s["more_items"]:
        a(f'- <a href="{GH}/{repo}">{ic(icon, 20, title)}</a> **{title}**: {desc}')
    a("")

    a(divider)
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

    a(divider)
    a(h2("activity", sc[3]) + "\n")
    a('<div align="center">\n')
    a(f'<img src="assets/stats/overview.svg" alt="{s["overview_alt"]}" width="100%">\n')
    a(f'<img src="assets/stats/languages.svg" alt="{s["languages_alt"]}" width="100%">\n')
    a(f'<img src="assets/activity.svg" alt="{s["activity_alt"]}" width="100%">\n')
    a("</div>\n")

    a(divider)
    a(h2("briefcase", sc[4]) + "\n")
    a(s["background"] + "\n")

    a(divider)
    a(h2("mail", sc[5]) + "\n")
    a('<div align="center">\n')
    a(f'<a href="https://www.linkedin.com/in/pablov-santos-dev">{ic("linkedin", 40, "LinkedIn")}</a> &nbsp; '
      f'<a href="{GH}">{ic("github", 40, "GitHub")}</a>\n')
    a("</div>\n")
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    for lang in ("en", "pt"):
        (ROOT / STR[lang]["file"]).write_text(build(lang), encoding="utf-8")
    print("ok")
