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
            'SC': r'Para',
            'RE': r'regresa',
            'OP': r'[\+\-\*/]',
            'EXP': r'[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;',
            'VRS': r'([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'NF': r'[a-zA-Z_]\w*',
            'ARGS': r'(\s*[a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?',
            'BODY': r'(\s*[a-zA-Z_]\w*\s*(\+\+|\-\-|\=[a-zA-Z_]\w*(\s*[\+\-\*/]\s*[a-zA-Z_]\w*)?)\s*;)+',
            'FUNC': r'func\s+[a-zA-Z_]\w*\s*\(\s*([a-zA-Z_]\w*\s*(,\s*[a-zA-Z_]\w*\s*)*)?\)\s*\{[^\}]*\}',
        }
        self.gramatica.update({
            'IMPRIMIR': r'imprimir',
            'CONDICION': r'[a-zA-Z_]\w*\s*(==|!=|>=|<=|>|<)\s*\d+',
            'SI': r'si',
            'SINO': r'sino',
            'IMPRIMIR_LLAMADA': r'imprimir\s*\(\s*".*?"\s*\)\s*;'
        })

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
    
    def match_imprimir(self):
        if not self.expect(self.gramatica['IMPRIMIR']):
            return False
        if not self.expect(r'\('):
            self.error = "Se esperaba '(' después de 'imprimir'"
            return False
        # Asegúrate de que la cadena esté bien formada
        cadena_imprimir = self.match(r'".*?"|\'.*?\'')
        if not cadena_imprimir:
            self.error = "Se esperaba una cadena entre comillas para 'imprimir'"
            return False
        # Verifica si la cadena está cerrada correctamente
        if cadena_imprimir.count('"') % 2 != 0 or cadena_imprimir.count("'") % 2 != 0:
            self.error = "La cadena de 'imprimir' no está cerrada correctamente"
            return False
        if not self.expect(r'\)'):
            self.error = "Se esperaba ')' después de la cadena de 'imprimir'"
            return False
        if not self.expect(';'):
            self.error = "Se esperaba ';' al final de la instrucción de 'imprimir'"
            return False
        return True

def expect(self, token_or_pattern):
    # Intentar obtener el patrón del diccionario de gramática usando token_or_pattern como clave
    pattern = self.gramatica.get(token_or_pattern, token_or_pattern)
    self.consumir_espacios()
    # Intentar hacer match con el patrón
    match_obj = re.match(pattern, self.entrada[self.indice:])
    if match_obj:
        self.indice += match_obj.end()
        return True
    # Si el match falla, configurar el mensaje de error
    self.error = f"Se esperaba '{token_or_pattern}'"
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

# Método para manejar la declaración de una función
def SF(self):
        # Verifica si hay una definición de función y procesa si la hay
        func_match = self.match(self.gramatica['FUNC'])
        if func_match:
            # Extraer el nombre de la función utilizando una expresión regular
            nombre_funcion_match = re.match(r'func\s+([a-zA-Z_]\w*)', func_match)
            if nombre_funcion_match:
                nombre_funcion = nombre_funcion_match.group(1)
                if nombre_funcion in self.nombres_declarados:
                    self.error = f"La función '{nombre_funcion}' ya ha sido declarada."
                    return False
                
                # Verificar si la función se llama 'cuerpo' y manejar las restricciones
                if nombre_funcion == 'cuerpo':
                    # Verificar que no haya argumentos y no se use 'regresa'
                    if not re.search(r'func\s+cuerpo\s*\(\s*\)', func_match):
                        self.error = "La función 'cuerpo' no debe tener argumentos."
                        return False
                    if 'regresa' in func_match:
                        self.error = "La función 'cuerpo' no debe contener 'regresa'."
                        return False

                self.nombres_declarados.add(nombre_funcion)
                # Aquí iría la lógica para analizar el resto de la definición de la función
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
                                return self.expect(';')
                            else:
                                self.error = f"Tipo de dato incorrecto para {tipo}: {valor}"
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

            # Verifica el contenido dentro del bloque 'si'
            if not self.match_imprimir():
                return False  # El error ya está configurado en match_imprimir

            if not self.expect(r'\}'):
                if not self.error:  # Si no se ha configurado un error previo
                    self.error = "Se esperaba '}' para cerrar el bloque del 'si'"
                return False

            # Opcionalmente manejar 'sino'
            if self.match(self.gramatica['SINO']):
                if not self.expect(r'\{'):
                    self.error = "Se esperaba '{' para iniciar el bloque del 'sino'"
                    return False

                # Verifica el contenido dentro del bloque 'sino'
                if not self.match_imprimir():
                    return False  # El error ya está configurado en match_imprimir

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