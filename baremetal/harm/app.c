#define LOOP        50
#define NB_ELEMENTS 16
#define INIT_VALUE  16

//#include "FIM.h"

int harm(int n);

int main(){

  int i, j;
  int aux=0;
  int input[NB_ELEMENTS];
  volatile int output[NB_ELEMENTS];

  for (i=0; i<NB_ELEMENTS; i++)
    input[i] = INIT_VALUE;

  for (i=0; i<LOOP; i++){

    for (j=0; j<NB_ELEMENTS; j++){

      output[j] = harm(input[j]);

    }

  }

//FIM_exit();


  return 0;
}


int harm(int n) {
  if (n == 1)
    return 1;
  return 1 / n + harm(n-1);
}
