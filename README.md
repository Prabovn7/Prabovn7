<div align="center">
  <h1>
    <img src="https://raw.githubusercontent.com/Prabovn7/Prabovn7/main/assets/banner.svg" alt="Pablo Vinicius, estudante de Engenharia de Software focado em backend" width="100%">
  </h1>
</div>

<p align="center">
  <a href="README.md">English</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#projetos">Projetos</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#stack">Stack</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="#contato">Contato</a>
</p>

Estudante de Engenharia de Software desenvolvendo projetos backend com autenticação, persistência de dados e testes. Atualmente focado em PostgreSQL, Docker e design seguro para concorrência.

---

## Projetos

<table>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/delivery-api-fastapi">Delivery API</a></h3>
      <p>API REST com autenticação JWT e gerenciamento de pedidos, com migrações e testes.</p>
      <img src="https://skillicons.dev/icons?i=py,fastapi,sqlite" height="40" alt="Python, FastAPI, SQLite"><br>
      <sub>Python, FastAPI, SQLAlchemy, Alembic, JWT</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/bus-ticket-api">Bus Ticket API</a> <sup>em andamento</sup></h3>
      <p>Venda de passagens de ônibus com reserva de assento por trecho, feita para impedir reserva dupla sob requisições concorrentes.</p>
      <img src="https://skillicons.dev/icons?i=py,fastapi,postgres,redis" height="40" alt="Python, FastAPI, PostgreSQL, Redis"><br>
      <sub>Python, FastAPI, PostgreSQL, Redis</sub>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/api-clima">Weather CLI</a></h3>
      <p>App de linha de comando que mostra o clima em tempo real a partir da WeatherAPI.</p>
      <img src="https://skillicons.dev/icons?i=py" height="40" alt="Python"><br>
      <sub>Python, API REST</sub>
    </td>
    <td width="50%" valign="top">
      <h3><a href="https://github.com/Prabovn7/Ferramenta-de-tracking">Tracking de Cases</a></h3>
      <p>Ferramenta local que distribui cases entre analistas e gera uma planilha de tracking em Excel com dashboard do gestor, controle de SLA e resumo em PDF.</p>
      <img src="https://skillicons.dev/icons?i=py" height="40" alt="Python"><br>
      <sub>Python, openpyxl, Excel (XLSM)</sub>
    </td>
  </tr>
</table>

Abra um projeto abaixo para ver os detalhes.

<details>
<summary><b>Delivery API: rodar localmente</b></summary>
<br>

```bash
git clone https://github.com/Prabovn7/delivery-api-fastapi.git
cd delivery-api-fastapi
python -m venv .venv
# Windows: .venv\Scripts\activate    macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
# copie .env.example para .env e preencha os valores
uvicorn main:app --reload
```

O FastAPI gera a documentação interativa da API em `http://127.0.0.1:8000/docs`.

</details>

<details>
<summary><b>Bus Ticket API: objetivos de design</b></summary>
<br>

- Um assento pode ser vendido para trechos diferentes da mesma rota, desde que os trechos não se sobreponham.
- Dois compradores pedindo o mesmo assento ao mesmo tempo nunca podem conseguir os dois.
- O PostgreSQL guarda as reservas. O Redis apoia o controle de concorrência.

</details>

<details>
<summary><b>Tracking de Cases: como funciona</b></summary>
<br>

1. Lê uma planilha Excel com os cases em aberto e valida os campos obrigatórios.
2. Ordena os cases pela data de abertura, do mais antigo para o mais recente.
3. Distribui de forma equilibrada entre os analistas. A diferença entre dois analistas é de no máximo um case.
4. Gera a planilha de tracking (`.xlsm`) com status, motivo e observação por case.
5. Adiciona dashboard do gestor, controle de SLA (4 dias úteis) e resumo em PDF.

Roda localmente e não precisa de integração externa. A demonstração pública usa dados fictícios.

</details>

---

## Stack

**Linguagens**<br>
<img src="https://skillicons.dev/icons?i=py,java,c,js,ts,html,css,bash" height="48" alt="Python, Java, C, JavaScript, TypeScript, HTML, CSS, Bash">

**Frameworks backend**<br>
<img src="https://skillicons.dev/icons?i=fastapi,flask,spring,nodejs,django,express,nestjs" height="48" alt="FastAPI, Flask, Spring, Node.js, Django, Express, NestJS">

**Bancos de dados e ferramentas**<br>
<img src="https://skillicons.dev/icons?i=postgres,sqlite,mysql,mongodb,redis,docker,git,github,githubactions,linux,nginx,postman,vscode" height="48" alt="PostgreSQL, SQLite, MySQL, MongoDB, Redis, Docker, Git, GitHub, GitHub Actions, Linux, Nginx, Postman, VS Code">

<details>
<summary><b>Estudando atualmente</b></summary>
<br>

Controle de concorrência em sistemas de reserva, Redis, segurança de aplicações e arquitetura limpa.

</details>

---

## Contato

<img src="https://raw.githubusercontent.com/Prabovn7/Prabovn7/main/assets/status-pt.svg" alt="Aberto a vagas de estágio e júnior em backend" width="400">

<p>
  <a href="https://www.linkedin.com/in/pablov-santos-dev"><img src="https://img.shields.io/badge/LinkedIn-0F1216?style=for-the-badge&logo=linkedin&logoColor=7C9CBF" alt="LinkedIn"></a>
  <a href="https://github.com/Prabovn7?tab=repositories"><img src="https://img.shields.io/badge/Reposit%C3%B3rios-0F1216?style=for-the-badge&logo=github&logoColor=7C9CBF" alt="Todos os repositórios no GitHub"></a>
</p>
