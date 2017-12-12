aliens = 2
password = "BADPASSWORD"
print("What's the password???")
guess = input("Enter the password: ").upper()
while guess != password:
    print("Nope")
    aliens = aliens ** 2
    print("Oh no, now there are", aliens, "aliens. Try again.")
    if aliens > 740000000000:
        break
    guess = input("Password: ").upper()
if aliens > 740000000000:
    print("Heck, you lost")
else:
    print("Hey, I think you won")
