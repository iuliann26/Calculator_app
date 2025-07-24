
# Python calculator with web interface

An advanced mathematical calculator built with Python (Flask) and HTML/JavaScript, with reliable expression evaluation and a modern interface.


## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![](https://img.shields.io/badge/python-3.7+-blue.svg)](https://opensource.org/licenses/)
[![flask](https://img.shields.io/badge/flask-2.3.3-green.svg)](http://www.gnu.org/licenses/agpl-3.0)


### Backend Python
- Evaluare sigură: folosește AST parsing în loc de eval()
-  Funcții matematice complete: trigonometrice, logaritmice, etc.
-  Constante matematice: pi, e, tau
-  Istoric calcule: păstrează ultimele 10 calcule
-  Gestionare erori: mesaje de eroare clare și utile
-  REST API: endpoint-uri curate pentru toate operațiunile

### Frontend HTML/JavaScript
-  Design modern: interfață glassmorphism cu animații
-  Comunicare în timp real: AJAX cu backend-ul Python
-  Istoric vizual: afișează calculele anterioare
-  Suport tastatură: introducere completă de la tastatură
-  Responsive: funcționează pe desktop și mobil
-  Status conex


## Instalare

### Prerequisite
- Python 3.7 sau mai nou
- pip (Python package manager)

### Pașii de instalare
1. **Clonează sau descarcă proiectul**
```bash
git clone https://github.com/iuliann26/Calculator_app
cd calculator-python

```
2.**Instalează dependențele**
```bash 
pip install flask flask-cors
```
3.**Creează structura de directoare**

```calculator-python/
├── app.py
├── requirements.txt
└── templates/
    └── calculator.html
```
4.**Rulează aplicația**

```bash
python app.py
```
5.**Deschide in browser**
```
http://localhost:5000

```
**Usage**

*Interfața Web*

* Click pe butoane sau folosește tastatura

* Operatori: +, -, *, /, ^ (putere)

* Funcții: sin(), cos(), tan(), log(), sqrt()

* Constante: pi, e, tau

* Paranteze pentru expresii complexe


* Taste Rapide

* Enter = calculează

* Escape = șterge tot

* Backspace = șterge ultimul caracter

* 0-9 = cifre

* +, -, *, / = operatori 


Exemple Calcule

```python
2 + 3 * 4        # = 14
sin(pi/2)        # = 1.0
log(100)         # = 2.0
sqrt(16)         # = 4.0
2pi + 3e         # = 14.5495
```



## Tech Stack

**Backend:**

* Python 3.7+
* Flask 2.3.3
* AST parsing pentru securitate

**Frontend:**

* HTML5
* CSS3 (Glassmorphism)
* Vanilla JavaScript
* AJAX pentru comunicare

**Securitate:**

* Evaluare sigură fără eval()
* Validare input
* Protecție CORS