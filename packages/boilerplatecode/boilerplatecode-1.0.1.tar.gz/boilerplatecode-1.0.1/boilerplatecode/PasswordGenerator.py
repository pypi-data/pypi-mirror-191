import random
import string

class PasswordGenerator:
    
    __version__ = '1.0.1'

    def __init__(self, password_length):
        '''Generates a password of num_chars length.
        
        Args:
            password_length (int): The length of the password to generate.
        
        Raises:
            TypeError: If password_length is not an integer.
            
        Returns:
            None
        
        '''
        self.password_length = password_length
        self.generate()
    
    # validate init arguments
    # ==========================================================================
    # num_chars
    @property
    def password_length(self):
        return self._password_length

    @password_length.setter
    def password_length(self, password_length):
        if not isinstance(password_length, int):
            raise TypeError('password_length must be an integer')
        self._password_length = password_length
    # ==========================================================================
    
    def generate(self):
        '''Generates a password of num_chars length'''
        password = []
        symbol_types = [self._get_uppercase, self._get_lowercase, self._get_number, self._get_punctuation]
        for char in range(self.password_length):
            symbol_type = random.choice(symbol_types)
            password.append(symbol_type())
        password = ''.join(password)
        self.password = password
        print(f'Your new password is: {self.password}')
        print('You are awesome!')
        
    def _get_uppercase(self):
        '''Returns a random uppercase letter'''
        return random.choice(string.ascii_uppercase)

    def _get_lowercase(self):
        '''Returns a random lowercase letter'''
        return random.choice(string.ascii_lowercase)
    
    def _get_number(self):
        '''Returns a random number'''
        return str(random.randint(0,9))

    def _get_punctuation(self):
        '''Returns a random punctuation character'''
        return random.choice(string.punctuation)