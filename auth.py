import bcrypt
import os


def hash_password(plain_text_password):

 # TODO: Encode the password to bytes (bcrypt requires byte strings)


 # TODO: Generate a salt using bcrypt.gensalt()


 # TODO: Hash the password using bcrypt.hashpw()


 # TODO: Decode the hash back to a string to store in a text file

 return


def verify_password():

 # TODO: Encode both the plaintext password and the stored hash to byt


 # TODO: Use bcrypt.checkpw() to verify the password
 # This function extracts the salt from the hash and compares

 return


