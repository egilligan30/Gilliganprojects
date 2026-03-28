"""
Matrix Operations Toolkit
------------------------
Purpose:
    A comprehensive toolkit for symbolic matrix operations using SymPy, including:
    - Determinants via recursive cofactor expansion
    - Manual RREF computation
    - Matrix inversion using augmented matrices
    - Eigenvalue and eigenvector computation
    - Diagonalization of square matrices

Outline:
    1. get_determinant: Compute determinant recursively
    2. get_invertible_matrix: Prompt user until an invertible matrix is provided
    3. rref: Manual computation of Reduced Row Echelon Form
    4. find_inverse: Compute matrix inverse using augmented matrix and RREF
    5. user_input_matrix: General matrix input helper
    6. manual_factor_polynomial: Factor characteristic polynomial and find roots
    7. compute_eigenvalues: Compute eigenvalues manually
    8. extract_nullspace_from_rref: Construct basis vectors for null space
    9. compute_eigenvectors: Compute eigenvectors for all eigenvalues
   10. diagonalize_matrix: Diagonalize matrix using eigenvectors and eigenvalues
   11. get_matrix_for_eigen: Prompt user for a square matrix for eigen computations
"""

import sympy as sp

# ---------------------- Determinant ----------------------
def get_determinant(M, depth=0):
    """
    Compute the determinant of a square matrix M recursively using cofactor expansion.
    Prints step-by-step details for learning purposes.
    
    Parameters:
        M (sp.Matrix): The matrix for which to compute the determinant.
        depth (int): Recursion depth for indentation in print statements.
    
    Returns:
        det (sp.Expr): Determinant of the matrix.
    """
    n = M.rows  # Get matrix size
    indent = "  " * depth  # Indentation for nested recursion

    print(f"\n{indent}Computing determinant of {n}×{n} matrix:")
    sp.pprint(M)
    print(f"{indent}" + "-" * 50)

    # Base case: 1x1 matrix
    if n == 1:
        val = M[0, 0]  # The only element is the determinant
        print(f"{indent}Base case (1×1): det = {val}")
        return val

    # Base case: 2x2 matrix
    if n == 2:
        a, b = M[0, 0], M[0, 1]
        c, d = M[1, 0], M[1, 1]
        det = a*d - b*c  # Formula for 2x2 determinant
        print(f"{indent}2×2: det = {a}×{d} - {b}×{c} = {det}")
        return det

    # Recursive cofactor expansion for n > 2
    det = 0
    term_strings = []  # Store string representations of each term for printing

    for col in range(n):
        sign = (-1) ** col  # Alternating sign for cofactors
        coeff = M[0, col]   # Element from first row for expansion
        submatrix = M.minor_submatrix(0, col)  # Matrix obtained by removing row 0 and current column

        print(f"\n{indent}→ Expanding on a[1,{col+1}] = {coeff} with sign {sign}")
        print(f"{indent}  Submatrix:")
        sp.pprint(submatrix)

        # Recursive call to compute determinant of submatrix
        subdet = get_determinant(submatrix, depth + 1)
        term = sign * coeff * subdet  # Compute current cofactor term
        det += term
        term_strings.append(f"{sign}×{coeff}×{subdet}")  # Record term for final display

        print(f"{indent}  Term = {term_strings[-1]} = {term}")
        print(f"{indent}  Running total = {det}")
        print(f"{indent}" + "-" * 50)

    if depth == 0:  # Top-level call: summarize result
        print(f"\nSum of terms: {' + '.join(term_strings)} = {det}")
        print(f"\nFinal Determinant = {det}")

        # Optional: Validate against SymPy's built-in determinant
        builtin_det = M.det()
        print(f"sympy.det(): {builtin_det}")
        if builtin_det != det:
            print("Mismatch! Custom result doesn't match sympy.")
        else:
            print("Validation: Custom result matches sympy.")

    return det


# ---------------------- Matrix Input & Validation ----------------------
def user_input_matrix(prompt="Enter matrix"):
    """
    Prompts user to input a square matrix of size n x n.
    Converts input strings to symbolic expressions using SymPy.
    
    Returns:
        sp.Matrix: User-input square matrix
    """
    n = int(input(f"{prompt} - size n x n, n = "))
    matrix_data = []

    for i in range(n):
        while True:
            row_input = input(f"Row {i+1}: ")
            row_values = row_input.strip().split()
            if len(row_values) != n:
                print(f"Please enter exactly {n} numbers.")
            else:
                try:
                    # Convert each input to a SymPy expression for symbolic calculations
                    row = [sp.sympify(val) for val in row_values]
                    matrix_data.append(row)
                    break
                except Exception:
                    print("Invalid input. Please enter numbers or valid expressions.")

    return sp.Matrix(matrix_data)


def get_invertible_matrix():
    """
    Repeatedly prompts user to input a square matrix until it is invertible.
    Computes determinant to ensure non-singularity.
    
    Returns:
        sp.Matrix: Invertible square matrix
    """
    while True:
        A = user_input_matrix("Input matrix for inversion")
        det = get_determinant(A)
        print(f"\nDeterminant: {det}")

        if det == 0:
            print("\nMatrix is not invertible (det = 0). Please input a different matrix.\n")
        else:
            print("\nMatrix is invertible (det ≠ 0). Proceeding to inversion...")
            return A


# ---------------------- Manual RREF ----------------------
def rref(A):
    """
    Computes the Reduced Row Echelon Form (RREF) of a matrix manually.
    Prints each elementary row operation step.
    
    Returns:
        sp.Matrix: Matrix in RREF
    """
    A = A.copy()
    rows, cols = A.shape
    pivot_row = 0
    step = 1

    print("\n=== INITIAL MATRIX ===")
    sp.pprint(A)
    print("=" * 60)

    # Forward elimination to form echelon
    for pivot_col in range(cols):
        if pivot_row >= rows:
            break

        # Find a row with non-zero pivot
        max_row = None
        for r in range(pivot_row, rows):
            if A[r, pivot_col] != 0:
                max_row = r
                break
        if max_row is None:
            continue

        # Swap rows if needed
        if max_row != pivot_row:
            print(f"\nStep {step}: Swap row {pivot_row+1} with row {max_row+1}")
            A.row_swap(pivot_row, max_row)
            sp.pprint(A)
            step += 1

        # Normalize pivot to 1
        pivot_val = A[pivot_row, pivot_col]
        if pivot_val != 1:
            print(f"\nStep {step}: Normalize row {pivot_row+1} (divide by {pivot_val})")
            A.row_op(pivot_row, lambda x, _: x / pivot_val)
            sp.pprint(A)
            step += 1

        # Eliminate entries below pivot
        for r in range(pivot_row + 1, rows):
            factor = A[r, pivot_col]
            if factor != 0:
                print(f"\nStep {step}: row {r+1} - ({factor})*row {pivot_row+1}")
                A.row_op(r, lambda x, j: x - factor * A[pivot_row, j])
                sp.pprint(A)
                step += 1

        pivot_row += 1

    # Backward elimination to remove entries above pivots
    for pivot_row in reversed(range(rows)):
        pivot_cols = [c for c in range(cols) if A[pivot_row, c] == 1]
        if not pivot_cols:
            continue
        pivot_col = pivot_cols[0]

        for r in range(pivot_row):
            factor = A[r, pivot_col]
            if factor != 0:
                print(f"\nStep {step}: row {r+1} - ({factor})*row {pivot_row+1}")
                A.row_op(r, lambda x, j: x - factor * A[pivot_row, j])
                sp.pprint(A)
                step += 1

    print("\n=== FINAL RREF MATRIX ===")
    sp.pprint(A)
    return A


# ---------------------- Matrix Inversion ----------------------
def find_inverse(A):
    """
    Computes the inverse of a square matrix A using augmented matrix method.
    Steps:
        1. Form augmented matrix [A | I]
        2. Reduce to RREF to get [I | A⁻¹]
    Prints each major step for educational purposes.
    
    Parameters:
        A (sp.Matrix): Invertible square matrix
    
    Returns:
        sp.Matrix: Inverse of A
    """
    n, m = A.shape
    if n != m:
        raise ValueError("Matrix must be square to compute its inverse.")

    print("\n=== AUGMENTED MATRIX [ A | I ] ===")
    I = sp.eye(n)  # Identity matrix of same size
    augmented = A.row_join(I)  # Create [A | I]
    sp.pprint(augmented)

    print("\n=== REDUCING TO [ I | A⁻¹ ] VIA RREF ===")
    inverse_augmented = rref(augmented)  # Use manual RREF to reduce

    print("\n=== FINAL INVERSE MATRIX (Right Half) ===")
    inverse = inverse_augmented[:, n:]  # Extract right half
    sp.pprint(inverse)

    # Validation: A * A⁻¹ should equal I
    print("\n=== VALIDATION: A * A⁻¹ = I ===")
    product = A * inverse
    simplified_product = product.applyfunc(sp.simplify)
    sp.pprint(simplified_product)
    if simplified_product == sp.eye(n):
        print("Validation passed: A × A⁻¹ = I")
    else:
        print("Validation failed: A × A⁻¹ ≠ I")

    return inverse


# ---------------------- Characteristic Polynomial & Eigenvalues ----------------------
def manual_factor_polynomial(poly, var):
    """
    Factor a polynomial and compute its roots.
    Prints factorization, roots, and multiplicities.
    
    Parameters:
        poly (sp.Expr): Polynomial expression
        var (sp.Symbol): Variable in polynomial
    
    Returns:
        dict: Dictionary mapping root -> algebraic multiplicity
    """
    print("\n=== FACTORING CHARACTERISTIC POLYNOMIAL ===")
    print(f"Polynomial: {poly}")
    factored = sp.factor(poly)
    print(f"Factored form: {factored}")

    # Solve for roots
    roots = sp.solve(poly, var)
    eigenvals_with_mult = {}
    for root in roots:
        root_simplified = sp.simplify(root)
        eigenvals_with_mult[root_simplified] = roots.count(root)

    print("Roots and multiplicities:")
    for root, mult in eigenvals_with_mult.items():
        print(f"  λ = {root}, multiplicity = {mult}")
    print("=" * 60)

    return eigenvals_with_mult


def compute_eigenvalues(A):
    """
    Compute eigenvalues of a square matrix A manually using:
        det(A - λI) = 0
    
    Returns:
        eigenvalues (list): Eigenvalues with repetitions
        eigenvals_dict (dict): Root -> algebraic multiplicity
        char_poly (sp.Expr): Characteristic polynomial
    """
    if A.rows != A.cols:
        raise ValueError("Matrix must be square for eigenvalues.")
    
    n = A.rows
    lam = sp.Symbol('lambda')
    I = sp.eye(n)

    print("\n=== COMPUTING CHARACTERISTIC POLYNOMIAL ===")
    char_matrix = A - lam * I
    print("Characteristic matrix (A - λI):")
    sp.pprint(char_matrix)

    char_poly_raw = get_determinant(char_matrix)  # Recursive determinant
    char_poly = sp.expand(char_poly_raw)
    print(f"\nExpanded characteristic polynomial: {char_poly}")

    eigenvals_dict = manual_factor_polynomial(char_poly, lam)

    # Flatten to list with repeated eigenvalues
    eigenvalues = []
    for eigval, mult in eigenvals_dict.items():
        eigenvalues.extend([eigval] * mult)

    print("Summary of eigenvalues (with multiplicities):")
    for eigval, mult in eigenvals_dict.items():
        print(f"λ = {eigval}, algebraic multiplicity = {mult}")
    return eigenvalues, eigenvals_dict, char_poly


# ---------------------- Null Space Extraction ----------------------
def extract_nullspace_from_rref(rref_matrix):
    """
    Constructs basis vectors for the null space from RREF matrix.
    
    Parameters:
        rref_matrix (sp.Matrix): RREF of (A - λI)
    
    Returns:
        list: List of basis vectors (sp.Matrix) for null space
    """
    rows, cols = rref_matrix.shape
    pivot_cols = []
    pivot_rows = []

    # Identify pivot and free columns
    for row in range(rows):
        for col in range(cols):
            if rref_matrix[row, col] != 0:
                pivot_cols.append(col)
                pivot_rows.append(row)
                break

    free_cols = [c for c in range(cols) if c not in pivot_cols]

    print(f"Pivot columns: {[c+1 for c in pivot_cols]}")
    print(f"Free columns: {[c+1 for c in free_cols]}")

    if not free_cols:
        print("No free variables: Null space = {0}")
        return []

    # Construct basis vectors
    basis_vectors = []
    for i, free_col in enumerate(free_cols):
        vec = [0] * cols
        vec[free_col] = 1  # Set free variable to 1

        # Back-substitute for basic variables
        for row in reversed(range(len(pivot_rows))):
            pivot_col = pivot_cols[row]
            sum_terms = sum(rref_matrix[row, col] * vec[col] for col in range(pivot_col+1, cols))
            vec[pivot_col] = -sum_terms
        basis_vectors.append(sp.Matrix(vec))

    return basis_vectors


# ---------------------- Eigenvectors ----------------------
def compute_eigenvectors(A, eigenvalues):
    """
    Compute eigenvectors for all eigenvalues of matrix A.
    Uses manual RREF and null space extraction.
    
    Returns:
        dict: eigenvalue -> list of basis eigenvectors
    """
    n = A.shape[0]
    eigenvectors_dict = {}
    unique_eigenvalues = list(set(eigenvalues))

    for eigval in unique_eigenvalues:
        print(f"\nEigenvectors for λ = {eigval}")
        I = sp.eye(n)
        null_matrix = A - eigval * I
        rref_matrix = rref(null_matrix)
        eigenvects = extract_nullspace_from_rref(rref_matrix)
        eigenvectors_dict[eigval] = eigenvects

    return eigenvectors_dict


# ---------------------- Diagonalization ----------------------
def diagonalize_matrix(A):
    """
    Diagonalizes matrix A if possible.
    Returns matrices P (eigenvectors) and D (diagonal eigenvalues)
    """
    n = A.shape[0]
    if A.rows != A.cols:
        raise ValueError("Matrix must be square to diagonalize.")

    eigenvalues, eigenvals_dict, _ = compute_eigenvalues(A)
    eigenvectors_dict = compute_eigenvectors(A, eigenvalues)

    total_eigenvectors = sum(len(vecs) for vecs in eigenvectors_dict.values())
    if total_eigenvectors < n:
        print("Matrix is NOT diagonalizable (insufficient independent eigenvectors).")
        return None, None

    # Construct P and D
    P_columns = []
    D_entries = []
    for eigval in eigenvals_dict.keys():
        for vec in eigenvectors_dict[eigval]:
            P_columns.append(vec)
            D_entries.append(eigval)
    P = sp.Matrix.hstack(*P_columns)
    D = sp.diag(*D_entries)

    # Verify diagonalization
    P_inv = find_inverse(P)
    if P * D * P_inv != A:
        print("Warning: Verification failed for A = P D P⁻¹")
    else:
        print("Matrix successfully diagonalized: A = P D P⁻¹")

    return P, D

def get_matrix_for_eigen():
    """
    Purpose:
        Prompts the user to input a square matrix for eigenvalue and diagonalization computations.
        Ensures valid input (correct size, numeric/symbolic entries).
    Returns:
        sp.Matrix object containing the user's input.
    """
    while True:  # Loop until a valid matrix is entered
        try:
            print("\n" + "="*60)
            print("      MATRIX INPUT (FOR EIGENVALUES/DIAGONALIZATION)")
            print("="*60)

            # Ask for matrix size
            n = int(input("Enter the size n of the n x n matrix: "))

            print(f"\nEnter the matrix row by row (each row should have {n} numbers separated by spaces):")
            matrix = []  # To store rows of the matrix

            # Loop through each row for input
            for i in range(n):
                # Convert input string to sympy expressions
                row = list(map(sp.sympify, input(f"Row {i+1}: ").strip().split()))
                
                # Ensure the user entered exactly n elements
                if len(row) != n:
                    raise ValueError(f"Each row must have exactly {n} elements.")
                
                matrix.append(row)  # Add row to matrix list

            # Convert list of lists into sympy Matrix object
            A = sp.Matrix(matrix)
            
            print("\nMatrix entered:")
            sp.pprint(A)  # Pretty-print the matrix
            return A  # Exit loop with valid matrix

        except Exception as e:  # Handle invalid input
            print("Invalid input:", e)
            print("Please try again.\n")


# ============================================================
# DRIVER CODE
# ============================================================

if __name__ == "__main__":
    # Display welcome banner and available operations
    print("\n" + "="*60)
    print("       MATRIX OPERATIONS TOOLKIT")
    print("="*60)
    print("\nAvailable operations:")
    print("1. Compute determinant (step-by-step cofactor expansion)")
    print("2. Find inverse matrix (via manual RREF)")
    print("3. Compute eigenvalues (manual characteristic polynomial)")
    print("4. Compute eigenvectors (manual null space extraction)")
    print("5. Diagonalize matrix (complete manual process)")
    print("="*60)
    
    # Prompt user for operation choice
    choice = input("\nEnter your choice (1-5): ").strip()
    
    # Branch to the appropriate function based on user input
    if choice == "1":
        # Determinant computation
        A = user_input_matrix()  # Safe user input
        get_determinant(A)       # Compute determinant with detailed steps
    
    elif choice == "2":
        # Inverse computation
        A = get_invertible_matrix()  # Ensures matrix is invertible
        find_inverse(A)              # Compute inverse manually via RREF
    
    elif choice == "3":
        # Eigenvalue computation
        A = get_matrix_for_eigen()      # Input square matrix
        compute_eigenvalues(A)          # Compute characteristic polynomial and eigenvalues
    
    elif choice == "4":
        # Eigenvector computation
        A = get_matrix_for_eigen()
        eigenvalues, eigenvals_dict, _ = compute_eigenvalues(A)  # First get eigenvalues
        compute_eigenvectors(A, list(eigenvals_dict.keys()))     # Then find eigenvectors manually
    
    elif choice == "5":
        # Full diagonalization
        A = get_matrix_for_eigen()
        P, D = diagonalize_matrix(A)  # Compute P, D for diagonalization and verify
    
    else:
        # Invalid choice handling
        print("Invalid choice! Please restart and select a number 1-5.")