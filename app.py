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

      # Variável devidamente inicializada e padronizada
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
  init_db()
  port = int(os.environ.get("PORT", 5000))
  app.run(host="0.0.0.0", port=port)