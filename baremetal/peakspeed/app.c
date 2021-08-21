/*
 *
 * Copyright (c) 2005-2012 Imperas Software Ltd., www.imperas.com
 *
 * The contents of this file are provided under the Software License
 * Agreement that you accepted before downloading this file.
 *
 * This source forms part of the Software and can be used for educational,
 * training, and demonstration purposes but cannot be used for derivative
 * works except in cases where the derivative works require OVP technology
 * to run.
 *
 * For open source models released under licenses that you can use for
 * derivative works, please visit www.OVPworld.org or www.imperas.com
 * for the location of the open source models.
 *
 */

#define NOINLINE __attribute__((noinline))

#define ITERATIONS 500

//#include "FIM.h"

int main()
{
    long a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7,
        i=8, j=9, k=10, l=11, m=12, n=13, o=14, p=15;
    long count, result;

    for(count=0; count<ITERATIONS; count++) {

        a = i;
        b = j;
        c = k;
        d = l;
        e = m;
        f = n;
        g = o;
        h = p;

        i = a;
        j = e;
        k = b;
        l = f;
        m = c;
        n = g;
        o = d;
        p = h;
    }

    result = a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p;

#ifdef DEBUG
    printf("result=%d\n", result);
#endif
    
//FIM_exit();

    return result;
}
