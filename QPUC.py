import requests
import random
from googletrans import Translator
import html
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Fonction pour démarrer le quiz
def start_quiz():
    try:
        num_questions = int(num_questions_entry.get())
        if num_questions <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Erreur", "Veuillez entrer un nombre valide de questions.")
        return

    # URL de l'API pour récupérer des questions de quiz
    url = f"https://opentdb.com/api.php?amount={num_questions}&type=multiple&regions=FR"

    # Faire une requête GET à l'API
    response = requests.get(url)

    # Vérifier si la requête a réussi
    if response.status_code == 200:
        try:
            global data
            data = response.json()
        except ValueError:
            print("Erreur : La réponse de l'API n'est pas au format JSON.")
            data = []
    else:
        print(f"Erreur : La requête a échoué avec le statut {response.status_code}.")
        data = []

    # Masquer l'écran de sélection et afficher le quiz
    selection_frame.pack_forget()
    quiz_frame.pack(pady=20)
    next_question()

# Fonction pour afficher la question suivante
def next_question():
    global current_question
    if current_question < len(data['results']):
        question_data = data['results'][current_question]
        question = html.unescape(question_data['question'])
        question = translator.translate(question, dest='fr').text
        correct_answer = html.unescape(question_data['correct_answer'])
        correct_answer = translator.translate(correct_answer, dest='fr').text
        incorrect_answers = [html.unescape(ans) for ans in question_data['incorrect_answers']]
        incorrect_answers = [translator.translate(ans, dest='fr').text for ans in incorrect_answers]
        options = incorrect_answers + [correct_answer]
        random.shuffle(options)
        
        question_label.config(text=question)
        for i, option in enumerate(options):
            option_buttons[i].config(text=option, state=tk.NORMAL, command=lambda opt=option: check_answer(opt, correct_answer))
        result_label.config(text="")
        next_button.config(state=tk.DISABLED)
    else:
        messagebox.showinfo("Quiz Terminé", f"Votre score final est : {score}/{len(data['results'])}")
        root.quit()

# Fonction pour vérifier la réponse
def check_answer(selected_option, correct_answer):
    global score, current_question
    if selected_option == correct_answer:
        result_label.config(text="Bonne réponse !", fg="#4CAF50")
        score += 1
    else:
        result_label.config(text=f"Mauvaise réponse. La bonne réponse était : {correct_answer}", fg="#F44336")
    current_question += 1
    for btn in option_buttons:
        btn.config(state=tk.DISABLED)
    next_button.config(state=tk.NORMAL)

# Initialisation du traducteur
translator = Translator()

# Initialisation du score
score = 0
current_question = 0

# Création de l'interface graphique
root = tk.Tk()
root.title("Quiz de Culture Générale")
root.geometry("600x400")
root.config(bg="#2C3E50")

# Cadre de sélection du nombre de questions
selection_frame = tk.Frame(root, bg="#2C3E50")
selection_frame.pack(pady=20)

num_questions_label = tk.Label(selection_frame, text="Nombre de questions :", font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1")
num_questions_label.pack(pady=10)

num_questions_entry = tk.Entry(selection_frame, font=("Helvetica", 14))
num_questions_entry.pack(pady=10)

start_button = ttk.Button(selection_frame, text="Démarrer le Quiz", command=start_quiz)
start_button.pack(pady=20)

# Cadre du quiz
quiz_frame = tk.Frame(root, bg="#2C3E50")

# Cadre pour la question
question_frame = tk.Frame(quiz_frame, bg="#2C3E50")
question_frame.pack(pady=20)

question_label = tk.Label(question_frame, text="", wraplength=500, justify="left", font=("Helvetica", 16, "bold"), bg="#2C3E50", fg="#ECF0F1")
question_label.pack()

# Cadre pour les options
options_frame = tk.Frame(quiz_frame, bg="#2C3E50")
options_frame.pack(pady=20)

option_buttons = []
for _ in range(4):
    btn = ttk.Button(options_frame, text="", style="TButton")
    btn.pack(pady=5)
    option_buttons.append(btn)

# Label pour afficher le résultat
result_label = tk.Label(quiz_frame, text="", wraplength=500, justify="left", font=("Helvetica", 14), bg="#2C3E50", fg="#ECF0F1")
result_label.pack(pady=20)

# Bouton pour passer à la question suivante
next_button = ttk.Button(quiz_frame, text="Question Suivante", state=tk.DISABLED, command=next_question, style="TButton")
next_button.pack(pady=20)

root.mainloop()