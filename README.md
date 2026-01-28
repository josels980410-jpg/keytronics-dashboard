# Para crear un entonrno virtual 
python -m venv venv - Crear entorno virtual

# para iniciar el entorno virtual 
C:\Entornos_Virtuales\venv_keytronics\Scripts\Activate.ps1

# Cambio de repositorio
# 1.- Eliminar la credencial de windows 
    Primero, obligamos al sistema a olvidar la contraseña o token que guardamos.
           1.- Presiona la tecla Windows y escribe: Administrador de credenciales.
           2.- Entra en Credenciales de Windows.
           3.- Busca en la lista "Credenciales genéricas" cualquier entrada que diga git:https://github.com o github.com.
           4.- Despliégala y dale clic en Quitar.
# 2.- Desvincular la cuenta en VS Code 
    Para que VS Code no intente usar la sesión de Keytronics que quedó abierta:
           1.-Haz clic en el ícono de la personita (abajo a la izquierda en la barra de actividad).
           2.- Si aparece la cuenta de (keytronics.soporte@gmail.com o josels980410@gmail.com), dale clic y selecciona Sign Out
# 3.- Configurar el nuevo repositorio
    Ahora, abre la carpeta de tu otro proyecto en VS Code y haz lo siguiente en la terminal:
    * Cambia el destino:
           git remote set-url origin https://github.com/josels980410-jpg/keytronics-dashboard.git
           git remote set-url origin https://github.com/      .git

    * Configura tu nombre personal
          git config user.name "Jose Luna"
          git config user.email "josels980410@gmail.com"

          git config user.email "keytronics.soporte@gmail.com"
          git config user.name "Keytronics Soporte"

    * Confirmamos correo y nombre 
         git config user.email
         git config user.name



# Para actualizar el repositorio

1.-    git add .
2.-    git commit -m "Actualización reporte en excel"
3.-    git push origin master

# Desactivar el entorno virtual
deactivate

# Para verificar versiones de Python y de pip 
python --version
pip --version

# reinicia VSCode internamente y vuelve a cargar el intérprete seleccionado.

Presiona Ctrl + Shift + P → escribe Reload Window → Enter.

# URL

https://keytronics-dashboard.onrender.com/

Usuario:  Jose_Consultor
Contraseña:  654321987

# Hoja sheet
Keytronics_Prueba_Sheets
https://docs.google.com/spreadsheets/d/14x3JapIuLdgclmk4_ls3NCMWZVJF5fjNhyIGI6G86dE/edit?gid=0#gid=0

# Seleccionar un interprete
En VSCode, presiona:
Ctrl + Shift + P
(o F1)

Escribe:
Python: Select Interpreter

Te saldrá una lista de intérpretes.
Debes elegir uno que se vea más o menos así:

✔ ./venv/Scripts/python.exe (en Windows)






# Correo de la gmail de la memora 
keytronics.soporte@gmail.com
Password1$

# Posible Power BI 
BusinessKey@Keytronics.onmicrosoft.com
Password1$