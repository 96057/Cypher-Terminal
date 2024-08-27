import os
import time
import bcrypt  # Import bcrypt for secure password hashing
from termcolor import colored

# Constants
USER_FILE = 'user.txt'
PASSWORD_FILE = 'password.txt'

def clear_screen():
    """Clear the console screen based on the OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def sign_up():
    """Handles user signup, including password hashing and storing credentials."""
    print(colored("Welcome! Please sign up for Cypher OS.", 'green', attrs=['bold']))
    susername = input(colored("Username: ", 'yellow', attrs=['bold'])).strip()
    spassword = input(colored("Password: ", 'yellow', attrs=['bold'])).strip()

    # Check for invalid inputs
    if not susername or not spassword:
        print(colored("Username or password cannot be empty.", 'red', attrs=['bold']))
        return sign_up()

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(spassword.encode('utf-8'), bcrypt.gensalt())

    # Write username and hashed password to files
    try:
        with open(USER_FILE, 'w') as username_file:
            username_file.write(susername)
        
        with open(PASSWORD_FILE, 'wb') as password_file:
            password_file.write(hashed_password)  # Save the hashed password as bytes
    except IOError as e:
        print(colored(f"Error writing to file: {e}", 'red', attrs=['bold']))
        return

    print(colored("Signup complete. Please log in.", 'green', attrs=['bold']))

def load_credentials():
    """Load stored credentials from files."""
    try:
        with open(USER_FILE, 'r') as username_file:
            username = username_file.read().strip()

        with open(PASSWORD_FILE, 'rb') as password_file:
            hashed_password = password_file.read().strip()

        return username, hashed_password
    except FileNotFoundError:
        print(colored("User not signed up. Redirecting to signup...", 'red', attrs=['bold']))
        sign_up()
        return None, None  # Return None values if sign_up is called
    except IOError as e:
        print(colored(f"Error reading files: {e}", 'red', attrs=['bold']))
        exit()

def login():
    """Handles user login by verifying entered credentials against stored ones."""
    user, stored_hashed_password = load_credentials()
    
    # If load_credentials triggered a signup, the function may return None values
    if user is None or stored_hashed_password is None:
        return False, None

    # Prompt user for login credentials
    entered_user = input(colored("Username: ", 'yellow', attrs=['bold'])).strip()
    entered_password = input(colored("Password: ", 'yellow', attrs=['bold'])).strip()

    # Verify credentials
    if entered_user == user and bcrypt.checkpw(entered_password.encode('utf-8'), stored_hashed_password):
        print(colored("Login successful!", 'green', attrs=['bold']))
        return True, user
    else:
        print(colored("Password or username is wrong. Please try again...", 'red', attrs=['bold']))
        return False, None

def main():
    """Main function to run the application."""
    if not os.path.exists(USER_FILE) or not os.path.exists(PASSWORD_FILE):
        sign_up()
    else:
        print(colored("User already signed up. Proceeding to login...", 'cyan', attrs=['bold']))
        time.sleep(1)

    clear_screen()
    
    # Login attempts loop
    attempts = 0
    logged_in = False
    user = None  # Initialize user variable
    while attempts < 3:  # Limit the number of login attempts
        logged_in, user = login()
        if logged_in:
            break
        attempts += 1
        time.sleep(1)  # Delay for failed login attempts

    if not logged_in:
        print(colored("Too many failed attempts. Exiting...", 'red', attrs=['bold']))
        exit()

    # Command loop after successful login
    while True:
        com = input(colored(f"{user}$ ", 'cyan', attrs=['bold'])).strip()
        if com == 'sign up':
            sign_up()
            exit()
        elif com in ['exit', 'quit']:
            print(colored("Exiting Cypher OS. Goodbye!", 'green', attrs=['bold']))
            exit()
        else:
            # You might want to restrict commands that can be executed for security reasons
            os.system(com)

if __name__ == "__main__":
    main()
