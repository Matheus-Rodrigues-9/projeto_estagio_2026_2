# Decisões de Projeto — VetAgenda

## 1. Tema escolhido

O tema escolhido foi o **VetAgenda**, um sistema de solicitação e gerenciamento de atendimentos veterinários.

A proposta foi desenvolver uma aplicação simples, mas próxima de uma situação real: o tutor solicita um atendimento e a clínica analisa posteriormente essa solicitação.

A solicitação não é considerada automaticamente confirmada. Todo novo registro é criado inicialmente com o status `pendente`.

---

## 2. Tecnologias escolhidas

### Python + Flask

O Flask foi escolhido por ser um framework leve e permitir compreender de forma clara o funcionamento das rotas, requisições, sessões e integração com o banco de dados.

Também permitiu desenvolver o projeto sem adicionar complexidade desnecessária.

### SQLite

O SQLite foi escolhido por não exigir a instalação ou configuração de um servidor de banco de dados externo.

Essa escolha facilita a execução do projeto em outras máquinas e atende bem ao escopo proposto.

### Flask-SQLAlchemy

Foi utilizado para realizar a comunicação entre a aplicação Flask e o banco SQLite através de modelos Python.

O uso de ORM também permitiu trabalhar com consultas e persistência utilizando as classes da aplicação.

### HTML + CSS + Jinja2

Foram utilizados para a construção da página pública, tela de login e painel administrativo.

O Jinja2 foi utilizado para integrar os dados enviados pelo Flask às páginas HTML.

### Werkzeug

Foi utilizado para geração e verificação do hash da senha administrativa.

Dessa forma, a senha não é armazenada diretamente em texto simples no banco de dados.

### python-dotenv

Foi utilizado para carregar a `SECRET_KEY` através de variável de ambiente.

Com isso, a chave real não precisa ficar armazenada diretamente no código-fonte ou no repositório.

---

## 3. Decisões de negócio

### Solicitações começam como pendentes

Ao enviar o formulário, o tutor não recebe uma confirmação automática do atendimento.

A solicitação é registrada inicialmente com o status:

`pendente`

Posteriormente, a equipe da clínica pode confirmar ou cancelar a solicitação através do painel administrativo.

### Conflito de horários

O sistema permite que existam várias solicitações pendentes para a mesma data e horário.

O conflito é verificado apenas quando o administrador tenta confirmar uma solicitação.

Caso já exista outro atendimento confirmado para a mesma data e horário, a nova confirmação é bloqueada.

Essa decisão foi tomada porque uma solicitação pendente ainda não representa um horário efetivamente reservado pela clínica.

---

## 4. Funcionalidades extras implementadas

Além das funcionalidades principais, foram implementados:

- prevenção de conflito de horários;
- dashboard com indicadores;
- contador total de solicitações;
- contador de solicitações pendentes;
- contador de solicitações confirmadas;
- contador de solicitações canceladas;
- busca pelo nome do tutor ou do animal;
- filtro por status;
- validações no front-end e no back-end;
- bloqueio de datas passadas;
- validação das opções de espécie, porte e serviço;
- mensagens visuais de sucesso e erro;
- senha administrativa armazenada com hash;
- chave secreta configurada através de variável de ambiente;
- interface responsiva;
- identidade visual relacionada ao tema veterinário.

---

## 5. Funcionalidades que não foram implementadas

Algumas funcionalidades foram deliberadamente deixadas fora do escopo para priorizar uma aplicação simples, funcional e bem testada.

Entre elas:

- cadastro de conta para tutores;
- prontuário veterinário;
- pagamento on-line;
- controle de estoque;
- receitas e prescrições;
- chat entre tutor e clínica;
- recuperação de senha;
- suporte a múltiplas clínicas.

A prioridade foi garantir que o fluxo principal estivesse completo, compreensível e funcionando corretamente.

---

# Uso de Inteligência Artificial

A inteligência artificial foi utilizada como ferramenta de apoio durante o desenvolvimento.

Ela foi utilizada principalmente para:

- discutir possíveis arquiteturas;
- auxiliar na organização da estrutura do projeto;
- explicar conceitos relacionados a Flask e SQLAlchemy;
- sugerir exemplos de implementação;
- auxiliar na análise de erros;
- revisar decisões de desenvolvimento;
- auxiliar na estruturação da documentação.

As sugestões não foram simplesmente copiadas sem análise. Cada funcionalidade foi implementada, executada e testada durante o desenvolvimento.

---

## 6. O que foi delegado para IA e o que foi feito manualmente?

A IA auxiliou principalmente com explicações, sugestões de código, organização das etapas e análise de erros.

Foram realizados manualmente:

- criação da estrutura de diretórios;
- criação e edição dos arquivos;
- implementação do código no VS Code;
- execução da aplicação;
- criação e ativação do ambiente virtual;
- instalação das dependências;
- preenchimento e envio dos formulários;
- testes das funcionalidades;
- criação dos registros;
- verificação do banco de dados;
- identificação de comportamentos incorretos;
- correção dos erros;
- novos testes após as correções;
- criação dos commits;
- gerenciamento do repositório utilizando GitHub Desktop;
- personalização visual da aplicação.

O desenvolvimento foi realizado de forma incremental, testando cada etapa antes de seguir para a próxima.

---

## 7. Exemplo de uma resposta da IA que não funcionou corretamente

Durante a implementação da prevenção de conflito de horários, uma consulta acabou contendo:

```python
horario=atendimento.data