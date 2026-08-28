from matrix import Matrix

# ==========================================
# 🛠️ JEST-LIKE TESTING MINI-FRAMEWORK
# ==========================================

class TestRunner:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def describe(self, name, func):
        print(f"\n📦 \033[1;34m{name}\033[0m")
        func()

    def it(self, name, func):
        try:
            func()
            print(f"  \033[1;32m✓\033[0m \033[90m{name}\033[0m")
            self.passed += 1
        except AssertionError as e:
            print(f"  \033[1;31m✗\033[0m \033[90m{name}\033[0m")
            print(f"    \033[31mAssertionError: {e}\033[0m")
            self.failed += 1
        except Exception as e:
            print(f"  \033[1;31m✗\033[0m \033[90m{name}\033[0m")
            print(f"    \033[31mError: {type(e).__name__}: {e}\033[0m")
            self.failed += 1

    def print_summary(self):
        print("\n" + "="*40)
        print("\033[1mTest Suites:\033[0m 1 passed, 1 total")
        
        total_tests = self.passed + self.failed
        if self.failed == 0:
            print(f"\033[1mTests:\033[0m       \033[1;32m{self.passed} passed\033[0m, {total_tests} total")
        else:
            print(f"\033[1mTests:\033[0m       \033[1;31m{self.failed} failed\033[0m, \033[1;32m{self.passed} passed\033[0m, {total_tests} total")
        print("="*40 + "\n")

class Expect:
    def __init__(self, actual):
        self.actual = actual

    def to_equal(self, expected):
        assert self.actual == expected, f"Expected {expected}, but received {self.actual}"

    def to_throw(self, error_type=Exception):
        try:
            self.actual()
        except error_type:
            return
        except Exception as e:
            assert False, f"Expected {error_type.__name__}, but received {type(e).__name__}"
        assert False, f"Expected {error_type.__name__} to be thrown, but nothing was thrown"

def expect(actual):
    return Expect(actual)

# Instantiating the global runner
runner = TestRunner()
describe = runner.describe
it = runner.it

# ==========================================j
# 🧪 TEST SUITES
# ==========================================

def run_all_tests():
    
    def test_initialization():
        def _valid_matrix():
            m = Matrix([[1, 2], [3, 4]])
            expect(m.rows).to_equal(2)
            expect(m.cols).to_equal(2)
        it("should initialize a valid matrix and set rows/cols correctly", _valid_matrix)

        def _invalid_matrix():
            # Using lambda to pass a callable that raises the error
            expect(lambda: Matrix([[1, 2], [3]])).to_throw(ValueError)
        it("should throw ValueError when rows have different lengths", _invalid_matrix)

    describe("Matrix Initialization & Validation", test_initialization)

    def test_class_methods():
        def _zeros():
            m = Matrix.zeros(2, 3)
            expect(m.data).to_equal([[0, 0, 0], [0, 0, 0]])
        it("should create a Matrix of zeros based on dimensions", _zeros)

        def _identity():
            m = Matrix.identity(3, 3)
            expect(m.data).to_equal([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        it("should create a correct Identity Matrix", _identity)

    describe("Class Methods (Factories)", test_class_methods)

    def test_math_operations():
        def _addition():
            m1 = Matrix([[1, 2], [3, 4]])
            m2 = Matrix([[5, 6], [7, 8]])
            result = m1 + m2
            expect(result.data).to_equal([[6, 8], [10, 12]])
        it("should correctly add two matrices (A + B)", _addition)

        def _subtraction():
            m1 = Matrix([[5, 5], [5, 5]])
            m2 = Matrix([[1, 2], [3, 4]])
            result = m1 - m2
            expect(result.data).to_equal([[4, 3], [2, 1]])
        it("should correctly subtract two matrices (A - B)", _subtraction)

        def _scalar_multiplication():
            m = Matrix([[1, -2], [0, 3]])
            result = m * 3
            expect(result.data).to_equal([[3, -6], [0, 9]])
        it("should multiply a matrix by a scalar correctly (A * c)", _scalar_multiplication)

        def _dot_product():
            m1 = Matrix([[1, 2], [3, 4]])
            m2 = Matrix([[2, 0], [1, 2]])
            result = m1 @ m2
            expect(result.data).to_equal([[4, 4], [10, 8]])
        it("should perform matrix multiplication / dot product correctly (A @ B)", _dot_product)
        
        def _transpose():
            m = Matrix([[1, 2, 3], [4, 5, 6]])
            result = m.transpose()
            expect(result.data).to_equal([[1, 4], [2, 5], [3, 6]])
        it("should transpose the matrix (swap rows and columns)", _transpose)

    describe("Mathematical Operations", test_math_operations)

    def test_determinant():
        def _det_2x2():
            m = Matrix([[3, 8], [4, 6]])
            expect(m.determinant()).to_equal(-14)
        it("should calculate the determinant of a 2x2 matrix", _det_2x2)

        def _det_3x3():
            m = Matrix([[6, 1, 1], [4, -2, 5], [2, 8, 7]])
            expect(m.determinant()).to_equal(-306)
        it("should calculate the determinant of a 3x3 matrix using Laplace", _det_3x3)

        def _det_zero():
            # A matrix where row 3 is the sum of row 1 and row 2 (Linear dependence)
            m = Matrix([[1, 2, 3], [4, 5, 6], [5, 7, 9]])
            expect(m.determinant()).to_equal(0)
        it("should return exactly 0 for a linearly dependent matrix", _det_zero)

        def _det_not_square():
            m = Matrix([[1, 2, 3], [4, 5, 6]])
            expect(lambda: m.determinant()).to_throw(ValueError)
        it("should throw a ValueError if trying to find det of non-square matrix", _det_not_square)

    describe("Determinant & Laplace Expansion", test_determinant)

    def test_row_operations():
        def _swap():
            m = Matrix([[1, 2], [3, 4]])
            m._swap_rows(0, 1)
            expect(m.data).to_equal([[3, 4], [1, 2]])
        it("should swap two rows correctly (_swap_rows)", _swap)

        def _multiply():
            m = Matrix([[1, 2], [3, 4]])
            m._multiply_row(1, 10)
            expect(m.data).to_equal([[1, 2], [30, 40]])
        it("should multiply an entire row by a scalar (_multiply_row)", _multiply)

        def _add_multiple():
            m = Matrix([[1, 2, 3], [4, 5, 6]])
            # Add to row 1 (target) the row 0 (source) multiplied by -4
            m._add_row_multiple(target_row=1, source_row=0, scalar=-4)
            # Row 0 * -4 = [-4, -8, -12]
            # Row 1 = [0, -3, -6]
            expect(m.data).to_equal([[1, 2, 3], [0, -3, -6]])
        it("should add a multiple of one row to another (_add_row_multiple)", _add_multiple)

    describe("Elementary Row Operations", test_row_operations)

    def test_rref():
        # Helper function to avoid float precision errors (e.g., 0.9999999 != 1.0)
        def round_data(data, decimals=5):
            return [[round(val, decimals) for val in row] for row in data]

        def _invertible_2x2():
            m = Matrix([[1, 2], [3, 4]])
            rref_m = m.rref()
            expected = [[1.0, 0.0], [0.0, 1.0]] # Should become the Identity matrix
            expect(round_data(rref_m.data)).to_equal(expected)
        it("should reduce an invertible 2x2 matrix to the identity matrix", _invertible_2x2)

        def _linear_system():
            # Represents the system:
            # 1x + 1y = 3
            # 2x - 1y = 0
            # Solution should be x=1, y=2
            m = Matrix([[1, 1, 3], [2, -1, 0]])
            rref_m = m.rref()
            expected = [
                [1.0, 0.0, 1.0], 
                [0.0, 1.0, 2.0]
            ]
            expect(round_data(rref_m.data)).to_equal(expected)
        it("should reduce a 2x3 matrix representing a linear system correctly", _linear_system)

        def _dependent_rows():
            # A 3x3 matrix where Row 3 is a combination of Row 1 and 2.
            # The last row should become entirely zeros.
            m = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            rref_m = m.rref()
            expected = [
                [1.0, 0.0, -1.0],
                [0.0, 1.0, 2.0],
                [0.0, 0.0, 0.0]
            ]
            expect(round_data(rref_m.data)).to_equal(expected)
        it("should zero out rows that are linearly dependent", _dependent_rows)

    describe("Gauss-Jordan Elimination (RREF)", test_rref)

    def test_solve_system():
        def _unique_solution():
            # Sistema:
            # 2x + y = 5
            # 3x - y = 0
            # Solução esperada: x = 1.0, y = 3.0
            A = Matrix([[2, 1], [3, -1]])
            B = Matrix([[5], [0]])
            solution = A.solve(B)
            expect(solution).to_equal([1.0, 3.0])
        it("should return the correct unique solution for a valid system (SPD)", _unique_solution)

        def _inconsistent_system_fallback():
            # Sistema de Regressão Linear: 3 pontos, 2 variáveis.
            # Matriz A (Tamanho, Intercepto) e B (Preços)
            A = Matrix([
                [1, 1], 
                [2, 1], 
                [3, 1]
            ])
            B = Matrix([
                [2], 
                [3], 
                [5]
            ])
            
            # Como não há reta perfeita, o solve() aciona o fallback para least_squares
            # O solve() desempacota e retorna uma lista: [1.5, 0.33333...]
            result = A.solve(B)
            
            # Arredondamos o resultado para 4 casas para o teste bater perfeitamente
            rounded_result = [round(val, 4) for val in result]
            expected = [1.5, 0.3333]
            
            expect(rounded_result).to_equal(expected)
        it("should fallback to least squares and return approximation for inconsistent systems", _inconsistent_system_fallback)

        def _infinite_solutions():
            # Sistema indeterminado (mesma linha sobreposta):
            # x + y = 2
            # 2x + 2y = 4
            A = Matrix([[1, 1], [2, 2]])
            B = Matrix([[2], [4]])
            expect(lambda: A.solve(B)).to_throw(ValueError)
        it("should throw ValueError for a dependent system (SPI - Infinite solutions)", _infinite_solutions)

        def _dimension_mismatch():
            # Tentando resolver com quantidade errada de constantes
            A = Matrix([[1, 2], [3, 4]])
            B = Matrix([[5]])
            expect(lambda: A.solve(B)).to_throw(ValueError)
        it("should throw ValueError if coefficient and constant dimensions mismatch", _dimension_mismatch)

    describe("Solving Linear Systems (.solve)", test_solve_system)

    def test_inverse():
        # Função auxiliar para lidar com a precisão dos decimais
        def round_data(data, decimals=5):
            return [[round(val, decimals) for val in row] for row in data]

        def _valid_inverse():
            # Matriz:
            # [4, 7]
            # [2, 6]
            # O determinante é (4*6) - (7*2) = 24 - 14 = 10
            # A inversa deve ser:
            # [ 0.6, -0.7]
            # [-0.2,  0.4]
            m = Matrix([[4, 7], [2, 6]])
            inv = m.inverse()
            expected = [[0.6, -0.7], [-0.2, 0.4]]
            expect(round_data(inv.data)).to_equal(expected)
        it("should calculate the correct inverse for a valid square matrix", _valid_inverse)

        def _not_square():
            m = Matrix([[1, 2, 3], [4, 5, 6]])
            expect(lambda: m.inverse()).to_throw(ValueError)
        it("should throw ValueError if matrix is not square", _not_square)

        def _singular_matrix():
            # Matriz singular (Linha 2 é o dobro da Linha 1, det = 0)
            m = Matrix([[1, 2], [2, 4]])
            expect(lambda: m.inverse()).to_throw(ValueError)
        it("should throw ValueError if matrix is singular (det = 0)", _singular_matrix)

    describe("Inverse Matrix (.inverse)", test_inverse)

    def test_least_squares():
        # Função auxiliar para arredondar dízimas (como 0.333333...)
        def round_data(data, decimals=4):
            return [[round(val, decimals) for val in row] for row in data]

        def _perfect_fit():
            # Pontos perfeitamente alinhados: (1, 2), (2, 4), (3, 6)
            # A equação exata dessa reta é y = 2x + 0 (m=2, b=0)
            A = Matrix([
                [1, 1], 
                [2, 1], 
                [3, 1]
            ])
            B = Matrix([
                [2], 
                [4], 
                [6]
            ])
            
            result = A.least_squares(B)
            
            expected = [[2.0], [0.0]]
            expect(round_data(result.data)).to_equal(expected)
        it("should find the exact line for perfectly aligned points", _perfect_fit)

        def _best_fit():
            # Pontos espalhados: (1, 2), (2, 3), (3, 5)
            # A melhor reta aproximada matematicamente é y = 1.5x + 0.3333
            A = Matrix([
                [1, 1], 
                [2, 1], 
                [3, 1]
            ])
            B = Matrix([
                [2], 
                [3], 
                [5]
            ])
            
            result = A.least_squares(B)
            
            expected = [[1.5], [0.3333]]
            expect(round_data(result.data, 4)).to_equal(expected)
        it("should find the best fit line for scattered points", _best_fit)

    describe("Least Squares (Linear Regression)", test_least_squares)

    def test_transformations():
        def _rotate_90_degrees():
            # Ponto em (1, 0)
            P = Matrix([[1], [0]])
            # Matriz de rotação de 90 graus
            R = Matrix.rotation_2d(90)
            
            # Rotacionando: R @ P
            result = R @ P
            
            # O ponto (1, 0) girado 90 graus vira (0, 1)
            # O Python pode retornar 0.0 e 1.0 devido à conversão de floats
            expected = [[0.0], [1.0]]
            expect(result.data).to_equal(expected)
        it("should rotate a single point 90 degrees correctly", _rotate_90_degrees)

        def _rotate_180_degrees():
            # Ponto em (1, 0)
            P = Matrix([[1], [0]])
            # Matriz de rotação de 180 graus
            R = Matrix.rotation_2d(180)
            
            result = R @ P
            
            # O ponto (1, 0) girado 180 graus vira (-1, 0)
            expected = [[-1.0], [0.0]]
            expect(result.data).to_equal(expected)
        it("should rotate a single point 180 degrees correctly", _rotate_180_degrees)

        def _rotate_shape():
            # Para rotacionar um triângulo (ou qualquer forma 2D), colocamos 
            # os pontos como colunas da matriz.
            # Pontos do triângulo: A(1, 0), B(0, 1), C(0, 0)
            triangle = Matrix([
                [1, 0, 0],  # Eixo X
                [0, 1, 0]   # Eixo Y
            ])
            
            R = Matrix.rotation_2d(90)
            
            # A mágica da Álgebra Linear: multiplicamos a matriz de rotação 
            # pela matriz de pontos, e TODOS os pontos giram simultaneamente!
            rotated_triangle = R @ triangle
            
            # Novos pontos esperados: A'(0, 1), B'(-1, 0), C'(0, 0)
            expected = [
                [0.0, -1.0, 0.0],
                [1.0,  0.0, 0.0]
            ]
            expect(rotated_triangle.data).to_equal(expected)
        it("should rotate multiple points of a shape simultaneously", _rotate_shape)

    describe("Geometric Transformations (2D)", test_transformations)
    # Finally, print the beautiful summary
    runner.print_summary()

if __name__ == "__main__":
    run_all_tests()