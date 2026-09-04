# VetAgenda 🐾

Sistema web para solicitação e gerenciamento de atendimentos veterinários, desenvolvido como projeto para o processo seletivo de estágio da Mupi Systems.

O VetAgenda permite que tutores solicitem atendimentos para seus animais por meio de uma página pública. A equipe da clínica utiliza uma área administrativa protegida para analisar, confirmar ou cancelar as solicitações.

---

## Funcionalidades

### Página pública

- Solicitação de atendimento veterinário;
- Cadastro dos dados do tutor;
- Cadastro dos dados do animal;
- Seleção de espécie, porte e serviço;
- Escolha de data e horário;
- Campo para observações;
- Validação dos dados no front-end e no back-end;
- Bloqueio de datas passadas;
- Feedback visual de sucesso ou erro;
- Solicitações iniciam automaticamente com status `pendente`;
- Interface responsiva;
- Identidade visual relacionada ao tema veterinário.

### Painel administrativo

- Login protegido;
- Senha administrativa armazenada com hash;
- Autenticação utilizando sessão;
- Logout;
- Proteção da rota administrativa;
- Listagem das solicitações cadastradas;
- Ordenação por data e horário;
- Alteração de status para:
  - `pendente`;
  - `confirmado`;
  - `cancelado`;
- Identificação visual dos status;
- Dashboard com contadores;
- Busca por nome do tutor ou animal;
- Filtro por status;
- Bloqueio de conflito entre atendimentos confirmados na mesma data e horário.

---

## Tecnologias utilizadas

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Werkzeug
- python-dotenv
- HTML5
- CSS3
- Jinja2
- Git
- GitHub

---

## Estrutura do projeto

```text
projeto_estagio_2026_2/
│
├── static/
│   ├── css/
│   │   └── style.css
│   │
│   └── img/
│       └── mupi-logo.png
│
├── templates/
│   ├── index.html
│   ├── login.html
│   └── admin.html
│
├── instance/
│   └── vetagenda.db
│       (gerado automaticamente)
│
├── .env.example
├── .gitignore
├── app.py
├── criar_admin.py
├── DECISOES.md
├── requirements.txt
└── README.md