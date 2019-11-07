import config
import mysql.connector
import tensorrec
from scipy.special import softmax
from data import Data


class Module:
    def __init__(self):
        self.model = tensorrec.TensorRec()
        self.fit()

    def select_data(self):
        self.connection = mysql.connector.connect(host=config.HOST_DB,
                                                  database=config.NAME_DB,
                                                  user=config.USER_DB,
                                                  password=config.PASS_DB)
        cur = self.connection.cursor()
        cur.execute(("SELECT id, friends FROM student"))
        students = cur.fetchall()

        cur.execute(("SELECT id, area_id, hash_tags FROM branch"))
        branches = cur.fetchall()

        cur.execute(("SELECT * FROM statistic"))
        actives = cur.fetchall()

        # print (students)
        # print (branches)
        # print (actives)
        cur.close()
        self.data = Data(students, branches, actives)
        self.users, self.branches, self.actions = self.data.get_data()

    def fit(self, epochs=100):
        self.select_data()
        self.model.fit(self.actions, self.users, self.branches, epochs=epochs, verbose=True)
        print ("FIT successful!")

    def get_all(self):
        predictions = self.model.predict(user_features=self.users,
                                         item_features=self.branches)
        result = []
        for x in predictions:
            result.append(list(softmax(x)))
        return result

    def update(self):
        self.fit()
        matrix = self.get_all()
        cur = self.connection.cursor()

        query = (
            "TRUNCATE TABLE student_branch"
        )
        cur.execute(query)
        self.connection.commit()

        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                query = (
                    "INSERT INTO student_branch (student_id, branch_id, ratio) VALUES (%s, %s, %s)"
                )
                data = (i,j,float(matrix[i][j]))
                cur.execute(query, data)
                self.connection.commit()
        cur.close()

        return matrix
