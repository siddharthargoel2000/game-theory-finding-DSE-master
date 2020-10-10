import sys
import numpy as np

def computeSDS( file_name ):
    
    # parse the file and get me all the required details
    game = NfgGameParser.parse_nfg_file(file_name)
    
    num_players = len(game['players'])
    strategies = list(map(int,game['no_of_strategies']))
    counter = 0
    multiplier = []
    temp = 1
    equilibria = []
    
    for i in range(len(strategies)):
        multiplier.append(temp)
        temp = temp * strategies[i]
        
    playerslist = list(range(num_players))
    return_value = -1
    strong_eq = []
    gamedata = []
    for x in np.nditer(game['pay_off_values']):
        gamedata.append(float(x))
    
    
    def select_index(player, args):
        result = 0
        for idx, arg in enumerate(args):
            result = result + (arg * multiplier[idx])
        result = result * num_players
        result += player
        return result
        
    def check_strong(playerno, totalplayer, topplayer, strategyarr = [], eqindex = -1):
        if(len(totalplayer) >= 1):
            cur_player = totalplayer[0]
            totalplayer = totalplayer[1:]
            temp = 0
            for strategy in range(strategies[cur_player]):
                # print "First eqindex ", eqindex
                temparray = strategyarr[:]
                # print "Tempar ", temparray
                temparray.append(strategy)
                temp = check_strong(playerno, totalplayer, topplayer, temparray, eqindex)
                # print "Temp value ", temp
                if(temp == -sys.maxsize): 
                    return temp
                else: 
                    eqindex = temp
            return temp
        else:
            # print "Eqindex ", eqindex
            max_payoff = -sys.maxsize
            max_index = -1
            other_payoffs = []
            for strategy in range(strategies[playerno]):
                temp1 = strategyarr[:]
                # print "T1 ", temp1
                temp1.insert(playerno, strategy)
                cur_payoff = gamedata[select_index(playerno, temp1)]
                if( max_payoff < cur_payoff):
                    max_payoff = cur_payoff
                    max_index = strategy
                else:
                    other_payoffs.append(cur_payoff)
            if(max_payoff in other_payoffs):
                return -sys.maxsize
            if( eqindex == -1 ):
                eqindex = max_index
            elif( eqindex != max_index ):
                return -sys.maxsize
            return eqindex
        
        
    # print check_strong(0, [1, 2], 1)
    for i in range(num_players):
        tempplayerlist = playerslist[:]
        tempplayerlist.remove(i)
        # print i, tempplayerlist, tempplayerlist[0]
        value = check_strong(i, tempplayerlist, tempplayerlist[0]) 
        if value == -sys.maxsize:
            # print "No Strongly Dominant Strategy equilibrium exists"
            return_value = 0
            break
        else:
            strong_eq.append(value)
        
                    
    if return_value == -1:
        # print "Strongly dominant strategy equilibrium (in order of P1, P2, ... ,Pn) is:",
        counter = counter + 1
        # print(strong_eq)
        equilibria.append(strong_eq)
        # for i in strong_eq:
        #     print(i, end=" ")
        # print()
        
    if (counter):
        res_list = []
        for equilibrium in equilibria:
            for j in range(len(equilibrium)):
                for i in range(strategies[j]):
                    if i == equilibrium[j]:
                        res_list.append(1)
                    else:
                        res_list.append(0)
            return (res_list)   # <<<<<<<<<<<<<<<-------------
            
    
    
def computeWDS( file_name ):
# Add file name here-------->>>
    # parse the file and get me all the required details
    game = NfgGameParser.parse_nfg_file(file_name)

    #Assigning Inputs
    num_players = len(game['players'])
    strategies = list(map(int,game['no_of_strategies']))
    counter = 0
    multiplier = []
    temp = 1
    equilibria = []
    
    for i in range(len(strategies)):
        multiplier.append(temp)
        temp = temp * strategies[i]
        
    playerslist = list(range(num_players))
    return_value = -1
    gamedata = []
    for x in np.nditer(game['pay_off_values']):
        gamedata.append(float(x))
    
    
    def select_index(player, args):
        result = 0
        for idx, arg in enumerate(args):
            result = result + (arg * multiplier[idx])
        result = result * num_players
        result += player
        return result

    def check_weak(playerno, totalplayer, topplayer, eqindex, strategyarr = []):
        if(len(totalplayer) >= 1):
            cur_player = totalplayer[0]
            temp = 0
            totalplayer = totalplayer[1:]
            for strategy in range(strategies[cur_player]):
                # print "First eqindex ", eqindex
                temparray = strategyarr[:]
                # print "Tempar ", temparray
                temparray.append(strategy)
                temp, eqindex = check_weak(playerno, totalplayer, topplayer, eqindex, temparray)
                # print "Temp value ", temp
                if( temp == -sys.maxsize):
                    return temp, eqindex
            return temp, eqindex
        else:
            # print "Eqindex ", eqindex
            max_payoff = -sys.maxsize
            max_index = []
            for strategy in range(strategies[playerno]):
                temp1 = strategyarr[:]
                # print "T1 ", temp1
                temp1.insert(playerno, strategy)
                cur_payoff = gamedata[select_index(playerno, temp1)]
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
        global counter
        if start < num_players - 1:
            for i in indexes[start]:
                tempvalues = valueindexes[:]
                tempvalues.append(i)
                print_weak(indexes, tempvalues, start + 1)
        else:
            for i in indexes[start]:
                tempresult = valueindexes[:]
                tempresult.append(i)
                counter = counter + 1
                equilibria.append(tempresult)
            
    min_eq_list = []
    for i in range(num_players):
        tempplayerlist = playerslist[:]
        tempplayerlist.remove(i)
        result_index = [-1]
        value, result_index = check_weak(i, tempplayerlist, tempplayerlist[0], result_index)
        if value == -sys.maxsize or len(result_index) == strategies[i]:
            print("There does not exists Dominant Strategy Equilibrium")
            return_value = -2
            break
        else:
            min_eq_list.append(result_index)

    if return_value != -2:
        # print "Weakly dominant strategy equilibrium(s) is (are): "
        # final result list        
        res_list = []
        for j in range(len(min_eq_list)):
            for i in range(strategies[j]):
                if [i] == min_eq_list[j]:
                    res_list.append(1)
                else:
                    res_list.append(0)
        return (res_list)   # <<<<<<<<<<<<<<<-------------
    if (counter):
        res_list = []
        wdse_list = []
        for equilibrium in equilibria:
            for j in range(len(equilibrium)):
                for i in range(strategies[j]):
                    if i == equilibrium[j]:
                        res_list.append(1)
                    else:
                        res_list.append(0)
            wdse_list.append(res_list)   # <<<<<<<<<<<<<<<-------------
        final_list = [0]*len(wdse_list[0])
        for i in range(len(wdse_list)):
            for j in range(len(wdse_list[0])):
                if wdse_list[i][j]==1:
                    final_list[j]=1
        return final_list