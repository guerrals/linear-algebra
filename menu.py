from matrix import Matrix

def display_menu():
    print("\n" + "="*30)
    print(" 🧮 LINEAR ALGEBRA TOOLKIT 🧮 ")
    print("="*30)
    print("1. Create a Matrix (Manual)")
    print("2. Create a Matrix (Random)")
    print("3. View Stored Matrices")
    print("4. Matrix Addition (A + B)")
    print("5. Scalar Multiplication (c * A)")
    print("6. Matrix Multiplication (A @ B)")
    print("7. Transpose Matrix (A^T)")
    print("8. Exit")
    print("="*30)

def get_matrix_name(prompt="Enter the name for this matrix (e.g., A, B, M1): "):
    return input(prompt).strip().upper()

def main():
    # Dictionary to store all the matrices the user creates
    matrices = {}

    while True:
        display_menu()
        choice = input("Select an option (1-8): ").strip()

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
                    # Convert input strings to ints
                    data.append([int(x) for x in row_input])
                else:
                    matrices[name] = Matrix(data)
                    print(f"\nMatrix '{name}' saved successfully!")

            elif choice == '2':
                name = get_matrix_name()
                rows = int(input("Enter number of rows: "))
                cols = int(input("Enter number of columns: "))
                # Using the random classmethod you implemented earlier
                matrices[name] = Matrix.random(rows, cols)
                print(f"\nRandom Matrix '{name}' saved successfully!")

            elif choice == '3':
                if not matrices:
                    print("\nNo matrices stored yet.")
                for name, matrix in matrices.items():
                    print(f"\n--- Matrix {name} ---")
                    print(matrix)

            elif choice == '4':
                name1 = get_matrix_name("Enter name of first matrix: ")
                name2 = get_matrix_name("Enter name of second matrix: ")
                
                result = matrices[name1] + matrices[name2]
                print("\nResult of Addition:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '5':
                name = get_matrix_name("Enter name of matrix: ")
                scalar = float(input("Enter the scalar value: "))
                
                result = matrices[name] * scalar
                print("\nResult of Scalar Multiplication:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '6':
                name1 = get_matrix_name("Enter name of first matrix (A): ")
                name2 = get_matrix_name("Enter name of second matrix (B): ")
                
                result = matrices[name1] @ matrices[name2]
                print("\nResult of Matrix Multiplication:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '7':
                name = get_matrix_name("Enter name of matrix to transpose: ")
                
                result = matrices[name].transpose()
                print("\nResult of Transposition:")
                print(result)
                
                if input("Save this result? (y/n): ").strip().lower() == 'y':
                    matrices[get_matrix_name("Save as: ")] = result

            elif choice == '8':
                print("Exiting Toolkit. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter a number between 1 and 8.")

        except KeyError as e:
            print(f"\n❌ Error: Matrix {e} not found in storage. Please create it first.")
        except ValueError as e:
            print(f"\n❌ Math/Input Error: {e}")
        except Exception as e:
            print(f"\n❌ An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()