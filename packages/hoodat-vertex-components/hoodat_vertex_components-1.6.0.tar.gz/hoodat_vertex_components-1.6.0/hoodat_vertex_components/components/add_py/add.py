import argparse


def _add(args):
    answer = args.a + args.b
    print(answer)
    return answer


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=int)
    parser.add_argument("--b", type=int)
    args = parser.parse_args()
    _add(args)
