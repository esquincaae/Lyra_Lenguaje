import re
import tkinter as tk
from tkinter import messagebox

class AnalizadorSintactico:
    def __init__(self, entrada):
        self.entrada = entrada.strip()
        self.indice = 0
        self.error = None
        self.nombres_declarados = set()
        self.tipos_de_datos = {
            'ent': r'^\d+$',
            'flot': r'^\d+\.\d+$',
            'booleano': r'^(true|false)$',
            'cadena': r'^".*"$',
            'caracter': r"^'.'$",
        }

        self.gramatica = {
            'var': r'var',
            'func': r'func',
            'T': r'(ent|flot|booleano|cadena|caracter)',
            'NV': r'[a-zA-Z][a-zA-Z0-9]*',  # Nombres de variables o funciones
            'VL': r'(\d+|\d+\.\d+|true|false|".*?"|\'.?\')',  # Valores literales
            'PC': r';',
            'I': r'=',
            'C': r',',
            'LA': r'\{',
            'LC': r'\}',
            'AV': r'\(',
            'CV': r'\)',
            'RE': r'regresa',
            'OP': r'[\+\-\*/]',
            'EXP': r'[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;',
            'VRS': r'([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'NF': r'[a-zA-Z_]\w*',
            'ARGS': r'(\s*[a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'BODY': r'(\s*[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;)+',
            'FUNC': r'func\s+[a-zA-Z_]\w*\s*\(\s*([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?\)\s*\{[^\}]*\}',
        }

    # Métodos para consumir espacios y hacer match con patrones...
    def consumir_espacios(self):
        while self.indice < len(self.entrada) and self.entrada[self.indice].isspace():
            self.indice += 1

    def match(self, pattern):
        self.consumir_espacios()
        match_obj = re.match(pattern, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            return match_obj.group(0).strip()
        return None

    def expect(self, pattern):
        matched = self.match(pattern)
        if not matched:
            self.error = f"Se esperaba el patrón {pattern}"
            return False
        return True

    # Método para manejar la declaración de una función
    def SF(self):
        # Verifica si hay una definición de función y procesa si la hay
        if self.match(self.gramatica['FUNC']):
            # Aquí podrías extender la lógica para manejar el contenido de la función en detalle
            return True
        return False

    # Método para manejar la declaración de una variable
    def SV(self):
        if self.expect('var'):
            tipo = self.match(self.gramatica['T'])
            if tipo:
                var_name = self.match(self.gramatica['NV'])
                if var_name:
                    if var_name in self.nombres_declarados:
                        self.error = f"La variable '{var_name}' ya ha sido declarada."
                        return False
                    self.nombres_declarados.add(var_name)
                    if self.expect('='):
                        valor = self.match(self.gramatica['VL'])
                        if valor:
                            patron = self.tipos_de_datos[tipo]
                            if re.match(patron, valor):
                                return self.expect(';')
                            else:
                                self.error = f"Tipo de dato incorrecto para {tipo}: {valor}"
                                return False
        return False

    # Método para realizar el análisis completo
    def analizar(self):
        while self.indice < len(self.entrada):
            self.consumir_espacios()
            if self.entrada[self.indice:].startswith('var '):
                if not self.SV():
                    return False
            elif self.entrada[self.indice:].startswith('func '):
                if not self.SF():
                    return False
            else:
                if self.error:  # Si se encontró un error, detener el análisis
                    return False
                self.error = "Se esperaba una declaración de variable o definición de función"
                return False
            self.consumir_espacios()
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
root.title("Analizador de Gramática")

entrada_texto = tk.Text(root, height=15, width=60)
entrada_texto.pack()

boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

root.mainloop()
