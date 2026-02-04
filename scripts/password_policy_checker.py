#!/usr/bin/env python3
import re
import sys

policies = {
    'NIST': {'min_len': 8, 'types': 3},
    'PCI': {'min_len': 7, 'types': 4},
    'Custom': {'min_len': 12, 'types': 4}
}

def check_password(password):
    length_ok = len(password) >= 12
    types = sum([bool(re.search(p, password)) for p in [r'[a-z]', r'[A-Z]', r'\d', r'[^a-zA-Z0-9]']])
    types_ok = types >= 3
    common = password.lower() in ['password', '123456', 'qwerty', 'admin']
    
    print(f"\n🔒 Policy Check for '{password}'")
    print(f"   Length: {len(password)} ✓" if length_ok else f"   Length: {len(password)} ✗")
    print(f"   Types: {types}/4 ✓" if types_ok else f"   Types: {types}/4 ✗")
    print("   Common: NO ✓" if not common else "   Common: YES ✗")
    print("✅ PASS" if length_ok and types_ok and not common else "❌ FAIL")

if __name__ == "__main__":
    password = sys.argv[1] if len(sys.argv) > 1 else input("Password: ")
    check_password(password)
