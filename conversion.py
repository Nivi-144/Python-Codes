text = input("Enter a string: ")
binary = ' '.join(format(ord(char), '08b') for char in text)
print("Binary representation:", binary)
