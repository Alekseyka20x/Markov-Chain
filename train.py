import argparse
import model
import os
import re


def train(md: model.Model, text:str) -> model.Model:
    text = re.sub('[^a-zа-яё\n.?!,-]', ' ', text.lower())
    for words in text.split("\n"):
        n_gramm = []
        for word in words.split():
            if word in ['', '.', ',', '?', '!', '-']:
                continue
            if word == ',':
                print(words)
            md.fit(n_gramm, word)
            n_gramm += [word]
            if len(n_gramm) > md.prefix_len:
                n_gramm = n_gramm[1:]
    return md


def main() -> None:
    parser = argparse.ArgumentParser(description="Markov chain train file")
    parser.add_argument('--model', type=str, help='path to model file', required=True)
    parser.add_argument("--input-dir", type=str, help="path to directory with documents")
    parser.add_argument("--prefix-len", type=int, default=3, help='length of prefix for generation (default 2)')
    args = parser.parse_args()

    texts = []
    md = model.Model(args.prefix_len)
    if not args.input_dir:
        train(md, input("Text: "))
    skipped = 0
    
    for filename in [] if not args.input_dir else os.listdir(args.input_dir):
        filepath = args.input_dir + '/' + filename
        if not os.path.isfile(filepath) or len(filepath) < 4 or filepath[-4:] != '.txt':
            continue
        try:
            with open(filepath, "r", encoding='utf-8') as f:
                text = f.read()
                print(f'Training on "{filename}"')
                train(md, text)
        except UnicodeDecodeError:
            print(f'Bad encoding of file "{filename}". Convert to utf-8.')
            skipped += 1
    
    print("Done" + ("" if not skipped else f" with {skipped} undecoded file{'' if skipped == 1 else 's'}") + ".")
    model.save(args.model, md)


if __name__ == '__main__':
    main()
