import json

    
def save_to_text(flashcards, file_name="flashcards.txt", separator="\t"):
    text_output = ""
    # last_meaning = ""
    for word, flashcard in flashcards.items():
        text_output += f"{word}{separator}"
        for f in flashcard:
            # if f['meaning'] != last_meaning:
            #     text_output += f"{f['meaning']}<br>"
            text_output += "<ul>"
            for d in f['definitions']:
                text_output += f"<li>{d}</li>"
            text_output += "</ul>"

            # last_meaning = f['meaning']
            
        text_output += "\n"
        
    with open(file_name, "w", encoding='utf-8') as f:
        f.write(text_output)


if __name__ == "__main__":
    with open("flashcards.json", "r") as f:
        fl = json.load(f)
        
    save_to_text(fl)
