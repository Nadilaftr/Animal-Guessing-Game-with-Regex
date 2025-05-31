from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import random
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Load the dataset
try:
    with open("kata-kata.txt", "r", encoding="utf-8") as file:
        words = [line.strip().lower() for line in file if line.strip()]
        print(f"Dataset loaded successfully with {len(words)} words.")
except FileNotFoundError:
    print("Error: Dataset file not found!")
    words = []

@app.route('/')
def intro():
    return render_template('intro.html')

@app.route('/list')
def list_page():
    return render_template('list.html')

@app.route('/index')
@app.route('/index')
def index():
    if 'points' not in session:
        session['points'] = 0
    if 'lives' not in session:
        session['lives'] = 3
    if 'game_over' not in session:
        session['game_over'] = False

    new_word()  # Set kata baru

    return render_template('index.html', 
                        word_masked=mask_word(session['word']), 
                        lives=session['lives'], 
                        points=session['points'], 
                        hint=session['hint'])


def new_word():
    """Reset soal dengan kata baru dan reset lives ke 3"""
    session['word'] = random.choice(words)
    session['lives'] = 3  # Reset lives setiap soal baru
    session['hint'] = generate_hint(session['word'])
    print(f"New word set: {session['word']} (Lives reset to 3)")

def generate_hint(word):
    hint = "^"
    for letter in word:
        choice = random.choice([0, 1, 2])
        if choice == 0:
            hint += letter  
        elif choice == 1:
            hint += "."  
        else:
            hint += f"[{letter}{chr(random.randint(97, 122))}]"  
    hint += "$"
    return hint

def mask_word(word):
    return "_" * len(word)

@app.route('/guess', methods=['POST'])
def guess():
    if session.get('game_over', False):
        return jsonify({
            "message": "Oops! 😭 You got them all wrong... <div>Try again next time! ✨<div>",
            "lives": session['lives'],
            "points": session['points'],
            "game_over": True,
            "correct_word": session['word']
        })

    regex_pattern = request.form.get('pattern', '').lower()
    print(f"User guessed with pattern: {regex_pattern}")

    if not regex_pattern:
        return jsonify({"error": "No pattern provided."})

    try:
        regex = re.compile(regex_pattern)
    except re.error as e:
        return jsonify({"error": f"Invalid regex pattern: {str(e)}"})

    if regex.fullmatch(session['word']):
        session['points'] += 1
        new_word()  # Reset soal + lives kembali 3
        response = {
            "message": "🎉 Incredible! You got it right! 🎉",
            "points": session['points'],
            "word_masked": mask_word(session['word']),
            "lives": session['lives'],  
            "hint": session['hint']
        }
        print(f"Correct answer! Moving to next word: {session['word']}")
    else:
        session['lives'] -= 1
        response = {
            "message": "Ooops! Still wrong ❌ Give it another shot! 🚀",
            "lives": session['lives'],
            "points": session['points'],
            "hint": session['hint'],
            "correct_word": session['word']
        }
        print(f"Incorrect guess. Lives remaining: {session['lives']}")

        if session['lives'] <= 0:
            session['game_over'] = True
            response["message"] = "You lose, try again!"
            response["game_over"] = True

    return jsonify(response)

@app.route('/restart', methods=['POST'])
def restart():
    session['points'] = 0
    session['game_over'] = False
    new_word()  # Reset ke soal pertama dan lives 3
    print(f"Game restarted with new word: {session['word']}")

    return jsonify({
        "word_masked": mask_word(session['word']),
        "lives": session['lives'],
        "points": session['points'],
        "hint": session['hint']
    })

if __name__ == "__main__":
    app.run(debug=True)
