import re
import tkinter as tk
from tkinter import messagebox
#la cadena de prueba para la declaracion de variables es...    var ent miVariable = 10;
class AnalizadorSintactico:
    def __init__(self, entrada):
        self.entrada = entrada
        # Gramática definida como un diccionario
        self.gramatica = {
            'LM': r'[a-z]',
            'L': r'[a-zA-Z]*',
            'N': r'\d+',
            'I': r'=',
            'PC': r';',
            'P': r'\.',
            'T': r'(ent|flot|booleano|cadena|caracter)',
            'NV': r'[a-z][a-zA-Z]*',
            'VL': r'(\d+(\.\d+)?|“[a-zA-Z]*“)',
            'SV': r'var\s+{T}\s+{NV}\s*{I}\s*{VL}\s*{PC}',
        }

    def analizar(self):
        sv_patron = self.gramatica['SV'].format(
            T=self.gramatica['T'],
            NV=self.gramatica['NV'],
            I=self.gramatica['I'],
            VL=self.gramatica['VL'],
            PC=self.gramatica['PC']
        )
        return bool(re.fullmatch(sv_patron, self.entrada))

# Función que se llama cuando se presiona el botón de la GUI
def evaluar_cadena():
    cadena = entrada_texto.get("1.0", "end-1c")
    analizador = AnalizadorSintactico(cadena)
    es_valida = analizador.analizar()
    mensaje = 'Válida' if es_valida else 'Inválida'
    messagebox.showinfo("Resultado del análisis", f'La cadena es {mensaje}')

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Analizador de Gramática de Declaración de Variables")

# Crear una caja de texto para la entrada de la cadena
entrada_texto = tk.Text(root, height=10, width=50)
entrada_texto.pack()

# Crear un botón para evaluar la cadena
boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

# Ejecutar el bucle principal de la GUI
root.mainloop()
