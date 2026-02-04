#!/usr/bin/env python3
import subprocess
import sys
import hashlib

def quick_crack_test(password):
    """Quick dictionary test"""
    h = hashlib.md5(password.encode()).hexdigest()
    with open('/tmp/test.hash', 'w') as f:
        f.write(f"{h}:{password}\n")
    
    result = subprocess.run([
        'hashcat', '--quiet', '--force', '-m', '0', '-a', '0',
        '/tmp/test.hash', '/usr/share/wordlists/rockyou.txt'
    ], capture_output=True, text=True, timeout=5)
    
    cracked = subprocess.run([
        'hashcat', '--show', '--force', '/tmp/test.hash'
    ], capture_output=True, text=True).stdout.strip()
    
    subprocess.run(['rm', '-f', '/tmp/test.hash'])
    return 'cracked' in cracked.lower()

if __name__ == "__main__":
    password = sys.argv[1] if len(sys.argv) > 1 else input("Password: ")
    
    print(f"\n🎯 COMPREHENSIVE TEST: '{password}'")
    print(f"   Dictionary Attack: {'🔴 CRACKED' if quick_crack_test(password) else '🟢 SURVIVED'}")
    exec(open('~/password_project/scripts/password_entropy.py').read())
    exec(open('~/password_project/scripts/password_policy_checker.py').read())
