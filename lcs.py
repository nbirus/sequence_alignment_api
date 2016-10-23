import logging
import __builtin__
from flask_restful import abort, request, reqparse, Resource
from flask import jsonify

import time


class LCS(Resource):

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.table_name = 'treatment_arm'
        self.local_excel_workbook_path = 'temp/temp.xlsx'

    def post(self):
        self.logger.info("Listener control GET")
        args = request.args
        print str(args)
        self.logger.debug(str(args))
        self.post = request.get_json()

        X = self.post.get('X')
        Y = self.post.get('Y')

        m = len(X)
        n = len(Y)


        start = time.time()
        C = LCS.get_LCS(X, Y)
        elapsed = time.time() - start

        B = [[0] * (n + 1) for _ in range(m + 1)]

        LCS_count = LCS.backTrack(C, X, Y, m, n, B)

        return jsonify({"LCS_count": LCS_count, "asigned_number_table": C, 'arrow_table': B, "time_elapsed": "%.5f" % (elapsed * 1000)})

    @staticmethod
    def get_LCS(X, Y):
        m = len(X)
        n = len(Y)

        # C = [[0] * (n + 1) for _ in range(m + 1)]
        # for i in range(1, m + 1):
        #     for j in range(1, n + 1):
        #         if X[i - 1] == Y[j - 1]:
        #             print C[i - 1][j - 1]
        #             C[i][j] = C[i - 1][j - 1] + 1
        #         else:
        #             C[i][j] = max(C[i][j - 1], C[i - 1][j])
        # print C

        C = [[{'asigned_number': 0, 'arrow_direction': ''}] * (n + 1) for _ in range(m + 1)]

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if X[i - 1] == Y[j - 1]:
                    C[i][j] = {'asigned_number': C[i - 1][j - 1]['asigned_number'] + 1, 'arrow_direction': 'diagnal'}
                else:
                    C[i][j] = {'asigned_number': max(C[i][j - 1]['asigned_number'], C[i - 1][j]['asigned_number']),
                               'arrow_direction': 'left' if C[i][j - 1]['asigned_number'] > C[i - 1][j]['asigned_number'] else 'up'}
        return C

    @staticmethod
    def backTrack(C, X, Y, i, j, B):

        if i == 0 or j == 0:
            return ""
        elif X[i - 1] == Y[j - 1]:
            B[i][j] = 2
            return LCS.backTrack(C, X, Y, i - 1, j - 1, B) + X[i - 1]
        else:
            if C[i][j - 1]['asigned_number'] > C[i - 1][j]['asigned_number']:
                B[i][j] = 1
                return LCS.backTrack(C, X, Y, i, j - 1, B)
            else:
                B[i][j] = 1
                return LCS.backTrack(C, X, Y, i - 1, j, B)




