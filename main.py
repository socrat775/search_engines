import app, sys, traceback


def main(argv):
    try:
        app.run(argv)
    except Exception as e:
        traceback.print_exc()


if __name__ == "__main__":
    sys.exit(main(sys.argv))
