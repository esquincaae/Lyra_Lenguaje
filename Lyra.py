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
            'LA': r'\{',
            'LC': r'\}',
            'AV': r'\(',
            'CV': r'\)',
            'VL': r'(\d+\.\d+|\d+|true|false|".*?"|\'.?\')',
            'SC': r'Para',
            'AD': r'(\+\+|\-\-)',
            'RE': r'regresa',
            'OP': r'[\+\-\*/]',
            'CN': r'contenido',
            'EXP': r'[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;',
            'VRS': r'([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'NF': r'[a-zA-Z_]\w*',
            'O': r'(==|!=|<=|>=|<|>)',
            'ARGS': r'(\s*[a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'BODY': r'(\s*[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;)+',
            'FUNC': r'func\s+[a-zA-Z_]\w*\s*\(\s*([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?\)\s*\{[^\}]*\}',
        }
        self.gramatica.update({
            'IMPRIMIR': r'imprimir',
            'CONDICION': r'[a-zA-Z_]\w*\s*(==|!=|>=|<=|>|<)\s*\d+',
            'SI': r'si',
            'SINO': r'sino',
            'IMPRIMIR_LLAMADA': r'imprimir\s*\(\s*".*?"\s*\)\s*;',
            'ARGUMENTOS_IMPRIMIR': r'((\s*".*?"\s*|\s*[a-zA-Z_]\w*\s*)(,\s*".*?"\s*|\s*,\s*[a-zA-Z_]\w*\s*)*)',
        })
        self.tipos_de_datos = {
            'ent': r'^\d+$',
            'flot': r'\d+(\.\d+)?',
            'booleano': r'^(true|false)$',
            'cadena': r'^".*"$',
            'caracter': r"^'.'$",
        }

    # Métodos para consumir espacios y hacer match con patrones...
    def consumir_espacios(self):
        while self.indice < len(self.entrada) and self.entrada[self.indice].isspace():
            self.indice += 1

    def match(self, pattern):
        self.consumir_espacios()  # Consumir espacios antes de intentar hacer match
        match_obj = re.match(pattern, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            self.consumir_espacios()  # Consumir espacios después de hacer match
            return match_obj.group(0).strip()
        return None
    
    def match_imprimir(self):
        if not self.expect(self.gramatica['IMPRIMIR']):
            return False
        if not self.expect(r'\('):
            self.error = "Se esperaba '(' después de 'imprimir'"
            return False

        argumentos_str = self.entrada[self.indice:].split(')')[0]  
        argumentos = [arg.strip() for arg in argumentos_str.split(',')]  

        for argumento in argumentos:
            if not re.match(r'^".*"$', argumento):  
                if argumento not in self.nombres_declarados:  
                    self.error = f"La variable '{argumento}' no ha sido declarada."
                    return False
        self.indice += len(argumentos_str) + 1  

        if not self.expect(';'):
            self.error = "Se esperaba ';' al final de la instrucción de 'imprimir'"
            return False

        return True



    def expect(self, token_or_pattern):
        pattern = self.gramatica.get(token_or_pattern, token_or_pattern)
        self.consumir_espacios()  
        match_obj = re.match(pattern, self.entrada[self.indice:])
        if match_obj:
            self.indice += match_obj.end()
            self.consumir_espacios()  
            return True
        self.error = f"Se esperaba '{token_or_pattern}'"
        return False

    

    def analizar_ciclo(self):
            if self.match(self.gramatica['SC']):
                if self.expect('AV'):
                   
                    if self.expect('var'):
                        tipo = self.match(self.gramatica['T'])
                        if tipo and self.match(self.gramatica['NV']):
                            if self.expect('I') and self.match(self.gramatica['N']) and self.expect('PC'):
                                if self.match(self.gramatica['NV']) and self.match(self.gramatica['O']) and self.match(self.gramatica['N']) and self.expect('PC'):
                                    if self.match(self.gramatica['NV']) and self.match(self.gramatica['AD']):
                                        if self.expect('CV'):
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

    # Método para manejar la declaración de una función
    def SF(self):
            func_match = self.match(self.gramatica['FUNC'])
            if func_match:
                nombre_funcion_match = re.match(r'func\s+([a-zA-Z_]\w*)', func_match)
                if nombre_funcion_match:
                    nombre_funcion = nombre_funcion_match.group(1)
                    if nombre_funcion in self.nombres_declarados:
                        self.error = f"La función '{nombre_funcion}' ya ha sido declarada."
                        return False
                    if nombre_funcion == 'cuerpo':
                        if not re.search(r'func\s+cuerpo\s*\(\s*\)', func_match):
                            self.error = "La función 'cuerpo' no debe tener argumentos."
                            return False
                        if 'regresa' in func_match:
                            self.error = "La función 'cuerpo' no debe contener 'regresa'."
                            return False

                    self.nombres_declarados.add(nombre_funcion)
                    return True
                else:
                    self.error = "Nombre de función inválido o no proporcionado."
                    return False
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
                                self.consumir_espacios()  
                                if self.expect(';'):
                                    return True
                                else:
                                    self.error = "Se esperaba ';' al final de la declaración de la variable."
                                    return False
                            else:
                                self.error = f"Tipo de dato incorrecto para {tipo}: {valor}"
                                return False
                    else:
                        self.error = "Se esperaba '=' después del nombre de la variable."
                        return False
                else:
                    self.error = "Se esperaba el nombre de la variable después del tipo de dato."
                    return False
            else:
                self.error = "Se esperaba el tipo de dato después de 'var'."
                return False
        return False



    def SSCO(self):
            if self.match(self.gramatica['SI']):
                if not self.expect(r'\('):
                    self.error = "Se esperaba '(' después de 'si'"
                    return False
                condicion = self.match(self.gramatica['CONDICION'])
                if not condicion:
                    self.error = "Condición del 'si' no válida o no proporcionada."
                    return False
                if not self.expect(r'\)'):
                    self.error = "Se esperaba ')' después de la condición del 'si'"
                    return False
                if not self.expect(r'\{'):
                    self.error = "Se esperaba '{' para iniciar el bloque del 'si'"
                    return False

 
                if not self.match_imprimir():
                    return False 

                if not self.expect(r'\}'):
                    if not self.error: 
                        self.error = "Se esperaba '}' para cerrar el bloque del 'si'"
                    return False

               
                if self.match(self.gramatica['SINO']):
                    if not self.expect(r'\{'):
                        self.error = "Se esperaba '{' para iniciar el bloque del 'sino'"
                        return False

                 
                    if not self.match_imprimir():
                        return False  

                    if not self.expect(r'\}'):
                        if not self.error:
                            self.error = "Se esperaba '}' para cerrar el bloque del 'sino'"
                        return False

                return True
            return False




    def analizar(self):
            # Aquí se inicia el análisis de la cadena
            while self.indice < len(self.entrada) and not self.error:
                self.consumir_espacios()
                if self.entrada[self.indice:].startswith('var '):
                    if not self.SV():
                        return False
                elif self.entrada[self.indice:].startswith('func '):
                    if not self.SF():
                        return False
                elif self.entrada[self.indice:].startswith(self.gramatica['SI']):
                    if not self.SSCO():
                        return False
                elif self.entrada[self.indice:].startswith(self.gramatica['SC']):
                    if not self.analizar_ciclo():
                        return False
                else:
                    if self.error:
                        return False
                    self.error = "Se esperaba una declaración de variable, definición de función, un condicional 'si' o un ciclo con 'Para'"
                    return False
                self.consumir_espacios()
            return not self.error

# Función que se llama cuando se presiona el botón de la GUI
def evaluar_cadena():
    cadena = entrada_texto.get("1.0", "end-1c")
    analizador = AnalizadorSintactico(cadena)
    if analizador.analizar():
        messagebox.showinfo("Resultado del análisis", 'La cadena es válida.')
    else:
        messagebox.showerror("Error encontrado", analizador.error or "Error desconocido.")

root = tk.Tk()
root.title("Lyra: Analizador Sintáctico")

entrada_texto = tk.Text(root, height=15, width=60)
entrada_texto.pack()

boton_evaluar = tk.Button(root, text="Evaluar cadena", command=evaluar_cadena)
boton_evaluar.pack()

root.mainloop()