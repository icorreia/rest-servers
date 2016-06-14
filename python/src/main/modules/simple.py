from sklearn import svm

def method(value):
    print 'Using scikit-learn'
    clf = svm.SVC(gamma=0.001, C=100.)
    return '\nHello world with post with value ' + value + '!\n'