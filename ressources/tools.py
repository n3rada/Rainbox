#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
import re
import random as rd
import time, datetime
import math

THIS_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DIRECTORY_FILES = os.path.join(THIS_FOLDER, "ressources/files/")

DIRECTORY_SAMPLES = os.path.join(DIRECTORY_FILES, "samples/")
DIRECTORY_WORDLISTS = os.path.join(DIRECTORY_FILES, "wordlists/")

DIRECTORY_BUFFER = os.path.join(DIRECTORY_WORDLISTS, "buffer/")
DIRECTORY_FRAGMENTS = os.path.join(DIRECTORY_WORDLISTS, "fragments/")
DIRECTORY_HEXA = os.path.join(DIRECTORY_WORDLISTS, "hexa/")
DIRECTORY_ALPHA = os.path.join(DIRECTORY_WORDLISTS, "alpha/")


def readableDigits(s):
    try:
        return format(int(s), ',').replace(',', '.')
    except:
        return s


isStringTrue = lambda s: s.lower(
) in ['true', '1', 't', 'y', 'yes', 'yeah', 'yup', 'certainly', 'uh-huh']

##########################################
##########################################
import itertools
from typing import Iterator


def createFragments(inputList, letters: int = 4) -> Iterator:
    """
    Generator to create fragments of number of letters from inputList. 
    """
    for elt in itertools.product(inputList, repeat=letters):
        # If the fragment contains more than maxRep letters
        frag = ''.join(elt)

        # No words with 3 times the same letter / number
        regex = r"^(?:(\w)\1?(?!\1))+$"
        if re.match(regex, frag):
            yield frag
        else:
            continue


##########################################
##########################################


def getInt(default=1, expected="choices"):
    print(f"Enter {expected} ({default} by default):")

    while True:
        i = input("> ")
        if i == "":
            return default
        else:
            return int(i)


def isHexa(string: str):
    """
    Check if a string is in hexadecimal or not
    """
    for ch in string:

        if ((ch < '0' or ch > '9') and (ch < 'A' or ch > 'F')):
            return False

    return True


def isPunctuated(s: str):
    """
    Check if a string contains punctuations.
    """
    import string
    for ch in s:
        if ch in string.punctuation:
            return True
    return False


def percentageMatch(seq1: str, seq2: str):
    """
    Output percentage of exact matching between two strings of same length.
    """
    assert len(seq1) == len(seq2)

    idem = 0
    total = len(seq1)

    for char1, char2 in zip(seq1, seq2):
        if char1 == char2:
            idem += 1
        else:
            continue

    percentage = float("%.2f" % ((idem / total) * 100))

    return percentage


def arrangement(n: int, p: int):
    """
    Return permutation https://en.wikipedia.org/wiki/Permutation#k-permutations_of_n numbers.
    """

    return int(math.factorial(n) / math.factorial(n - p))


##########################################
##########################################


def clear(withAscii: bool = True):
    """
    Clearing the screen.
    """
    if os.name == 'nt':
        os.system("cls")
    else:
        os.system("clear")

    if withAscii:
        print("""
                                        ██████╗  █████╗ ██╗███╗   ██╗██████╗  ██████╗ ██╗  ██╗
                                        ██╔══██╗██╔══██╗██║████╗  ██║██╔══██╗██╔═══██╗╚██╗██╔╝
                                        ██████╔╝███████║██║██╔██╗ ██║██████╔╝██║   ██║ ╚███╔╝ 
                                        ██╔══██╗██╔══██║██║██║╚██╗██║██╔══██╗██║   ██║ ██╔██╗ 
                                        ██║  ██║██║  ██║██║██║ ╚████║██████╔╝╚██████╔╝██╔╝ ██╗
                                        ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
                                                    A generator of wifi router keys
                                                            Author: n3rada
                """)


def countLines(file_path):
    count = 0
    chunkSize = 8192 * 1024

    with open(file_path, 'rb') as fh:
        while True:
            buffer = fh.read(chunkSize)
            if not buffer:
                break
            count += buffer.count(b'\n')
    return count


def rmFile(name: str, directory=DIRECTORY_FILES):
    """Remove named file."""
    try:
        os.remove(directory + name)
    except FileNotFoundError:
        pass


def whatInThere(directory=DIRECTORY_FILES):
    """
    Return elements present in given directory in list format.
    """
    return [f for f in os.listdir(directory)]


def isStringInFile(fullPath: str, string: str):
    """
    Return tuple saying if string is into the file and in which line.
    """
    lines = 1
    with open(fullPath, 'r') as f:
        for line in f:
            if string in line:
                return (True, lines)
            else:
                lines += 1

        return (False, lines)


def eraseAllFromDir(directory=DIRECTORY_BUFFER):
    """
    Erase all files in given directory (default: buffer dir)
    """
    for f in whatInThere(directory):
        rmFile(name=f, directory=directory)


def mergeFiles(fullNameNew: str, filenames: list):
    """
    Merge all files "filenames" from directory in a new file.
    """
    import shutil
    with open(fullNameNew, "ab") as outputF:
        for file in filenames:
            with open(file, "rb") as inputF:
                shutil.copyfileobj(inputF, outputF)
                os.remove(file)


def mergeAllFiles(newFileFullName: str, filenames: list):
    """
    Merge all files "filenames" from directory in a new file and remove duplicates.
    """
    ### Merge all
    merge = DIRECTORY_BUFFER + "-MERGED.txt"
    with open(merge, "w") as outfile:
        for name in filenames:
            with open(name) as infile:
                outfile.write(infile.read())

    ### Remove duplicates
    count = 0
    lines_seen = set()

    with open(newFileFullName, "a") as output_file:
        for each_line in open(merge, "r"):
            if each_line not in lines_seen:
                output_file.write(each_line)
                lines_seen.add(each_line)
                count += 0

    print(f"\nAfter merging, {count} of the generated keys are duplicates.\n")


def isFileHere(fullPath: str):
    """Return if given name file's is here or is not."""
    return os.path.isfile(fullPath)


def handleDirectory(dirName: str, directory=DIRECTORY_FILES):
    """ If given directory doesn't exist, then create it. """
    if not os.path.exists(directory + dirName):
        os.makedirs(directory + dirName)


def writeVarToFile(var: object, name: str, directory=DIRECTORY_FILES):
    """Write given variable into a file with variable name"""
    # r+ for reading and writing
    name = directory + name
    with open(name, "w+") as f:
        f.truncate(0)
        f.write(f"{var}")

    return var


def extractVarFromFile(fileName: str, directory=DIRECTORY_FILES):
    """Extract variable contenant's from file."""
    import ast
    with open(directory + fileName, "r+") as f:
        contents = f.read()
        try:
            extracted = ast.literal_eval(contents)
        except Exception:
            extracted = contents

    return extracted


def mergedSamples():
    """
    Return a list of merged keys.
    """
    merged = []

    for file in whatInThere(DIRECTORY_SAMPLES):

        file = DIRECTORY_SAMPLES + file

        with open(file, "r") as f:

            for line in f:
                line = line.strip().split(sep="|")[0]
                merged.append(''.join([elt.upper() for elt in line]))

    return merged


def mergedSamplesIn4():
    """
    Return a list of merged keys in "XXXX" scheme.
    """
    merged4 = []

    for elt in mergedSamples():
        elt = elt.split(sep="-")

        for toAdd in elt:
            merged4.append(toAdd)

    return merged4


##########################################
##########################################

from math import floor

numberOf4Fragments = lambda i: floor(i / 4)
numberOfCharRemaining = lambda i: i % 4


def handleFragments(fragName: str):
    """
    Because generators are like ticker tapes, call them when you need them.

    Available generators: FRAG_2_HEXA, FRAG_2, FRAG_4_HEXA, FRAG_4
    Both with mixed, lower and upper case as "low","up","mix"
    To specify cases use : handleFragments("FRAG_2_HEXA","low") 
    """
    import string

    # "FRAG_4-up-True" => ("FRAG_4","up","True")
    fragName, case, punctuation = fragName.split("-")

    fragName = fragName.upper()
    case = case.lower()

    if isStringTrue(punctuation):
        # Ponctuations vues dans certains codes wifi
        base = string.digits + "."
    else:
        base = string.digits

    if fragName == "FRAG_2_HEXA":
        if case == "low":
            return createFragments(base + 'abcdef', letters=2)
        elif case == "up":
            return createFragments(base + 'ABCDEF', letters=2)
        elif case == "mix":
            return createFragments(string.hexdigits, letters=2)

    elif fragName == "FRAG_4_HEXA":
        if case == "low":
            return createFragments(base + 'abcdef', letters=4)
        elif case == "up":
            return createFragments(base + 'ABCDEF', letters=4)
        elif case == "mix":
            return createFragments(string.hexdigits, letters=4)

    elif fragName == "FRAG_2_ALPHA":
        if case == "low":
            return createFragments(base + string.ascii_lowercase, letters=2)
        elif case == "up":
            return createFragments(base + string.ascii_uppercase, letters=2)
        elif case == "mix":
            return createFragments(base + string.ascii_letters, letters=2)

    elif fragName == "FRAG_4_ALPHA":
        if case == "low":
            return createFragments(base + string.ascii_lowercase, letters=4)
        elif case == "up":
            return createFragments(base + string.ascii_uppercase, letters=4)
        elif case == "mix":
            return createFragments(base + string.ascii_letters, letters=4)


def choose2Fragments(fragL, stockList=[]) -> tuple:
    """
    Return two fragments from given frag list's according to previous choosen words.
    """

    word1, word2 = rd.choice(fragL), rd.choice(fragL)
    while (word1 in stockList
           or word2 in stockList) or (word1.isnumeric() and word2.isnumeric()):
        word1, word2 = rd.choice(fragL), rd.choice(fragL)

    # Never two digital fragments that follow each other
    try:
        if stockList[-1].isnumeric():
            while word1.isnumeric():
                word1 = rd.choice(fragL)
    except IndexError:
        pass

    return word1, word2


def choose1Fragment(fragL, stockList=[]) -> str:
    """
    Return one fragment from given frag list's according to previous choosen words.
    """

    word = rd.choice(fragL)
    while word in stockList or word.isnumeric():
        word = rd.choice(fragL)

    # Never two digital fragments that follow each other
    try:
        if stockList[-1].isnumeric():
            while word.isnumeric():
                word = rd.choice(fragL)
    except IndexError:
        pass

    return word


def generateKey(length: int, fragments: list):
    """
    This function will be called by all processors once for generate key.
    """

    frag4 = numberOf4Fragments(length)
    others = numberOfCharRemaining(length)

    #print(f"{length} key = {frag4} frag-4 + {others} chars.")

    fragL4, fragL2 = fragments

    finalWord = ""
    alreadyPickedUp = []

    # We first deal with fragments of 4
    count4 = 0
    while count4 != frag4:

        if (count4 + 2) < frag4:
            word1, word2 = choose2Fragments(fragL4, stockList=alreadyPickedUp)

            alreadyPickedUp.append(word1)
            alreadyPickedUp.append(word2)

            finalWord += word1 + word2

            #print("Adding 2 frag4.")
            count4 += 2

        else:
            word = choose1Fragment(fragL4, stockList=alreadyPickedUp)
            alreadyPickedUp.append(word)

            finalWord += word

            #print("Adding 1 frag4.")
            count4 += 1

    if others:

        countO = 0
        while countO != others:
            # if other = 2 => adding one frag2 !
            if others == 2:
                word = choose1Fragment(fragL2, stockList=alreadyPickedUp)

                alreadyPickedUp.append(word)

                finalWord += word

                #print("Adding 1 frag2.")
                countO += 2
            else:
                word = choose1Fragment(fragL4, stockList=alreadyPickedUp)

                if others == 3:
                    word = word[:-1]
                elif others == 1:
                    word = word[0]

                alreadyPickedUp.append(word)

                finalWord += word

                #print("Adding 1 cutted frag4.")
                countO += 1

    return finalWord


def infiniteKeysGenerator(length: int, fragments: list):
    while True:
        yield generateKey(length, fragments)


def init_worker():
    import signal
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def workerWriter(fileName: str, fragList: list, keySize: int):
    """
    Infinitly add keys to given file.
    """
    with open(fileName, "w+") as f:
        try:
            for key in infiniteKeysGenerator(length=keySize,
                                             fragments=fragList):
                f.write(f"{key}\n")
        except KeyboardInterrupt:
            f.close()


def multiprocWriter(cores: int, fragName: str, keySize: int,
                    fragmentList: list, keyToFind: str, possibilities: int):
    import multiprocessing as mp

    poule = mp.Pool(cores, init_worker)

    #############
    type = fragName.split("-")[0].split("_")[-1]

    if type == "HEXA":
        directory = DIRECTORY_HEXA
    else:
        directory = DIRECTORY_ALPHA

    name = fragName.split("_")[-1] + "-" + str(keySize) + "-keys"
    bufferName = DIRECTORY_BUFFER + "buffer"
    finalName = directory + name + ".txt"
    ##############

    data = [(f"{bufferName}-{i}.txt", fragmentList, keySize)
            for i in range(cores)]

    print(
        "\n\t\t\t\t  --> Use keyboard interrupt command to stop the generating process <--"
    )

    starting = time.time()
    try:
        poule.starmap(workerWriter, data)

    except KeyboardInterrupt:

        poule.terminate()
        poule.close()
        poule.join()

        clear(withAscii=True)
        print(
            "Interruption intercepted ! Wait for the program to process the necessary information...\n"
        )

        finishing = time.time()
        elapsed = finishing - starting

        previousLines = 0
        if isFileHere(fullPath=finalName):
            previousLines = countLines(file_path=finalName)

        mergeFiles(finalName, [f"{bufferName}-{i}.txt" for i in range(cores)])
        eraseAllFromDir(directory=DIRECTORY_BUFFER)

        total = countLines(file_path=finalName)
        lines = total - previousLines
        keysPerSeconds = floor(lines / elapsed)

        if keyToFind:
            isInFile, line = isStringInFile(finalName, keyToFind)

            if isInFile:
                print(
                    f"You key ({keyToFind}) have been found during the generating process !"
                )
                print(
                    f"It's at line {readableDigits(line)} into the file {finalName}."
                )
            else:
                print(
                    f"Among all {readableDigits(line)} keys of the file, no key like yours appears..."
                )

        timeMesure = datetime.timedelta(seconds=elapsed)

        gigas = os.path.getsize(finalName) / (1024 * 1024 * 1024)

        keysPerGiga = floor(line / gigas)

        print(f"\nEach Giga represents {readableDigits(keysPerGiga)} keys.")
        print(
            f"Approximately {readableDigits(keysPerSeconds)} keys were generated per second."
        )
        print(
            f"{readableDigits(lines)} keys have been added in {timeMesure} to the {readableDigits(previousLines)} keys already present into the wordlist."
        )
        print(
            f"For a total of {readableDigits(total)} keys availables into the {gigas} Gigabyte wordlist.\n"
        )

        if isinstance(possibilities, int):
            timeOfCalc = (possibilities / keysPerSeconds)

            try:
                timeF = datetime.timedelta(seconds=timeOfCalc)
            except OverflowError:
                timeF = (timeOfCalc / 31536000) / 100  # centuries
                timeF = f"{timeF} centuries"

            print(
                f"Thus, you would need a {possibilities/keysPerGiga} Gigabyte wordlist to have all the possibilities."
            )
            print(
                f"This is equivalent to {timeF} of calculation with this power.\n"
            )

        sys.exit(0)


def consoleWriter(keySize: int, fragmentList: list, keyToFind: str):
    starting = time.time()
    count = 0

    try:
        if not keyToFind:
            for key in infiniteKeysGenerator(length=keySize,
                                             fragments=fragmentList):
                print(key)
                count += 1
        else:
            print(
                f"The generator will generate keys until he finds yours: {keyToFind}"
            )
            print(
                f"Only the keys corresponding to more than 50% with yours will be displayed."
            )
            print(
                f"The generation above is infinite, use the keyboard interrupt to stop it."
            )

            for key in infiniteKeysGenerator(length=keySize,
                                             fragments=fragmentList):
                match = percentageMatch(key, keyToFind)
                count += 1

                if key == keyToFind:
                    print(f"{key} =/= {keyToFind} | Matching : {match}")

                    raise KeyboardInterrupt
                else:
                    if match > 50:
                        print(f"{key} =/= {keyToFind} | Matching : {match}")

    except KeyboardInterrupt:
        #clear()
        ended = time.time()
        elapsed = ended - starting

        keysPerSeconds = floor(count / elapsed)

        timeMesure = datetime.timedelta(seconds=elapsed)
        print(f"\n{timeMesure} elapsed !")
        print(
            f"Approximately {readableDigits(keysPerSeconds)} keys were generated per second (with one core)."
        )
        sys.exit(0)


def writer(keySize: int,
           cores: int,
           fragName: str = "FRAG_4_HEXA-up",
           wordlist: bool = False,
           keyToFind: str = None):
    """
    Writing output:

    If not wordlist:
        One core into standard output
    else:
        Multiprocessed writing process during "till" seconds.

    keyToFind: arg to pass if you want to test your key.
    """

    # Updating parameters if a key has been passed as argument for finding.
    if keyToFind:
        #keyToFind = keyToFind.replace("-","")
        keySize = len(keyToFind)

        print(
            f"You have provided a {keySize} length key's to test ({keyToFind})."
        )
        print("The parameters will be automatically adapted to the said key.")

        fragName = "FRAG_4_"

        tail = ""

        if isHexa(keyToFind):
            tail += "HEXA"
        else:
            tail += "ALPHA"

        if keyToFind.isupper():
            tail += "-up"
        elif keyToFind.islower():
            tail += "-low"
        else:
            tail += "-mix"

        if isPunctuated(keyToFind):
            tail += "-True"
        else:
            tail += "-False"

        fragName += tail
        print(f"The generation will proceed with parameters: {tail}\n")
    #

    print(f"Creating Fragments list:\n")

    nOf4 = numberOf4Fragments(keySize)

    nOf2 = numberOfCharRemaining(keySize)

    print(
        f">The generated key is composed of {nOf4} fragments of 4 and {nOf2} remaining chars !"
    )
    print(f">{fragName} ...")
    fragL4 = list(handleFragments(fragName))
    lFragL4 = len(fragL4)
    print(
        f"Fragments {fragName} have been created and contains {readableDigits(lFragL4)} elements !"
    )

    if nOf2 > 0:
        frag2Name = "FRAG_2_" + fragName.split("_")[-1]
        print(f">{frag2Name} ...")
        fragL2 = list(handleFragments(frag2Name))
        lFragL2 = len(fragL2)
        print(
            f"Fragments {frag2Name} have been created and contains {readableDigits(lFragL2)} elements !"
        )
    else:
        fragL2 = []
        lFragL2 = 0

    fragL = [fragL4, fragL2]

    print("\nAll fragments have been generated, computing will start now !")
    print("You have 3 seconds to read this.")
    time.sleep(3)

    clear(withAscii=True)

    if (lFragL2 > 100000 or lFragL4 > 100000):
        possibilities = "<Woh this number is too huge to being compute easly>"
    else:
        possibilities = arrangement(lFragL4, nOf4) * arrangement(lFragL2, nOf2)

    print(
        f"With each generation, you have a 1 in {readableDigits(possibilities)} chance of finding the right key. Good luck !\n"
    )

    if wordlist:
        multiprocWriter(cores=cores,
                        fragName=fragName,
                        keySize=keySize,
                        fragmentList=fragL,
                        keyToFind=keyToFind,
                        possibilities=possibilities)
    else:
        consoleWriter(keySize=keySize, fragmentList=fragL, keyToFind=keyToFind)
