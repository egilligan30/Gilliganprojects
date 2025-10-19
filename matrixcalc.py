import sympy as sp

def get_determinant(M, depth=0):
     n = M.rows
     indent = "  " * depth
     show_steps = True


     if show_steps:
         print(f"\n{indent}Computing determinant of {n}×{n} matrix:")
         sp.pprint(M)
         print(f"{indent}" + "-" * 50)
     #1x1 matrix
     if n == 1:
         val = M[0, 0]
         print(f"{indent}Base case (1×1): det = {val}")
         return val
     #2x2 matrix
     if n == 2:
         a, b = M[0, 0], M[0, 1]
         c, d = M[1, 0], M[1, 1]
         det = a * d - b * c
         print(f"{indent}2×2: det = {a}×{d} - {b}×{c} = {det}")
         return det


     det = 0
     term_strings = []


     for col in range(n):
         sign = (-1) ** col
         coeff = M[0, col]
         submatrix = M.minor_submatrix(0, col)

         print(f"\n{indent}→ Expanding on a[1,{col+1}] = {coeff} with sign {sign}")
         print(f"{indent}  Submatrix (remove row 1, column {col+1}):")
         sp.pprint(submatrix)


         subdet = get_determinant(submatrix, depth + 1)
         term = sign * coeff * subdet
         det += term

         term_str = f"{sign}×{coeff}×{subdet}"
         term_strings.append(term_str)


         print(f"{indent}  Term = {term_str} = {term}")
         print(f"{indent}  Running total = {det}")
         print(f"{indent}" + "-" * 50)


     if depth == 0:
         full_expansion = " + ".join(term_strings)
         print(f"\nSum of terms: {full_expansion} = {det}")
         print(f"\ninal Determinant = {det}")


     builtin_det = M.det()
     print(f"sympy.det(): {builtin_det}")
     if builtin_det != det:
         print("Mismatch! Custom result doesn't match sympy.")
     else:
         print("Validation: Custom result matches sympy.")


     return det

def get_invertible_matrix():
    while True:
        try:
            print("\n" + "="*60)
            print("           USER MATRIX INPUT (FOR INVERSE)")
            print("="*60)


            n = int(input("Enter the size n of the n x n matrix: "))
            print(f"\nEnter the matrix row by row (each row should have {n} numbers separated by spaces):")
            matrix = []
            for i in range(n):
                row = list(map(sp.sympify, input(f"Row {i+1}: ").strip().split()))
                if len(row) != n:
                    raise ValueError(f"Each row must have exactly {n} elements.")
                matrix.append(row)


            A = sp.Matrix(matrix)


            det = A.det()
            print(f"\nDeterminant: {det}")


            if det == 0:
                print("\nThe matrix is **not invertible** (det = 0).")
                print("Please input a different matrix.\n")
            else:
                print("\nMatrix is invertible (det ≠ 0). Proceeding to RREF...")
                return A


        except Exception as e:
            print("Invalid input:", e)
            print("Please try again.\n")

def rref(A):
    A = A.copy()
    rows, cols = A.shape
    pivot_row = 0
    step = 1


    print("\n" + "="*60)
    print("       REDUCED ROW ECHELON FORM (RREF)")
    print("="*60)
    print("\n=== INITIAL MATRIX ===")
    sp.pprint(A)
    print("=" * 60)


    for pivot_col in range(cols):
        if pivot_row >= rows:
            break


        # Step 1: Find pivot
        max_row = None
        for r in range(pivot_row, rows):
            if A[r, pivot_col] != 0:
                max_row = r
                break
        if max_row is None:
            continue


        # Step 2: Swap
        if max_row != pivot_row:
            print(f"\n=== SWAP ROWS ===")
            print(f"Step {step}: Swap row {pivot_row+1} with row {max_row+1}")
            A.row_swap(pivot_row, max_row)
            sp.pprint(A)
            print("=" * 60)
            step += 1


        # Step 3: Normalize pivot row
        pivot_val = A[pivot_row, pivot_col]
        if pivot_val != 1:
            print(f"\n=== NORMALIZE PIVOT ROW ===")
            print(f"Step {step}: Normalize row {pivot_row+1} (divide by {pivot_val})")
            A.row_op(pivot_row, lambda x, _: x / pivot_val)
            sp.pprint(A)
            print("=" * 60)
            step += 1


        # Step 4: Eliminate below
        for r in range(pivot_row + 1, rows):
            factor = A[r, pivot_col]
            if factor != 0:
                print(f"\n=== ELIMINATE BELOW ===")
                print(f"Step {step}: row {r+1} - ({factor}) * row {pivot_row+1}")
                A.row_op(r, lambda x, j: x - factor * A[pivot_row, j])
                sp.pprint(A)
                print("=" * 60)
                step += 1


        pivot_row += 1


    # Step 5: Eliminate above
    for pivot_row in reversed(range(rows)):
        pivot_cols = [c for c in range(cols) if A[pivot_row, c] == 1]
        if not pivot_cols:
            continue
        pivot_col = pivot_cols[0]


        for r in range(pivot_row):
            factor = A[r, pivot_col]
            if factor != 0:
                print(f"\n=== ELIMINATE ABOVE ===")
                print(f"Step {step}: row {r+1} - ({factor}) * row {pivot_row+1}")
                A.row_op(r, lambda x, j: x - factor * A[pivot_row, j])
                sp.pprint(A)
                print("=" * 60)
                step += 1


    print("\n=== FINAL RREF MATRIX ===")
    sp.pprint(A)
    print("=" * 60)
    return A

def find_inverse(A):
    n, m = A.shape
    if n != m:
        raise ValueError("Matrix must be square to compute its inverse.")


    print("\n" + "=" * 60)
    print("        AUGMENTED MATRIX [ A | I ]")
    print("=" * 60)


    I = sp.eye(n)
    augmented = A.row_join(I)
    sp.pprint(augmented)


    print("\n" + "=" * 60)
    print("        REDUCING TO [ I | A⁻¹ ] VIA RREF")
    print("=" * 60)


    inverse_augmented = rref(augmented)


    print("\n" + "=" * 60)
    print("        FINAL INVERSE MATRIX (Right Half)")
    print("=" * 60)


    inverse = inverse_augmented[:, n:]
    sp.pprint(inverse)


    print("\n" + "=" * 60)
    print("        VALIDATING: A × A⁻¹ = I ?")
    print("=" * 60)


    product = A * inverse
    simplified_product = product.applyfunc(sp.simplify)
    sp.pprint(simplified_product)


    if simplified_product == sp.eye(n):
        print("\nValidation passed: A × A⁻¹ = I")
    else:
        print("\nValidation failed: A × A⁻¹ ≠ I")


    return inverse

def user_input_matrix():
    print("Enter the size of the matrix (n for n x n):")
    n = int(input("n = "))

    print(f"Enter the {n}x{n} matrix row by row, with space-separated numbers:")
    matrix_data = []

    for i in range(n):
        while True:
            row_input = input(f"Row {i+1}: ")
            row_values = row_input.strip().split()
            if len(row_values) != n:
                print(f"Please enter exactly {n} numbers.")
            else:
                try:
                    row = [sp.sympify(val) for val in row_values]
                    matrix_data.append(row)
                    break
                except Exception:
                    print("Invalid input. Please enter numbers or valid expressions.")

    return sp.Matrix(matrix_data)

# (to actually run remove the hash and this text in parentheses) A = get_invertible_matrix()
# (same as above) find_inverse(A)
