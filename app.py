from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# Inisialisasi Flask dan SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///confession.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Definisikan model database
class Confession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Buat database dan tabel jika belum ada
with app.app_context():
    db.create_all()  # Membuat database dan tabel

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        message = request.form["message"]
        
        # Menyimpan confession ke database
        new_confession = Confession(name=name, message=message)
        db.session.add(new_confession)  # Menambah data ke session
        db.session.commit()  # Menyimpan perubahan ke database

        # Redirect ke halaman utama setelah POST
        return redirect(url_for('home'))

    # Mengambil semua confession dari database
    confessions = Confession.query.all()
    return render_template("home.html", confessions=confessions)

@app.route("/delete/<int:id>")
def delete_confession(id):
    confession = Confession.query.get_or_404(id)  # Mendapatkan confession berdasarkan ID
    db.session.delete(confession)  # Menghapus confession dari database
    db.session.commit()  # Menyimpan perubahan ke database
    return redirect(url_for('home'))  # Kembali ke halaman utama setelah dihapus
from waitress import serve

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=5000)
