#include <stdio.h>
#include <ctype.h>
#include <string.h>

#define MAX_TEXT 50000

int main()
{
    FILE *in, *out;

    char cipher[MAX_TEXT];
    char plain[MAX_TEXT];

    /*
       Cipher -> Plain recovered key
    */
    const char key[] = "KXVMCNOPHQRSZYIJADLEGWBUFT";

    in = fopen("ciphertext.txt", "r");

    if (in == NULL) {
        perror("Error opening ciphertext.txt");
        return 1;
    }

    int i = 0;
    int ch;

    while ((ch = fgetc(in)) != EOF && i < MAX_TEXT - 1) {
        cipher[i++] = ch;
    }

    cipher[i] = '\0';

    fclose(in);


    /* Apply recovered substitution */
    for (i = 0; cipher[i] != '\0'; i++) {

        if (cipher[i] >= 'A' && cipher[i] <= 'Z') {

            plain[i] = key[cipher[i] - 'A'];
        }

        else if (cipher[i] >= 'a' && cipher[i] <= 'z') {

            plain[i] = tolower(key[cipher[i] - 'a']);
        }

        else {

            plain[i] = cipher[i];
        }
    }

    plain[i] = '\0';


    printf("========== RECOVERED PLAINTEXT ==========\n\n");
    printf("%s\n", plain);


    out = fopen("recovered_plaintext.txt", "w");

    if (out == NULL) {
        perror("Error creating recovered_plaintext.txt");
        return 1;
    }

    fprintf(out, "%s", plain);

    fclose(out);


    printf("\nRecovered plaintext saved to recovered_plaintext.txt\n");

    return 0;
}
