/* MDH WCET BENCHMARK SUITE. */

/* Changes:
 * JG 2005/12/08: Prototypes added, and changed exit to return in main.
 */

typedef  unsigned char  bool;
typedef  unsigned int   uint;

bool divides (uint n, uint m);
bool even (uint n);
bool prime (uint n);
void swap (uint* a, uint* b);

//#include "FIM.h"

int main () {

int i;
for(i=0;i<40;i++)
{

  uint x =  21649;
  uint y = 513239;
  swap (&x, &y);
  int b = prime(x) && prime(y);
#ifdef DEBUG
  printf("%d",!(prime(x) && prime(y)));
#endif
} 

//FIM_exit();
  return 0;
}

bool divides (uint n, uint m) {
  return (m % n == 0);
}

bool even (uint n) {
  return (divides (2, n));
}

bool prime (uint n) {
  uint i;
  if (even (n))
      return (n == 2);
  for (i = 3; i * i <= n; i += 2) { 
      if (divides (i, n)) /* ai: loop here min 0 max 357 end; */
          return 0; 
  }
  return (n > 1);
}

void swap (uint* a, uint* b) {
  uint tmp = *a;
  *a = *b; 
  *b = tmp;
}
