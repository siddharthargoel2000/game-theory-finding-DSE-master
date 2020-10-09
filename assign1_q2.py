# importing libraries
import sys
import numpy as np  
import re

#_______________________________________________________________________________________________________
# exception to be thrown in case the file format is invalid
class InvalidFileException(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        #print('calling str')
        if self.message:
            return 'InvalidFileException: {0} '.format(self.message)
        else:
            return 'InvalidFileException has been raised'



class NfgGameParser(object):
    # various error messages used by the InvalidFileException
    EXTREME_VERSIONS_MESSAGE = "\nInvalid Format, We have included examples of our test formats of input .nfg file inside NfgTestCases folder, kindly take a look at it and " \
                               "do the corrections that are required "

    WRONG_NUMBER_OF_STRATEGIES = "\nnumber of strategies passed seems to be wrong with respect to number of players, kindly correct it."

    NON_POSITIVE_INTEGER_STRATEGY_VALUES = "\n number of Strategies passed is not an integer value, kindly check"

    WRONG_NUMBER_OF_PAYOFF_VALUES = "\nno of pay off values passed seems to be wrong with respect to number of players, kindly correct it."

    WRONG_PAYOFF_VALUES_FORMAT = "\npayoff values format doesn't seem to be right, kindly check"


    # return game dictionary keys and the value types
    # string
    GAME_NAME = "game_name"

    # tuple of strings
    PLAYERS = "players"

    # tuple of integers
    NO_OF_STRATEGIES = "no_of_strategies"

    # string
    GAME_COMMENT = "game_comment"

    # N-d Array, payoff[0][2][1][3] means
    # player-1 using 3rd strategy
    # player-2 using 1st strategy
    # player-3 using 2nd strategy
    # player-4 using 1st strategy
    PAY_OFF_VALUES = "pay_off_values"

    @classmethod
    # function to parse the NFG file
    def parse_nfg_file( cls, filename ):

        # print the file name for verifying, used it while testing
        print(filename + " : ")

        # read the lines of the file
        with open(filename, 'r') as infile:
            lines = ' '.join(infile.readlines())         # regex will takecare of the newline character

        # regex matching
        # old regex , 'NFG *1 *R *"(.*?)" *{(.*?)} *{(.*?)}(?: *"(.*?)")? *(.+)'
        # NOTE: '\s' will match wide range of whitespace characters, instead of just 'space' character
        match_obj = re.match('NFG\s+1\s+R\s+"(.*?)"\s+{(.*?)}\s+{(.*?)}(?:\s+"(.*?)")?\s+(.+)', lines)

        # try to extract the values
        try:
            game_name, players_str, no_of_strategies_str, game_comment, payoff_values_str = match_obj.groups()
        except AttributeError:
            raise InvalidFileException(cls.EXTREME_VERSIONS_MESSAGE)
        except Exception:
            raise InvalidFileException(cls.EXTREME_VERSIONS_MESSAGE)

        # we have players
        players = [player for player in re.findall('"(.+?)"', players_str.strip())]
        # this needs further processing
        no_of_strategies_str = no_of_strategies_str.strip().split()
        payoff_values_str = payoff_values_str.strip().split()
        #print(no_of_strategies_str)
        #print(payoff_values_str)

        # check the counter of strategies against the no of players
        no_of_players = len(players)
        if (len(no_of_strategies_str) != no_of_players):
            raise InvalidFileException(cls.WRONG_NUMBER_OF_STRATEGIES)

        # extract the values in a list
        no_of_strategies = []
        total_combinations = 1
        for count_str in no_of_strategies_str:
            try:
                counter = int(count_str)
            except ValueError:
                InvalidFileException(cls.NON_POSITIVE_INTEGER_STRATEGY_VALUES)

            no_of_strategies.append(counter)
            total_combinations *= counter

        # check the counter of strategies against no of players and no of strategies
        if (len(payoff_values_str) / no_of_players != total_combinations):
            raise InvalidFileException(cls.WRONG_NUMBER_OF_PAYOFF_VALUES)

        # extract the payoff values as tuples
        payoff_values = []
        for i in range(0,len(payoff_values_str),no_of_players):
            payoff_single = []
            for j in range (i,i+no_of_players,1):
                try:
                    #print(payoff_values_str[j])
                    # NOTE: consider using float/int instead of eval
                    evaluated = float(payoff_values_str[j])
                    #print(evaluated)
                except Exception:
                    raise InvalidFileException (cls.WRONG_PAYOFF_VALUES_FORMAT)
                payoff_single.append(evaluated)

            #print(payoff_single)
            payoff_single = tuple(payoff_single)
            payoff_values.append(payoff_single)

        # we will use a list of lists to intialise the N-d Array
        # for getting this list of lists, we need to extract data with respect to different dimensions
        last_list = payoff_values
        for dimension in no_of_strategies[0:len(no_of_strategies)-1]:
            new_list = []
            for i in range(0,len(last_list), dimension):
                l = last_list[i:i+dimension]
                new_list.append(l)
            #print(new_list)
            last_list = new_list

        # n-d array declaration
        payoff_values = np.array(last_list)
        #print(payoff_values[3][0][2])
        # create tuples so that it can't be modified later
        no_of_strategies = tuple(no_of_strategies)
        players = tuple(players)


        #print(payoff_values[0][0], payoff_values[0][1], payoff_values[1][0],payoff_values[2][1] )
        # create a dict for output
        game = { cls.GAME_NAME : game_name, cls.PLAYERS : players, cls.GAME_COMMENT : game_comment, cls.NO_OF_STRATEGIES:no_of_strategies ,
                 cls.PAY_OFF_VALUES : payoff_values }
        return game
#Functions________________________________________________________________________________________________
#

def select_index(player, args):
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
            

#_________________________________________________________________________________________________________
#Checking on the examples for exceptions, NFG format

for count in range(1,4):
    
    # Add file name here-------->>>
    file_name = 'D:\ACADEMICS 5th\CS771A\game-theory-finding-DSE-master\Example{}.nfg'.format(count)
    try:
        game = NfgGameParser.parse_nfg_file(file_name);
    except InvalidFileException as e: # exception handling
        print(e)
    except Exception as e:
        print("other exception :\n" + str(e))
    
    #Assigning Inputs
    gameinfo = game['game_name']
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
        gamedata.append(int(x))
            
        
    # print find_strongly_dominant_eq(0, [1, 2], 1)
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
        counter = counter + 1
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
            print(res_list)   # <<<<<<<<<<<<<<<-------------
    
    if (counter):
        res_list = []
        for equilibrium in equilibria:
            for j in range(len(equilibrium)):
                for i in range(strategies[j]):
                    if i == equilibrium[j]:
                        res_list.append(1)
                    else:
                        res_list.append(0)
            print(res_list)   # <<<<<<<<<<<<<<<-------------