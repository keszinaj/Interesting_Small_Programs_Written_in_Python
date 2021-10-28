# made by keszinaj
'''
    Function takes the election results of parties over the threshold and the number of available seats, 
    and returns the number of seats per party count using D'Hondt method.
'''
def dhondt_method(election_result, seats):
    
    #    I want to have  
    #    (1) dict_party_and_score = {'150' = ["PO", "PSL"]...}
    #    (2) array_of_all_scores = [... , 150, ..., 100, ..., 40, ...] 
    
    dict_party_and_score = {}
    array_of_all_scores = []

    for l  in range(1, seats + 1, 1):
        for p in election_result:
            c = election_result[p]/l
            array_of_all_scores.append(c)
            if c in dict_party_and_score:
                dict_party_and_score[c].append(p)                
            else:
                dict_party_and_score[c] = [ p ]
    array_of_all_scores.sort(reverse = True)

    #print(dict_party_and_score)
    #print(array_of_all_scores)

    # dict which will contain ["party": seats]
    number_of_seats_per_party = {}
    for p in election_result:
        number_of_seats_per_party[p] = 0


    i = 0

    while seats > 0:
        weight_of_votes = array_of_all_scores[i]
        i += 1
        parties_with_the_same_weight_votes = dict_party_and_score[weight_of_votes]
        num_parties_the_same_weight_votes = len(parties_with_the_same_weight_votes)
        # if we can give seat for every party with n weight of vote
        if num_parties_the_same_weight_votes < seats :
            for p in parties_with_the_same_weight_votes:
                number_of_seats_per_party[p] += 1
            seats -= num_parties_the_same_weight_votes
        
        # If there are more parties with the same weight of votes then seats, 
        # then Polish law gives a seat to the party with the greater number of votes overall
        else: 
            # https://stackoverflow.com/questions/613183/how-do-i-sort-a-dictionary-by-value?page=1&tab=votes#tab-top
            sorted_election_result ={k: v for k, v in sorted(election_result.items(), key=lambda item: item[1], reverse=True)}
            for p in sorted_election_result:
                if seats > 0 and p in parties_with_the_same_weight_votes:
                    number_of_seats_per_party[p] += 1
                    seats -= 1 
                elif seats == 0:
                    break
    return(number_of_seats_per_party)
