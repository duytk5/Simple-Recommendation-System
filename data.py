from tensorrec.input_utils import create_tensorrec_dataset_from_sparse_matrix

import config
from scipy.special import softmax
import scipy.sparse as sp
import numpy as np


def str2list(hash_tags):
    return [x.strip() for x in hash_tags.replace("[", "").replace("]", "").split(" ")]


def map_branches(branches):
    list_tags = []
    list_area = []
    for branch in branches:
        id, area_id, hash_tags = branch
        hash_tags = str2list(hash_tags)
        if area_id not in list_area:
            list_area.append(area_id)
        for tag in hash_tags:
            if tag not in list_tags:
                list_tags.append(tag)
    list_tags.sort()
    map_tag = {}
    for id, tag in enumerate(list_tags):
        map_tag[tag] = id
    list_area.sort()
    map_area = {}
    for id, area in enumerate(list_area):
        map_area[area] = id
    dim_tags = len(list_tags)
    dim_area = len(list_area)

    ans = [[0 for i in range(dim_tags + dim_area)] for i in range(len(branches))]

    for i, branch in enumerate(branches):
        id, area_id, hash_tags = branch
        hash_tags = str2list(hash_tags)
        for tag in hash_tags:
            ans[i][map_tag[tag]] = 1
        ans[i][map_area[area_id]] = 1
    return ans


def get_pos(x):
    map_pos = {}
    for pos, y in enumerate(x):
        id = list(y)[0]
        map_pos[id] = pos
    return map_pos


def map_actives(actives, pos_students, pos_branches, n, m):
    ans = [[0 for i in range(m)] for j in range(n)]
    for active in actives:
        active = list(active)
        i = pos_students[active[1]]
        j = pos_branches[active[2]]
        d_sum = 0
        for id, v in enumerate(active[3:17]):
            if not v:
                v = 0
            d_sum += config.score_action[id] * v
        ans[i][j] = d_sum

    for i in range(n):
        ans[i] = softmax(ans[i])
    return ans


class Data:
    def __init__(self, students, branches, actives):
        a = []
        for user in students:
            a.append([1])

        b = map_branches(branches)

        self.pos_students = get_pos(students)
        self.pos_branches = get_pos(branches)

        c = map_actives(actives, self.pos_students, self.pos_branches, len(a), len(b))

        self.a = sp.csr_matrix(np.array(a))
        self.b = sp.csr_matrix(np.array(b))
        self.c = sp.csr_matrix(np.array(c))

    def get_data(self):
        return self.a, self.b, self.c
