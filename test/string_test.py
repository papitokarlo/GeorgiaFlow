word = "skka fsf sasf"
l=[]
s = word.split()
for w in s:
    x=w.capitalize()
    l.append(x)
# using list comprehension
listToStr = ' '.join([str(elem) for elem in l])
 
print(listToStr)