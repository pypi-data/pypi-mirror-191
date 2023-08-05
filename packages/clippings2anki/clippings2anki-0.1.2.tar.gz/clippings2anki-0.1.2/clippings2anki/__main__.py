import sys
sys.path.append("")

import clippings2anki.clippings as clippings

if __name__ == "__main__":
    # read cli arguments
    import argparse
    parser = argparse.ArgumentParser(description="Convert Kindle clippings to Anki flashcards")
    parser.add_argument("input_file", type=str, help="Path to the 'My clippings.txt' file")
    parser.add_argument("language", type=str, help="Language of the clippings (e.g. 'english' or 'german' for English or German)")
    parser.add_argument('-o', "--output", type=str, default="Kindle flashcards.txt", help="Path to the output file (default: 'Kindle flashcards.txt')")
    parser.add_argument('--json', action=argparse.BooleanOptionalAction, help="Save the parsed clippings as a json file (default: False)")
    parser.add_argument('--anki-separator', type=str, default="\t", help="Separator for the anki flashcard output (default: Tab)")
    args = parser.parse_args()

    clippings.main(args.input_file, args.language, args.output, save_json=(args.json==True), anki_separator=args.anki_separator)
