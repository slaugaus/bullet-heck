upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCDEFGHIJKLMNOPQRSTUVWXYZ"
lower = "abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
stringToEncrypt = input("Please input some text to encrypt: ")
shiftAmount = int(input("Please input a whole number from 1-25 to be your key. "))
encryptedString = ""
for currentCharacter in stringToEncrypt:
    uposition = upper.find(currentCharacter)
    unewPosition = uposition + shiftAmount
    lposition = lower.find(currentCharacter)
    lnewPosition = lposition + shiftAmount
    if currentCharacter in upper:
        encryptedString = encryptedString + upper[unewPosition]
    elif currentCharacter in lower:
        encryptedString = encryptedString + lower[lnewPosition]
    else:
        encryptedString = encryptedString + currentCharacter
print("Your encrypted message is:")
print(encryptedString)
