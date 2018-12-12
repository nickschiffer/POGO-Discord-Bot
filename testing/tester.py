from gymFinder import findGym
import cProfile
import pstats


test_file = open("inputPhrases.txt", "r")
test_list = test_file.read().lower().splitlines()

pr = cProfile.Profile()
i = 0
#test list
j = 0
#result
k = 0
expected = []
result = []
for j in range(0,1):
    i = 0
    for testLine in test_list:
        if (i%2):
            #odd
            expected.append(testLine)
            i = i+1
        else:
            #even
            pr.enable()
            result.append(findGym(testLine)) 
            pr.disable()
            i = i+1



sortby = 'time'
ps = pstats.Stats(pr).sort_stats(sortby)
correct = 0
ran = 0
i = 0

for expect in expected:
    if(expect.lower() == result[ran][0] or (expect.lower() == "none" and result[ran][0] == None)):
        correct += 1
    else:
        print(f"Orig Message: {test_list[i]}")
        print(f"Expected: {expect.lower()},  result: {result[ran][0]}")
    i += 2
    ran += 1
print(f"Spelling Confidence: 0.95")
print(f"Correct: {correct}, Total = {ran}")
ps.print_stats()


#message = "I found something at Tot"
#message = ""

#gym, confidence = findGym(message)

#cProfile.run('findGym(message)')

#print(f"gym: {gym}, confidence: {confidence}")