Documentação Kanban API

Este documento descreve as funcionalidades da API de um quadro Kanban e como testá-las. A ferramenta desenvolvida tem como objetivo permitir aos usuários criar e gerenciar quadros, etapas e tarefas. Cada quadro está atribuído a um usuário, cada etapa está vinculada a um quadro, e cada tarefa está associada a um quadro e a uma etapa. A API segue o modelo CRUD (Criar, Ler, Atualizar e Deletar),

Pré-requisitos: 

Para rodar e testar o projeto serão necessários alguns pré-requisitos.  
1 - Ferramentas necessárias: 
  Python  
  Postamn ou insomnia para testar a API 
  Um ambiente virtual (recomendado usar venv) 

Com o código aberto utilizando uma IDE execute as instruções via terminal
2- Dependências do projeto: 
  Instale as dependências do projeto utilizando 
  pip install –r requirements.txt 
 
3- Configuração do projeto: 
  Após instalar as dependências execute os comandas para fazer as migrações do banco de dados e iniciar o servidor: 
  python manage.py migrate
  python manage.py createsuperuser
  python manage.py runserver 

URLs da API:

As URLs do projeto permitem acessar e interagir com os dados. Elas são descritas a seguir:

1. Visualizar e criar quadros:
  URL: http://127.0.0.1:8000/kanban_api/boards/
  Métodos: GET, POST
  Descrição:
    GET: Retorna todos os quadros criados pelo usuário autenticado.
    POST: Cria um novo quadro para o usuário autenticado.

2. Visualizar, alterar e deletar um quadro específico:
URL: http://127.0.0.1:8000/kanban_api/boards/<board_name>/
Métodos: GET, PUT, DELETE
Descrição:
  GET: Visualiza os detalhes de um quadro específico.
  PUT: Atualiza o quadro com base no nome.
  DELETE: Deleta o quadro.
Obeservação: O nome do quadro na URL deve ser o mesmo nome do quadro criado.

3. Visualizar, criar e deletar etapas de um quadro:
URL: http://127.0.0.1:8000/kanban_api/boards/<board_name>/statuses/
Métodos: GET, POST
Descrição:
  GET: Retorna todas as etapas associadas ao quadro.
  POST: Cria uma nova etapa para o quadro especificado.

4. Deletar uma etapa do quadro:
URL: http://127.0.0.1:8000/kanban_api/boards/<board_name>/statuses/<status_name>/
Descrição;
   DELETE: Delete a etapa através do nome.

5. Visualizar e criar tarefas em um quadro:
URL: http://127.0.0.1:8000/kanban_api/cards/<board_name>/
Métodos: GET, POST
Descrição:
  GET: Retorna todas as tarefas associadas ao quadro.
  POST: Cria uma nova tarefa dentro do quadro.

6. Visualizar, atualizar ou deletar uma tarefa específica de um quadro:
URL: http://127.0.0.1:8000/kanban_api/cards/<board_name>/<card_name>/
Métodos: GET, PUT, PATCH, DELETE
Descrição:
  GET: Retorna os detalhes de uma tarefa específica.
  PUT: Atualiza a tarefa com base no nome.
  PATCH: Atualiza a etapa.
  DELETE: Deleta a tarefa.

Exemplos de Requisição:

1. Criar um novo quadro (POST)
URL: http://127.0.0.1:8000/kanban_api/boards/
Requisição em JSON:
{
    "title":"NomedoQuadro",
    "owner":"NomedoUsuario"
}
Resposta esperada: 201 CREATED

2. Visualizar um quadro (GET)
URL: http://127.0.0.1:8000/kanban_api/boards/NomedoQuadro/
Resposta em JSON:
{
 (informações de todos os quadros criados)
}
Resposta espera: 200 OK

3. Criar uma etapa para o quadro (POST)
URL: http://127.0.0.1:8000/kanban_api/boards/NomedoQuadro/statuses/
Requisição em JSON:
{
    "title":"fazer"
}
Resposta esperada : 201 CREATED

4. Criar uma nova tarefa (POST)
URL: http://127.0.0.1:8000/kanban_api/cards/NomedoQuadro/
Requisição em JSON:
{
    "title":"NomedaTerefa",
    "status":"fazer",
    "board":"NomedoQuadro",
    "classification":"tarefa",
    "responsible":"Usuario"
}
Resposta esperada : 201 CREATED

5. Atualizar uma tarefa (PUT)
URL: http://127.0.0.1:8000/kanban_api/cards/NomedoQuadro/NomedaTerefa/
Requisição em JSON:
{
    "title":"NomedaTerefa atualizado",
    "status":"fazer",
    "board":"NomedoQuadro",
    "classification":"tarefa",
    "responsible":"Usuario"
}
Resposta esperada : 200 OK

6. Atualizar a etapa (PATCH)
URL: http://127.0.0.1:8000/kanban_api/cards/NomedoQuadro/NomedaTerefa/
requisição em JSON
{
    "status":"feito"
}
Resposta esperada : 200 OK

Observações finais:

Não consta nos exemplos, porém, como dito anteriormente é possivel deletar Quadros,Etapas e Tarefas.
Para atualizar uma etapa de uma tarefa é necessário ter as etapas criadas e associadas a um quadro, apenas assim para conseguir fazer a transição de etapas.
É possivel criar, visualizar, modificar e deleter informações via usuario administrador(http://127.0.0.1:8000/admin/), podendo visualizar as infrormações através das URL's diretamente no navegador.


