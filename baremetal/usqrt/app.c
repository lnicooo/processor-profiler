/* +++Date last modified: 05-Jul-1997 */
#define BITSPERLONG 32

#define TOP2BITS(x) ((x & (3L << (BITSPERLONG-2))) >> (BITSPERLONG-2))


/* usqrt:
    ENTRY x: unsigned long
    EXIT  returns floor(sqrt(x) * pow(2, BITSPERLONG/2))

    Since the square root never uses more than half the bits
    of the input, we use the other half of the bits to contain
    extra bits of precision after the binary point.

    EXAMPLE
        suppose BITSPERLONG = 32
        then    usqrt(144) = 786432 = 12 * 65536
                usqrt(32) = 370727 = 5.66 * 65536

    NOTES
        (1) change BITSPERLONG to BITSPERLONG/2 if you do not want
            the answer scaled.  Indeed, if you want n bits of
            precision after the binary point, use BITSPERLONG/2+n.
            The code assumes that BITSPERLONG is even.
        (2) This is really better off being written in assembly.
            The line marked below is really a "arithmetic shift left"
            on the double-long value with r in the upper half
            and x in the lower half.  This operation is typically
            expressible in only one or two assembly instructions.
        (3) Unrolling this loop is probably not a bad idea.

    ALGORITHM
        The calculations are the base-two analogue of the square
        root algorithm we all learned in grammar school.  Since we're
        in base 2, there is only one nontrivial trial multiplier.

        Notice that absolutely no multiplications or divisions are performed.
        This means it'll be fast on a wide range of processors.
*/

void* memcpy(void* dest, const void* src, int count) {
        char* dst8 = (char*)dest;
        char* src8 = (char*)src;

        while (count--) {
            *dst8++ = *src8++;
        }
        return dest;
}

struct int_sqrt {
      unsigned sqrt,
               frac;
};

void usqrt(unsigned long x, struct int_sqrt *q)
{
      unsigned long a = 0L;                   /* accumulator      */
      unsigned long r = 0L;                   /* remainder        */
      unsigned long e = 0L;                   /* trial product    */

      int i;

      for (i = 0; i < BITSPERLONG; i++)   /* NOTE 1 */
      {
            r = (r << 2) + TOP2BITS(x); x <<= 2; /* NOTE 2 */
            a <<= 1;
            e = (a << 1) + 1;
            if (r >= e)
            {
                  r -= e;
                  a++;
            }
      }      
      memcpy(q,&a,4);//4 bytes
}


//#include <stdio.h>
//#include <stdlib.h>

//#include "FIM.h"

main(void)
{
      int i;
      unsigned long l = 0x3fed0169L;
      struct int_sqrt q;


      for (i = 0; i < 200; ++i)
      {
            usqrt(i, &q);            
      }
      #ifdef DEBUG
      printf("sqrt(%3d) = %2d, remainder = %2d\n",i, q.sqrt, q.frac);//sqrt(200) = 924499, remainder = -2146958524
      #endif
      
//FIM_exit();
      
      return q.sqrt;
      //return 0;
}

