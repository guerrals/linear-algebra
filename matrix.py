import random

class Matrix:
    def __init__(self, data):
        """
        Initialize the matrix.
        'data' is a list of lists, e.g., [[1, 2], [3, 4]]
        
        TODO: 
        1. Store the data.
        2. Calculate and store self.rows (number of rows).
        3. Calculate and store self.cols (number of columns).
        4. (Optional) Check that all rows have the same length.
        """
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    @classmethod
    def random(cls, rows, cols, seed=None):
        """
        Generates a new Matrix of size (rows x cols) 
        filled with random integers between 0 and 99.
        """
        if seed is not None:
            random.seed(seed)

        data = []
        for _ in range(rows):
            new_row = []
            for _ in range(cols):
                new_row.append(random.randint(0, 99))
            data.append(new_row)

        return cls(data)

    def __str__(self):
        """
        Prints the matrix with separating lines for rows and columns.
        """
        if not self.data:
            return "Empty Matrix"

        # 1. Calculate the maximum string width for each column
        col_widths = []
        for j in range(self.cols):
            # Extract column j, convert to string, and find the max length
            max_width = max(len(str(self.data[i][j])) for i in range(self.rows))
            col_widths.append(max_width)

        # 2. Build the horizontal separator (e.g., +----+-------+)
        separator = "+"
        for width in col_widths:
            separator += "-" * (width + 2) + "+"  # +2 accounts for the left/right space padding

        # 3. Construct the full grid
        result = [separator]
        for i in range(self.rows):
            row_str = "|"
            for j in range(self.cols):
                # Format the number, right-aligned (>) to the column's max width
                val = str(self.data[i][j])
                row_str += f" {val:>{col_widths[j]}} |"
            
            result.append(row_str)
            result.append(separator)

        return '\n'.join(result)

    def __add__(self, other):
        """
        Matrix Addition: A + B
        
        Math: $C_{ij} = A_{ij} + B_{ij}$
        
        TODO:
        1. Check if self.rows == other.rows and self.cols == other.cols.
           (Raise a ValueError if they don't match!)
        2. Create a new list of lists containing the summed elements.
        3. Return a new Matrix object with the resulting data.
        """

        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions to add.")

        data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] + other.data[row_index][column_index])
            data.append(row)
        return Matrix(data)

    def __sub__(self, other):
        """
        Matrix Subtraction: A - B
        
        Math: $C_{ij} = A_{ij} - B_{ij}$
        """
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrices must have the same dimensions to add.")

        data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] - other.data[row_index][column_index])
            data.append(row)

        return Matrix(data)

    def __mul__(self, scalar):
        """
        Scalar Multiplication: A * c

        Math: $C_{ij} = c \\times A_{ij}$

        TODO:
        Multiply every element in the matrix by the 'scalar' value.
        """
        if not isinstance(scalar, (int, float)):
            raise TypeError(f"Cannot multiply Matrix by non-scalar of type '{type(scalar).__name__}'")

        data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(self.cols):
                row.append(self.data[row_index][column_index] * scalar)
            data.append(row)
        return Matrix(data)

    def __rmul__(self, scalar):
        """
        Provided for you! This allows scalar * A (reverse order).
        It simply calls your __mul__ method.
        """
        return self.__mul__(scalar)

    def __matmul__(self, other):
        """
        Matrix Multiplication (Dot Product): A @ B
        
        Math: $C_{ij} = \\sum_{k=1}^{n} A_{ik} B_{kj}$
        
        TODO:
        1. Check if self.cols == other.rows. (Raise ValueError if not).
        2. Create a new matrix of size (self.rows x other.cols).
        3. Compute the dot product for each row/column pair.
        """

        if self.cols != other.rows:
            raise ValueError(f"Cannot multiply {self.rows}x{self.cols} by {other.rows}x{other.cols}.")

        data = []
        for row_index in range(self.rows):
            row = []
            for column_index in range(other.cols):
                product = 0 
                for product_index in range(other.cols):
                    product += self.data[row_index][product_index] * other.data[product_index][column_index]
                row.append(product)
            data.append(row)
        return Matrix(data)

    def transpose(self):
        """
        Matrix Transposition: A^T

        Math: $A^T_{ij} = A_{ji}$

        TODO:
        Swap the rows and columns. A matrix of size (m x n) becomes (n x m).
        """
        data = []
        for column_index in range(self.cols):
            row = []
            for row_index in range(self.rows):
                row.append(self.data[row_index][column_index])
            data.append(row)
        return Matrix(data)
