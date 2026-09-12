#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_TEXT 50000

void encrypt_text(const char *plain, char *cipher, const char *key)
{
    int i;

    for (i = 0; plain[i] != '\0'; i++) {

        if (plain[i] >= 'A' && plain[i] <= 'Z')
            cipher[i] = key[plain[i] - 'A'];

        else if (plain[i] >= 'a' && plain[i] <= 'z')
            cipher[i] = tolower(key[plain[i] - 'a']);

        else
            cipher[i] = plain[i];
    }

    cipher[i] = '\0';
}

int main()
{
    char plaintext[MAX_TEXT];
    char generated[MAX_TEXT];
    char original[MAX_TEXT];

    const char key[] =
        "QWERTYUIOPASDFGHJKLZXCVBNM";

    FILE *fp;
    int i = 0;
    int ch;

    /* Read recovered plaintext */
    fp = fopen("recovered_plaintext.txt", "r");

    if (fp == NULL) {
        perror("Error opening recovered_plaintext.txt");
        return 1;
    }

    while ((ch = fgetc(fp)) != EOF && i < MAX_TEXT - 1)
        plaintext[i++] = ch;

    plaintext[i] = '\0';

    fclose(fp);


    /* Read original ciphertext */
    fp = fopen("ciphertext.txt", "r");

    if (fp == NULL) {
        perror("Error opening ciphertext.txt");
        return 1;
    }

    i = 0;

    while ((ch = fgetc(fp)) != EOF && i < MAX_TEXT - 1)
        original[i++] = ch;

    original[i] = '\0';

    fclose(fp);


    /* Re-encrypt recovered plaintext */
    encrypt_text(plaintext, generated, key);


    /* Compare */
    if (strcmp(generated, original) == 0) {

        printf("\n========== VERIFICATION ==========\n");
        printf("SUCCESS!\n");
        printf("Re-encrypted ciphertext matches original ciphertext.\n");
        printf("Recovered key is correct.\n");
    }
    else {

        printf("\n========== VERIFICATION ==========\n");
        printf("FAILED!\n");
        printf("Re-encrypted ciphertext does not match.\n");
    }

    return 0;
}
