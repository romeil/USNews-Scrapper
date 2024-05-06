import locale

locale.setlocale(locale.LC_ALL, '')

class College:
    def __init__(self, name, state, rank, tuition, acceptance_rate, sat_range, act_range, 
                 engineering_rep_score, business_rep_score, cs_rep_score, nursing_rep_score):
        self.__name = name
        self.__state = state
        self.__rank = rank
        self.__tuition = tuition
        self.__acceptance_rate = acceptance_rate
        self.__sat_range = sat_range
        self.__act_range = act_range
        self.__engineering_rep_score = engineering_rep_score
        self.__business_rep_score = business_rep_score
        self.__cs_rep_score = cs_rep_score
        self.__nursing_rep_score = nursing_rep_score

    @classmethod
    def getFromJSON(cls, json_data):
        name = state = rank = tuition = acceptance_rate = sat_range = act_range = None
        engineering_rep_score = business_rep_score = cs_rep_score = nursing_rep_score = None
        
        try:        
            name = json_data["institution"]["displayName"]
        except KeyError:
            pass

        try:
            state = json_data["institution"]["state"]
        except KeyError:
            pass

        try:
            rank = int(json_data["parent"]["sortRank"])
        except KeyError:
            pass
        
        try: 
            tuition = locale.atof(json_data["searchData"]["tuition"]["displayValue"].replace("$", ""))
        except (KeyError, AttributeError):
            tuition = locale.atof(json_data["searchData"]["tuition"]["displayValue"][0]["value"].replace("$", ""))
        except ValueError:
            pass
        
        try:
            acceptance_rate = float(json_data["searchData"]["acceptanceRate"]["displayValue"].strip("%"))/100
        except KeyError:
            pass

        try:
           sat_range = json_data["searchData"]["testAvgs"]["displayValue"][0]["value"]
        except KeyError:
            pass

        try:
            act_range = json_data["searchData"]["testAvgs"]["displayValue"][1]["value"]
        except KeyError:
            pass

        try:
            engineering_rep_score = float(json_data["searchData"]["engineeringRepScore"]["rawValue"])
        except (KeyError, ValueError, TypeError):
            pass

        try:
            business_rep_score = float(json_data["searchData"]["businessRepScore"]["rawValue"])
        except (KeyError, ValueError, TypeError):
            pass

        try:
            cs_rep_score = float(json_data["searchData"]["computerScienceRepScore"]["rawValue"])
        except (KeyError, ValueError, TypeError):
            pass

        try:
            nursing_rep_score = float(json_data["searchData"]["nursingRepScore"]["rawValue"])
        except (KeyError, ValueError, TypeError):
            pass

        return cls(name, state, rank, 
                   tuition, acceptance_rate, sat_range, act_range, 
                   engineering_rep_score, business_rep_score, cs_rep_score, nursing_rep_score)

    def __iter__(self):
        yield self.__rank
        yield self.__name
        yield self.__state
        yield self.__tuition
        yield self.__acceptance_rate
        yield self.__sat_range
        yield self.__act_range
        yield self.__engineering_rep_score
        yield self.__business_rep_score
        yield self.__cs_rep_score
        yield self.__nursing_rep_score

    def __str__(self):
        return "name : {} \nstate : {} \nrank : {} \ntuition : {}  \nacceptance rate : {} \nsat range : {} \n"\
               "act range : {} \nengineering score : {} \ncomputer science score : {} \nbusiness score : {} \n"\
               "computer science score : {} \nnursing score : {}".format(self.__name, self.__state, self.__rank, 
                                                                         self.__tuition, self.__acceptance_rate, 
                                                                         self.__sat_range, self.__act_range, 
                                                                         self.__engineering_rep_score, self.__business_rep_score, 
                                                                         self.__cs_rep_score, self.__nursing_rep_score)
    