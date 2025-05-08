import pyperclip
import os
from datetime import datetime  # Importer le module datetime

# Définir les codes de couleur ANSI pour le vert et la réinitialisation
GREEN = '\033[92m'
RESET = '\033[0m'

def main():
    # Récupérer le contenu du presse-papier
    clipboard_content = pyperclip.paste()
    
    # Diviser les chemins de fichiers en lignes
    file_paths = clipboard_content.strip().split('\n')
    
    # Listes pour stocker les informations
    successful_files = []
    error_files = []
    
    total_lines = 0
    total_chars = 0
    
    # Première passe : traiter les fichiers et collecter les informations
    for filepath in file_paths:
        filepath = filepath.strip()
        if not filepath:
            continue  # Ignorer les lignes vides
        
        if os.path.isfile(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as file:
                    content = file.read().strip()
                    filename = os.path.basename(filepath)
                    num_lines = content.count('\n') + 1 if content else 0
                    num_chars = len(content)
                    
                    # Mettre à jour les totaux
                    total_lines += num_lines
                    total_chars += num_chars
                    
                    # Enregistrer les informations pour le résultat et la notification
                    successful_files.append({
                        'filename': filename,
                        'content': content,
                        'lines': num_lines,
                        'chars': num_chars
                    })
            except Exception as e:
                error_files.append({
                    'filename': os.path.basename(filepath),
                    'error': str(e)
                })
        else:
            error_files.append({
                'filename': os.path.basename(filepath),
                'error': 'Fichier non trouvé'
            })
    
    # Deuxième passe : formater le contenu à copier dans le presse-papier
    result = []
    total_successful = len(successful_files)
    
    for index, file in enumerate(successful_files):
        # Vérifier si c'est le dernier fichier
        is_last = (index == total_successful - 1)
        
        if is_last:
            # Sans le point-virgule et les retours à la ligne
            formatted_content = (
                f'Voici le contenu de la version la plus récente du fichier {file["filename"]} :\n'
                f'"{file["content"]}"'
            )
        else:
            # Avec le point-virgule et les cinq retours à la ligne
            formatted_content = (
                f'Voici le contenu de la version la plus récente du fichier {file["filename"]} :\n'
                f'"{file["content"]}" ;\n\n\n\n\n'
            )
        
        result.append(formatted_content)
    
    # Ajouter les erreurs au résultat final
    for error in error_files:
        formatted_error = f'Erreur en traitant le fichier {error["filename"]} : {error["error"]} ;'
        result.append(formatted_error)
    
    # Joindre tous les résultats en une seule chaîne
    final_result = ' '.join(result)
    
    # Copier le résultat dans le presse-papier
    pyperclip.copy(final_result)
    
    # Récupérer la date et l'heure actuelles
    now = datetime.now()
    formatted_datetime = now.strftime("%Y-%m-%d %H:%M:%S")  # Format: AAAA-MM-JJ HH:MM:SS
    
    # Préparer les notifications détaillées
    notification = f"{GREEN}Date et heure d'exécution : {formatted_datetime}{RESET}\n\n"
    notification += "Le contenu formaté a été copié dans le presse-papier.\n\n"
    
    if successful_files:
        notification += "Fichiers traités avec succès :\n"
        for file in successful_files:
            # Ajouter la couleur verte au nom du fichier
            notification += f" - {GREEN}{file['filename']}{RESET} : {file['lines']} lignes, {file['chars']} caractères\n"
        # Afficher le nombre total de lignes en vert
        notification += f"\nNombre total de lignes copiées : {GREEN}{total_lines}{RESET}\n"
        notification += f"Nombre total de caractères copiés : {total_chars}\n"
    else:
        notification += "Aucun fichier n'a été traité avec succès.\n"
    
    if error_files:
        notification += "\nErreurs rencontrées :\n"
        for file in error_files:
            notification += f" - {file['filename']} : {file['error']}\n"
    else:
        notification += "\nAucune erreur n'a été rencontrée."
    
    print(notification)

if __name__ == "__main__":
    main()
