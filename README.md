Controle de Estudantes, Cursos e Notas (MongoDB)

Projeto em Python que implementa CRUD completo para Estudantes, Cursos e Lançamento de Notas, migrado do Oracle para o banco de dados MongoDB (NoSQL - Orientado a Documentos). O sistema utiliza uma estrutura de dados desnormalizada onde as notas e os metadados do curso são incorporados (embedded) nos documentos de Estudante. O sistema é uma aplicação de linha de comando (CLI) simples.

Estrutura

main.py: Ponto de entrada com menu CLI.

src/: Código Python para conexão, modelos e operações CRUD.

requirements.txt: Dependências (pymongo em vez de cx_Oracle).

config.ini: Esvaziado, pois a conexão agora utiliza uma URI direta do MongoDB.

db/: Arquivos SQL (agora vazios/removidos), pois o MongoDB é schemaless (sem esquema rígido).

Pré-requisitos

Python 3.8+

MongoDB Server instalado e rodando (padrão em mongodb://localhost:27017/).

Biblioteca Python pymongo (instalar com pip install -r requirements.txt).

Como usar

Instale as dependências:

pip install -r requirements.txt


Certifique-se de que o MongoDB está ativo:
O código assume que o servidor MongoDB está rodando no endereço padrão (mongodb://localhost:27017/).

Execute a aplicação:

python3 main.py


O esquema será criado (incluindo o índice de unicidade da matrícula) automaticamente no primeiro acesso.

Use o menu CLI para gerenciar estudantes, cursos e notas.

Modelo de Dados (MongoDB)

O modelo NoSQL utiliza incorporação (embedding):

Coleção ESTUDANTE: Documento principal, contendo todos os dados do estudante e um array chamado cursos que armazena as notas e os dados do curso associados. Isso otimiza o acesso ao histórico individual do aluno.

Coleção CURSO: Coleção de metadados para gerenciamento mestre de cursos.

Observações

Geração de IDs: Os IDs (ex: id_estudante, id_curso) são gerados sequencialmente via lógica Python, simulando o comportamento de sequences do Oracle. O MongoDB usa seu próprio _id internamente.

Notas: As operações de nota (Lançar, Atualizar, Excluir) agora são feitas usando a combinação ID do Estudante e ID do Curso, pois a tabela NOTA relacional foi eliminada.

Situação: As operações de média e situação consideram média >= 6.0 como "APROVADO"
