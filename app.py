from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import math
import ast
import operator
import re

app = Flask(__name__)
CORS(app)  # activeaza CORS pentru toate rutele

class CalculatorPython:
    """un evaluator sigur de expresii python pentru operatiuni de calculator"""
    
    # operatori permisi
    operatori = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }
    
    # functii permise
    functii = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'sinh': math.sinh,
        'cosh': math.cosh,
        'tanh': math.tanh,
        'log': math.log10,
        'ln': math.log,
        'log2': math.log2,
        'sqrt': math.sqrt,
        'abs': abs,
        'ceil': math.ceil,
        'floor': math.floor,
        'round': round,
        'exp': math.exp,
        'factorial': math.factorial,
        'degrees': math.degrees,
        'radians': math.radians,
    }
    
    # constante
    constante = {
        'pi': math.pi,
        'e': math.e,
        'tau': math.tau,
    }
    
    def __init__(self):
        self.istoric = []
    
    def evaluare_sigura(self, nod, variabile=None):
        """evalueaza in siguranta un nod AST"""
        if variabile is None:
            variabile = {}
            
        if isinstance(nod, ast.Constant):  # python 3.8+
            return nod.value
        elif isinstance(nod, ast.Num):  # python < 3.8
            return nod.n
        elif isinstance(nod, ast.Name):
            if nod.id in self.constante:
                return self.constante[nod.id]
            elif nod.id in variabile:
                return variabile[nod.id]
            else:
                raise ValueError(f"variabila necunoscuta: {nod.id}")
        elif isinstance(nod, ast.BinOp):
            stanga = self.evaluare_sigura(nod.left, variabile)
            dreapta = self.evaluare_sigura(nod.right, variabile)
            if type(nod.op) in self.operatori:
                return self.operatori[type(nod.op)](stanga, dreapta)
            else:
                raise ValueError(f"operator nesuportat: {type(nod.op)}")
        elif isinstance(nod, ast.UnaryOp):
            operand = self.evaluare_sigura(nod.operand, variabile)
            if type(nod.op) in self.operatori:
                return self.operatori[type(nod.op)](operand)
            else:
                raise ValueError(f"operator unar nesuportat: {type(nod.op)}")
        elif isinstance(nod, ast.Call):
            if isinstance(nod.func, ast.Name) and nod.func.id in self.functii:
                functie = self.functii[nod.func.id]
                argumente = [self.evaluare_sigura(arg, variabile) for arg in nod.args]
                return functie(*argumente)
            else:
                raise ValueError(f"functie necunoscuta: {nod.func.id if isinstance(nod.func, ast.Name) else 'invalid'}")
        else:
            raise ValueError(f"nod AST nesuportat: {type(nod)}")
    
    def proceseaza_expresie(self, expresie):
        """proceseaza expresia pentru a gestiona cazuri speciale"""
        # elimina spatiile
        expresie = expresie.replace(' ', '')
        
        # inlocuieste simbolurile comune
        expresie = expresie.replace('×', '*')
        expresie = expresie.replace('÷', '/')
        expresie = expresie.replace('^', '**')
        
        # gestioneaza inmultirea implicita (ex: 2pi -> 2*pi, 2(3+4) -> 2*(3+4))
        expresie = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expresie)
        expresie = re.sub(r'(\d)(\()', r'\1*\2', expresie)
        expresie = re.sub(r'(\))(\d)', r'\1*\2', expresie)
        expresie = re.sub(r'(\))(\()', r'\1*\2', expresie)
        
        return expresie
    
    def calculeaza(self, expresie):
        """calculeaza rezultatul unei expresii matematice"""
        try:
            # proceseaza expresia
            expresie_procesata = self.proceseaza_expresie(expresie)
            
            # parseaza expresia intr-un AST
            arbore = ast.parse(expresie_procesata, mode='eval')
            
            # evalueaza AST-ul in siguranta
            rezultat = self.evaluare_sigura(arbore.body)
            
            # gestioneaza cazuri speciale
            if isinstance(rezultat, complex):
                if rezultat.imag == 0:
                    rezultat = rezultat.real
                else:
                    rezultat = f"{rezultat.real}+{rezultat.imag}j"
            
            # rotunjeste pentru a preveni erorile de virgula mobila
            if isinstance(rezultat, float):
                if abs(rezultat) < 1e-10:  # numere foarte mici
                    rezultat = 0
                else:
                    rezultat = round(rezultat, 12)
            
            # adauga la istoric
            self.istoric.append({
                'expresie': expresie,
                'rezultat': str(rezultat)
            })
            
            # pastreaza doar ultimele 10 calcule
            if len(self.istoric) > 10:
                self.istoric = self.istoric[-10:]
            
            return {
                'succes': True,
                'rezultat': str(rezultat),
                'expresie': expresie
            }
            
        except ZeroDivisionError:
            return {
                'succes': False,
                'eroare': 'impartire la zero'
            }
        except ValueError as e:
            return {
                'succes': False,
                'eroare': str(e)
            }
        except Exception as e:
            return {
                'succes': False,
                'eroare': f'expresie invalida: {str(e)}'
            }
    
    def obtine_istoric(self):
        """obtine istoricul calculelor"""
        return self.istoric

# instanta globala a calculatorului
calculator = CalculatorPython()

@app.route('/')
def index():
    """serveste pagina principala a calculatorului"""
    return render_template('calculator.html')

@app.route('/calculeaza', methods=['POST'])
def calculeaza():
    """endpoint pentru calcul"""
    date = request.get_json()
    expresie = date.get('expresie', '')
    
    if not expresie:
        return jsonify({
            'succes': False,
            'eroare': 'nu s-a furnizat nicio expresie'
        })
    
    rezultat = calculator.calculeaza(expresie)
    return jsonify(rezultat)

@app.route('/istoric', methods=['GET'])
def obtine_istoric():
    """obtine istoricul calculelor"""
    return jsonify({
        'succes': True,
        'istoric': calculator.obtine_istoric()
    })

@app.route('/sterge_istoric', methods=['POST'])
def sterge_istoric():
    """sterge istoricul calculelor"""
    calculator.istoric = []
    return jsonify({
        'succes': True,
        'mesaj': 'istoric sters'
    })

@app.route('/functii', methods=['GET'])
def obtine_functii():
    """obtine functiile si constantele disponibile"""
    return jsonify({
        'succes': True,
        'functii': list(calculator.functii.keys()),
        'constante': list(calculator.constante.keys())
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)