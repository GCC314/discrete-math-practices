## Checking functions for each statement

def Check_A(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement A:", all(any(n ** 2 < m for m in m_range) for n in n_range))

def Check_B(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement B:", any(all(n < m ** 2 for m in m_range) for n in n_range))

def Check_C(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement C:", all(any(n + m == 0 for m in m_range) for n in n_range))

def Check_D(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement D:", any(all(n * m == m for m in m_range) for n in n_range))

def Check_E(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement E:", any(any(n ** 2 + m ** 2 == 5 for m in m_range) for n in n_range))

def Check_F(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement F:", any(any(n ** 2 + m ** 2 == 6 for m in m_range) for n in n_range))

def Check_G(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement G:", any(any(n + m == 4 and n - m == 1 for m in m_range) for n in n_range))

def Check_H(n_range, m_range):
    print("When n in", n_range, ", m in", m_range)
    print("Statement H:", any(any(n + m == 4 and n - m == 2 for m in m_range) for n in n_range))

def Check_I(n_range, m_range, p_range):
    print("When n in", n_range, ", m in", m_range, ", p in", p_range)
    print("Statement I:", all(all(any(p * 2 == n + m for p in p_range) for m in m_range) for n in n_range))


if __name__ == '__main__':
    Check_A(range(-100, 101), range(10010))             # n in [-100, 101), m in [0, 10010)
    Check_B(range(-1, 1), range(100000))                # n in [-1, 1), m in [0, 100000)
    Check_C(range(-1000, 1001), range(-1000, 1001))     # n in [-1000, 1001), m in [-1000, 1001)
    Check_D(range(0, 3), range(100000))                 # n in [0, 3), m in [0, 100000)
    Check_E(range(0, 5), range(0, 5))                   # n in [0, 5), m in [0, 5)
    Check_F(range(0, 5), range(0, 5))                   # n in [0, 5), m in [0, 5)
    Check_G(range(-10, 11), range(-10, 11))             # n in [-10, 11), m in [-10, 11)
    Check_H(range(-10, 11), range(-10, 11))             # n in [-10, 11), m in [-10, 11)
    Check_I(range(0, 5), range(0, 5), range(0, 10))     # n in [0, 5), m in [0, 5), p in [0, 10)