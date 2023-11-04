import re
import tkinter as tk
from tkinter import messagebox

class AnalizadorSintactico:
    def __init__(self, entrada):
        self.entrada = entrada.strip()
        self.indice = 0
        self.error = None

        # Gramática con expresiones regulares para cada tipo de variable
        self.gramatica = {
            'var': r'var',
            'T': {
                'ent': r'\d+',
                'flot': r'\d+\.\d+',
                'booleano': r'(true|false)',
                'cadena': r'".*?"',
                'caracter': r"'.'"
            },
            'PC': r';',
            'I': r'='
        }
        self.tipo_actual = None

    def consumir_espacios(self):
        while self.indice < len(self.entrada) and self.entrada[self.indice].isspace():
            self.indice += 1

    def match(self, regex):
        self.consumir_espacios()
        match_obj = re.match(regex, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            return match_obj.group(0).strip()
        return None

    def expect(self, token):
        matched = self.match(self.gramatica[token])
        if not matched:
            self.error = f"Se esperaba '{token}'"
            return False
        return True

    def analizar(self):
        while self.indice < len(self.entrada):
            if not self.expect('var'):
                return False
            tipo = self.match(r'(ent|flot|booleano|cadena|caracter)')
            if tipo in self.gramatica['T']:
                self.tipo_actual = tipo
                var_name = self.match(r'[a-zA-Z_][a-zA-Z0-9_]*')
                if not var_name:
                    self.error = "Nombre de variable inválido"
                    return False
                if not self.expect('I'):
                    return False
                valor = self.match(self.gramatica['T'][self.tipo_actual])
                if not valor:
                    self.error = f"Valor inválido para el tipo {self.tipo_actual}"
                    return False
                if not self.expect('PC'):
                    return False
            else:
                self.error = "Tipo de variable inválido"
                return False
            self.consumir_espacios()  # Prepararse para la siguiente declaración
        return True

# Función que se llama cuando se presiona el botón de la GUI
def evaluar_cadena():
    cadena = entrada_texto.get("1.0", "end-1c")
    analizador = AnalizadorSintactico(cadena)
    if analizador.analizar():
        messagebox.showinfo("Resultado del análisis", 'La cadena es válida.')
    else:
        messagebox.showerror("Error encontrado", analizador.error or "Error desconocido.")

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Analizador de Declaraciones de Variables")

# Crear una caja de texto para la entrada de la cadena
entrada_texto = tk.Text(root, height=10, width=50)
entrada_texto.pack()

# Crear un botón para evaluar la cadena
boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

# Ejecutar el bucle principal de la GUI
root.mainloop()
