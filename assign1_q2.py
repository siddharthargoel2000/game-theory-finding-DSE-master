#!/usr/bin/python
import sys
# import time
# start_time = time.time()

f = open(sys.argv[1], "r")
gameinfo = f.readline()
data = f.readline().split(" ")
data = data[data.index("{") + 1: data.index("}\n")]
data = data[data.index("{") + 1:]
num_players = len(data)
strategies = list(map(int, data))
multiplier = []
temp = 1
count = 0
equilibria = []
for i in range(len(strategies)):
    multiplier.append(temp)
    temp = temp * strategies[i]

f.readline()
data = f.readline().split(" ")
# print data
gamedata = list(map(int, data))

def sel_index(player, args):
    result = 0
    for idx, arg in enumerate(args):
        result = result + (arg * multiplier[idx])
    result = result * num_players
    result += player
    return result

def find_strongly_dominant_eq(playerno, totalplayer, topplayer, strategyarr = [], eqindex = -1):
    if(len(totalplayer) >= 1):
        cur_player = totalplayer[0]
        totalplayer = totalplayer[1:]
        temp = 0
        for strategy in range(strategies[cur_player]):
            # print "First eqindex ", eqindex
            temparray = strategyarr[:]
            # print "Tempar ", temparray
            temparray.append(strategy)
            temp = find_strongly_dominant_eq(playerno, totalplayer, topplayer, temparray, eqindex)
            # print "Temp value ", temp
            if(temp == -sys.maxsize): return temp
            else: eqindex = temp
        return temp
    else:
        # print "Eqindex ", eqindex
        max_payoff = -sys.maxsize
        max_index = -1
        other_payoffs = []
        other_index = []
        for strategy in range(strategies[playerno]):
            temp1 = strategyarr[:]
            # print "T1 ", temp1
            temp1.insert(playerno, strategy)
            cur_payoff = gamedata[sel_index(playerno, temp1)]
            if( max_payoff < cur_payoff):
                max_payoff = cur_payoff
                max_index = strategy
            else:
                other_payoffs.append(cur_payoff)
                other_index = strategy
        if(max_payoff in other_payoffs):
            return -sys.maxsize
        if( eqindex == -1 ):
            eqindex = max_index
        elif( eqindex != max_index ):
            return -sys.maxsize
        return eqindex

def find_weakly_dominant_eq(playerno, totalplayer, topplayer, eqindex, strategyarr = []):
    if(len(totalplayer) >= 1):
        cur_player = totalplayer[0]
        temp = 0
        totalplayer = totalplayer[1:]
        for strategy in range(strategies[cur_player]):
            # print "First eqindex ", eqindex
            temparray = strategyarr[:]
            # print "Tempar ", temparray
            temparray.append(strategy)
            temp, eqindex = find_weakly_dominant_eq(playerno, totalplayer, topplayer, eqindex, temparray)
            # print "Temp value ", temp
            if( temp == -sys.maxsize):
                return temp, eqindex
        return temp, eqindex
    else:
        # print "Eqindex ", eqindex
        max_payoff = -sys.maxsize
        other_payoffs = []
        max_index = []
        for strategy in range(strategies[playerno]):
            temp1 = strategyarr[:]
            # print "T1 ", temp1
            temp1.insert(playerno, strategy)
            cur_payoff = gamedata[sel_index(playerno, temp1)]
            if( max_payoff < cur_payoff):
                max_payoff = cur_payoff
                max_index = []
                max_index.append(strategy)
            elif max_payoff == cur_payoff:
                max_index.append(strategy)
        if eqindex[0] == -1:
            eqindex = max_index
        else:
            temp_index = list(set(eqindex) & set(max_index))
            eqindex = temp_index[:]
        if not eqindex:
            return -sys.maxsize, eqindex
        else:
            return eqindex[0], eqindex

def print_weak(indexes, valueindexes = [], start = 0):
    global count
    if start < num_players - 1:
        for i in indexes[start]:
            tempvalues = valueindexes[:]
            tempvalues.append(i)
            print_weak(indexes, tempvalues, start + 1)
    else:
        for i in indexes[start]:
            tempresult = valueindexes[:]
            tempresult.append(i)
            count=count+1
            # print(tempresult)
            equilibria.append(tempresult)
            # for v in tempresult:
            #     print(v, end=" ")
            # print()

# print find_strongly_dominant_eq(0, [1, 2], 1)
playerslist = list(range(num_players))
return_value = -1
strong_eq = []
for i in range(num_players):
    tempplayerlist = playerslist[:]
    tempplayerlist.remove(i)
    # print i, tempplayerlist, tempplayerlist[0]
    value = find_strongly_dominant_eq(i, tempplayerlist, tempplayerlist[0]) 
    if value == -sys.maxsize:
        # print "No Strongly Dominant Strategy equilibrium exists"
        return_value = 0
        break
    else:
        strong_eq.append(value)
if return_value == -1:
    # print "Strongly dominant strategy equilibrium (in order of P1, P2, ... ,Pn) is:",
    count=count+1
    # print(strong_eq)
    equilibria.append(strong_eq)
    # for i in strong_eq:
    #     print(i, end=" ")
    # print()
else:
    min_eq_list = []
    for i in range(num_players):
        tempplayerlist = playerslist[:]
        tempplayerlist.remove(i)
        result_index = [-1]
        value, result_index = find_weakly_dominant_eq(i, tempplayerlist, tempplayerlist[0], result_index)
        if value == -sys.maxsize or len(result_index) == strategies[i]:
            print("No Dominant Strategy Equilibria exist")
            return_value = -2
            break
        else:
            min_eq_list.append(result_index)

    if return_value != -2:
        # print "Weakly dominant strategy equilibrium(s) is (are): "
        # print min_eq_list
        print_weak(min_eq_list)

if (count):
    print(count)
    for equilibrium in equilibria:
        for i in equilibrium:
            print(i, end=" ")
        print()
# print()
# print("--- %s ---" % (time.time() - start_time))
