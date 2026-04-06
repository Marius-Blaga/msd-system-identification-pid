"""
Stage 2 - Parameter Identification
"""

from src.identification import SystemIdentifier


def main():
    print("🚀 Stage 2 → Parameter Identification\n")
    
    # 1. Initialize identifier
    identifier = SystemIdentifier()
    
    # True parameters (for validation)
    m_true = 1.0
    c_true = 2.0
    k_true = 10.0
    
    # 2. Generate data
    df = identifier.generate_data(
        m_true=m_true,
        k_true=k_true,
        c_true=c_true,
        noise_level=0.015
    )
    
    # 3. Identify parameters
    result = identifier.identify_parameters(df)
    
    m_est = result["m"]
    c_est = result["c"]
    k_est = result["k"]
    cost = result["cost"]
    
    # 4. Compute relative errors
    err_m = abs(m_est - m_true) / m_true * 100
    err_c = abs(c_est - c_true) / c_true * 100
    err_k = abs(k_est - k_true) / k_true * 100
    
    # 5. Print results
    print("\n" + "=" * 65)
    print("                 FINAL RESULTS")
    print("=" * 65)
    
    print(f"True parameters      : m = {m_true:.4f} | c = {c_true:.4f} | k = {k_true:.4f}")
    print(f"Estimated parameters : m = {m_est:.4f} | c = {c_est:.4f} | k = {k_est:.4f}")
    
    print("\nRelative errors (%)")
    print(f"m error: {err_m:.2f}%")
    print(f"c error: {err_c:.2f}%")
    print(f"k error: {err_k:.2f}%")
    
    print(f"\nCost function value  : {cost:.6f}")
    
    print("=" * 65)
    
    print("\n✅ Stage 2 completed successfully!")
    print("   Data saved in 'data/' folder")


if __name__ == "__main__":
    main()