from matrix import Matrix

def display_menu():
    print("\n" + "="*35)
    print(" 🧮 LINEAR ALGEBRA TOOLKIT 🧮 ")
    print("="*35)
    print("1. Create a Matrix (Manual)")
    print("2. Create a Matrix (Random)")
    print("3. Create an Identity Matrix")
    print("4. Create a Zero Matrix")
    print("5. View Stored Matrices")
    print("6. Matrix Addition (A + B)")
    print("7. Matrix Subtraction (A - B)")
    print("8. Scalar Multiplication (c * A)")
    print("9. Matrix Multiplication (A @ B)")
    print("10. Transpose Matrix (A^T)")
    print("11. Calculate Determinant")
    print("12. Reduced Row Echelon Form (RREF)")
    print("13. Solve Linear System (Ax = B)")
    print("14. Inverse Matrix (A^-1)")
    print("15. Visualize 2D Linear System (Graph)")
    print("0. Exit")
    print("="*35)

def get_matrix_name(prompt="Enter the name for this matrix (e.g., A, B, M1): "):
    return input(prompt).strip().upper()

def main():
    # Dictionary to store all the matrices the user creates
    matrices = {}

    while True:
        display_menu()
        choice = input("Select an option (0-14): ").strip()

        try:
            if choice == '1':
                name = get_matrix_name()
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                
                print(f"Enter the elements row by row (separated by spaces):")
                data = []
                for i in range(rows):
                    row_input = input(f"Row {i+1}: ").strip().split()
                    if len(row_input) != cols:
                        print(f"Error: You must enter exactly {cols} numbers.")
                        break
                    # Convert input strings to floats to support decimals easily
                    data.append([float(x) for x in row_input])
                else:
                    matrices[name] = Matrix(data)
                    print(f"\nMatrix '{name}' saved successfully!")

            elif choice == '2':
                name = get_matrix_name()
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                matrices[name] = Matrix.random(rows, cols)
                print(f"\nRandom Matrix '{name}' saved successfully!")

            elif choice == '3':
                name = get_matrix_name()
                size = int(input("Enter the size of the square matrix (e.g., 3 for 3x3): "))
                matrices[name] = Matrix.identity(size, size)
                print(f"\nIdentity Matrix '{name}' saved successfully!")

            elif choice == '4':
                name = get_matrix_name()
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                matrices[name] = Matrix.zeros(rows, cols)
                print(f"\nZero Matrix '{name}' saved successfully!")

            elif choice == '5':
                if not matrices:
                    print("\nNo matrices stored yet.")
                for name, matrix in matrices.items():
                    print(f"\n--- Matrix {name} ---")
                    print(matrix)

            elif choice == '6':
                name1 = get_matrix_name("Enter name of first matrix: ")
                name2 = get_matrix_name("Enter name of second matrix: ")
                
                result = matrices[name1] + matrices[name2]
                print("\nResult of Addition:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '7':
                name1 = get_matrix_name("Enter name of first matrix (A): ")
                name2 = get_matrix_name("Enter name of second matrix (B): ")
                
                result = matrices[name1] - matrices[name2]
                print("\nResult of Subtraction (A - B):")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '8':
                name = get_matrix_name("Enter name of matrix: ")
                scalar = float(input("Enter the scalar value: "))
                
                result = matrices[name] * scalar
                print("\nResult of Scalar Multiplication:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '9':
                name1 = get_matrix_name("Enter name of first matrix (A): ")
                name2 = get_matrix_name("Enter name of second matrix (B): ")
                
                result = matrices[name1] @ matrices[name2]
                print("\nResult of Matrix Multiplication:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '10':
                name = get_matrix_name("Enter name of matrix to transpose: ")
                
                result = matrices[name].transpose()
                print("\nResult of Transposition:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '11':
                name = get_matrix_name("Enter name of matrix to calculate determinant: ")
                
                det = matrices[name].determinant()
                print(f"\nResult: The determinant of Matrix {name} is {det}")

            elif choice == '12':
                name = get_matrix_name("Enter name of matrix to calculate RREF: ")
                
                result = matrices[name].rref()
                print("\nResulting Reduced Row Echelon Form:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '13':
                print("\n[Note: You need a coefficient matrix (A) and a constants column matrix (B)]")
                name_a = get_matrix_name("Enter name of coefficient matrix (A): ")
                name_b = get_matrix_name("Enter name of constants matrix (B): ")
                
                solutions = matrices[name_a].solve(matrices[name_b])
                
                print("\n✅ System Solved Successfully:")
                # We usually map variables as x, y, z for readability, or x1, x2, x3...
                variables = ['x', 'y', 'z', 'w', 'v'] 
                for i, sol in enumerate(solutions):
                    var_name = variables[i] if i < len(variables) else f"x_{i+1}"
                    print(f"  {var_name} = {sol}")

            elif choice == '14':
                name = get_matrix_name("Enter name of matrix to invert: ")
                
                result = matrices[name].inverse()
                print("\nResulting Inverse Matrix:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '0':
                print("Exiting Toolkit. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 0 and 14.")

        except KeyError as e:
            print(f"\n❌ Error: Matrix {e} not found in storage. Please create it first.")
        except ValueError as e:
            print(f"\n❌ Math/Input Error: {e}")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()