#!/bin/bash

# Automated Password Strength Testing Framework
# Usage: ./automated_password_test.sh <password_file> <output_dir>

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <password_file> <output_dir>"
    exit 1
fi

PASSWORD_FILE="$1"
OUTPUT_DIR="$2"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
REPORT_FILE="${OUTPUT_DIR}/password_report_${TIMESTAMP}.txt"

echo "Starting automated password strength testing..."
echo "Timestamp: $(date)"
echo "Password file: ${PASSWORD_FILE}"
echo "Output directory: ${OUTPUT_DIR}"
echo ""

# Create output directory
mkdir -p "${OUTPUT_DIR}"

# Header
echo "================================================================================" > "${REPORT_FILE}"
echo "PASSWORD STRENGTH TESTING REPORT" >> "${REPORT_FILE}"
echo "================================================================================" >> "${REPORT_FILE}"
echo "Generated: $(date)" >> "${REPORT_FILE}"
echo "Test file: ${PASSWORD_FILE}" >> "${REPORT_FILE}"
echo "Total passwords: $(wc -l < "${PASSWORD_FILE}")" >> "${REPORT_FILE}"
echo "" >> "${REPORT_FILE}"

# Process each password
PASSWORD_COUNT=0
CRACKED_COUNT=0
WEAK_COUNT=0
STRONG_COUNT=0

while IFS= read -r PASSWORD; do
    PASSWORD_COUNT=$((PASSWORD_COUNT + 1))
    
    echo "Testing password ${PASSWORD_COUNT}: ${PASSWORD}"
    
    # Calculate hash for testing
    MD5_HASH=$(echo -n "${PASSWORD}" | md5sum | awk '{print $1}')
    
    # Write hash to temp file
    echo "${MD5_HASH}:test${PASSWORD_COUNT}" > /tmp/test_hash.txt
    
    # Test with hashcat dictionary attack
    echo "  Testing with hashcat..." | tee -a "${REPORT_FILE}"
    timeout 10 hashcat -m 0 -a 0 /tmp/test_hash.txt ~/password_project/wordlists/rockyou_top10k.txt --force --quiet 2>/dev/null
    
    # Check if cracked
    if hashcat --show /tmp/test_hash.txt --force --quiet 2>/dev/null | grep -q ":"; then
        CRACKED_COUNT=$((CRACKED_COUNT + 1))
        STATUS="CRACKED (dictionary)"
        WEAK_COUNT=$((WEAK_COUNT + 1))
        echo "  Status: ${STATUS}" | tee -a "${REPORT_FILE}"
    else
        STATUS="NOT CRACKED"
        
        # Additional strength checks
        LENGTH=${#PASSWORD}
        HAS_UPPER=$(echo "${PASSWORD}" | grep -q '[A-Z]' && echo 1 || echo 0)
        HAS_LOWER=$(echo "${PASSWORD}" | grep -q '[a-z]' && echo 1 || echo 0)
        HAS_DIGIT=$(echo "${PASSWORD}" | grep -q '[0-9]' && echo 1 || echo 0)
        HAS_SPECIAL=$(echo "${PASSWORD}" | grep -q '[^a-zA-Z0-9]' && echo 1 || echo 0)
        
        SCORE=$((LENGTH * 2))
        SCORE=$((SCORE + HAS_UPPER * 10))
        SCORE=$((SCORE + HAS_LOWER * 5))
        SCORE=$((SCORE + HAS_DIGIT * 10))
        SCORE=$((SCORE + HAS_SPECIAL * 15))
        
        if [ ${SCORE} -ge 60 ]; then
            STRENGTH="STRONG"
            STRONG_COUNT=$((STRONG_COUNT + 1))
        elif [ ${SCORE} -ge 40 ]; then
            STRENGTH="MODERATE"
        else
            STRENGTH="WEAK"
            WEAK_COUNT=$((WEAK_COUNT + 1))
        fi
        
        echo "  Status: ${STATUS}" | tee -a "${REPORT_FILE}"
        echo "  Length: ${LENGTH}" | tee -a "${REPORT_FILE}"
        echo "  Score: ${SCORE}/100" | tee -a "${REPORT_FILE}"
        echo "  Strength: ${STRENGTH}" | tee -a "${REPORT_FILE}"
    fi
    
    echo "" >> "${REPORT_FILE}"
    
done < "${PASSWORD_FILE}"

# Summary
echo "" >> "${REPORT_FILE}"
echo "================================================================================" >> "${REPORT_FILE}"
echo "SUMMARY" >> "${REPORT_FILE}"
echo "================================================================================" >> "${REPORT_FILE}"
echo "Total passwords tested: ${PASSWORD_COUNT}" >> "${REPORT_FILE}"
echo "Passwords cracked: ${CRACKED_COUNT} ($((CRACKED_COUNT * 100 / PASSWORD_COUNT))%)" >> "${REPORT_FILE}"
echo "Weak passwords: ${WEAK_COUNT} ($((WEAK_COUNT * 100 / PASSWORD_COUNT))%)" >> "${REPORT_FILE}"
echo "Strong passwords: ${STRONG_COUNT} ($((STRONG_COUNT * 100 / PASSWORD_COUNT))%)" >> "${REPORT_FILE}"
echo "" >> "${REPORT_FILE}"
echo "Weak passwords are those that were either cracked or scored below 40." >> "${REPORT_FILE}"
echo "Strong passwords scored 60 or above and were not cracked." >> "${REPORT_FILE}"

echo ""
echo "Testing complete!"
echo "Report saved to: ${REPORT_FILE}"
echo ""
echo "Summary:"
echo "  Total passwords: ${PASSWORD_COUNT}"
echo "  Cracked: ${CRACKED_COUNT} ($((CRACKED_COUNT * 100 / PASSWORD_COUNT))%)"
echo "  Weak: ${WEAK_COUNT} ($((WEAK_COUNT * 100 / PASSWORD_COUNT))%)"
echo "  Strong: ${STRONG_COUNT} ($((STRONG_COUNT * 100 / PASSWORD_COUNT))%)"
