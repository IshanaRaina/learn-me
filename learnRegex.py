#! python3
import re

message = 'Call me at 862-294-9108 or 212-273-2318 for my office line'

phoneRegex = re.compile(r'(\d\d\d)-\d\d\d-\d\d\d\d')
print(type(phoneRegex)) # Pattern object returned after using the 'compile' method
mo = phoneRegex.search(message)
print(type(mo)) # Match object is the first match returned after using the 'search' method

print(mo.group())
print(mo.group(1))

print("----------findall() method----------")
# search() method returns a match object whereas findall() returns a list with all group matches 
print(phoneRegex.findall(message))

print("----------Pipe character----------")
batRegex = re.compile(r'Bat(man|mobile)')
mo = batRegex.search("Batmobile lost a wheel")
print(mo.group())
mo = batRegex.search("Batmotorcycle lost a wheel")
print(mo) #None type object doesn't need group() to print

print("---? character -> 0 or 1 occurences of whatever is before ?---")
batRegex = re.compile(r'Bat(wo)?man')
mo = batRegex.search("The Adventures of Batman")
print(mo.group())
mo = batRegex.search("The Adventures of Batwoman")
print(mo.group())

print("---* character -> 0 or more occurences of whatever is before *---")
batRegex = re.compile(r'Bat(wo)*man')
mo = batRegex.search("The Adventures of Batman")
print(mo.group())
mo = batRegex.search("The Adventures of Batwowowowoman")
print(mo.group())

print("---+ character -> 1 or more occurences of whatever is before +---")
print("---Matching a specific number of times with {}---")
print("---Matching a specific number of times in a range {x,y}---")
digitRegex = re.compile(r'(\d){3,5}')
mo = digitRegex.search('1234567890')
#12345 will be matched cos Python performs greedy matches (matches longest possible string)
print("Performing a greedy match ---> ", mo.group())

print("---Performing a non greedy match by placing ? after pattern rather than after group---")
digitRegex = re.compile(r'(\d){3,5}?')
mo = digitRegex.search('1234567890')
print("Performing a non greedy match ---> ", mo.group())

print("----------Character Classes----------")
lyrics = ''' 11 pipers piping (ding)
10 lords a leaping (dong)
9 ladies dancing (ding)
8 maids a milking (dong)
7 swans a swimming (ding)
6 geese a laying (dong)
5 golden rings
4 calling birds
3 french hens
2 turtle doves '''
xmasRegex = re.compile(r'\d+\s\w+')
print(xmasRegex.findall(lyrics))

print("---Making your own character classes using [] - can be used to specify ranges too---")
lettersRegex = re.compile(r'[a-fA-F]{2}')
print(lettersRegex.findall("Robocop eats baby Food."))

print("-----Negative character classes using ^ at the start of the pattern-----")
consonantsRegex = re.compile(r'[^aeiouAEIOU]')
print(consonantsRegex.findall("Robocop eats baby Food."))

print("-----Exact matches at the start of the string using ^-----")
beginsWithHelloRegex = re.compile(r'^Hello')
print(beginsWithHelloRegex.findall('Hello World'))

print("-----Exact matches at the end of the string using $-----")
endsWithWorldRegex = re.compile(r'World$')
print(endsWithWorldRegex.findall('Hello World'))

print("-----Entire string to be matched using ^$-----")
entireStringRegex = re.compile(r'^\d+$')
print(entireStringRegex.findall('123'))
print(entireStringRegex.findall('1x3'))

print("---Anything except newline using .---")
atRegex = re.compile(r'.at')
print(atRegex.findall("The cat in the hat sat on the flat mat"))
atRegex = re.compile(r'.{1,2}at')
print(atRegex.findall("The cat in the hat sat on the flat mat"))

print("---Anything using .*---")
nameRegex = re.compile(r'First Name: (.*) Last Name: (.*)')
print(nameRegex.findall("First Name: Ishana Last Name: Raina"))
#DOTALL as a second argument to compile() to include newline as well

print("----------Using VERBOSE----------")
phoneRegex = re.compile(r'''
\d\d\d #area code
-
\d\d\d
-
\d\d\d\d
''', re.VERBOSE) #Use | to pass multiple arguments. Only works with the compile method()
print(phoneRegex.findall(message))