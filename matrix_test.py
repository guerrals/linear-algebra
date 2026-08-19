from matrix import Matrix

def run_tests():
    print("Starting Matrix Operations Tests...\n")
    passed_tests = 0
    total_tests = 4

    # Define our test matrices
    A = Matrix([[1, 2], 
                [3, 4]])
    
    B = Matrix([[5, 6], 
                [7, 8]])

    # ---------------------------------------------------------
    # TEST 1: Addition
    # ---------------------------------------------------------
    try:
        result_add = A + B
        expected_add = [[6, 8], 
                        [10, 12]]
        
        assert result_add.data == expected_add, f"Expected {expected_add}, got {result_add.data}"
        print("✅ Addition (A + B): PASSED")
        passed_tests += 1
    except Exception as e:
        print(f"❌ Addition (A + B): FAILED -> {e}")

    # ---------------------------------------------------------
    # TEST 2: Scalar Multiplication
    # ---------------------------------------------------------
    try:
        result_scalar = A * 3
        expected_scalar = [[3, 6], 
                           [9, 12]]
        
        assert result_scalar.data == expected_scalar, f"Expected {expected_scalar}, got {result_scalar.data}"
        print("✅ Scalar Multiplication (A * 3): PASSED")
        passed_tests += 1
    except Exception as e:
        print(f"❌ Scalar Multiplication (A * 3): FAILED -> {e}")

    # ---------------------------------------------------------
    # TEST 3: Matrix Multiplication (Dot Product)
    # ---------------------------------------------------------
    try:
        result_mult = A @ B
        expected_mult = [[19, 22], 
                         [43, 50]]
        
        assert result_mult.data == expected_mult, f"Expected {expected_mult}, got {result_mult.data}"
        print("✅ Matrix Multiplication (A @ B): PASSED")
        passed_tests += 1
    except Exception as e:
        print(f"❌ Matrix Multiplication (A @ B): FAILED -> {e}")

    # ---------------------------------------------------------
    # TEST 4: Transpose
    # ---------------------------------------------------------
    try:
        result_transpose = A.transpose()
        expected_transpose = [[1, 3], 
                              [2, 4]]
        
        assert result_transpose.data == expected_transpose, f"Expected {expected_transpose}, got {result_transpose.data}"
        print("✅ Transpose (A^T): PASSED")
        passed_tests += 1
    except Exception as e:
        print(f"❌ Transpose (A^T): FAILED -> {e}")

    # ---------------------------------------------------------
    # Final Score
    # ---------------------------------------------------------
    print("\n" + "="*30)
    print(f"TEST RESULTS: {passed_tests}/{total_tests} Passed")
    print("="*30)
    if passed_tests == total_tests:
        print("🎉 Congratulations! All core matrix operations are working perfectly.")

if __name__ == "__main__":
    run_tests()