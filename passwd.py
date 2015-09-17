import core, bcrypt, sys
from getpass import getpass

class UserClass(object):
    database = core.get_auth() # import from database.json

    def __init__(self, user, password):
        self.user = user
        self.password = password

    # If user is valid check password is correct.
    def user_auth(self):
        try:
            return bcrypt.hashpw(self.password, self.database[self.user][0])
        except (KeyError):
            print('User does not exist.')

    # If user_auth returns True check if user is in group 'superuser'.
    def admin_auth(self):
        if self.user_auth():
            return 'superuser' in self.database[self.user][1]
        else:
            return False

    # Add new user with encrypted password & group to 'database'
    def add_user(self, new_user, new_password, group):
        hashed_password = bcrypt.hashpw(new_password+core.SECRET_KEY, bcrypt.gensalt())
        self.database[new_user] = ['0', ['1']]
        self.database[new_user][0] = hashed_password
        self.database[new_user][1][0] = group
        core.save_auth(self.database)

    # Remove selected user from 'database'.
    def del_user(self, select_user):
        del self.database[select_user]
        core.save_auth(self.database)

    # Reset selected user's password.
    def reset_password(self, select_user, new_password):
        hashed_password = bcrypt.hashpw(new_password+core.SECRET_KEY, bcrypt.gensalt())
        self.database[select_user][0] = hashed_password
        core.save_auth(self.database)

    # Add group to selected user.
    def add_group(self, select_user, group):
        self.database[select_user][1].append(group)
        core.save_auth(self.database)

    # Remove selected user from group.
    def remove_group(self, select_user, group):
        self.database[select_user][1].remove(group)
        core.save_auth(self.database)

class HandlerClass(UserClass):

    def __init__(self, user, password):
        UserClass.__init__(self, user, password)
        self.dispatch = {
                'exit': sys.exit,
                'add-user': self.add_user_handler,
                'remove-user': self.del_user_handler,
                'reset-password': self.reset_password_handler,
                'add-group': self.add_group_handler,
                'remove-group': self.remove_group_handler
                }

    def add_user_handler(self):
        new_user = input("New User: ").lower()
        if new_user not in self.database:
            group = input("User Group (default is [default-group]: ").lower() or "default-group"
            new_password = getpass('Enter New Password: ')
            confirm_password = getpass('Confirm New Password: ')
            if new_password == confirm_password:
                self.add_user(new_user, new_password, group)
                print('New User Registered')
                loop()
            else:
                print('Passwords do not match.')
                loop()
        else:
            print('User already exists.')
            loop()

    def del_user_handler(self):
        select_user = input("Select user: ").lower()
        if select_user in self.database:
            self.del_user(select_user)
            print('User removed.')
            loop()
        else:
            print('User does not exsist.')
            loop()

    def reset_password_handler(self):
        select_user = input("Select user: ").lower()
        if select_user in self.database:
            new_password = getpass('Enter New Password: ')
            confirm_password = getpass('Confirm New Password: ')
            if new_password == confirm_password:
                self.reset_password(select_user, new_password)
                print("Password reset.")
                loop()
            else:
                print("Password did not match, try again.")
                loop()
        else:
            print('User does not exist.')
            loop()

    def add_group_handler(self):
        select_user = input("Select user: ").lower()
        if select_user in self.database:
            group = input('Enter new group: ')
            self.add_group(select_user, group)
            print('Group added to {0}'.format(select_user))
            loop()
        else:
            print('User does not exist.')
            loop()

    def remove_group_handler(self):
        select_user = input("Select user: ").lower()
        if select_user in self.database:
            try:
                group = input('Enter group: ')
                self.remove_group(select_user, group)
                print('{0} removed from {1}'.format(select_user, group))
                loop()
            except:
                print('{0} is not a member of {1}'.format(select_user, group))
                loop()
        else:
            print('User does not exist.')

user = input('Username: ').lower()
password = getpass('Password: ') + core.SECRET_KEY
login = HandlerClass(user, password)

def main():
    if login.admin_auth() == True:
        print('User Authenticated as {0}\n'.format(login.user))
        print('Valid Commands: ')
        loop()
    else:
        print("Access Denied.")

def loop():
    display_options = (list(login.dispatch.keys()))
    print(display_options)
    try:
        return login.dispatch[input(': ').lower()]()
    except (KeyError):
        print('Invalid Command')
        loop()

if __name__ == '__main__':
    main()
