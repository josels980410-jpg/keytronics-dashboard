import os
from flask import Flask, render_template, request, redirect, url_for, session
from datetime import timedelta

# ------------------- CONFIGURACIÓN FLASK -------------------
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "keytronics123")
app.permanent_session_lifetime = timedelta(minutes=30)

# ------------------- USUARIOS PERMITIDOS -------------------
USUARIOS = {
    "admin": "1234",
    "keytronics": "2025"
}

# ------------------- RUTAS PRINCIPALES -------------------
@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if username in USUARIOS and USUARIOS[username] == password:
        session.permanent = True
        session["user"] = username
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Usuario o contraseña incorrectos")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))

    # 🟢 Reemplaza aquí con TU enlace público de Power BI
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiNzI5NWQ3ODctMTZlYy00MGI2LThiZGMtZWI0NzVjYjQ4MmVkIiwidCI6IjAzODk5MTIxLWQ5NzYtNDRlOS1iODI0LTFmYzU1N2JmZGRjZSJ9"

    return f"""
    <html>
        <head>
            <title>Dashboard Power BI</title>
            <style>
                body {{
                    font-family: 'Segoe UI', Arial, sans-serif;
                    background-color: #0a0a0a;
                    color: #00ff80;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: flex-start;
                    padding: 20px;
                    height: 100vh;
                    margin: 0;
                }}
                h2 {{
                    margin-bottom: 15px;
                    color: #00ff80;
                    text-shadow: 0 0 8px #00ff80;
                }}
                iframe {{
                    width: 95%;
                    height: 85vh;
                    border: none;
                    border-radius: 10px;
                    box-shadow: 0 0 25px #00ff80;
                    overflow: hidden;
                }}
                iframe::-webkit-scrollbar {{
                    display: none;
                }}
                .logout {{
                    position: absolute;
                    top: 15px;
                    right: 25px;
                    background-color: transparent;
                    color: #00ff80;
                    border: 1px solid #00ff80;
                    padding: 8px 15px;
                    border-radius: 6px;
                    text-decoration: none;
                    transition: 0.3s;
                }}
                .logout:hover {{
                    background-color: #00ff80;
                    color: #0a0a0a;
                }}
            </style>
        </head>
        <body>
            <a href="{url_for('logout')}" class="logout">Cerrar sesión</a>
            <h2>Bienvenido</h2>

            <!-- 🔒 IFRAME DE POWER BI SIN BOTONES -->
            <iframe src="{embed_url}" allowfullscreen="true"
                sandbox="allow-same-origin allow-scripts allow-forms"
                onload="ocultarElementosPowerBI(this)">
            </iframe>

            <script>
                function ocultarElementosPowerBI(iframe) {{
                    try {{
                        let doc = iframe.contentWindow.document;
                        setTimeout(() => {{
                            // Intenta ocultar el logo y los botones si aparecen
                            const botones = doc.querySelectorAll('button, a, div');
                            botones.forEach(el => {{
                                if (el.innerText.includes('Microsoft') || el.innerText.includes('Power BI') || el.title?.includes('Compartir')) {{
                                    el.style.display = 'none';
                                }}
                            }});
                        }}, 3000);
                    }} catch (e) {{
                        console.warn("No se pudo modificar el contenido embebido (seguridad del iframe)");
                    }}
                }}
            </script>
        </body>
    </html>
    """


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ------------------- EJECUCIÓN APP -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0",port=port, debug=True)
