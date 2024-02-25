from bgo.interface import init_interface, parser, processing_args


def main():
    init_interface()

    args = parser.parse_args()
    processing_args(args)


if __name__ == "__main__":
    main()
