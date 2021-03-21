
import secrets
import string
import requests
import hashlib
import math

commonSymbols = "~!@#$%^&*_-+=,.?"
brackets = "<>{}[]()"
irregularSymbols = ";:\"\'"


def generateMemorablePassword(length=4, hasCapitals=True, paddingType=list(string.digits)):
    """
    Generates a memorable passord from 4 dictionary words (of at least 4 letters),
    one of the words will be in fullcaps if hasCapitals is True.
    Words are separated by some padding character determined by padding type.
    """

    wordlist = getWordlist()

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
        characterPool += list(commonSymbols)
    if hasAdvancedSymbos:
        characterPool += list(brackets)

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
    if len(password) == 0:
        return "empty"
    elif isPasswordKnown(password)>0:
        return "Known Password"
    else:
        entropy = passwordEntropy(password)

        if entropy<28:
            return "Very Weak"
        elif entropy<36:
            return "Weak"
        elif entropy<60:
            return "Reasonable"
        elif entropy<128:
            return "Strong"
        else:
            return "Very Strong"



def passwordEntropy(password):
    """
    Calcualtes the entropy of a password
    """

    charPool = 0
    if any(c in password for c in string.ascii_lowercase):
        charPool += len(string.ascii_lowercase)

    if any(c in password for c in string.ascii_uppercase):
        charPool += len(string.ascii_uppercase)

    if any(c in password for c in string.digits):
        charPool += len(string.digits)

    if any(c in password for c in commonSymbols):
        charPool += len(commonSymbols)

    if any(c in password for c in brackets):
        charPool += len(brackets)

    if any(c in password for c in irregularSymbols):
        charPool += len(irregularSymbols)

    # Each character has a basic entroy as the size of the character pool
    entropy = [charPool for i in range(len(password))]

    # Repetitious characters have less entropy
    for i in range(1,len(password)):
        if password[i] == password[i-1]:
            entropy[i] = entropy[i-1]/2


    wordlist = getWordlist()
    simplePass = password.lower()

    # Iterates over possible character combinations, looking for words
    # Starting with 4 characters, since <4 character words have higher entropy
    # than the individual characters
    for wordLength in range(4,len(password)+1):
        for pos in range(0,len(password)-wordLength+1):
            if (simplePass[pos:pos+wordLength] in wordlist):

                # Words have an entropy equal to the common wordlist size (8000),
                # spread over each character in the word
                wordEntropy = 8000**(1.0/wordLength)
                # Capitals increase the word entropy
                if any(c in password[pos:pos+wordLength] for c in string.ascii_uppercase):
                    wordEntropy*=2
                # Selects the minimum entropy for a given character
                for char in range(pos,pos+wordLength):
                    entropy[char] = min(entropy[char], wordEntropy)

    # Entropy is usually formatted as 2 to the power of the entropy equals the possibilities
    return math.log2(prod(entropy))


def prod(list):
    """
    Returns the product of a list
    """
    product = 1
    for item in list:
        product*=item

    return product



def getWordlist():
    """
    Returns the word wordlist
    current wordlist coppied from usr/bin/share/dict/words
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

    return wordlist



if __name__ == "__main__":
    passwords = ["password", "LittleRedridding", "123096521",
        generateMemorablePassword(), generatePassword()]

    for password in passwords:
        print(password + ": " + passwordStrength(password))
