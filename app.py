from flask import Flask, render_template, request, redirect, url_for, flash, Response
from database import get_db, init_db
import csv
import io

app = Flask(__name__)
app.secret_key = "agenda-contactos-cambia-esta-clave"

@app.route("/")
def inicio():
    q = request.args.get("q", "").strip()
    categoria = request.args.get("categoria", "").strip()
    favoritos = request.args.get("favoritos", "")
    db = get_db()
    sql = "SELECT * FROM contactos WHERE 1=1"
    params = []
    if q:
        sql += " AND (nombre LIKE ? OR telefono LIKE ? OR correo LIKE ?)"
        params += [f"%{q}%"] * 3
    if categoria:
        sql += " AND categoria = ?"
        params.append(categoria)
    if favoritos == "1":
        sql += " AND favorito = 1"
    sql += " ORDER BY favorito DESC, nombre COLLATE NOCASE"
    contactos = db.execute(sql, params).fetchall()
    total = db.execute("SELECT COUNT(*) FROM contactos").fetchone()[0]
    favs = db.execute("SELECT COUNT(*) FROM contactos WHERE favorito=1").fetchone()[0]
    familias = db.execute("SELECT COUNT(*) FROM contactos WHERE categoria='Familia'").fetchone()[0]
    escuelas = db.execute("SELECT COUNT(*) FROM contactos WHERE categoria='Escuela'").fetchone()[0]
    db.close()
    return render_template("index.html", contactos=contactos, q=q, categoria=categoria,
                           favoritos=favoritos, total=total, favs=favs,
                           familias=familias, escuelas=escuelas)

@app.route("/agregar", methods=["POST"])
def agregar():
    datos = [request.form.get(x, "").strip() for x in
             ("nombre", "telefono", "correo", "categoria", "cumpleanos", "notas")]
    if not datos[0] or not datos[1] or not datos[3]:
        flash("Nombre, teléfono y categoría son obligatorios.", "error")
        return redirect(url_for("inicio"))
    db = get_db()
    db.execute("""INSERT INTO contactos
        (nombre, telefono, correo, categoria, cumpleanos, notas)
        VALUES (?, ?, ?, ?, ?, ?)""", datos)
    db.commit()
    db.close()
    flash("¡Contacto guardado correctamente!", "ok")
    return redirect(url_for("inicio"))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    db = get_db()
    contacto = db.execute("SELECT * FROM contactos WHERE id=?", (id,)).fetchone()
    if contacto is None:
        db.close()
        flash("No se encontró ese contacto.", "error")
        return redirect(url_for("inicio"))
    if request.method == "POST":
        datos = [request.form.get(x, "").strip() for x in
                 ("nombre", "telefono", "correo", "categoria", "cumpleanos", "notas")]
        if not datos[0] or not datos[1] or not datos[3]:
            flash("Completa nombre, teléfono y categoría.", "error")
            db.close()
            return redirect(url_for("editar", id=id))
        db.execute("""UPDATE contactos SET nombre=?, telefono=?, correo=?,
            categoria=?, cumpleanos=?, notas=? WHERE id=?""", (*datos, id))
        db.commit()
        db.close()
        flash("Contacto actualizado.", "ok")
        return redirect(url_for("inicio"))
    db.close()
    return render_template("editar.html", contacto=contacto)

@app.route("/favorito/<int:id>", methods=["POST"])
def favorito(id):
    db = get_db()
    db.execute("UPDATE contactos SET favorito = CASE WHEN favorito=1 THEN 0 ELSE 1 END WHERE id=?", (id,))
    db.commit()
    db.close()
    return redirect(request.referrer or url_for("inicio"))

@app.route("/eliminar/<int:id>", methods=["POST"])
def eliminar(id):
    db = get_db()
    db.execute("DELETE FROM contactos WHERE id=?", (id,))
    db.commit()
    db.close()
    flash("Contacto eliminado.", "ok")
    return redirect(url_for("inicio"))

@app.route("/exportar")
def exportar():
    db = get_db()
    rows = db.execute("SELECT nombre, telefono, correo, categoria, cumpleanos, notas FROM contactos ORDER BY nombre").fetchall()
    db.close()
    salida = io.StringIO()
    writer = csv.writer(salida)
    writer.writerow(["Nombre", "Telefono", "Correo", "Categoria", "Cumpleanos", "Notas"])
    for row in rows:
        writer.writerow(list(row))
    return Response("\\ufeff" + salida.getvalue(), mimetype="text/csv",
                    headers={"Content-Disposition": "attachment; filename=mis_contactos.csv"})

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5000, debug=True)
