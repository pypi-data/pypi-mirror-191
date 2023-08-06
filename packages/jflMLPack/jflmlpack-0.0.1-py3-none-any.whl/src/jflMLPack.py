import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt

# 取消用科学计数法表达
np.set_printoptions(suppress=True)

def calculate_best_randomstate(degree, algo, x, y, times):
    train_score = []
    test_score = []
    randomstate = []
    totalscore = []
    for i in range(0, times):
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.2,
            random_state=i
        )

        d = degree
        poly_Reg = Pipeline([
            ('poly', PolynomialFeatures(degree=d)),
            ('std_scale', StandardScaler()),
            ('lin_reg', algo)
        ])

        poly_Reg.fit(x_train, y_train)
        train_score.append(poly_Reg.score(x_train, y_train))
        test_score.append(poly_Reg.score(x_test, y_test))
        randomstate.append(i)

    for i in range(len(train_score)):
        totalscore.append(train_score[i] + test_score[i])

    totalscore = pd.DataFrame(totalscore, columns=['totalscore'])
    bestrandoms = totalscore['totalscore'].idxmax()
    print('Best randomstate is: '+str(bestrandoms))

    randomstate = pd.DataFrame(randomstate, columns=['randomstate'])
    train_score = pd.DataFrame(train_score, columns=['train_score'])
    test_score = pd.DataFrame(test_score, columns=['test_score'])
    score_matrix = pd.concat([randomstate,train_score,test_score,totalscore], axis=1)

    return  score_matrix, bestrandoms

def cut_head_score_matrix_list(col, score_matrix, top):
    if col == 1:
        c = 'train_score'
    elif col == 2:
        c = 'test_score'
    elif col == 3:
        c = 'totalscore'
    score_matrix_head = score_matrix.sort_values(by=c, ascending=False)
    score_matrix_head = score_matrix_head.head(top)
    return score_matrix_head

def return_nice_model(degree, algo, x, y, bestrandoms):
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=0.2,random_state=bestrandoms)

    poly_Reg = Pipeline([
        ('poly', PolynomialFeatures(degree=degree)),
        ('std_scale', StandardScaler()),
        ('lin_reg', algo)
    ])
    poly_Reg.fit(x_train, y_train)
    y_pre = poly_Reg.predict(x)
    print('Train Score is: '+str(poly_Reg.score(x_train,y_train)))
    print('Test Score is: '+ str(poly_Reg.score(x_test,y_test)))
    print('MSE(Mean Squared Error) is: '+str(mean_squared_error(y,y_pre)))
    print('RMSE(Sqrt Mean Squared Error) is: '+str(np.sqrt(mean_squared_error(y,y_pre))))

    return algo

def plot_learning_curve(algo, x_train, x_test, y_train, y_test):
    train_score = []
    test_score = []
    for i in range(1, len(x_train) + 1):
        algo.fit(x_train[:i], y_train[:i])

        y_train_predict = algo.predict(x_train[:i])
        train_score.append(mean_squared_error(y_train[:i],y_train_predict))

        y_test_predict = algo.predict(x_test)
        test_score.append(mean_squared_error(y_test,y_test_predict))

    plt.plot([i for i in range(1, len(x_train) + 1)], np.sqrt(train_score), label='train')
    plt.plot([i for i in range(1, len(x_train) + 1)], np.sqrt(test_score), label='test')
    plt.legend()
    # plt.axis([0, len(x_train)+1],0,4)
    plt.show()
