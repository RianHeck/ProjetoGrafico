import math

class ndarray:
    def __init__(self, data):
        if isinstance(data, ndarray):
            data = data.data
        if isinstance(data, (list, tuple)) and data and isinstance(data[0], (list, tuple)):
            self.data = [list(row) for row in data]
        elif isinstance(data, (list, tuple)):
            self.data = list(data)
        else:
            self.data = [data]

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, idx):
        return self.data[idx]

    @property
    def T(self):
        if not self.data:
            return ndarray([])
        if isinstance(self.data[0], list):
            return ndarray([list(row) for row in zip(*self.data)])
        return ndarray([[x] for x in self.data])


def array(obj):
    return ndarray(obj)


def eye(n):
    return ndarray([[1 if i == j else 0 for j in range(n)] for i in range(n)])


def dot(a, b):
    A = a.data if isinstance(a, ndarray) else a
    B = b.data if isinstance(b, ndarray) else b

    def is_matrix(x):
        return x and isinstance(x[0], (list, tuple))

    if not is_matrix(A):
        A = [A]
    if not is_matrix(B):
        B = [[elem] for elem in B]
    A_rows, A_cols = len(A), len(A[0])
    B_rows, B_cols = len(B), len(B[0])
    if A_cols != B_rows:
        raise ValueError("shapes not aligned")
    result = [[sum(A[i][k] * B[k][j] for k in range(A_cols)) for j in range(B_cols)] for i in range(A_rows)]
    if A_rows == 1 and B_cols == 1:
        return result[0][0]
    if A_rows == 1:
        return ndarray(result[0])
    if B_cols == 1:
        return ndarray([row[0] for row in result])
    return ndarray(result)


def radians(x):
    return math.radians(x)


def cos(x):
    return math.cos(x)


def sin(x):
    return math.sin(x)


def allclose(a, b, tol=1e-8):
    A = a.data if isinstance(a, ndarray) else a
    B = b.data if isinstance(b, ndarray) else b
    if isinstance(A[0], (list, tuple)):
        A = [item for sub in A for item in sub]
    if isinstance(B[0], (list, tuple)):
        B = [item for sub in B for item in sub]
    return all(abs(x - y) <= tol for x, y in zip(A, B))
