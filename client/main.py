if __name__ == "__main__":
    WELCOME_MESSAGE = "Welcome To SCSE Bank."
    MENU_MESSAGE = """----------------------------Bank Menu------------------------------------\n 
        Please choose a service by typing [1-8]:\n
        1: Open a new bank account\n
        2: Query information from a bank account\n
        3: Deposit to a bank account\n
        4: Withdraw from a bank account\n
        5: Monitor update from other accounts\n
        6: Pay monthly maintenance fee from a bank account\n
        7: Close a bank account\n
        8: Print the menu\n
        0: Stop the client\n"""
    EXIT_MESSAGE = "Thank you for using SCSE Bank."
    
    print(WELCOME_MESSAGE)

    authenticate()

    print(MENU_MESSAGE)
    while user_selection := input('>'):
        user_selection = user_selection.strip()
        if user_selection == '1':
            pass
        elif user_selection == '2':
            pass
        elif user_selection == '3':
            pass
        elif user_selection == '4':
            pass
        elif user_selection == '5':
            pass
        elif user_selection == '6':
            pass
        elif user_selection == '7':
            pass
        elif user_selection == '8':
            pass
        else:
            print(f'{user_selection} is invalid. Please try again')
            print(MENU_MESSAGE)
