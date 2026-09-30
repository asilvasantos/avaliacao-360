import os
import sqlite3

DB_NAME = "database.db"
DB_OLD = "database_antigo.db"

if os.path.exists(DB_NAME):
  os.remove(DB_NAME)

print("Criando novo banco de dados estruturado...")
conn = sqlite3.connect(DB_NAME)
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Criação das tabelas
cursor.execute(
    "CREATE TABLE teams (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,"
    " class_name TEXT)"
)
cursor.execute(
    "CREATE TABLE students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT,"
    " team_id INTEGER, FOREIGN KEY(team_id) REFERENCES teams(id))"
)
cursor.execute("""
    CREATE TABLE evaluations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        submission_group TEXT,
        evaluated_id INTEGER,
        q_tecnica INTEGER,
        q_problemas INTEGER,
        q_teoria INTEGER,
        q_colaboracao INTEGER,
        q_tarefas INTEGER,
        q_feedback INTEGER,
        q_comunicacao INTEGER,
        q_proatividade INTEGER,
        q_postura INTEGER,
        pontos_fortes TEXT,
        oportunidades TEXT,
        FOREIGN KEY(evaluated_id) REFERENCES students(id)
    )
""")

# Inserção das turmas e alunos
turma_1_data = {
    "Equipe 1": [
        "Víctor Hugo Lima Schmidt",
        "Marlon Martins Braga",
        "Samantha Yumi Tanaka",
        "Raissa Silva de Oliveira",
        "Antonio Leonardo Souto Gomes",
        "Kyara Esteves de Sousa",
    ],
    "Equipe 2": [
        "Milena Marques Simões de Oliveira",
        "Ian Lucca Soares Mesquita",
        "Gabriel da Cruz Teixeira Ojo",
        "Maria Eduarda dos Anjos Martins",
        "Laura Carolina de Sousa Gomes",
        "Arthur Miranda Suares",
    ],
    "Equipe 3": [
        "Estevão Lins Maia",
        "Stenio Ashlen Simplicio Gomes",
        "Hazel de Paula Bernardo",
        "Talita Fernandes Nunes",
        "Luan da Silva Feres",
        "Giulio dos Anjos Santos",
        "Ivan Vieira Delmondez de Oliveira",
    ],
    "Equipe 4": [
        "Ian Costa Guimarães",
        "Maykon Júnio dos Santos Soares",
        "Luísa Amâncio Brambilla",
        "Rebeca Bontempo Caputo",
        "Ellen Kauany Silva da Vitória",
        "Natalia e M Santos",
    ],
    "Equipe 5": [
        "Thiago Correia Gonzaga",
        "Gabriella Oliveira de Souza Dias",
        "Maria Eduarda Denis Duarte Marques",
        "Guilherme Silva Dutra",
        "Eliane Orlandin do Carmo",
        "Daltro Oliveira Vinuto",
    ],
    "Equipe 6": [
        "David Zimmermann Balbe",
        "Gabriel Maciel Araújo",
        "Amanda Cristina Veloso Teixeira",
        "Zaine Sousa Silveira",
        "Graziella Silva Viana Doche",
        "Luiz Felipe de Oliveira Araujo",
    ],
    "Equipe 7": [
        "Ana Paula Gomes de Matos",
        "Matheus Henrique Picone Rosa",
        "Pedro Henrique Gonçalves de Oliveira",
        "JHECY KETLIN GOMES VIEIRA",
        "Maria Luisa Oliveira Lima",
        "Guilherme Bastos Moreira",
    ],
    "Equipe 8": [
        "Ketlyn Karen Silva de Morais",
        "João Vítor Carvalho Barbosa",
        "Keila Alves Ferreira",
        "Vinícius César Sena Torres",
        "Victor Barbosa da Silva",
        "Thayna Goncalves Dutra",
    ],
    "Equipe 9": [
        "Felipe Carvalho Balbino da Silva",
        "Luiz Oryone Moraes Lira",
        "Mahiaara Amanda Pereira Barros",
        "Mylena Trindade de Mendonça",
        "Pedro Henrique Pereira Santos",
    ],
    "Equipe 10": [
        "Letícia Araújo da Silva Amparo",
        "Pedro Henrique Muniz de Oliveira",
        "Ricardo Correa Ribeiro",
        "Iasmin Morena Vitor Marques",
        "Maria Eduarda Dos Santos Rosa",
        "Paulo Henrique Sousa Soares e Silva",
    ],
    "Equipe 11": [
        "Emilly da Costa Queiroz Soares",
        "Angela Severo Barbosa Medeiros",
        "Yzabella Miranda Pimenta",
        "Samara Nascimento Santos",
        "Sarah Gleice Andrade de Souza",
    ],
}

turma_2_data = {
    "Equipe 1": [
        "Ana Beatriz de Oliveira Marques",
        "Túlio Augusto Celeri",
        "Maria Carolina Martins Frota",
        "Maria Eduarda de Oliveira Gomes",
        "Felipe Matheus Ribeiro Lopes",
    ],
    "Equipe 2": [
        "Leticia Miti",
        "Rayssa Lorrane Costa Souza",
        "Rafaella Borges Ribeiro",
        "Mayara Vieira Martins Santos",
        "Tayrine",
        "Davi Leite",
    ],
    "Equipe 3": [
        "Artur Braz Lopes",
        "Pedro Henrique Silva de Sousa",
        "Laisa Paiva",
        "Maria Clara Alves de Sousa",
        "Samara Pereira Quintanilha",
    ],
    "Equipe 4": [
        "Breno dos Santos Guimarães",
        "Vítor Gonçalves de Andrade Silva",
        "Wingrid da Costa Silva",
        "Jhessica Evelyn Viana Vieira",
        "Samara Letícia Alves dos Santos",
    ],
    "Equipe 5": [
        "Cauan da Silva Soares",
        "Isabel Azar de Holanda",
        "Mariah Gladys de Oliveira Santos",
        "Arthur de Melo Garcia",
        "Mickeias Charles de Oliveira Paiva",
    ],
    "Equipe 6": [
        "Ana Júlia Batista de Souza",
        "Ingrid da Cruz Galvão dos Santos Soares",
        "Eduarda Christina Silva dos Reis",
        "Cibelly Lourenço Ferreira",
        "Paulo Vitor Gomes de Brito Matos",
    ],
    "Equipe 7": [
        "Camila Silva Cavalcante",
        "Mariana Simion dos Santos",
        "Marjorie Mitzi Cavalcante Rodrigues",
        "Victoria Ferreira Santos",
        "Jessika Cardoso do Nascimento",
    ],
    "Equipe 8": [
        "Matheus Sales",
        "Marlon Dias Marques",
        "Pedro Augusto Reis Alvim",
        "Víctor Moreira Almeida",
        "Joao Artur Leles Ferreira Pinheiro",
        "Isabela França",
    ],
    "Equipe 9": [
        "Amanda Elisa de Oliveira Carvalho",
        "Nasser Caixeta",
        "Pedro Lucas Dourado Santos",
        "Jhiovana Silva Ribeiro",
        "Léo Alec Marquez de Barros",
    ],
    "Equipe 10": [
        "André Alves Acioli da Silveira",
        "Ingrid Hanna de Oliveira Nóbrega",
        "Melissa Santos",
        "Samuel de Souza Rodrigues",
        "Guilherme Barros Jacintho Ribeiro",
    ],
    "Equipe 11": [
        "Felipe de Jesus Rodrigues",
        "Ranni Heler Lopes",
        "George Filipe Rodrigues de Lacerda",
        "Eric Luiz Rodrigues de França",
        "Larissa Moreira de Alencar Giffoni Lacerda",
    ],
    "Equipe 12": [
        "Alexandre Pereira de Sousa",
        "Rebeca Vitoria",
        "Lucas Alves Vilela",
        "Luana Barbosa Souza",
        "Marcos Santos Bittar",
    ],
    "Equipe 13": [
        "Ruan Sobreira Carvalho",
        "Ester Luiza Souza Campos",
        "Eduarda Lima de Oliveira",
        "Davi Vasconcelos de Araújo",
        "Yan Santos Rodrigues",
    ],
}

for team_name, members in turma_1_data.items():
  cursor.execute(
      "INSERT INTO teams (name, class_name) VALUES (?, ?)", (team_name, "Turma 1")
  )
  team_id = cursor.lastrowid
  for member in members:
    cursor.execute(
        "INSERT INTO students (name, team_id) VALUES (?, ?)", (member, team_id)
    )

for team_name, members in turma_2_data.items():
  cursor.execute(
      "INSERT INTO teams (name, class_name) VALUES (?, ?)", (team_name, "Turma 2")
  )
  team_id = cursor.lastrowid
  for member in members:
    cursor.execute(
        "INSERT INTO students (name, team_id) VALUES (?, ?)", (member, team_id)
    )

conn.commit()

# Migração dos dados antigos se o arquivo existir
if os.path.exists(DB_OLD):
  print("Migrando dados do banco antigo...")
  conn_old = sqlite3.connect(DB_OLD)
  conn_old.row_factory = sqlite3.Row
  evals_old = conn_old.execute("SELECT * FROM evaluations").fetchall()

  migradas = 0
  for ev in evals_old:
    cursor.execute(
        """
            INSERT INTO evaluations (
                submission_group, evaluated_id, q_tecnica, q_problemas, q_teoria, 
                q_colaboracao, q_tarefas, q_feedback, q_comunicacao, q_proatividade, 
                q_postura, pontos_fortes, oportunidades
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            "migrado_legado",
            ev["evaluated_id"],
            ev["q_tecnica"],
            ev["q_problemas"],
            ev["q_teoria"],
            ev["q_colaboracao"],
            ev["q_tarefas"],
            ev["q_feedback"],
            ev["q_comunicacao"],
            ev["q_proatividade"],
            ev["q_postura"],
            ev["pontos_fortes"] if "pontos_fortes" in ev.keys() else "",
            ev["oportunidades"] if "oportunidades" in ev.keys() else "",
        ),
    )
    migradas += 1
  conn.commit()
  conn_old.close()
  print(f"Migração concluída! {migradas} registros migrados com sucesso.")
else:
  print("Nenhum banco antigo encontrado para migrar. Banco criado limpo.")

conn.close()