# Terra Lab

## Description

...

## Installation

### Prérequis
Assurez-vous que **Python 3.9** est installé sur votre système.  
Vous pouvez télécharger Python 3.9 depuis le site officiel :  
[Python 3.9.0 - Python.org](https://www.python.org/downloads/release/python-390/)  

### Configuration de Python 3.9 sous Git Bash
1. Ouvrez le fichier `~/.bashrc` :
   ```bash
   nano ~/.bashrc
   ```

2. Ajoutez l'alias suivant dans le fichier :
   ```bash
   alias python3.9='/c/Users/james/AppData/Local/Programs/Python/Python39/python.exe'
   ```

3. Rechargez la configuration du shell :
   ```bash
   source ~/.bashrc
   ```

### Étapes d'installation
1. Clonez le projet :
   ```bash
   git clone <repository-url>
   cd terra_lab
   ```

2. Installez le package et ses dépendances avec **Python 3.9** :
   ```bash
   python3.9 -m pip install -e .
   ```

3. Vérifiez que les modules sont bien installés :
   ```bash
   python3.9 -m pip list
   ```

---

## Usage

### Lancer le projet
Exécutez le package en utilisant **Python 3.9** :

```bash
python3.9 -m terra_lab
```

---

## Environnement Virtuel (Recommandé)

Pour éviter tout conflit avec d'autres versions de Python, vous pouvez utiliser un environnement virtuel :

1. Créez un environnement virtuel basé sur **Python 3.9** :
   ```bash
   python3.9 -m venv venv
   ```

2. Activez l'environnement :
   - **Linux/macOS** :
     ```bash
     source venv/bin/activate
     ```
   - **Windows** :
     ```bash
     venv\Scripts\activate
     ```

3. Installez le package dans l'environnement :
   ```bash
   python -m pip install -e .
   ```

4. Lancez le projet :
   ```bash
   python -m terra_lab
   ```

---

## Vérification

Pour vérifier que vous utilisez bien **Python 3.9** dans le projet, exécutez la commande suivante :
```bash
python3.9 -c "import sys; print(sys.version)"
```

...
