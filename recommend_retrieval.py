'''
输入仅一个症状

input:
    symp: string. 输入的症状. 仅一个
    data_path: string. 检索对象的文件path. 格式为 s1 s2 s3\th1 h2 h3. s为症状, 空格分割. h为中药, 空格分隔. 两者\t分割
    result_num: int. 返回的药方个数. 若症状完全匹配则返回对应的药方, 一般为1个. 该参数失效.  

return: list( list(string), list(string) ) # symps_list, herbs_list

检索逻辑:
1. 若症状完全匹配, 返回对应的1个药方.
2. 若不完全匹配, 按照被检索数据中症状集合的个数从小到大排序, 取前result_num个.

'''

def herb_retrieval_input_only_one_symp(symp, data_path, result_num):
    # 全部的结果
    all_result = []
    # 全匹配的结果
    all_match_result = []

    with open(data_path, 'r') as f:
        for line in f.readlines():
            symps, herbs = line.strip().split('\t')
            symps_list = symps.split(' ')
            herbs_list = herbs.split(' ')
            if symp in symps_list:
                all_result.append([symps_list, herbs_list])
                if len(symps_list) == 1:
                    all_match_result.append([symps_list, herbs_list])

    if len(all_match_result) > 0:
        return [all_match_result[0]]

    sorted_result = sorted(all_result, key=lambda x:len(x[0]))
    result_num = min(result_num, len(sorted_result))

    return sorted_result[:result_num]

'''
输入至少两个症状

input:
    symp: list(string). 输入的症状list
    data_path: string. 检索对象的文件path. 格式为 s1 s2 s3\th1 h2 h3. s为症状, 空格分割. h为中药, 空格分隔. 两者\t分割
    result_num: int. 返回的药方个数. 若症状完全匹配则返回对应的药方, 一般为1个. 该参数失效.  

return: list( list(string), list(string) ) # symps_list, herbs_list

检索逻辑:
1. 若症状完全匹配, 返回对应的1个药方.
2. 若不完全匹配: 
    a. 若 输入症状list 全部出现在 被检索数据中症状集合 中, 取全部对应药方, 按 被检索数据中症状集合 的症状个数从小到大排序, 取前result_num个.
    b. 没有a则: 按照 输入症状list 和 被检索数据中症状集合 的交集占比 (哪个集合大哪个集合是分母) 从大到小排序, 取前result_num个.
        i. 若 被检索数据中症状集合 全部出现在 输入症状list中, 取全部对应药方
        ii. 否则输出全部result_num个.

'''
def herb_retrieval_input_at_least_two_symps(input_symps, data_path, result_num):
    # 全部结果
    all_result = []
    # 全匹配的结果
    all_match_result = []
    # 输入症状list 全部出现在 被检索数据中症状集合 的结果
    all_in_result = []

    with open(data_path, 'r') as f:
        for line in f.readlines():
            symps, herbs = line.strip().split('\t')
            symps_list = symps.split(' ')
            herbs_list = herbs.split(' ')

            intersection = list(set(symps_list) & set(input_symps))

            if set(intersection) == set(input_symps):
                if set(intersection) == set(symps_list):
                    all_match_result.append([symps_list, herbs_list])
                else:
                    all_in_result.append([symps_list, herbs_list]) 
            elif len(intersection) > 0:
                p = 0
                if len(intersection) >= len(symps_list):
                    p = len(intersection) / len(input_symps)
                else:
                    p = len(intersection) / len(symps_list)
                all_result.append([symps_list, herbs_list, p])

    if len(all_match_result) > 0:
        return all_match_result[0]
    
    if len(all_in_result) > 0:
        return all_in_result[:result_num]
    
    sorted_result = sorted(all_result, key=lambda x:x[-1], reverse=True)
    result_num = min(result_num, len(sorted_result))
    sorted_result = [[i[0], i[1]] for i in sorted_result[:result_num]]
    
    sorted_all_in_result = [i for i in sorted_result if set(i[0]) < set(input_symps)]
    if len(sorted_all_in_result) > 0:
        return sorted_all_in_result

    return sorted_result

'''
input:
    symp: list(string). 输入的症状list
    data_path: string. 检索对象的文件path. 格式为 s1 s2 s3\th1 h2 h3. s为症状, 空格分割. h为中药, 空格分隔. 两者\t分割
    result_num: int. 返回的药方个数. 若症状完全匹配则返回对应的药方, 一般为1个. 该参数失效.  

return: list(list(string)). # herbs_list
'''

def main(input_symps, data_path, result_num):
    result_herbs = []

    symps_herbs_list = []
    if len(input_symps) == 1:
        symps_herbs_list = herb_retrieval_input_only_one_symp(input_symps[0], data_path, result_num)
    elif len(input_symps) > 1:
        symps_herbs_list = herb_retrieval_input_at_least_two_symps(input_symps, data_path, result_num)

    for i in symps_herbs_list:
        if i[1] not in result_herbs:
            result_herbs.append(i[1])

    return result_herbs


if __name__ == '__main__':
    data_path = './SHL_core_clean.txt'

    symps_list = ['下痢']

    result = main(symps_list, data_path, 5)

    print(result)