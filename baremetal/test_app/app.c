#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

/*---- Application Iterations----*/
#define BUBBLE_SIZE 100
#define FIB 38

/*---- DEBUG----*/
//#define DEBUG
//#define SHOW_RESULT

/*---- TMR ----*/
//#define TMR_LOOP 3
//#define TMR

/*---- Aux Functions ----*/

int fac (int n)
{
  if (n == 0)
    return 1;
  else
    return (n * fac (n-1));
}

bool divides (uint n, uint m) {
  return (m % n == 0);
}

bool even (uint n) {
  return (divides (2, n));
}

void swap (uint* a, uint* b) {
  uint tmp = *a;
  *a = *b;
  *b = tmp;
}

bool calc_prime (uint n) {
  uint i;
  if (even (n))
    return (n == 2);
  for (i = 3; i * i <= n; i += 2) {
    if (divides (i, n)) /* ai: loop here min 0 max 357 end; */
      return 0;
  }
  return (n > 1);
}

/*---- Test Functions ----*/

int prime(){

  uint x =  21649;
  uint y = 513239;
  swap (&x, &y);
  int b = calc_prime(x) && calc_prime(y);

  return !(calc_prime(x) && calc_prime(y));

}

long int factorial () {

  int i ;
  long int s = 0;
  volatile int n;

  n = 25;
  for (i = 0;  i <= n; i++)
    s += fac (i);

  return s;
}

long int bubble_sort() {

    long c, d, t, n, a, list[ BUBBLE_SIZE];

    n = BUBBLE_SIZE;

    for (c=0; c<n; c++)
      list[c]=n-c;

    for (c=0; c < (n- 1 ); c++){
      for (d=0; d < n-c-1; d++){
        if (list[d] > list[d+1]){
          /* Swapping */
          t         = list[d];
          list[d]   = list[d+1];
          list[d+1] = t;
        }
      }
    }
    a=0;
    //Sum all sorted values
    for ( c = 0 ; c < n ; c++ )
      a+=list[c]*(c+1);

    return a;
}

int fibonacci(){

    int i,OLD1,OLD2,temp;

    OLD1 = 0;
    OLD2 = 1;

    for(i=2; i<FIB+1; i++){
        temp = OLD2;
        OLD2 = OLD1+ OLD2;
        OLD1 = temp; //Valor antigo
    }

    return OLD2;
}

/*----- MAIN ------*/

int main(){

  int fac_r,bub_r,fib_r,pri_r;

#ifdef TMR
  int i, reslt[TMR_LOOP],maj;

  for(i=0; i<TMR_LOOP; i++){
    reslt[i] = bubble_sort();
  }

  // Voter
  if(reslt[0] == reslt[1])      maj = reslt[0];
  else if(reslt[0] == reslt[2]) maj = reslt[0];
  else maj = reslt[1];

  bub_r = maj;

#endif /* TMR */

  fac_r = factorial();
  bub_r = bubble_sort();
  fib_r = fibonacci();
  pri_r = prime();

#ifdef SHOW_RESULT
  printf("Factorial: %d\n", fac_r);
  printf("Bubble:    %d\n", bub_r);
  printf("Fibonacci: %d\n", fib_r);
  printf("Prime:     %d\n", pri_r);
#endif /* SHOW_RESULT */

  return 0;
}
