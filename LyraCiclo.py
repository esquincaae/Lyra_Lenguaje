import re
import tkinter as tk
from tkinter import messagebox

class AnalizadorSintactico:
    def __init__(self, entrada):
        self.entrada = entrada.strip()
        self.indice = 0
        self.error = None
        self.nombres_declarados = set()  # Para evitar nombres duplicados
        self.gramatica = {
            'LM': r'[a-z]',
            'L': r'[a-zA-Z]',
            'N': r'\d+',
            'T': r'(ent|flot|booleano|cadena|caracter)',
            'NV': r'[a-z][a-zA-Z]*\d*',
            'PC': r';',
            'I': r'=',
            'AV': r'\(',
            'CV': r'\)',
            'LA': r'\{',
            'LC': r'\}',
            'SC': r'Para',
            'O': r'(==|>=|<=|!=|>|<)',
            'AD': r'(\+\+|\-\-)',
            'R': r'LA CN LC',
            'CN': r'contenido',  # Aquí se simplifica el contenido
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
    # ... (otros métodos)

    def expect(self, token):
        pattern = self.gramatica.get(token, token)
        self.consumir_espacios()
        match_obj = re.match(pattern, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            return True
        self.error = f"Se esperaba '{token}'"
        return False


    def analizar_ciclo(self):
        if self.match(self.gramatica['SC']):
            if self.expect('AV'):
                # Analizar inicialización de variable dentro del ciclo
                if self.expect('var'):
                    tipo = self.match(self.gramatica['T'])
                    if tipo and self.match(self.gramatica['NV']):
                        if self.expect('I') and self.match(self.gramatica['N']) and self.expect('PC'):
                            # Analizar condición del ciclo
                            if self.match(self.gramatica['NV']) and self.match(self.gramatica['O']) and self.match(self.gramatica['N']) and self.expect('PC'):
                                # Analizar actualización de la variable del ciclo
                                if self.match(self.gramatica['NV']) and self.match(self.gramatica['AD']):
                                    if self.expect('CV'):
                                        # Asegurar que el cuerpo del ciclo esté presente
                                        if self.expect('LA') and self.match(self.gramatica['CN']) and self.expect('LC'):
                                            return True
                                        else:
                                            self.error = "Error en el cuerpo del ciclo."
                                    else:
                                        self.error = "Se esperaba ')'"
                                else:
                                    self.error = "Error en la actualización del ciclo."
                            else:
                                self.error = "Error en la condición del ciclo."
                        else:
                            self.error = "Error en la inicialización del ciclo."
                else:
                    self.error = "Se esperaba la palabra clave 'var' después de 'Para'"
            else:
                self.error = "Se esperaba '(' después de 'Para'"
        return False

    def analizar(self):
        while self.indice < len(self.entrada) and not self.error:
            self.consumir_espacios()
            if self.entrada[self.indice:].startswith(self.gramatica['SC']):
                if not self.analizar_ciclo():
                    return False
            else:
                self.error = "Se esperaba una declaración de ciclo con 'Para'"
                return False
            self.consumir_espacios()
        return not self.error


# Función que se llama cuando se presiona el botón de la GUI
def evaluar_cadena():
    cadena = entrada_texto.get("1.0", "end-1c")
    analizador = AnalizadorSintactico(cadena)
    if analizador.analizar_ciclo():
        messagebox.showinfo("Resultado del análisis", 'La cadena es válida')
    else:
        messagebox.showerror("Error encontrado", analizador.error or "Error desconocido.")

# Configuración de la ventana principal de Tkinter
root = tk.Tk()
root.title("Analizador Sintáctico de Ciclos")

entrada_texto = tk.Text(root, height=15, width=60)
entrada_texto.pack()

boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

root.mainloop()