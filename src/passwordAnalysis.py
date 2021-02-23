
import secrets
import string
import requests
import hashlib

def generateMemorablePassword(length=4, hasCapitals=True, paddingType=list(string.digits)):
    """
    Generates a memorable passord from 4 dictionary words (of at least 4 letters),
    one of the words will be in fullcaps if hasCapitals is True.
    Words are separated by some padding character determined by padding type.
    """

    wl = open('./dict/words', 'r')
    fullWordlist = wl.readlines()
    wl.close()

    wordlist = []
    for word in fullWordlist:
        # Filters for words of length 4 or more,
        # since words still have line break at the end
        if len(word) > 4:
            wordlist.append(word[:-1])

    # Selects which word should be in fullcaps
    if hasCapitals:
        isCapital = secrets.randbelow(length)
    else:
        isCapital = -1

    password = ""
    for i in range(length):
        word = secrets.choice(wordlist)
        if i == isCapital:
            word = word.upper()
        password += word
        password += secrets.choice(paddingType)

    return password

def generatePassword(length=20, hasAlphabet=True, hasCapitals=True, hasDigits=True,
                    hasBasicSymbols=True, hasAdvancedSymbos=False):
    """
    Creates a random password of specified length from the pool of selected characters
    """

    characterPool = []

    # Adds the characters to the pool if they are True
    if hasAlphabet:
        characterPool += list(string.ascii_lowercase)
    if hasCapitals:
        characterPool += list(string.ascii_uppercase)
    if hasDigits:
        characterPool += list(string.digits)
    if hasBasicSymbols:
        characterPool += list("!@#$%&*?")
    if hasAdvancedSymbos:
        characterPool += list("<>{}[](),.")

    password = ""
    for i in range(length):
        password += secrets.choice(characterPool)

    return password

def isPasswordKnown(password):
    """
    Determins if the password is a known password found in haveibeenpwned.com
    Returns the number of times the passord has been found in a breach
    Anything more than 0 means the password is compromised and should not be used

    The haveibeenpwned API takes the first 5 characters from the sha1 hash,
    and returns any matching hashes (not including the matching first 5 characters)
    """

    url = "https://api.pwnedpasswords.com/range/"
    hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    response = requests.get(url+hash[:5])

    possibleMatches = response.text.split()
    for possibleMatch in possibleMatches:
        if hash[5:] in possibleMatch:
            return int(possibleMatch.split(":")[1])
    return 0


def passwordStrength(password):
    """
    This determins the passowrd strength of the passed password
    """
    if isPasswordKnown(password)>0:
        return "known Password"
    else:
        return "TODO"



if __name__ == "__main__":
    print(generateMemorablePassword())
