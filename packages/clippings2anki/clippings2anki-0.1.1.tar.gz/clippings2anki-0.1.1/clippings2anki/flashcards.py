import re


def get_flashcard(word, parser, log=False):
    # get definition of the word
    wiki_data = parser.fetch(word)
    definitions = []
    
    for w in wiki_data:
        definitions_set = []
        for d in w["definitions"]:
            definitions_set.extend(d["text"])
            
        definitions.append(definitions_set)

    if len(definitions) == 0 or len(definitions[0]) == 0:
        return None, None
    
    flashcard = []
    
    if log:
        print('\n==')
        print(word)
    for m in definitions:
        if log:
            print('--')
            print("\n".join(m))
            print()
        
        meaning = m[0]
        definitions = m[1:]
    
        flashcard.append({
            "meaning": meaning,
            "definitions": definitions
        })
    
    # check if the only definition is "* of *"
    first_definition = flashcard[0]['definitions'][0]
    
    base_re = re.compile(r".* of (\w*)\n")
    base_word = re.match(base_re, first_definition+"\n")

    if base_word:
        if log:
            print(f"base word: {base_word.group(1)}")
        
        return get_flashcard(base_word.group(1), parser)
        
    return word, flashcard
