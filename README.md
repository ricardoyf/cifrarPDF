# cifrarPDF

Aplicación sencilla para Windows que cifra archivos PDF localmente con contraseña usando AES-256.

## Uso

- Arrastra un PDF a la ventana o selecciónalo.
- Introduce la contraseña dos veces.
- Pulsa **Cifrar PDF**.
- El programa propone guardar el resultado como `nombre_cifrado.pdf`.

## Ejecutar desde Python

```powershell
pip install -r requirements.txt
python pdf_cifrador.py
```

Esta versión usa `pikepdf`, por lo que no necesita `qpdf.exe` instalado ni añadido al PATH.

## Compilar para Windows

El workflow de GitHub Actions incluido genera `PDF_Cifrador.exe` mediante PyInstaller.
