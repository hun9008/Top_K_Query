'''    
1. Replace folder name "000012345" with your student !! 
   !!WARNING!! you will get 0 score, 
   if your folder name is "000012345"
2. Implement Fagin method
3. Implement TA method
4. Implement NRA method

Input: num_dim, top_k
    num_dim: Number of dimension
    top_k: Variable k in top-'k' query
Output: uids_result, cnt_access
    uid_result: Result of top-k uids of the scores. 
                The summation function is used 
                for the score function.

                i.e., num_dim = 4, k = 2
                ----------------------------
                 uid    D0   D1    D2    D3
                ----------------------------
                "001"    1    1     1     1
                "002"    2    2     2     2
                "003"    3    3     3     3
                "004"    5    5     5     5
                ----------------------------                
                
                score("001") = 1 + 1 + 1 + 1 = 4
                score("002") = 2 + 2 + 2 + 2 = 8
                score("003") = 3 + 3 + 3 + 3 = 12  --> top-2
                score("004") = 4 + 4 + 4 + 4 = 16  --> top-1
                
                uids_result: ["004", "003"]

    cnt_access: Number of access in each algorithm

Tip: Use Naive method to check your code
     Naive method is the free gift for the code understanding
'''
from collections import defaultdict
from typing import Tuple

def get_score(list_values) -> float:
    result = 0.0
    for v in list_values:
        result += v
    return result

class Algo():
    def __init__(self, list_sorted_entities, uid2dim2value):
        self.list_sorted_entities = list_sorted_entities

        '''
        variable for random access,
        but please do not use this variable directly.
        If you want to get the value of the entity,
        use method 'random_access(uid, dim)'
        '''
        self.__uid2dim2value__ = uid2dim2value
    
    def random_access(cls, uid, dim) -> float:
        return cls.__uid2dim2value__[uid][dim]

    def Naive(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        # read all values from the sorted lists
        uid2dim2value = defaultdict(dict)
        for dim in range(num_dim):            
            for uid,value in cls.list_sorted_entities[dim]:
                uid2dim2value[uid][dim] = value
                cnt_access += 1
        
        # compute the score and sort it
        uid2score = defaultdict(float)
        for uid, dim2value in uid2dim2value.items():
            list_values = []
            for dim in range(num_dim):
                list_values.append(dim2value[dim])
            score = get_score(list_values)
            uid2score[uid] = score
        
        sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])

        # get the top-k results
        for i in range(top_k):
            uids_result.append(sorted_uid2score[i][0])

        return uids_result, cnt_access


    # Please use random_access(uid, dim) for random access
    def Fagin(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        allFound = defaultdict(dict)
        foundUid = defaultdict(int)
        entitiesNum = len(cls.list_sorted_entities[0])
        # print(len(cls.list_sorted_entities))
        # each row
        allDim = False
        cnt = 0
        for i in range(entitiesNum):
            # each column
            if(allDim == False):
                for dim in range(num_dim):
                    cUid = cls.list_sorted_entities[dim][i][0]
                    cValue = cls.list_sorted_entities[dim][i][1]
                    if (cUid in foundUid):
                        nowCnt = foundUid[cUid]
                        foundUid[cUid] = nowCnt + 1
                    else:
                        foundUid[cUid] = 1

                    if (cUid, dim not in allFound):
                        allFound[cUid][dim] = cValue

                    cnt_access += 1

                for fUid, fValue in foundUid.items():
                    if(foundUid[fUid] == num_dim):
                        # allDim = True
                        cnt += 1
                if(cnt >= top_k):
                    allDim = True
                    cnt = 0
                    # print("find end Point!! ", i)
                    # print("uids", foundUid)
            else:
                # print("true ", i)
                # for fUid, fValue in foundUid.items():
                #     if(foundUid[fUid] < num_dim):
                uid2score = defaultdict(float)
                for uid, value in allFound.items():
                    uid_list = []
                    for dim in range(num_dim):
                        if (uid, dim is not allFound):
                            allFound[uid][dim] = cls.random_access(uid, dim)
                            cnt_access += 1
                        uid_list.append(allFound[uid][dim])
                    score = get_score(uid_list)
                    uid2score[uid] = score

                sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])

                for i in range(top_k):
                    uids_result.append(sorted_uid2score[i][0])

                break
            
        # for uid, value in cls.list_sorted_entities:   
        #     for dim in range(num_dim):
            
        return uids_result, cnt_access

    # Please use random_access(uid, dim) for random access
    def TA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        allFound = defaultdict(dict)
        uid2score = defaultdict(float)
        entitiesNum = len(cls.list_sorted_entities[0])
        for i in range(entitiesNum):
            threshold = 0
            for dim in range(num_dim):
                cUid = cls.list_sorted_entities[dim][i][0]
                cValue = cls.list_sorted_entities[dim][i][1]

                if ((cUid, dim) not in allFound):
                    allFound[cUid][dim] = cValue
                    cnt_access += 1
                    # print("array retreive")
                
                threshold += cValue

            # print("threshold : ", threshold, " i : ", i)
            for uid, value in allFound.items():
                uid_list = []
                if(uid not in uid2score):
                    for dim in range(num_dim):

                        if ((uid, dim) in allFound):
                            uid_list.append(allFound[uid][dim])
                        else:
                            allFound[uid][dim] = cls.random_access(uid, dim)
                            cnt_access += 1
                            uid_list.append(allFound[uid][dim])
                    score = get_score(uid_list)
                    uid2score[uid] = score
            
            sorted_uid2score = sorted(uid2score.items(), key = lambda x : -x[1])
            # print(len(sorted_uid2score))

            FoundTopK = False
            top_k_uid2score = []
            if (len(sorted_uid2score) >= top_k):
                top_k_uid2score = sorted_uid2score[:top_k]
                # print("top_k_list : ", top_k_uid2score)
                FoundTopK = True
            else:
                # top_k_uid2score = sorted_uid2score
                FoundTopK = False

            # 2번째 threshold..부터
            if(FoundTopK):
                if(threshold <= top_k_uid2score[-1][1]):
                    for i in range(top_k):
                        uids_result.append(top_k_uid2score[i][0])
                    # print("threshold : ", threshold, " minimum topK : ", top_k_uid2score[-1][1])
                    break

            # if(len(sorted_uid2score) > 100):
            #     break
        
        

        return uids_result, cnt_access

    # You cannot use random access in this method
    def NRA(cls, num_dim, top_k) -> Tuple[list, int]:
        uids_result = []
        cnt_access = 0

        allFound = defaultdict(dict)
        Lb_Ub_score = defaultdict(float)
        entitiesNum = len(cls.list_sorted_entities[0])
        for i in range(entitiesNum):
            lowerBound = defaultdict(float)
            upperBound = defaultdict(float)

            for dim in range(num_dim):
                cUid = cls.list_sorted_entities[dim][i][0]
                if (cUid in Lb_Ub_score):
                    # Lb_Ub = Lb_Ub_score[cUid]
                    lowerBound[cUid] = Lb_Ub_score[cUid][0]
            
            for dim in range(num_dim):
                cUid = cls.list_sorted_entities[dim][i][0]
                cValue = cls.list_sorted_entities[dim][i][1]

                for dim_ub in range(num_dim):
                    local_min_value = cls.list_sorted_entities[dim_ub][i][1]
                    if((cUid, dim_ub) not in allFound):
                        upperBound[cUid] += local_min_value
                    else:
                        upperBound[cUid] += allFound[cUid][dim_ub]

                if ((cUid, dim) not in allFound):
                    allFound[cUid][dim] = cValue
                    cnt_access += 1
                
                lowerBound[cUid] += cValue
                
            for uid in upperBound:
                if(uid in Lb_Ub_score):
                    current_lb = Lb_Ub_score[uid][0]
                    current_ub = Lb_Ub_score[uid][1]
                    if(current_ub > upperBound[uid]):
                        Lb_Ub_score[uid] = (current_lb, upperBound[uid])
                else:
                    Lb_Ub_score[uid] = (0, upperBound[uid])
            
            for uid in lowerBound:
                if(uid in Lb_Ub_score):
                    current_lb = Lb_Ub_score[uid][0]
                    current_ub = Lb_Ub_score[uid][1]
                    if(current_lb < lowerBound[uid]):
                        Lb_Ub_score[uid] = (lowerBound[uid], current_ub)
                        # if(current_lb != 0):
                        #     print("lowerbound updated at i : ", i)
                        #     print("to : ", lowerBound[uid])
                else:
                    print("나 안함 씨벌것")
                    break

            sorted_Lb_Ub = sorted(Lb_Ub_score.items(), key=lambda x: -x[1][0])
            
            # if (i % 1000 == 0):
            #     keys = [ key[0] for key in sorted_Lb_Ub]
            #     for key in keys:
            #         for i in sorted_Lb_Ub:
            #             if i[0] ==key:
            #                 print(i)
            #     print("================")
                # for i  in sorted_Lb_Ub[:10]:
                #     print(i)

            FoundTopK = False
            top_k_Lb_Ub = []
            if (len(sorted_Lb_Ub) > top_k):
                top_k_Lb_Ub = sorted_Lb_Ub[:top_k]
                FoundTopK = True
                # print("found top K i : ", i)
            else:
                FoundTopK = False


            endpoint = False
            if(FoundTopK):

                lb_min = top_k_Lb_Ub[-1][1][0]
                ex_topk = sorted_Lb_Ub[top_k:]
                up_list =  [ i[1][1] for i in ex_topk]
                up_max = max(up_list)
                endpoint = True
                if(len(sorted_Lb_Ub) == top_k):
                    endpoint = False


                for key, (lb, ub) in sorted_Lb_Ub[top_k:]:

        
                    if(lb_min < ub):
                        endpoint = False
                        break

            if (endpoint):
                
                for t in range(top_k):
                    uids_result.append(top_k_Lb_Ub[t][0])

                # print("last line : ", i)
                break
        
        return uids_result, cnt_access
