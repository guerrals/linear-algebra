import unittest
from matrix import Matrix

class TestMatrixLibrary(unittest.TestCase):

    def assertMatrixAlmostEqual(self, mat_a, expected_data, places=4):
        """Método auxiliar para comparar matrizes lidando com imprecisões de ponto flutuante."""
        self.assertEqual(len(mat_a.data), len(expected_data), "Número de linhas difere.")
        for r_idx, (row_a, row_exp) in enumerate(zip(mat_a.data, expected_data)):
            self.assertEqual(len(row_a), len(row_exp), f"Número de colunas difere na linha {r_idx}.")
            for c_idx, (val_a, val_exp) in enumerate(zip(row_a, row_exp)):
                self.assertAlmostEqual(
                    val_a, val_exp, places=places,
                    msg=f"Divergência na posição ({r_idx}, {c_idx}): obtido {val_a}, esperado {val_exp}"
                )

    # ==========================================
    # 1. OPERAÇÕES BÁSICAS (Soma, Subtração, Escalar)
    # ==========================================
    def test_addition(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[5, 6], [7, 8]])
        result = a + b
        self.assertEqual(result.data, [[6, 8], [10, 12]])

    def test_addition_dimension_mismatch(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            _ = a + b

    def test_subtraction(self):
        a = Matrix([[5, 7], [9, 11]])
        b = Matrix([[1, 2], [3, 4]])
        result = a - b
        self.assertEqual(result.data, [[4, 5], [6, 7]])

    def test_scalar_multiplication(self):
        a = Matrix([[1, -2], [3, 0]])
        result = a * 3
        self.assertEqual(result.data, [[3, -6], [9, 0]])
        # Teste de reflexividade (3 * a)
        result_reflected = 3 * a
        self.assertEqual(result_reflected.data, [[3, -6], [9, 0]])

    # ==========================================
    # 2. MULTIPLICAÇÃO DE MATRIZES & TRANSPOSTA
    # ==========================================
    def test_matrix_multiplication(self):
        a = Matrix([[1, 2], [3, 4]])
        b = Matrix([[2, 0], [1, 2]])
        result = a @ b
        self.assertEqual(result.data, [[4, 4], [10, 8]])

    def test_matrix_multiplication_incompatible_dimensions(self):
        a = Matrix([[1, 2, 3]])  # 1x3
        b = Matrix([[1, 2], [3, 4]])  # 2x2
        with self.assertRaises(ValueError):
            _ = a @ b

    def test_transpose(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])
        result = a.transpose()
        self.assertEqual(result.data, [[1, 4], [2, 5], [3, 6]])

    # ==========================================
    # 3. DETERMINANTE
    # ==========================================
    def test_determinant_2x2(self):
        a = Matrix([[4, 6], [3, 8]])
        self.assertAlmostEqual(a.determinant(), 14.0)

    def test_determinant_3x3(self):
        a = Matrix([
            [6, 1, 1],
            [4, -2, 5],
            [2, 8, 7]
        ])
        self.assertAlmostEqual(a.determinant(), -306.0)

    def test_determinant_non_square(self):
        a = Matrix([[1, 2, 3], [4, 5, 6]])
        with self.assertRaises(ValueError):
            a.determinant()

    # ==========================================
    # 4. FORMA ESCALONADA REDUZIDA (RREF)
    # ==========================================
    def test_rref_identity_reduction(self):
        a = Matrix([[2, 1], [4, 3]])
        rref = a.rref()
        self.assertMatrixAlmostEqual(rref, [[1.0, 0.0], [0.0, 1.0]])

    def test_rref_rectangular(self):
        a = Matrix([
            [1, 2, -1, -4],
            [2, 3, -1, -11],
            [-2, 0, -3, 22]
        ])
        expected = [
            [1.0, 0.0, 0.0, -8.0],
            [0.0, 1.0, 0.0, 1.0],
            [0.0, 0.0, 1.0, -2.0]
        ]
        self.assertMatrixAlmostEqual(a.rref(), expected)

    # ==========================================
    # 5. MATRIZ INVERSA
    # ==========================================
    def test_inverse_2x2(self):
        a = Matrix([[4, 7], [2, 6]])
        expected = [
            [0.6, -0.7],
            [-0.2, 0.4]
        ]
        self.assertMatrixAlmostEqual(a.inverse(), expected)

    def test_inverse_singular_matrix(self):
        # Determinante = 0
        a = Matrix([[1, 2], [2, 4]])
        with self.assertRaises(ValueError):
            a.inverse()

    # ==========================================
    # 6. RESOLUÇÃO DE SISTEMAS LINEARES (SOLVE)
    # ==========================================
    def test_solve_unique_solution(self):
        # 2x + y = 5
        # 4x + 3y = 11
        a = Matrix([[2, 1], [4, 3]])
        b = Matrix([[5], [11]])
        solution = a.solve(b)
        self.assertAlmostEqual(solution[0], 2.0, places=4)
        self.assertAlmostEqual(solution[1], 1.0, places=4)

    def test_solve_infinite_solutions(self):
        # Sistema Possível Indeterminado (SPI)
        a = Matrix([[1, 2], [2, 4]])
        b = Matrix([[3], [6]])
        with self.assertRaises(ValueError):
            a.solve(b)

    def test_solve_fallback_to_least_squares(self):
        # Sistema Impossível tratado automaticamente com Regressão Linear
        a = Matrix([[1, 1], [2, 1], [3, 1]])
        b = Matrix([[2], [3], [5]])
        solution = a.solve(b)
        self.assertAlmostEqual(solution[0], 1.5, places=4)
        self.assertAlmostEqual(solution[1], 0.3333, places=2)

    # ==========================================
    # 7. MÍNIMOS QUADRADOS (LEAST SQUARES)
    # ==========================================
    def test_least_squares_exact_fit(self):
        # Pontos perfeitamente colineares: (1, 2), (2, 4), (3, 6) -> y = 2x + 0
        a = Matrix([[1, 1], [2, 1], [3, 1]])
        b = Matrix([[2], [4], [6]])
        result = a.least_squares(b)
        self.assertMatrixAlmostEqual(result, [[2.0], [0.0]])

    def test_least_squares_scattered_data(self):
        # Pontos reais: (1, 2), (2, 3), (3, 5) -> y = 1.5x + 0.3333
        a = Matrix([[1, 1], [2, 1], [3, 1]])
        b = Matrix([[2], [3], [5]])
        result = a.least_squares(b)
        self.assertMatrixAlmostEqual(result, [[1.5], [0.3333]])

    # ==========================================
    # 8. TRANSFORMAÇÕES GEOMÉTRICAS (2D)
    # ==========================================
    def test_rotation_2d_single_point(self):
        p = Matrix([[1], [0]])
        r90 = Matrix.rotation_2d(90)
        p_rotated = r90 @ p
        self.assertMatrixAlmostEqual(p_rotated, [[0.0], [1.0]])

        r180 = Matrix.rotation_2d(180)
        p_rotated_180 = r180 @ p
        self.assertMatrixAlmostEqual(p_rotated_180, [[-1.0], [0.0]])

    def test_rotation_2d_multiple_points(self):
        # Triângulo: (1,0), (0,1), (0,0)
        triangle = Matrix([
            [1, 0, 0],
            [0, 1, 0]
        ])
        r90 = Matrix.rotation_2d(90)
        rotated = r90 @ triangle
        expected = [
            [0.0, -1.0, 0.0],
            [1.0, 0.0, 0.0]
        ]
        self.assertMatrixAlmostEqual(rotated, expected)

    # ==========================================
    # 9. ESPAÇOS VETORIAIS: RANK & INDEPENDÊNCIA LINEAR
    # ==========================================
    def test_rank(self):
        # Matriz com posto completo (2x2)
        a = Matrix([[1, 2], [3, 4]])
        self.assertEqual(a.rank(), 2)

        # Matriz com linhas dependentes (L2 = 2 * L1) -> Posto 1
        b = Matrix([[1, 2], [2, 4]])
        self.assertEqual(b.rank(), 1)

        # Matriz retangular 3x3 com posto 2
        c = Matrix([
            [1, 0, 1],
            [-2, -3, -5],
            [1, 0, 1]
        ])
        self.assertEqual(c.rank(), 2)

    def test_linear_independence(self):
        # Vetores canônicos no R3 -> LI
        v1 = [1, 0, 0]
        v2 = [0, 1, 0]
        v3 = [0, 0, 1]
        self.assertTrue(Matrix.is_linearly_independent([v1, v2, v3]))

        # Vetores onde v3 = v1 + v2 -> LD
        v_ld1 = [1, 2, 3]
        v_ld2 = [0, 1, 1]
        v_ld3 = [1, 3, 4]
        self.assertFalse(Matrix.is_linearly_independent([v_ld1, v_ld2, v_ld3]))

        # 3 vetores no R2 -> Sempre LD (mais vetores que a dimensão do espaço)
        u1 = [1, 0]
        u2 = [0, 1]
        u3 = [2, 3]
        self.assertFalse(Matrix.is_linearly_independent([u1, u2, u3]))

if __name__ == '__main__':
    unittest.main(verbosity=2)