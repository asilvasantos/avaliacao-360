import sqlite3
conn = sqlite3.connect('database.db') # ou o caminho do seu banco
cursor = conn.cursor()
cursor.execute("INSERT INTO students (id, name, team_id) VALUES (133, 'João Marcos Melo Monteiro', 22)")
conn.commit()
print("Aluno inserido com sucesso!")
conn.close()
