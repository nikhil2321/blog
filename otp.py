import random
def genotp():
    uppercase = [chr(i) for i in range(ord('A'),ord('Z')+1)]
    lowercase = [chr(i) for i in range(ord('a'),ord('z')+1)]
    otp = ''
    for i in range(2):
        otp+=random.choice(uppercase)
        otp+=str(random.randint(0,9))
        otp+=random.choice(lowercase)
    return otp