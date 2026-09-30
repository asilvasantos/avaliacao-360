import os
import sqlite3
import traceback
import uuid
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)
DATABASE = "database.db"


def get_db():
  conn = sqlite3.connect(DATABASE)
  conn.row_factory = sqlite3.Row
  return conn


def init_db():
  with get_db() as conn:
    conn.execute(
        "CREATE TABLE IF NOT EXISTS teams (id INTEGER PRIMARY KEY AUTOINCREMENT,"
        " name TEXT, class_name TEXT)"
    )
    conn.execute(
        "CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY"
        " AUTOINCREMENT, name TEXT, team_id INTEGER, FOREIGN KEY(team_id)"
        " REFERENCES teams(id))"
    )
    conn.execute("""
            CREATE TABLE IF NOT EXISTS evaluations (
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

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM teams")
    if cursor.fetchone()[0] == 0:
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
            "INSERT INTO teams (name, class_name) VALUES (?, ?)",
            (team_name, "Turma 1"),
        )
        team_id = cursor.lastrowid
        for member in members:
          cursor.execute(
              "INSERT INTO students (name, team_id) VALUES (?, ?)",
              (member, team_id),
          )

      for team_name, members in turma_2_data.items():
        cursor.execute(
            "INSERT INTO teams (name, class_name) VALUES (?, ?)",
            (team_name, "Turma 2"),
        )
        team_id = cursor.lastrowid
        for member in members:
          cursor.execute(
              "INSERT INTO students (name, team_id) VALUES (?, ?)",
              (member, team_id),
          )

      conn.commit()


# Executa a inicialização do banco ao carregar o aplicativo
init_db()


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/admin")
def admin():
  return render_template("admin.html")


@app.route("/api/students")
def get_students():
  with get_db() as conn:
    students = conn.execute(
        """
            SELECT s.id, s.name, t.name as team_name, t.class_name, t.id as team_id 
            FROM students s 
            JOIN teams t ON s.team_id = t.id 
            ORDER BY t.class_name, t.name, s.name
        """
    ).fetchall()
    return jsonify([dict(row) for row in students])


@app.route("/api/team-mates/<int:student_id>")
def get_team_mates(student_id):
  with get_db() as conn:
    student = conn.execute(
        "SELECT team_id FROM students WHERE id = ?", (student_id,)
    ).fetchone()
    if not student:
      return jsonify([])
    team_id = student["team_id"]

    mates = conn.execute(
        "SELECT id, name FROM students WHERE team_id = ? AND id != ?",
        (team_id, student_id),
    ).fetchall()
    return jsonify([dict(row) for row in mates])


@app.route("/api/submit", methods=["POST"])
def submit_evaluation():
  data = request.json
  evaluations = data.get("evaluations", [])
  sub_group = str(uuid.uuid4())[:8]

  with get_db() as conn:
    for ev in evaluations:
      conn.execute(
          """
                INSERT INTO evaluations (submission_group, evaluated_id, q_tecnica, q_problemas, q_teoria, q_colaboracao, q_tarefas, q_feedback, q_comunicacao, q_proatividade, q_postura, pontos_fortes, oportunidades)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
          (
              sub_group,
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
              ev.get("pontos_fortes", ""),
              ev.get("oportunidades", ""),
          ),
      )
    conn.commit()
  return jsonify({"status": "success"})


@app.route("/api/admin/results")
def admin_results():
  try:
    with get_db() as conn:
      query = """
                SELECT 
                    s.id as student_id,
                    s.name as student_name,
                    t.name as team_name,
                    t.class_name,
                    COUNT(e.id) as total_evaluations,
                    ROUND(AVG(e.q_tecnica), 2) as avg_tecnica,
                    ROUND(AVG(e.q_problemas), 2) as avg_problemas,
                    ROUND(AVG(e.q_teoria), 2) as avg_teoria,
                    ROUND(AVG(e.q_colaboracao), 2) as avg_colaboracao,
                    ROUND(AVG(e.q_tarefas), 2) as avg_tarefas,
                    ROUND(AVG(e.q_feedback), 2) as avg_feedback,
                    ROUND(AVG(e.q_comunicacao), 2) as avg_comunicacao,
                    ROUND(AVG(e.q_proatividade), 2) as avg_proatividade,
                    ROUND(AVG(e.q_postura), 2) as avg_postura
                FROM students s
                JOIN teams t ON s.team_id = t.id
                LEFT JOIN evaluations e ON s.id = e.evaluated_id
                GROUP BY s.id
                ORDER BY t.class_name, t.name, s.name
            """
      results = conn.execute(query).fetchall()

      submissions_query = """
                SELECT id, submission_group, evaluated_id, q_tecnica, q_problemas, q_teoria, 
                       q_colaboracao, q_tarefas, q_feedback, q_comunicacao, q_proatividade, 
                       q_postura, pontos_fortes, oportunidades
                FROM evaluations
                ORDER BY evaluated_id, submission_group
            """
      raw_evals = conn.execute(submissions_query).fetchall()

      evals_by_student = {}
      for ev in raw_evals:
        e_id = ev["evaluated_id"]
        if e_id not in evals_by_student:
          evals_by_student[e_id] = []
        evals_by_student[e_id].append(dict(ev))

      output = []
      for row in results:
        row_dict = dict(row)
        st_id = row["student_id"]
        row_dict["individual_submissions"] = evals_by_student.get(st_id, [])
        output.append(row_dict)

      return jsonify(output)
  except Exception as e:
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)