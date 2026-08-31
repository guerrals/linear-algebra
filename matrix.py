import random
import math

class Matrix:
    def __init__(self, data):
        """
        [MATH ON PAPER]: Matrix Initialization.
        On paper, you draw a pair of large brackets and fill it with a grid of numbers. 
        The dimensions are read as "Rows x Columns".
        
        [HOW IT WORKS IN CODE]:
        We take a 2D list (list of lists) and store it in `self.data`. We calculate 
        `self.rows` by counting the outer list, and `self.cols` by counting the inner list.
        We also enforce that every row must have the exact same number of columns.
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0
        for row_index in range(self.rows):
            for column_index in range(self.cols):
                if self.cols != len(self.data[row_index]):
                    raise ValueError("Matrices must have the same number of elements in each row.")

    @classmethod
    def random(cls, rows, cols, seed=None):
        """
        Helper method to generate a matrix with random integers.
        """
        if seed is not None:
            random.seed(seed)

        matrix_data = []
        for _ in range(rows):
            new_row = []
            for _ in range(cols):
                new_row.append(random.randint(0, 99))
            matrix_data.append(new_row)

        return cls(matrix_data)

    @classmethod
    def zeros(cls, rows, cols):
        """
        [MATH ON PAPER]: Null Matrix.
        A matrix completely filled with zeros. It acts like the number "0" in matrix algebra.
        """
        matrix_data = []
        for row_index in range(rows):
            row = []
            for column_index in range(cols):
                row.append(0)
            matrix_data.append(row)

        return cls(matrix_data)
    
    @classmethod
    def identity(cls, rows, cols):
        """
        [MATH ON PAPER]: Identity Matrix (I).
        This is the matrix equivalent of the number "1". On paper, you draw a square matrix, 
        write 1s diagonally from the top-left to the bottom-right, and fill the rest with 0s.
        Multiplying any matrix A by I just gives you A back.
        
        [HOW IT WORKS IN CODE]:
        We loop through rows and columns. If the row index matches the column index 
        (e.g., [0][0], [1][1]), we place a 1. Otherwise, we place a 0.
        """
        matrix_data = []
        for row_index in range(rows):
            row = []
            for column_index in range(cols):
                if row_index == column_index:
                    row.append(1)
                else:
                    row.append(0)
            matrix_data.append(row)

        return cls(matrix_data)

    @staticmethod
    def rotation_2d(angle_degrees):
        """
        [MATH ON PAPER]: Matriz de Rotação 2D.
        Gera a matriz capaz de rotacionar pontos em um determinado ângulo.
        """
        rad = math.radians(angle_degrees)
        cos = round(math.cos(rad), 5)
        sin = round(math.sin(rad), 5)
        return Matrix([
            [cos, -sin],
            [sin,  cos]
        ])

    @staticmethod
    def is_linearly_independent(vectors):
        """
        [MATH ON PAPER]: Independência Linear (LI vs LD).
        Recebe uma lista de vetores (onde cada vetor é uma lista ou Matrix coluna).
        Retorna True se forem LI, False se forem LD.
        """
        if not vectors:
            raise ValueError("A lista de vetores não pode estar vazia.")

        num_vectors = len(vectors)
        vector_dim = len(vectors[0])

        # Monta a matriz colocando os vetores como COLUNAS
        # Matriz de dimensões (vector_dim x num_vectors)
        matrix_data = []
        for r in range(vector_dim):
            row = [vectors[c][r] for c in range(num_vectors)]
            matrix_data.append(row)

        A = Matrix(matrix_data)
        
        # É LI se o posto for exatamente igual ao número de vetores
        return A.rank() == num_vectors

    def rank(self):
        """
        [MATH ON PAPER]: Posto de uma Matriz.
        Calcula o número de linhas não nulas na forma RREF.
        """
        reduced = self.rref()
        non_zero_rows = 0
        
        for row in reduced.data:
            # Verifica se há pelo menos um elemento diferente de zero na linha
            if any(abs(val) > 1e-7 for val in row):
                non_zero_rows += 1
                
        return non_zero_rows

    def _get_submatrix(self, row, column):
        """
        [MATH ON PAPER]: Laplace Cut (Minors).
        On paper, if you pick a specific number in the matrix, you draw a vertical line 
        through its column and a horizontal line through its row, crossing them out. 
        The numbers that survive form a smaller, new matrix.
        
        [HOW IT WORKS IN CODE]:
        We iterate through the entire matrix but use `continue` to skip the specific 
        row index and column index. Everything else is appended to `submatrix_data`.
        """
        submatrix_data = []
        for row_index in range(self.rows):
            if row_index == row:
                continue
            subrow = []
            for column_index in range(self.cols):
                if column_index == column:
                    continue
                subrow.append(self.data[row_index][column_index])
            submatrix_data.append(subrow)
        
        return Matrix(submatrix_data)

    def _swap_rows(self, from_row, to_row):
        """
        [MATH ON PAPER]: Elementary Row Operation - Swap.
        Notation: R1 <-> R2
        If your pivot is zero, you literally just rewrite the matrix on a new step, 
        switching the places of two entire equations.
        """
        self.data[from_row], self.data[to_row] = self.data[to_row], self.data[from_row]
    
    def _multiply_row(self, row, scalar):
        """
        [MATH ON PAPER]: Elementary Row Operation - Multiply.
        Notation: R1 -> c * R1
        You multiply an entire equation (row) by a constant. Usually done to turn 
        the pivot number into a 1 (by multiplying by 1/pivot).
        """
        if scalar == 0:
            raise ValueError("Cannot multiply a row by scalar equal to zero.")

        for column_index in range(self.cols):
            self.data[row][column_index] *= scalar

    def _add_row_multiple(self, source_row, target_row, scalar):
        """
        [MATH ON PAPER]: Elementary Row Operation - The Laser.
        Notation: R_target -> R_target + (c * R_source)
        To eliminate a number under a pivot, you multiply the pivot's equation by 
        the opposite of the target number, and add the result to the target equation. 
        This turns the target number into 0.
        """
        for column_index in range(self.cols):
            self.data[target_row][column_index] += self.data[source_row][column_index] * scalar

    def __str__(self):
        """Visual formatting for terminal output."""
        if not self.data:
            return "Empty Matrix"

        col_widths = []
        for j in range(self.cols):
            max_width = max(len(str(self.data[i][j])) for i in range(self.rows))
            col_widths.append(max_width)

        separator = "+"
        for width in col_widths:
            separator += "-" * (width + 2) + "+" 

        result = [separator]
        for i in range(self.rows):
            row_str = "|"
            for j in range(self.cols):
                val = str(self.data[i][j])
                row_str += f" {val:>{col_widths[j]}} |"
            
            result.append(row_str)
            result.append(separator)

        return '\n'.join(result)

    def __add__(self, other):
        """
        [MATH ON PAPER]: Matrix Addition.
        Math: C[i][j] = A[i][j] + B[i][j]
        On paper, you just add the number in the top-left of A with the top-left of B, 
        and write the result in the top-left of C. Repeat for every position.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions to add.")

        matrix_data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] + other.data[row_index][column_index])
            matrix_data.append(row)

        return Matrix(matrix_data)

    def __sub__(self, other):
        """
        [MATH ON PAPER]: Matrix Subtraction.
        Math: C[i][j] = A[i][j] - B[i][j]
        Same process as addition, but subtracting the overlapping elements.
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions to subtract.")

        matrix_data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] - other.data[row_index][column_index])
            matrix_data.append(row)

        return Matrix(matrix_data)

    def __mul__(self, scalar):
        """
        [MATH ON PAPER]: Scalar Multiplication.
        Math: C[i][j] = c * A[i][j]
        On paper, you take the number outside the matrix and distribute it, 
        multiplying it by every single element inside the brackets.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Cannot multiply Matrix by non-scalar of type '{type(scalar).__name__}'")

        matrix_data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] * scalar)
            matrix_data.append(row)

        return Matrix(matrix_data)

    def __rmul__(self, scalar):
        return self.__mul__(scalar)

    def __matmul__(self, other):
        """
        [MATH ON PAPER]: Matrix Dot Product (A @ B).
        On paper, this is the "Dive and Swim" method. You grab an entire ROW from 
        matrix A, and an entire COLUMN from matrix B. You multiply their matching 
        elements one by one (1st with 1st, 2nd with 2nd) and add those products 
        together to get a single number for the new matrix.
        
        [HOW IT WORKS IN CODE]:
        Three nested loops. 
        Loop 1: Iterates rows of Matrix A.
        Loop 2: Iterates columns of Matrix B.
        Loop 3 (product_index): Iterates through the items inside that specific row/col 
        pair to multiply and sum them up into the 'product' variable.
        """
        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply {self.rows}x{self.cols} by {other.rows}x{other.cols}.")

        matrix_data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(other.cols):
                product = 0 
                # FIX: We iterate up to self.cols (which equals other.rows)
                for product_index in range(self.cols):
                    product += self.data[row_index][product_index] * other.data[product_index][column_index]
                row.append(product)
            matrix_data.append(row)

        return Matrix(matrix_data)

    def transpose(self):
        """
        [MATH ON PAPER]: Transposition (A^T).
        On paper, you rewrite the matrix by turning its rows into columns. 
        Row 1 becomes Column 1. Row 2 becomes Column 2.
        
        [HOW IT WORKS IN CODE]:
        We reverse the standard loop order. We iterate through columns first, 
        then rows, appending the elements to reconstruct the flipped shape.
        """
        matrix_data = []
        for column_index in range(self.cols):
            row = []
            for row_index in range(self.rows):
                row.append(self.data[row_index][column_index])
            matrix_data.append(row)

        return Matrix(matrix_data)

    def determinant(self): 
        """
        [MATH ON PAPER]: Laplace Expansion.
        To find the "volume" of the matrix, you walk across the top row. For each 
        number, you apply a (+ - + -) pattern, cross out its row and column, and 
        multiply the number by the determinant of the smaller surviving matrix.
        
        [HOW IT WORKS IN CODE]:
        This is a classic recursive function. It calls itself on smaller and smaller 
        sub-matrices (created by `_get_submatrix`) until it hits the 2x2 or 1x1 
        base case, then bubbles the answers back up.
        """
        if self.rows != self.cols:
            raise ValueError("Determinant is only defined for square matrices.")

        if self.rows == 1:
            return self.data[0][0]

        if self.rows == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]

        determinant = 0
        for column_index in range(self.cols):
            signal = (-1) ** column_index
            cell_value = self.data[0][column_index]
            sub_matrix = self._get_submatrix(0, column_index)
            determinant += signal * cell_value * sub_matrix.determinant()

        return determinant
    
    def rref(self):
        """
        [MATH ON PAPER]: Gauss-Jordan Elimination (Row Reduction).
        1. Find a non-zero number in the current column (swap rows if needed).
        2. Divide the entire row by that number to make it a 1 (the pivot).
        3. Use the laser operation (add multiples of this row) to turn every 
           other number in that column into 0.
        4. Move down and to the right, and repeat.
        
        [HOW IT WORKS IN CODE]:
        We operate on a deep copy of the matrix. We track the `lead_col`. We find 
        the pivot, perform the `_swap_rows`, use `_multiply_row` to get our 1, 
        and then loop over all other rows using `_add_row_multiple` to zero them out.
        """
        rref_data = [row[:] for row in self.data]
        rref_matrix = Matrix(rref_data)
        lead_col = 0
        
        for current_row in range(self.rows):
            if lead_col >= self.cols:
                break
                
            pivot_index = current_row
            while rref_matrix.data[pivot_index][lead_col] == 0:
                pivot_index += 1
                if pivot_index == rref_matrix.rows:
                    pivot_index = current_row
                    lead_col += 1
                    if lead_col == rref_matrix.cols:
                        return rref_matrix

            rref_matrix._swap_rows(pivot_index, current_row)
            pivot_val = rref_matrix.data[current_row][lead_col]
            rref_matrix._multiply_row(current_row, 1.0 / pivot_val)
            
            for row_index in range(self.rows):
                if row_index != current_row:
                    value = rref_matrix.data[row_index][lead_col]
                    # target is row_index, source is current_row
                    rref_matrix._add_row_multiple(current_row, row_index, -value)
                    
            lead_col += 1
            
        return rref_matrix

    def solve(self, constants):
        """
        [MATH ON PAPER]: Solving a Linear System.
        If you have 2x + y = 5 and 3x - y = 0:
        1. Write the coefficients [2, 1] and [3, -1] as Matrix A.
        2. Glue the results [5] and [0] to the right side (Augmented Matrix).
        3. Perform RREF (Gauss-Jordan) until the left side is an Identity matrix.
        4. The right side now holds the answers: x = 1, y = 3.
        
        [HOW IT WORKS IN CODE]:
        We manually stitch the constants vector to the end of our rows, call 
        our newly minted rref() algorithm, and then analyze the result. If a row 
        shows 0x + 0y = 5, we throw an Inconsistent error (SI). If we don't have 
        enough valid equations for our variables, we throw a Dependent error (SPI).

        Obs: self -> Variables Matrix | augmented_matrix or [A | B] or reduced_matrix -> [ Variables | Constants]
        """
        if self.rows != constants.rows:
            raise ValueError("Matrix and Constants doesn't have the number of rows.")

        if constants.cols != 1:
            raise ValueError("Constants must be a column vector (i.e. nx1)")

        augmented_data = []
        for row_index in range(self.rows):
            augmented_row = self.data[row_index][:]
            augmented_row.append(constants.data[row_index][0])
            augmented_data.append(augmented_row)
        augmented_matrix = Matrix(augmented_data)

        reduced_matrix = augmented_matrix.rref()

        non_zero_rows = 0
        for row_index in range(reduced_matrix.rows):
            constant = reduced_matrix.data[row_index][reduced_matrix.cols - 1]
            all_zeros = True
            for column_index in range(self.cols):
                if abs(reduced_matrix.data[row_index][column_index]) > 1e-7:
                    all_zeros = False

            if all_zeros and abs(constant) > 1e-7:
                print("System is Inconsistent (No solution). Using least squares to find approximate solution.")
                regression_matrix = self.least_squares(constants)
                approximated_solutions = []
                for approximated_solution in regression_matrix.data:
                    approximated_solutions.append(round(approximated_solution[0], 2))
                return approximated_solutions
            elif not all_zeros:
                non_zero_rows += 1

        if non_zero_rows < self.cols:
            raise ValueError("System has Infinite Solutions")

        solutions = []
        for row_index in range(self.cols):
            value = reduced_matrix.data[row_index][reduced_matrix.cols - 1]
            solutions.append(round(value, 2))
        return solutions

    def inverse(self):
        """
        [MATH ON PAPER]: Finding the Inverse Matrix.
        1. Write your matrix A.
        2. Write an Identity matrix of the same size next to it: [A | I].
        3. Perform RREF.
        4. The left side becomes I. The right side becomes A^(-1).
        """
        if self.rows != self.cols:
            raise ValueError("Only square matrices can be inverted.")

        if self.determinant() == 0:
            raise ValueError ("Matrix is singular (determinant is 0) and cannot be inverted.")

        identity_matrix = Matrix.identity(self.rows, self.cols)
        augmented_data = []
        for row_index in range(self.rows):
            row = self.data[row_index][:]
            identity_matrix_row = identity_matrix.data[row_index][:]
            augmented_data.append(row + identity_matrix_row)

        augmented_matrix = Matrix(augmented_data)
        reduced_matrix = augmented_matrix.rref()
        inverse_data = []
        for row_index in range(reduced_matrix.rows):
            right_side_matrix_row = []
            for column_index in range(self.cols, reduced_matrix.cols):
                right_side_matrix_row.append(reduced_matrix.data[row_index][column_index])
            inverse_data.append(right_side_matrix_row)

        inverse_matrix = Matrix(inverse_data)
        return inverse_matrix

    def least_squares(self, constants):
        """
        [MATH ON PAPER]: Regressão Linear / Mínimos Quadrados.
        Fórmula: X = (A^T * A)^-1 * A^T * B
        Usado para encontrar a melhor aproximação para sistemas impossíveis (mais equações que variáveis).
        """
        transposed = self.transpose()
        transposed_self = transposed @ self
        inversed_transposed_self = transposed_self.inverse()
        transposed_constants = transposed @ constants
        regression_vector = inversed_transposed_self @ transposed_constants
        return regression_vector

    def column_space(self):
        """
        [MATEMÁTICA]: Espaço Coluna (Column Space).
        O espaço coluna de uma matriz A é o subespaço gerado por suas colunas. 
        Para encontrar uma base para o espaço coluna:
        1. Calculamos a RREF da matriz para identificar onde estão as colunas pivô.
        2. As colunas da matriz RREF que possuem pivôs indicam quais são as 
           colunas ORIGINAIS de A que formam a base do espaço coluna.
           
        [PASSO A PASSO PARA IMPLEMENTAR]:
        1. Obtenha a matriz RREF chamando self.rref().
        2. Percorra as colunas da RREF da esquerda para a direita.
        3. Identifique quais colunas possuem um pivô (geralmente o primeiro elemento 
           não nulo de uma linha escalonada, respeitando a tolerância de 1e-7).
        4. Para cada índice de coluna pivô encontrado, extraia a coluna CORRESPONDENTE 
           da matriz ORIGINAL (self).
        5. Retorne uma lista contendo esses vetores (ou uma nova Matrix formada por essas colunas).
        """
        # TODO: Implementar a extração das colunas pivô baseadas na RREF
        raise NotImplementedError("Método column_space ainda não implementado.")

    def null_space(self):
        """
        [MATEMÁTICA]: Espaço Nulo ou Núcleo (Null Space / Kernel).
        O espaço nulo consiste em todas as soluções do sistema homogêneo Ax = 0.
        Para encontrá-lo:
        1. Aplica-se a RREF na matriz aumentada com zeros [A | 0].
        2. Identificam-se as colunas com pivô (variáveis básicas) e as sem pivô (variáveis livres).
        3. Expressam-se as variáveis básicas em função das variáveis livres, gerando 
           os vetores que compõem a base do núcleo.
           
        [PASSO A PASSO PARA IMPLEMENTAR]:
        1. Obtenha a RREF da matriz.
        2. Mapeie quais colunas são variáveis básicas (têm pivô) e quais são livres.
        3. Se não houver variáveis livres (apenas solução trivial x = 0), retorne um vetor nulo.
        4. Para cada variável livre, atribua o valor 1 para ela e 0 para as outras livres, 
           resolvendo o sistema linear resultante para encontrar os componentes dos vetores base.
        5. Retorne a lista de vetores que formam a base do espaço nulo.
        """
        # TODO: Implementar o cálculo das soluções do sistema homogêneo Ax = 0
        raise NotImplementedError("Método null_space ainda não implementado.")
