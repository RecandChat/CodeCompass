from API import get_data


def main():
    # Making sure code works
    if get_data.get_user_repo("Lukasaurus11"):
        print("Success!")
    else:
        print("Failure!")
