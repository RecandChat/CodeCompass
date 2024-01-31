from API import get_data


def main():
    # Making sure code works
    if get_data.get_most_starred_repos():
        print("Success!")
    else:
        print("Failure!")


main()
