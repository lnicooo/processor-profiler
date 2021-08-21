#define LOOP        4
#define NB_ELEMENTS 16*16
#define INIT_A      16
#define INIT_B      524


//#include "FIM.h"

int mdc(int a, int b) {
  if (a % b == 0)
    return b;
  return mdc(b, a % b);
}

int main(){

  int i, j;
  int input_A[NB_ELEMENTS], input_B[NB_ELEMENTS], output[NB_ELEMENTS];

  for (i=0; i<NB_ELEMENTS; i++){
    input_A[i] = INIT_A + i;
    input_B[i] = INIT_B + i;
  }

  for (i=0; i<LOOP; i++){
    for (j=0; j<NB_ELEMENTS; j++)
      output[j] = mdc(input_A[j], input_B[j]);
  }


//FIM_exit();

  return 0;
}
