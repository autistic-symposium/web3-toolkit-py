#!/usr/bin/env python3

# Examples from the exercise.
id_list1 = [122, 144, 122, 144, 182]
id_list1_return = [122, 123, 144, 145, 182]
id_list2 = [13458, 13890, 13890, 144568, 144568]
id_list2_return = [13458, 13890, 13891, 144568, 144569]

# Additional examples,
id_list3 = []
id_list4 = [0, 0, 0, 0, 0]
id_list4_return = [0, 1, 2, 3, 4]


def deduplicate_copilots_ids(id_list):
    ''' Take an array of unsorted integer IDs and use sequential
    addition to deduplicate. Returns a sorted list of these IDs.'''

    aux_dict = {}
    for k in id_list:
        if k in aux_dict.keys():
            aux_dict[k] = aux_dict[k] + 1
        else:
            aux_dict[k] = 1
    
    new_list = []
    for key, value in aux_dict.items():
        for i in range(0, value):
            new_list.append(key + i)

    # Note: sorted() used Timsort algorithm, which is nLog(n)
    return sorted(new_list)


# Tests should pass.
assert(deduplicate_copilots_ids(id_list1) == id_list1_return)
assert(deduplicate_copilots_ids(id_list2) == id_list2_return)
assert(deduplicate_copilots_ids(id_list3) == [])
assert(deduplicate_copilots_ids(id_list4) == id_list4_return)
