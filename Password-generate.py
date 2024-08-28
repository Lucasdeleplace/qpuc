import random
import string

def generate_password(num_letters, num_digits, num_specials, include_uppercase, include_lowercase):
    if not include_uppercase and not include_lowercase:
        raise ValueError("Vous devez inclure au moins les majuscules ou les minuscules.")
    
    letters = ''
    if include_uppercase:
        letters += string.ascii_uppercase
    if include_lowercase:
        letters += string.ascii_lowercase
    
    letters = ''.join(random.choices(letters, k=num_letters))
    digits = ''.join(random.choices(string.digits, k=num_digits))
    specials = ''.join(random.choices(string.punctuation, k=num_specials))
    
    password = letters + digits + specials
    
    password = ''.join(random.sample(password, len(password)))
    
    return password

num_letters = int(input("Entrez le nombre de lettres : "))
num_digits = int(input("Entrez le nombre de chiffres : "))
num_specials = int(input("Entrez le nombre de caractères spéciaux : "))
include_uppercase = input("Voulez-vous inclure des majuscules ? (oui/non) : ").strip().lower() == 'oui'
include_lowercase = input("Voulez-vous inclure des minuscules ? (oui/non) : ").strip().lower() == 'oui'

if not include_uppercase and not include_lowercase:
    print("Erreur : Vous devez inclure au moins les majuscules ou les minuscules.")
else:
    print(f"Mot de passe généré : {generate_password(num_letters, num_digits, num_specials, include_uppercase, include_lowercase)}")