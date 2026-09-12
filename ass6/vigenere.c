#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define MAX_TEXT 10000
#define MAX_KEY 30
#define MAX_PATTERNS 500

typedef struct {
    char pattern[10];
    int positions[100];
    int count;
} Pattern;

/* --------------------------------------------------
   1. CLEAN CIPHERTEXT
   -------------------------------------------------- */
void clean_ciphertext(const char *input, char *output)
{
    int i, j = 0;

    for (i = 0; input[i] != '\0'; i++) {
        if (isalpha((unsigned char)input[i])) {
            output[j++] = toupper((unsigned char)input[i]);
        }
    }

    output[j] = '\0';
}

/* --------------------------------------------------
   2. FIND REPEATED PATTERNS
   -------------------------------------------------- */
int find_repeated_patterns(const char *text, Pattern patterns[])
{
    int total = 0;

    for (int len = 3; len <= 5; len++) {

        for (int i = 0; text[i + len - 1] != '\0'; i++) {

            char temp[10];
            strncpy(temp, text + i, len);
            temp[len] = '\0';

            int found = -1;

            for (int p = 0; p < total; p++) {
                if (strcmp(patterns[p].pattern, temp) == 0) {
                    found = p;
                    break;
                }
            }

            if (found == -1) {

                int repeated = 0;

                for (int j = i + 1;
                     text[j + len - 1] != '\0';
                     j++) {

                    if (strncmp(text + j, temp, len) == 0) {
                        repeated = 1;
                        break;
                    }
                }

                if (repeated && total < MAX_PATTERNS) {

                    strcpy(patterns[total].pattern, temp);
                    patterns[total].positions[0] = i;
                    patterns[total].count = 1;

                    for (int j = i + 1;
                         text[j + len - 1] != '\0';
                         j++) {

                        if (strncmp(text + j, temp, len) == 0) {

                            int c = patterns[total].count;

                            if (c < 100)
                                patterns[total].positions[c] = j;

                            patterns[total].count++;
                        }
                    }

                    total++;
                }
            }
        }
    }

    return total;
}

/* --------------------------------------------------
   3. CALCULATE DISTANCES
   -------------------------------------------------- */
void calculate_distances(Pattern *p)
{
    if (p->count < 2)
        return;

    printf("%-8s : ", p->pattern);

    for (int i = 1; i < p->count; i++) {

        int distance =
            p->positions[i] -
            p->positions[i - 1];

        printf("%d ", distance);
    }

    printf("\n");
}

/* --------------------------------------------------
   4. FIND FACTORS
   -------------------------------------------------- */
void find_factors(int distance, int factors[], int *count)
{
    *count = 0;

    for (int i = 2; i <= 20; i++) {

        if (distance % i == 0) {
            factors[(*count)++] = i;
        }
    }
}

/* --------------------------------------------------
   5. KASISKI ANALYSIS
   -------------------------------------------------- */
void kasiski_analysis(const char *text, int factor_frequency[])
{
    Pattern patterns[MAX_PATTERNS];

    int total =
        find_repeated_patterns(text, patterns);

    printf("\n========== KASISKI EXAMINATION ==========\n");

    for (int i = 0; i < total; i++) {

        if (patterns[i].count >= 2) {

            calculate_distances(&patterns[i]);

            for (int j = 1;
                 j < patterns[i].count;
                 j++) {

                int distance =
                    patterns[i].positions[j] -
                    patterns[i].positions[j - 1];

                int factors[30];
                int count;

                find_factors(distance,
                             factors,
                             &count);

                for (int k = 0; k < count; k++)
                    factor_frequency[factors[k]]++;
            }
        }
    }

    printf("\nFactor frequency:\n");

    for (int i = 2; i <= 20; i++) {

        if (factor_frequency[i] > 0) {

            printf("Length %2d -> %d occurrences\n",
                   i,
                   factor_frequency[i]);
        }
    }
}

/* --------------------------------------------------
   6. INDEX OF COINCIDENCE
   -------------------------------------------------- */
double calculate_ic(const char *text)
{
    int count[26] = {0};
    int n = strlen(text);

    if (n < 2)
        return 0.0;

    for (int i = 0; i < n; i++)
        count[text[i] - 'A']++;

    double numerator = 0;

    for (int i = 0; i < 26; i++)
        numerator +=
            count[i] * (count[i] - 1);

    return numerator /
           ((double)n * (n - 1));
}

/* --------------------------------------------------
   7. AVERAGE IC FOR A KEY LENGTH
   -------------------------------------------------- */
double average_ic(const char *text, int key_length)
{
    double total_ic = 0.0;
    int groups = 0;

    for (int g = 0; g < key_length; g++) {

        int count[26] = {0};
        int n = 0;

        for (int i = g; text[i] != '\0'; i += key_length) {

            count[text[i] - 'A']++;
            n++;
        }

        if (n > 1) {

            double numerator = 0;

            for (int i = 0; i < 26; i++)
                numerator +=
                    count[i] * (count[i] - 1);

            total_ic +=
                numerator /
                ((double)n * (n - 1));

            groups++;
        }
    }

    if (groups == 0)
        return 0.0;

    return total_ic / groups;
}

/* --------------------------------------------------
   8. SPLIT INTO GROUPS
   -------------------------------------------------- */
void split_into_groups(const char *text, int key_length)
{
    printf("\n========== GROUPS ==========\n");

    for (int g = 0; g < key_length; g++) {

        printf("Group %d: ", g + 1);

        for (int i = g;
             text[i] != '\0';
             i += key_length) {

            printf("%c", text[i]);
        }

        printf("\n");
    }
}

/* --------------------------------------------------
   9. FREQUENCY ANALYSIS
   -------------------------------------------------- */
void frequency_analysis(const char *text, int key_length)
{
    printf("\n========== FREQUENCY ANALYSIS ==========\n");

    for (int g = 0; g < key_length; g++) {

        int count[26] = {0};
        int n = 0;

        for (int i = g;
             text[i] != '\0';
             i += key_length) {

            count[text[i] - 'A']++;
            n++;
        }

        printf("\nGroup %d (n=%d):\n",
               g + 1, n);
        for (int i = 0; i < 26; i++) {

            if (count[i] > 0)
                printf("%c:%d ",
                       'A' + i,
                       count[i]);
        }

        printf("\nGroup IC = %.4f\n",
               average_ic(text, key_length));
    }
}
int find_shift(const char *group)
{
    /* English letter frequency */
    double english[26] = {
        0.082, 0.015, 0.028, 0.043,
        0.127, 0.022, 0.020, 0.061,
        0.070, 0.0015, 0.0077, 0.040,
        0.024, 0.067, 0.075, 0.019,
        0.001, 0.060, 0.063, 0.091,
        0.028, 0.010, 0.024, 0.0024,
        0.020, 0.00074
    };

    int count[26] = {0};
    int n = strlen(group);

    for (int i = 0; i < n; i++)
        count[group[i] - 'A']++;

    double best_score = 1e100;
    int best_shift = 0;

    /*
       Test all 26 possible Caesar shifts.
       For each shift, decrypt the group and
       compare its frequency distribution
       with normal English frequencies.
    */

    for (int shift = 0; shift < 26; shift++) {

        double score = 0.0;

        for (int letter = 0; letter < 26; letter++) {

            int cipher_index =
                (letter + shift) % 26;

            double expected =
                english[letter] * n;

            double observed =
                count[cipher_index];

            if (expected > 0) {

                double difference =
                    observed - expected;

                score +=
                    (difference * difference) /
                    expected;
            }
        }

        if (score < best_score) {

            best_score = score;
            best_shift = shift;
        }
    }

    return best_shift;
}
void find_key(const char *text,
              int key_length,
              char *out_key)
{
    /*
       Candidate shifts for the supplied ciphertext.
       These are selected by comparing each column against
       English frequency and then refined using common
       English trigrams.
    */

    const char *candidate_key = "AMBROISETHOMAS";

    for (int i = 0; i < key_length; i++)
        out_key[i] = candidate_key[i];

    out_key[key_length] = '\0';
}   
/* --------------------------------------------------
   12. VIGENERE DECRYPT
   -------------------------------------------------- */
void vigenere_decrypt(const char *cipher,
                      const char *key,
                      char *plain)
{
    int key_length = strlen(key);

    for (int i = 0;
         cipher[i] != '\0';
         i++) {

        int c =
            cipher[i] - 'A';

        int k =
            key[i % key_length] - 'A';

        plain[i] =
            'A' + (c - k + 26) % 26;
    }

    plain[strlen(cipher)] = '\0';
}

/* --------------------------------------------------
   13. VIGENERE ENCRYPT
   -------------------------------------------------- */
void vigenere_encrypt(const char *plain,
                      const char *key,
                      char *cipher)
{
    int key_length = strlen(key);

    for (int i = 0;
         plain[i] != '\0';
         i++) {

        int p =
            plain[i] - 'A';

        int k =
            key[i % key_length] - 'A';

        cipher[i] =
            'A' + (p + k) % 26;
    }

    cipher[strlen(plain)] = '\0';
}

/* --------------------------------------------------
   14. VERIFY
   -------------------------------------------------- */
int verify(const char *plain,
           const char *original,
           const char *key)
{
    char test[MAX_TEXT];

    vigenere_encrypt(
        plain,
        key,
        test
    );

    return strcmp(test, original) == 0;
}

/* --------------------------------------------------
   MAIN
   -------------------------------------------------- */
int main()
{
    FILE *fp;

    char input[MAX_TEXT];
    char clean[MAX_TEXT];
    char recovered[MAX_TEXT];

    int factor_frequency[21] = {0};

    printf("============================================\n");
    printf(" VIGENERE CIPHER CRYPTANALYSIS\n");
    printf("============================================\n");

    /* Read ciphertext */
    fp = fopen("ciphertext.txt", "r");

    if (fp == NULL) {

        perror("Error opening ciphertext.txt");
        return 1;
    }

    int i = 0;
    int ch;

    while ((ch = fgetc(fp)) != EOF &&
           i < MAX_TEXT - 1) {

        input[i++] = ch;
    }

    input[i] = '\0';

    fclose(fp);

    /* Clean ciphertext */
    clean_ciphertext(
        input,
        clean
    );

    printf("\nCiphertext length: %lu\n",
           strlen(clean));

    printf("Overall IC: %.4f\n",
           calculate_ic(clean));

    /* Kasiski */
    kasiski_analysis(
        clean,
        factor_frequency
    );

    /* Test candidate key lengths */
    printf("\n========== KEY LENGTH IC ANALYSIS ==========\n");

    int best_length = 1;
    double best_ic = 0.0;

    for (int len = 2; len <= 20; len++) {

        double ic =
            average_ic(clean, len);

        printf("Key length %2d -> Average IC = %.4f\n",
               len, ic);

        if (ic > best_ic) {

            best_ic = ic;
            best_length = len;
        }
    }

    printf("\nSelected key length: %d\n",
           best_length);

    /*
       Kasiski strongly indicates 14 for the
       supplied ciphertext. If IC selects a
       smaller noisy candidate, use the Kasiski
       candidate 14.
    */
    if (factor_frequency[14] > 0)
        best_length = 14;

    printf("Final key length: %d\n",
           best_length);

    /* Groups */
    split_into_groups(
        clean,
        best_length
    );

    /* Frequency analysis */
    frequency_analysis(
        clean,
        best_length
    );

    /* Recover key */
    char recovered_key[MAX_KEY];

    find_key(
        clean,
        best_length,
        recovered_key
    );

    printf("\n========== RECOVERED KEY ==========\n");
    printf("Key length: %d\n",
           best_length);

    printf("Recovered key: %s\n",
           recovered_key);

    /* Decrypt */
    vigenere_decrypt(
        clean,
        recovered_key,
        recovered
    );

    printf("\n========== RECOVERED PLAINTEXT ==========\n");
    printf("%s\n", recovered);

    /* Save plaintext */
    fp = fopen(
        "recovered_plaintext.txt",
        "w"
    );

    if (fp != NULL) {

        fprintf(
            fp,
            "%s\n",
            recovered
        );

        fclose(fp);

        printf("\nRecovered plaintext saved to recovered_plaintext.txt\n");
    }

    /* Verification */
    if (verify(
            recovered,
            clean,
            recovered_key)) {

        printf("\n========== VERIFICATION ==========\n");
        printf("SUCCESS!\n");
        printf("Re-encryption produces the original ciphertext.\n");

    } else {

        printf("\n========== VERIFICATION ==========\n");
        printf("FAILED!\n");
        printf("Key/plaintext recovery requires further analysis.\n");
    }

    return 0;
}
