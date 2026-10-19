<div align="center">
  <h1>
    <img src="https://raw.githubusercontent.com/Prabovn7/Prabovn7/main/assets/banner.svg" alt="Pablo Vinicius, Software Engineering Student focused on backend" width="100%">
  </h1>
</div>

<p align="center">
  <a href="README.pt-BR.md">Português (BR)</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#projects">Projects</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#stack">Stack</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#contact">Contact</a>
</p>

Software Engineering student building backend projects with authentication, data persistence and tests. Currently focused on PostgreSQL, Docker and concurrency-safe designs.

---

## Projects

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/delivery-api-fastapi">Delivery API</a></h3>
      <p>REST API for JWT authentication and order management, with migrations and tests.</p>
      <img src="https://skillicons.dev/icons?i=py,fastapi,sqlite" height="40" alt="Python, FastAPI, SQLite"><br>
      <sub>Python, FastAPI, SQLAlchemy, Alembic, JWT</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/bus-ticket-api">Bus Ticket API</a> <sup>in progress</sup></h3>
      <p>Bus ticket sales with seat reservation per route segment, built to prevent double-booking under concurrent requests.</p>
      <img src="https://skillicons.dev/icons?i=py,fastapi,postgres,redis" height="40" alt="Python, FastAPI, PostgreSQL, Redis"><br>
      <sub>Python, FastAPI, PostgreSQL, Redis</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/api-clima">Weather CLI</a></h3>
      <p>Command-line app that shows real-time weather conditions from WeatherAPI.</p>
      <img src="https://skillicons.dev/icons?i=py" height="40" alt="Python"><br>
      <sub>Python, REST API</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/Ferramenta-de-tracking">Case Tracking Tool</a></h3>
      <p>Local tool that distributes cases among analysts and builds an Excel tracking workbook with a manager dashboard, SLA control and a PDF summary.</p>
      <img src="https://skillicons.dev/icons?i=py" height="40" alt="Python"><br>
      <sub>Python, openpyxl, Excel (XLSM)</sub>
    </td>
  </tr>
</table>

Open a project below for details.

<details>
<summary><b>Delivery API: run it locally</b></summary>
<br>

```bash
git clone https://github.com/Prabovn7/delivery-api-fastapi.git
cd delivery-api-fastapi
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# copy .env.example to .env and fill in your values
uvicorn main:app --reload
```

FastAPI serves interactive API docs at `http://127.0.0.1:8000/docs`.

</details>

<details>
<summary><b>Bus Ticket API: design goals</b></summary>
<br>

- A seat can be sold for different parts of the same route, as long as the segments don't overlap.
- Two buyers asking for the same seat at the same time must never both succeed.
- PostgreSQL holds the reservations. Redis supports the concurrency control.

</details>

<details>
<summary><b>Case Tracking Tool: how it works</b></summary>
<br>

1. Reads an Excel file with the open cases and validates the required fields.
2. Sorts the cases by opening date, oldest first.
3. Distributes them evenly among the analysts. The difference between any two analysts is at most one case.
4. Generates the tracking workbook (`.xlsm`) with status, reason and notes per case.
5. Adds a manager dashboard, SLA control (4 business days) and a PDF summary.

It runs locally and needs no external integration. The public demo uses fictional data.

</details>

---

## Stack

**Languages**<br>
<img src="https://skillicons.dev/icons?i=py,java,c,js,ts,html,css,bash" height="48" alt="Python, Java, C, JavaScript, TypeScript, HTML, CSS, Bash">

**Backend frameworks**<br>
<img src="https://skillicons.dev/icons?i=fastapi,flask,spring,nodejs,django,express,nestjs" height="48" alt="FastAPI, Flask, Spring, Node.js, Django, Express, NestJS">

**Databases and tools**<br>
<img src="https://skillicons.dev/icons?i=postgres,sqlite,mysql,mongodb,redis,docker,git,github,githubactions,linux,nginx,postman,vscode" height="48" alt="PostgreSQL, SQLite, MySQL, MongoDB, Redis, Docker, Git, GitHub, GitHub Actions, Linux, Nginx, Postman, VS Code">

<details>
<summary><b>Currently learning</b></summary>
<br>

Concurrency control in booking systems, Redis, application security and clean architecture.

</details>

---

## Contact

<img src="https://raw.githubusercontent.com/Prabovn7/Prabovn7/main/assets/status-en.svg" alt="Open to junior and internship backend roles" width="400">

<p>
  <a href="https://www.linkedin.com/in/pablov-santos-dev"><img src="https://img.shields.io/badge/LinkedIn-0F1216?style=for-the-badge&logo=linkedin&logoColor=7C9CBF" alt="LinkedIn"></a>
  <a href="https://github.com/Prabovn7?tab=repositories"><img src="https://img.shields.io/badge/Repositories-0F1216?style=for-the-badge&logo=github&logoColor=7C9CBF" alt="All repositories on GitHub"></a>
</p>
