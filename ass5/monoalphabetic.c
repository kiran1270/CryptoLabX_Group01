#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define ALPHABET 26
#define MAX_TEXT 50000
#define MAX_WORD 100
#define MAX_WORDS 5000


/* -------------------------------------------------
   Read plaintext/ciphertext from file
   ------------------------------------------------- */
int read_file(const char *filename, char *text)
{
    FILE *fp = fopen(filename, "r");

    if (fp == NULL) {
        perror("Error opening file");
        return 0;
    }

    int ch;
    int i = 0;

    while ((ch = fgetc(fp)) != EOF && i < MAX_TEXT - 1) {
        text[i++] = (char)ch;
    }

    text[i] = '\0';

    fclose(fp);

    return i;
}


/* -------------------------------------------------
   Generate monoalphabetic substitution ciphertext
   ------------------------------------------------- */
void encrypt_text(const char *plain,
                  char *cipher,
                  const char *key)
{
    int i;

    for (i = 0; plain[i] != '\0'; i++) {

        if (plain[i] >= 'A' && plain[i] <= 'Z') {

            cipher[i] = key[plain[i] - 'A'];
        }
        else if (plain[i] >= 'a' && plain[i] <= 'z') {

            cipher[i] = tolower(key[plain[i] - 'a']);
        }
        else {
            cipher[i] = plain[i];
        }
    }

    cipher[i] = '\0';
}


/* -------------------------------------------------
   Letter Frequency Analysis
   ------------------------------------------------- */
void frequency_analysis(const char *text)
{
    int freq[ALPHABET] = {0};
    int total = 0;

    for (int i = 0; text[i] != '\0'; i++) {

        if (isalpha((unsigned char)text[i])) {

            char c = toupper((unsigned char)text[i]);

            freq[c - 'A']++;
            total++;
        }
    }

    printf("\n========== LETTER FREQUENCY ANALYSIS ==========\n");

    printf("\nLetter\tCount\tPercentage\n");

    for (int i = 0; i < ALPHABET; i++) {

        double percentage = 0;

        if (total > 0)
            percentage = (freq[i] * 100.0) / total;

        printf("%c\t%d\t%.2f%%\n",
               'A' + i,
               freq[i],
               percentage);
    }

    printf("\nTotal letters = %d\n", total);


    /* Display letters in descending frequency */
    printf("\nLetters in descending frequency:\n");

    int used[ALPHABET] = {0};

    for (int k = 0; k < ALPHABET; k++) {

        int max = -1;
        int index = -1;

        for (int i = 0; i < ALPHABET; i++) {

            if (!used[i] && freq[i] > max) {
                max = freq[i];
                index = i;
            }
        }

        if (index != -1) {

            used[index] = 1;

            printf("%c(%d) ",
                   'A' + index,
                   freq[index]);
        }
    }

    printf("\n");
}


/* -------------------------------------------------
   Word Frequency Analysis
   ------------------------------------------------- */
void word_frequency_analysis(const char *text)
{
    char words[MAX_WORDS][MAX_WORD];
    int counts[MAX_WORDS] = {0};
    int word_count = 0;

    char current[MAX_WORD];
    int pos = 0;

    for (int i = 0; ; i++) {

        char c = text[i];

        if (isalpha((unsigned char)c)) {

            if (pos < MAX_WORD - 1)
                current[pos++] = tolower((unsigned char)c);
        }
        else {

            if (pos > 0) {

                current[pos] = '\0';

                int found = -1;

                for (int j = 0; j < word_count; j++) {

                    if (strcmp(words[j], current) == 0) {
                        found = j;
                        break;
                    }
                }

                if (found >= 0) {

                    counts[found]++;
                }
                else if (word_count < MAX_WORDS) {

                    strcpy(words[word_count], current);
                    counts[word_count] = 1;
                    word_count++;
                }

                pos = 0;
            }

            if (c == '\0')
                break;
        }
    }


    printf("\n========== WORD FREQUENCY ANALYSIS ==========\n");

    for (int k = 0; k < word_count; k++) {

        int max_index = -1;
        int max_count = -1;

        for (int i = 0; i < word_count; i++) {

            if (counts[i] > max_count) {
                max_count = counts[i];
                max_index = i;
            }
        }

        if (max_index >= 0) {

            printf("%-15s %d\n",
                   words[max_index],
                   counts[max_index]);

            counts[max_index] = -1;
        }
    }
}


/* -------------------------------------------------
   Pattern Analysis
   ------------------------------------------------- */
void get_pattern(const char *word, char *pattern)
{
    int map[ALPHABET];

    for (int i = 0; i < ALPHABET; i++)
        map[i] = -1;

    int next = 0;

    for (int i = 0; word[i] != '\0'; i++) {

        int index = word[i] - 'a';

        if (map[index] == -1) {
            map[index] = next++;
        }

        pattern[i] = '0' + map[index];
    }

    pattern[strlen(word)] = '\0';
}


void pattern_analysis(const char *text)
{
    char words[MAX_WORDS][MAX_WORD];
    int word_count = 0;

    char current[MAX_WORD];
    int pos = 0;

    for (int i = 0; ; i++) {

        char c = text[i];

        if (isalpha((unsigned char)c)) {

            if (pos < MAX_WORD - 1)
                current[pos++] = tolower((unsigned char)c);
        }
        else {

            if (pos > 0) {

                current[pos] = '\0';

                if (word_count < MAX_WORDS) {
                    strcpy(words[word_count], current);
                    word_count++;
                }

                pos = 0;
            }

            if (c == '\0')
                break;
        }
    }


    printf("\n========== WORD PATTERN ANALYSIS ==========\n");

    for (int i = 0; i < word_count; i++) {

        char pattern[MAX_WORD];

        get_pattern(words[i], pattern);

        printf("%-15s Pattern: %s\n",
               words[i],
               pattern);
    }
}


/* -------------------------------------------------
   Apply suspected substitution
   key[cipher letter] = plaintext letter
   ------------------------------------------------- */
void apply_substitution(const char *cipher,
                        char *plain,
                        const char *key)
{
    for (int i = 0; cipher[i] != '\0'; i++) {

        char c = cipher[i];

        if (c >= 'A' && c <= 'Z') {

            char mapped = key[c - 'A'];

            if (mapped == '?')
                plain[i] = '_';
            else
                plain[i] = mapped;
        }

        else if (c >= 'a' && c <= 'z') {

            char mapped = key[c - 'a'];

            if (mapped == '?')
                plain[i] = '_';
            else
                plain[i] = tolower(mapped);
        }

        else {

            plain[i] = c;
        }
    }

    plain[strlen(cipher)] = '\0';
}


/* -------------------------------------------------
   Display partial plaintext
   ------------------------------------------------- */
void display_partial_plaintext(const char *cipher,
                               const char *key)
{
    char plain[MAX_TEXT];

    apply_substitution(cipher, plain, key);

    printf("\n========== PARTIAL PLAINTEXT ==========\n");

    for (int i = 0; i < 1000 && plain[i] != '\0'; i++)
        putchar(plain[i]);

    printf("\n");
}


/* -------------------------------------------------
   Verify recovered key by re-encryption
   ------------------------------------------------- */
void verify_solution(const char *plain,
                     const char *cipher,
                     const char *key)
{
    char generated[MAX_TEXT];

    encrypt_text(plain, generated, key);

    if (strcmp(generated, cipher) == 0) {

        printf("\n========== VERIFICATION ==========\n");
        printf("SUCCESS: Re-encryption matches ciphertext.\n");
    }
    else {

        printf("\n========== VERIFICATION ==========\n");
        printf("FAILED: Re-encryption does not match ciphertext.\n");
    }
}


/* -------------------------------------------------
   Main
   ------------------------------------------------- */
int main()
{
    char plaintext[MAX_TEXT];
    char ciphertext[MAX_TEXT];

    /*
       Example substitution key.

       IMPORTANT:
       This is only a sample key for demonstrating
       encryption. You can change it for your experiment.

       Plain alphabet:
       ABCDEFGHIJKLMNOPQRSTUVWXYZ

       Cipher alphabet:
       QWERTYUIOPASDFGHJKLZXCVBNM
    */

    const char key[ALPHABET + 1] =
        "QWERTYUIOPASDFGHJKLZXCVBNM";


    printf("=============================================\n");
    printf(" MONOALPHABETIC SUBSTITUTION CIPHER\n");
    printf("=============================================\n");


    /* Read plaintext */
    if (!read_file("plaintext.txt", plaintext)) {
        return 1;
    }

    printf("\nPlaintext loaded successfully.\n");


    /* Generate ciphertext */
    encrypt_text(plaintext, ciphertext, key);


    FILE *fp = fopen("ciphertext.txt", "w");

    if (fp == NULL) {

        perror("Error creating ciphertext file");

        return 1;
    }

    fprintf(fp, "%s", ciphertext);

    fclose(fp);

    printf("Ciphertext generated: ciphertext.txt\n");


    /* Frequency analysis */
    frequency_analysis(ciphertext);


    /* Word frequency analysis */
    word_frequency_analysis(ciphertext);


    /* Pattern analysis */
    pattern_analysis(ciphertext);


    /* Example partial substitution */
    char recovered_key[ALPHABET + 1];

    for (int i = 0; i < ALPHABET; i++)
        recovered_key[i] = '?';

    recovered_key[ALPHABET] = '\0';


    printf("\nCurrent recovered key:\n");
    printf("%s\n", recovered_key);


    display_partial_plaintext(ciphertext,
                              recovered_key);


    /*
       For the actual cryptanalysis experiment,
       modify recovered_key based on frequency,
       word patterns and repeated words.
    */


    printf("\nProgram completed.\n");

    return 0;
}
