# made by keszinaj
import matplotlib.pyplot as plt
from election_data import election_results_from_nibyland, special_paries, political_parties
from dhondt_methon_implementation import dhondt_method



'''
    Function return parties which reach the election threshold(5% or "special") and the number of votes cast for them
'''
def parties_beyond_threshold(input_data):
    votes_per_party = {} 
    for p in political_parties:
        votes_per_party[p] = 0
    num_all_votes = 0

    # count all votes
    for i in range(len(input_data)):
        votes_per_party[input_data[i]['party']] += input_data[i]['votes']  
        num_all_votes += input_data[i]['votes']

    # first loop finds parties under threshold, second loop remove them 
    parties_under_threshold =[]
    for i in votes_per_party:
        if i in special_paries:
            continue
        else:
            if votes_per_party[i]/num_all_votes < 0.05:
                votes_per_party[i] = -1
                parties_under_threshold.append(i)
            else:
                continue
    for i in parties_under_threshold:
        del votes_per_party[i]

    return votes_per_party



'''
    Function takes number of seats per party count using D'Hondt method and default data from election, 
    and returns names of politican which will have a seat in goverment
'''
def final_result(num_of_seats_per_party, input_data):
    #sorted_wynik_wyb ={k: v for k, v in sorted(wynik_wyb.items(), key=lambda item: item[1], reverse=True)}
    seats_list = {}
    # go through every party and sort every candidate per votes
    for p in political_parties:
        sorted_input_data = {}
        for i in range(len(input_data)):
           if input_data[i]['party'] == p:
               sorted_input_data[input_data[i]['name']] = input_data[i]['votes'] 
        sorted_input_data ={k: v for k, v in sorted(sorted_input_data.items(), key=lambda item: item[1], reverse=True)}
        seats_list[p] = []
        try:
            num_of_seats = num_of_seats_per_party[p]
            for l in sorted_input_data:
                if(num_of_seats > 0):
                    seats_list[p].append(l)
                    num_of_seats -= 1
                else:
                   break
        except:
            continue  
    return(seats_list)



'''
    Function take input count using D'Hondt method and save chart
'''
def chart(data):
    values = []
    labels = []
    try:
        for i in data:
            if data[i]> 0:
                labels.append(i)
                values.append(data[i])
        plt.pie(values, labels=labels, autopct='%.2f')
    #plt.pie(values, labels=labels)
        plt.show()
        plt.savefig("results.png")
    except:
        print("chart doesn't save")



'''
    Function main
'''
def main(input_data, seats):
    votes_per_party = parties_beyond_threshold(input_data)
    num_of_seats_per_party = dhondt_method(votes_per_party, seats)
    chart(num_of_seats_per_party)
    return final_result(num_of_seats_per_party, input_data)




print(main(election_results_from_nibyland, 5))




