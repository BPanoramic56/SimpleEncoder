#region Imports
from operator import index
import os
from re import L, S
from tkinter import E
import random
from math import gcd 
import colorama
#endregion

#region Variables
class color:
    red = colorama.Fore.RED
    green = colorama.Fore.GREEN
    yellow = colorama.Fore.YELLOW
    default = colorama.Fore.RESET
    blue = colorama.Fore.BLUE
    grey = colorama.Fore.LIGHTBLACK_EX
    lightblue = colorama.Fore.CYAN
    hide = '\x1b[?25l'
    show = '\x1b[?25h'
    
msg, currentMethod, autoKey = '', 'Undefined', 'a'
numberCount, letterCount, charCount, totalCount, encodingIndex, methodIndex, affineA, affineB, affineM, scopeIndex, squareIndex = 0, 0, 0, 0, -1, 0, 1, 2, 26, 0, 0
encoder, monosubAlpha = [], []
notPossible, useCapital, showEvolution, decodeCipherMethod, changeMessage = False, False, False, False, False
#endregion

def Clear():
    os.system('clear')

def RandomAlpha(useCapital):
    monosubAlpha = []
    if useCapital == False:
        while len(monosubAlpha) != 26:
            n = random.randint(97, 122)
            if chr(n) not in monosubAlpha:
                monosubAlpha.append(chr(n))
            else:
                continue

    elif useCapital == True:
        while len(monosubAlpha) != 52:
            if len(monosubAlpha) % 2:
                n = random.randint(97, 122)
            else:
                n = random.randint(65, 90)

            if chr(n) not in monosubAlpha:
                monosubAlpha.append(chr(n))

    return monosubAlpha

def CreateCustomAlpha():
    monosubAlpha = []
    if useCapital == False:
        missingLetters = [chr(x) for x in range(97, 123)]
    elif useCapital == True:
        missingLetters = [chr(x) for x in range(97, 123)] + [chr(x) for x in range(65,91)]
    size = len(missingLetters)
    while len(monosubAlpha) != size:
        print(color.grey + 'Missing letters: ' + ', '.join(missingLetters))
        print('Current letters: %s' % (', '. join(monosubAlpha)) + color.default)
        while True:
            try:
                newLetter = input('New letter to be added: ')[0]
                break
            except ValueError as e:
                print('The typed value is not allowed - Source: %s' % (e))

        if newLetter in monosubAlpha:
            print('The letter %s is already in the list' % (newLetter))
        elif newLetter in missingLetters:
            monosubAlpha.append(newLetter)
            missingLetters.remove(newLetter)
        else:
            print('The letter %s is not allowed in this context' % (newLetter))

    return monosubAlpha

def Define():
    global msg, numberCount, letterCount, charCount, totalCount
    msg = input('What message do you want to encode: ')
    while len(list(msg)) == 0:
        print('Message cannot be empty')
        msg = input('What message do you want to encode: ')

    return str(msg)

def DecodeCipher():
    global msg
    words = []

    while True:
        try:
            scope = int(input('Scope of search, including positive and negative: '))
            break
        except ValueError as e:
            print('Invalid value for scope - Source: %s' % (e))

    print(color.hide)

    for scopeIndex in range(-scope, +scope+1):
        decoder = list(msg)
        for i in range(0, len(decoder)):
            decoder[i] = int(ord(decoder[i])) + int(scopeIndex)
            decoder[i] = chr(decoder[i])
        decoder = ''.join(decoder)
        words.append(decoder)

    with open('/Users/brunogomespascotto/Programming/words.txt', 'r') as file: 
        foundNumber = 0
        for line in file.read().splitlines():
            for word in words:
                print(word)
                if str(line) in str(word) or str(words) and len(line) != 1 in str(line) and len(line) != 1:
                    print('\n%s\nPossible Solution Found: %s\nCipher Index: %i\nWord Equivalent: %s\n%s\n' % ('-' * 10, word, words.index(word)-len(words)//2, line, '-' * 10))
                    input('Press anything to continue search')
                    foundNumber += 1
    print('%i word%s found for the given message and index' % (foundNumber, ' was' if foundNumber == 1 else 's were'))

def TestCoprime(testInput):
    return gcd(testInput, affineM)

def FindCoPrimes(findCos, rg): 
    lst = []
    for i in range (0, rg):
        if gcd(findCos, i) == 1:
            lst.append(str(i))
    return lst

def Variables(currentMethod):
    optionVar = 1
    global changeMessage

#region CaesarVar
    if currentMethod == 'Caesar Method':
        global encodingIndex

        while optionVar != 0:
            Clear()
            print(color.blue + 'Ceaser Method Variable Menu\tMessage = %s' % (msg) + color.default + '\n\t0 - Go back\n\t1 - Change Index (%i)\n\t2 - Change Message' % (encodingIndex))

            while True:
                try:
                    optionVar = int(input('Option: '))
                    break
                except:
                    continue

            if optionVar == 0:
                return encodingIndex

            elif optionVar == 1:
                print('Current encoder Index: %i' % (encodingIndex))
                encodingIndex = int(input('Type desired encoding index: '))

            elif optionVar == 2:
                if changeMessage == True:
                    changeMessage = False
                else:
                    changeMessage = True
                print('Change Message Variable was changed to %s' % (changeMessage))
                input('Press anything to continue')
#endregion

#region AffineVar
    elif currentMethod == 'Affine Method':
        global affineA, affineB, affineM
        while optionVar != 0:
            Clear()
            print(color.blue + 'Affine Method Variable Menu\tMessage = %s' % (msg) + color.default + '\n\t0 - Go back\n\t1 - Change Index A (A = %i)\n\t2 - Change index B (B = %i)\n\t3 - Find Coprimes\n\t[Value of M cannot be changed and has to be coprime to A]\n\t4 - Change Message' % (affineA, affineB))
            while True:
                try:
                    optionVar = int(input('Option: '))
                    break
                except:
                    continue

            if optionVar == 0:
                return affineA, affineB, affineM,

            elif optionVar == 1:
                print('Current A Index: %i' % (affineA))
                testInput = int(input('Type desired encoding index: '))
                if TestCoprime(testInput) == 1:
                    affineA = testInput
                    print('The index of A was changed to %i' % (affineA))
                else:
                    print('The value %i is not coprime of M (%i)' % (testInput, affineM))
                print(color.hide, end = '')
                input('Press anything to continue', end = '\r')
                print(color.show, end = '')

            elif optionVar == 2:
                print('Current B Index: %i' % (affineB))
                affineB = int(input('Type desired encoding index: '))

            elif optionVar == 3:
                findCos = int(input('What number do you want to find the coprimes of: '))
                rg = int(input('Range of search: '))    
                lst = FindCoPrimes(findCos, rg)
                print('There are %i coprimes of %i between 0 and %i: \n%s' % (len(lst), findCos, rg, ', '.join(lst)))

            elif optionVar == 4:
                if changeMessage == True:
                    changeMessage = False
                else:
                    changeMessage = True
                print('Change Message Variable was changed to %s' % (changeMessage) + color.hide)
                input('Press anything to continue')
                print(color.show)
#endregion

#region MonoVar
    elif currentMethod == 'Monoalphabetical Substitution Method':
        global monosubAlpha, showEvolution, useCapital
        while optionVar != 0:
            Clear()
            print(color.blue + 'Monoalphabetical Substitution Method\tMessage = %s' % (msg) + color.default + '\n\t0 - Go back\n\t1 - Randomize Alphabet A (%s)\n\t2 - Create Custom Alphabet\n\t3 - Randomize with Capital Letters (%s)\n\t4 - Show Evolution (%s)\n\t5 - Change Message\n\t6 - QWERTY alpahbetic display' % (', '.join(monosubAlpha), useCapital, showEvolution))
            while True:
                try:
                    optionVar = int(input('Option: '))
                    break
                except:
                    continue
            if optionVar == 0:
                return monosubAlpha

            elif optionVar == 1:
                monosubAlpha = RandomAlpha(useCapital)

            elif optionVar == 2:
                monosubAlpha = CreateCustomAlpha()
            
            elif optionVar == 3:
                if useCapital == False:
                    useCapital = True
                else:
                    useCapital = False
            
            elif optionVar == 4:
                if showEvolution == True:
                    showEvolution = False
                else:
                    showEvolution = True

            elif optionVar == 5:
                if changeMessage == True:
                    changeMessage = False
                else:
                    changeMessage = True
                print('Change Message Variable was changed to %s' % (changeMessage))

            elif optionVar == 6:
                monosubAlpha = ['q', 'W', 'e', 'R', 't', 'Y', 'u', 'I', 'o', 'P', 'a', 'S', 'd', 'F', 'g', 'H', 'j', 'L', 'z', 'X', 'c', 'V', 'b', 'N', 'm', 'Q', 'w', 'E', 'r', 'T', 'y', 'U', 'i', 'O', 'p', 'A', 's', 'D', 'f', 'G', 'h', 'J', 'l', 'Z', 'x', 'C', 'v', 'B', 'n', 'M']
                if useCapital == False:
                    monosubAlpha = list(set(x.lower() for x in monosubAlpha))
            print(color.hide, end = '')
            input('Press anything to continue')
            print(color.show, end = '')
#endregion

    elif currentMethod == 'Autokey Method':
        global autoKey
        while optionVar != 0:
            Clear()
            print(color.blue + 'Autokey Method Variable Menu\tMessage = %s' % (msg) + color.default + '\n\t0 - Go back\n\t1 - Change AutoKey %s - (' % (autoKey), end = '')
            for i in autoKey:
                print(ord(i) - 96, end = '')
            print(')\n\t2 - Change Message')
            while True:
                try:
                    optionVar = int(input('Option: '))
                    break
                except:
                    continue

            if optionVar == 0:
                return autoKey

            elif optionVar == 1:
                print('Current AutoKey: %s (%i)' % (autoKey, ord(autoKey)-96))
                while True:
                    try:
                        autoKey = int(input(')\nOption: '))
                        break
                    except:
                        continue
            
            elif optionVar == 2:
                if changeMessage == True:
                    changeMessage = False
                else:
                    changeMessage = True
                print('Change Message Variable was changed to %s' % (changeMessage))
                input('Press anything to continue')

#region Menu

def Menu(currentMethod):
    currentMethod = 'Undefined'
    global encodingIndex, affineA, affineB, affineM, notPossible, autoKey, monosubAlpha, msg
    while True:
        option = 999
        while option != 0:

            Clear()
            print(color.blue + 'Message = %s' % (msg) + '\tCurrent method: %s%s' % (color.red if currentMethod == 'Undefined' else color.blue, currentMethod) + color.default)
            print('1 - Caesar Cipher Method', end = '')
            print(color.grey if currentMethod != 'Caesar Method' else color.default, '\n\tCurrent encoder Index = %i' % (encodingIndex) + color.default)
            print('\n2 - Affine Cipher Method', end = '')
            print(color.grey if currentMethod != 'Affine Method' else color.default, '\n\tA = %i\n\tB = %i\n\tM = %i' % (affineA, affineB, affineM) + color.default)
            print('\n3 - AutoKey Cipher Method')
            print(color.grey if currentMethod != 'Autokey Method' else color.default, '\tCurrent autoKey Index = (%s) - (%i)' % (autoKey, ord(autoKey)-97) + color.default)
            print('\n4 - Monoalphabetical Substitution Method')
            print(color.grey if currentMethod != 'Monoalphabetical Substitution Method' else color.default, '\tCurrent Alphabet = %s' % ('[]' if currentMethod != 'Monoalphabetical Substitution Method' else ', '.join(monosubAlpha)) + color.default)
            print('\n5 - Decode Cipher Method')
            print('\n6 - Randomize letters')
            print('\n7 - Change message')
            print('\n8 - Columnar Transposition Cipher')
            print(color.grey if currentMethod == 'Undefined' else color.default, '\033[1D\n9 - Change variables of %s' % (currentMethod) + color.default)
            try:
                option = int(input('\nOption: '))
            except:
                continue
            if option == 1:
                CeaserMethod = True
                currentMethod = 'Caesar Method'
                print('Method was changed to: %s' % (currentMethod))

            elif option == 2:
                for i in msg:
                    if i.isdigit() == True:
                        print('%s is not a valid input for the Affine Method' % (i))
                        notPossible = True
                if notPossible == False:
                    AffineMethod = True
                    currentMethod = 'Affine Method'
                    print('Method was changed to: %s' % (currentMethod))

            elif option == 3:
                for i in msg:
                    if i.isdigit() == True:
                        print('%s is not a valid input for the AutoKey Method' % (i))
                        notPossible = True
                if notPossible == False:
                    autokeyMethod = True
                    currentMethod = 'Autokey Method'
                    print('Method was changed to: %s' % (currentMethod))

            elif option == 4:
                for i in msg:
                    if i.isdigit() == True:
                        print('%s is not a valid input for the AutoKey Method' % (i))
                        notPossible = True
                if notPossible == False:
                    currentMethod = 'Monoalphabetical Substitution Method'
                    print('Method was changed to: %s' % (currentMethod))
                    monosubAlpha = RandomAlpha(useCapital)

            elif option == 5:
                DecodeCipher()

            elif option == 6:
                currentMethod = 'Randomize letters'

            elif option == 7:
                msg = input('New message: ')

            elif option == 8:
                currentMethod = 'Columnar Transposition Cipher'

            elif option == 9:
                if currentMethod == 'Undefined':
                    print('No method choosen', end = '')
                    input()
                    continue
                Variables(currentMethod)

            print(color.hide + 'Press anything to continue', end = '\r')
            input()
            print(color.show, end = '')
            continue

        if currentMethod == 'Undefined':
            print('No method was choosen')
            continue
        else:
            return currentMethod
#endregion

#region Encoding
def Encode():
    global msg, encoder, methodIndex, currentMethod, decodeCipherMethod
    encoder = list(msg)
    print(color.green + currentMethod + color.default)
#region Caesar
    if currentMethod == 'Caesar Method':
        global encodingIndex
        for i in range(0, len(encoder)):
            encoder[i] = int(ord(encoder[i])) + int(encodingIndex)
            encoder[i] = chr(encoder[i])
#endregion

#region Affine
    elif currentMethod == 'Affine Method':
        global affineA, affineB, affineM
        for l in encoder:
            l = l.lower()
        for i in range(0, len(encoder)):
            encoder[i] = int(((ord(encoder[i])-97) * affineA + affineB) % affineM)
            encoder[i] = chr(encoder[i] + 97)
#endregion

#region Autokey
    elif currentMethod == 'Autokey Method':
        encoder_original = encoder
        global autoKey

        for l in encoder:
            l = l.lower()

        for i in autoKey:
            encoder = list(i) + encoder
        del encoder[-len(autoKey):]
        print(encoder)
        for i in range(0, len(encoder)):
            encoder[i] = int(ord(encoder[i])) - 97 + int(ord(encoder_original[i]) - 97) % 26
            encoder[i] = chr(encoder[i] + 97)
#endregion
#region Monoalphabetical
    elif currentMethod == 'Monoalphabetical Substitution Method':
        global monosubAlpha, showEvolution, useCapital

        if useCapital != False:
            for l in encoder:
                l = l.lower()
        
        ls = []
        encoder = ''.join(encoder)
        quantityLetters = 1
        o = 0
        for i in range(len(monosubAlpha)):
            if i > len(encoder)-1:
                break
            if encoder[i] == ' ':
                continue
            if encoder[i] not in ls:
                quantityLetters += encoder.count(encoder[i])
                encoder = encoder.replace(encoder[i], monosubAlpha[i])
                ls.append(encoder[i])
                o += 1
                if showEvolution == True:
                    print('Change %s: ' % (o) + encoder, '(Letter %s)' % (monosubAlpha[i]))
        encoder = list(encoder)
#endregion
#region Random
    elif currentMethod == 'Randomize letters':
        lst = list(msg)
        l = []
        encoder = [x for x in lst]
        f = 0
        while len(l) != len(lst):
            n = random.randint(0, len(encoder)-1)
            if n in l:
                continue
            else:
                encoder[n] = lst[f]
                l.append(n)
                f += 1

        print('New message = ' + ', '.join(encoder))
#endregion
#region Column
    elif currentMethod == 'Columnar Transposition Cipher':
        global squareIndex
        encoder = []

        sentence = ''
        columnsCreated = False
        while columnsCreated != True:
            keyWord = list(str(input('Type the desired keyword for the method: ')))
            columnTable = []

            for i in range(1, len(msg)+1):
                sentence += msg[i-1]

                if i % len(keyWord) == 0:
                    columnTable.append(list(sentence))
                    sentence = ''

                if i == len(msg) and i % len(keyWord) != 0:
                    underlineCounter = 0
                    while i % len(keyWord) != 0:
                        sentence += '_'
                        i += 1
                        underlineCounter += 1
                    print('%i underline%s added to the end of the message to fullfil the keyword requirements' % (underlineCounter, 's' if underlineCounter != 1 else ''))
                    columnTable.append(sentence)
                    columnsCreated = True
                    
                elif i == len(msg) and i % len(keyWord) == 0:
                    print('Columns created')
                    columnsCreated = True

        sortKey = sorted(keyWord)
        indexer = []
        indexer = list(sortKey.index(i) for i in keyWord)
        completeIndex = sorted(indexer)
        for index in completeIndex:
            for column in columnTable:
                encoder.append(column[indexer.index(index)])
#endregion
    
    if changeMessage == True:
        msg = ''.join(encoder)   

    return ''.join(encoder)
#endregion

while True:
    if changeMessage == False:
        Define()
    currentMethod = Menu(currentMethod)
    print(color.lightblue + 'Final Message: ' + Encode() + color.default)
    input()
