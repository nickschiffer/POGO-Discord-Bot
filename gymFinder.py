import nltk
import re
from difflib import SequenceMatcher
from difflib import get_close_matches
from array import *
from operator import itemgetter
import numpy as np
gym_file = open("POGOgyms.txt", "r")
gym_nouns_file = open("POGOgyms_NounsOnly.txt", "r")
noun_file = open("NounList.txt", "r")
noun_list = noun_file.read().lower().splitlines()
# exception_file = open(r'C:\College\Python\ExceptionList.txt')
gym_list = gym_nouns_file.read().lower().splitlines()
gym_list_final = gym_file.read().splitlines()


spelling_confidence = 0.90

def similar(a,b):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def extractNouns(message):
       
        nouns = []
        for word, pos in nltk.pos_tag(nltk.word_tokenize(str(message))):
                if pos.startswith("NN"):
                        nouns.append(word.lower())
                else:
                        for extraNoun in noun_list:
                                if similar(extraNoun, word.lower()) > spelling_confidence:
                                        nouns.append(word.lower())
        
        return nouns
#print(gym_list)
def appendInc(nounMatches, nounMatchCounts, gym):
        found = False
        i = -1
        if nounMatches:
                for matches in nounMatches:
                        i = i + 1
                        if(gym == matches):
                                nounMatchCounts[i] += 1
                                found = True       
                        
        if(found == False):
                nounMatches.append(gym)
                nounMatchCounts.append(1)

        return nounMatches


def findGym(sentence):
        # sentence = "raid popping up at Interlock mural  9:35"
        #sentence = "Something Something Got lunch and Box found something Center Arts Veterans"
        nouns = []
        nouns = extractNouns(sentence)
        nounMatch = []
        nounMatchCount = []
        print(nouns)
        workingNoun = ""
        #pass 1
        i = 0
        for noun in nouns:
                noun = noun.lower()
                for gym in gym_list:
                        gym = gym.lower()
                        for gymtoken in gym.split():
                                
                                if(similar(noun,gymtoken) > spelling_confidence):
                                        print(f"noun: {noun}. gymToken: {gymtoken}. Sub pass 1: {similar(noun,gymtoken)}")
                                        appendInc(nounMatch,nounMatchCount,gym)
        x = np.array(nounMatchCount)
        # print(f"x: {x}")
        if len(x) == 0:
                print(f"No match, aborting")
                return None,None
        #pass 2
        print(f"noun match:{nounMatch}")
        index = np.argmax(x)
        print(f"argmax: {np.argmax(x)}")
        final_index = gym_list.index(nounMatch[index])
        #need to find confidence

        print(f"match: {nounMatch[index]}")

        match = nounMatch[index]
        match_final = gym_list_final[final_index]
        print(f"match_final: {match_final}")
        gym_length = len(nltk.word_tokenize(match_final))
        numMatches = x[index]
        confidence = numMatches / gym_length
        print(f"confidence = {confidence}")
        result = (match_final,confidence)
        return match_final,confidence


