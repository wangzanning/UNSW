import pickle
from Inv_Index import InvertedIndex
import Inv_Index
from project_part1 import WAND_Algo

def main():
    documents = {
        1: 'Ink helps drive democracy in Asia The Kyrgyz Republic a small mountainous state of the former Soviet republic is using invisible ink and ultraviolet readers in the country s elections as part of a dri',
        2: 'China net cafe culture crackdown Chinese authorities closed 12575 net cafes in the closing months of 2004 the country s government said According to the official news agency most of the net cafes were',
        3: 'Microsoft seeking spyware trojan Microsoft is investigating a trojan program that attempts to switch off the firm s anti  spyware software The spyware tool was only released by Microsoft in the last f',
        4: 'Digital guru floats sub100 PC Nicholas Negroponte chairman and founder of MIT s Media Labs says he is developing a laptop PC that will go on sale for less than  100 £ 53 He told the BBC World Service ',
        5: 'Technology gets the creative bug The hi tech and the arts worlds have for some time danced around each other and offered creative and technical help when required Often this help has come in the form ',
        6: 'Wi fi web reaches farmers in Peru A network of community computer centres linked by wireless technology is providing a helping hand for poor farmers in Peru The pilot scheme in the Huaral Valley 80 ki',
        7: 'Microsoft releases bumper patches Microsoft has warned PC users to update their systems with the latest security fixes for flaws in Windows programs In its monthly security bulletin it flagged up eigh',
        8: 'Virus poses as Christmas e mail Security firms are warning about a Windows virus disguising itself as an electronic Christmas card The Zafi D virus translates the Christmas greeting on its subject lin',
        9: 'Apple laptop is greatest gadget The Apple Powerbook 100 has been chosen as the greatest gadget of all time by US magazine Mobile PC The 1991 laptop was chosen because it was one of the first lightweig',
        10: 'Google s toolbar sparks concern Search engine firm Google has released a trial tool which is concerning some net users because it directs people to pre  selected commercial websites The AutoLink featu',
        11: 'UK net users leading TV downloads British TV viewers lead the trend of illegally downloading US shows from the net according to research New episodes of 24 Desperate Housewives and Six Feet Under appe',
        12: 'IBM puts cash behind Linux push IBM is spending  100 m £ 52 m over the next three years beefing up its commitment to Linux software The cash injection will be used to help its customers use Linux on e',
        13: 'UK pioneers digital film network The world s first digital cinema network will be established in the UK over the next 18 months The UK Film Council has awarded a contract worth £ 115 m to Arts Allianc',
        14: 'EU software patent law faces axe The European Parliament has thrown out a bill that would have allowed software to be patented Politicians unanimously rejected the bill and now it must go through anot',
        15: 'Xbox power cable fire fear Microsoft has said it will replace more than 14 million power cables for its Xbox consoles due to safety concerns The company said the move was a preventative step after rep',
        16: 'Global blogger action day called The global web blog community is being called into action to lend support to two imprisoned Iranian bloggers The month old Committee to Protect Bloggers is asking thos',
        17: 'Finding new homes for old phones Re using old mobile phones is not just good for the environment it has social benefits too Research has found that in some developing nations old mobile phones can hel',
        18: 'PlayStation 3 chip to be unveiled Details of the chip designed to power Sony s PlayStation 3 console will be released in San Francisco on Monday Sony IBM and Toshiba who have been working on the Cell ',
        19: 'Intel unveils laser breakthrough Intel has unveiled research that could mean data is soon being moved around chips at the speed of light Scientists at Intel have overcome a fundamental problem that be',
        20: 'Security scares spark browser fix Microsoft is working on a new version of its Internet Explorer web browser The revamp has been prompted by Microsoft s growing concern with security as well as increa'}
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    ## Test cases1
    # Top-k result =  [(8, 1), (4, 2), (4, 3)]
    # Evaluation Count =  4
    query_terms = ["the", "Ink"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases1")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases2
    # Top-k result =  [(6, 3), (6, 7)]
    # Evaluation Count =  4
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["Microsoft", "will", "Search"]
    top_k = 2
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases2")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases3
    # Top-k result =  [(12, 1), (10, 3), (10, 9)]
    # Evaluation Count =  15
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["the", "The", "a", "is"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases3")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases4
    # Top-k result =  [(6, 3), (6, 7)]
    # Evaluation Count =  4
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["Microsoft", "will", "Search"]
    top_k = 2
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases4")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases5
    # Top-k result =  [(12, 1)]
    # Evaluation Count =  2
    inverted_index = {'A': [(1, 4), (2, 4), (3, 4), (4, 4)],
                      'B': [(1, 4), (2, 4), (3, 4), (4, 4)],
                      'C': [(1, 4), (2, 4), (3, 4), (4, 4)]}
    query_terms = ["A","B","C"]
    top_k = 1
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases5")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases6
    # Top-k result =  [(14, 1), (14, 13), (12, 3)]
    # Evaluation Count =  11
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["the", "The", "a", "the"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases6")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases7
    inverted_index = {
        'a':[(1,3),(2,1),(3,1),(4,2),(5,2)],
        'b':[(1,3),(2,1),(3,1),(4,2),(6,2)],
        'c':[(1,3),(2,1),(3,1),(5,2),(6,2)],
    }
    query_terms = ["a","b","c"]
    # top-1 expected result:[(9,1)], 3
    top_k = 1
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases7")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    # top-2 expected result [(9,1),(4,4)], 6
    top_k = 2
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases7")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    # top-3 expected result [(9,1),(4,4),(4,5)], 6
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases7")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases8
    # Top-k result =  [(4, 10)]
    # Evaluation Count =  1
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["Search"]
    top_k = 4
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases8")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases9
    # Top-k result =  [(11, 2), (3, 1)]
    # Evaluation Count =  2
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["country", "cafes"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases9")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases10
    # Top-k result =  [(6, 1), (2, 2)]
    # Evaluation Count =  3
    inverted_index = {
        'a': [(1, 3), (2, 1), (3, 1)],
        'b': [(1, 3), (2, 1), (3, 1)],
    }
    query_terms = ["a","b"]
    top_k = 2
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases10")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases11
    # Top-k result =  [(12, 1), (12, 2), (12, 3)]
    # Evaluation Count =  4
    inverted_index = {
        'a': [(1, 4), (2, 4), (3, 4), (4, 1), (5, 4)],
        'b': [(1, 4), (2, 4), (3, 4), (4, 2), (6, 2)],
        'c': [(1, 4), (2, 4), (3, 4), (5, 2), (6, 2)],
    }
    query_terms = ["a", "b", "c"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases11")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)
    ## Test cases12
    # Top-k result =  
    # Evaluation Count =  
    inverted_index = Inv_Index.InvertedIndex(documents).get_inverted_index()
    query_terms = ["the", "is", "the"]
    top_k = 3
    topk_result, full_evaluation_count = WAND_Algo(query_terms, top_k, inverted_index)
    print("Test cases9")
    print('Top-k result = ', topk_result)
    print('Evaluation Count = ', full_evaluation_count)


if __name__ == '__main__':
    main()