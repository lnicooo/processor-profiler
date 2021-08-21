#define LOOP        1
#define NB_ELEMENTS 1
#define INIT_VALUE  15


//#include "FIM.h"

void hanoi(int n, char a[], char b[], char c[]);

int main(){

  int i, j;
  int input[NB_ELEMENTS];
  char a[] = "src";
  char b[] = "dst";
  char c[] = "tmp";

  for (i=0; i<NB_ELEMENTS; i++)
    input[i] = INIT_VALUE - i;

  for (i=0; i<LOOP; i++){
    for (j=0; j<NB_ELEMENTS; j++)
      hanoi(input[j], a, b, c);
  }

//FIM_exit();

  return 0;
}

void hanoi(int n, char a[], char b[], char c[]) {
  if (n != 1) {
    hanoi(n - 1, a, c, b);
    hanoi(n - 1, c, b, a);
  }
}
