import model
import argparse
import re


def main() -> None:
    parser = argparse.ArgumentParser(description="Markov chain generate file")
    parser.add_argument("--model", type=str, help="path to directory with documents", required=True)
    parser.add_argument('--length', type=int, help='count of words', required=True)
    parser.add_argument('--prefix', type=str, help='first words for generator', nargs='+')
    args = parser.parse_args()
    md = model.load(args.model)
    if not md: return

    prev = []
    res = ''
    if args.prefix:
        pref = re.sub('[^a-zа-яё\n.?!,-]', ' ', (' '.join(args.prefix)).lower())
        res = pref + ' '
        prev = pref.split()[-md.prefix_len:]

    for i in range(args.length):
        prev += [md.get_next(prev)]
        if len(prev) > md.prefix_len:
            prev = prev[1:]
        res += prev[-1] + ' '
    print(res)



if __name__ == '__main__':
    main()