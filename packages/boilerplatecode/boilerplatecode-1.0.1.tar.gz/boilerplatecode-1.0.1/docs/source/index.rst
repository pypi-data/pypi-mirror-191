############################
boilerplatecode 1.0.1 Documentation
############################
Library template for 'how to publish a python package on pypi' video tutorial.

boilerplatecode package contains the following tools:

* **PasswordGenerator** - generates a random password

.. note:: 

  Getting boilerplatecode

  $ ``pip install boilerplatecode``

  $ ``pip install --upgrade boilerplatecode``


******************
PasswordGenerator
******************

Automatic password generator

Logic
================================================================

Generates a password of a length specified by the user. The password is generated using the
uppercase letters, lowercase letters, numbers 0 to 9 and special characters.
Makes a user smile :)


**Initialize PasswordGenerator**
.. code-block:: python

  from boilerplatecode import PasswordGenerator
  
  pg = PasswordGenerator(12) # initialize with password length of 12 characters
  
Parameters
===========================
* ``password_length`` [default=None]

  Number of desired symbols in the password to be generated.

Methods
===========================
* ``generate()``

  Generate a new password.

Attributes
===========================

* ``password``

  Last generated password.

Examples
================================================================

.. code-block:: python

  from boilerplatecode import PasswordGenerator
  pg = PasswordGenerator(12)


******************
Links
******************
`Git <https://github.com/DanilZherebtsov/boilerplatecode>`_

`pypi <https://pypi.org/project/boilerplatecode/>`_

`author <https://www.linkedin.com/in/danil-zherebtsov/>`_