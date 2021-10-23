/*
 *
 * Copyright (c) 2005-2019 Imperas Software Ltd., www.imperas.com
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


#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "op/op.h"

#define MODULE_NAME "top"
#define MODULE_INSTANCE "u1"
#define HARNESS_NAME "harness"

#define CHUNK 8192

struct optionsS {
    const char*  appdisassembly;
} options = {
    .appdisassembly = NULL,
};

int main(int argc, const char *argv[]) {

    FILE *f;

    char file_buffer[CHUNK + 64];

    int buf_count = 0;

    opSessionInit(OP_VERSION);

    optCmdParserP parser = opCmdParserNew(HARNESS_NAME, OP_AC_ALL);

    opCmdParserAdd(parser, "appdisassembly", 0, "string", "user", OP_FT_STRINGVAL,
                           &options.appdisassembly,
                           "Disassembly output filename",
                           OP_AC_ALL, 0, 1);


    if (!opCmdParseArgs(parser, argc, argv)) {
         opMessage("E", HARNESS_NAME, "Command line parse incomplete");
    }
    f = fopen(options.appdisassembly, "w");

    optModuleP mr = opRootModuleNew(0, MODULE_NAME, 0);

    const char *u1_path = "module";
    optModuleP mi = opModuleNew(
        mr,                 // parent module
        u1_path,            // modelfile
        MODULE_INSTANCE,    // name
        0,
        0
    );

    // get the handle for the processor in the module
    optProcessorP processor = opObjectByName(mi, "cpu1", OP_PROCESSOR_EN).Processor;

    // construction complete
    opRootModulePreSimulate(mr);

    Bool done = False;

    while(!done) {

        buf_count += sprintf(&file_buffer[buf_count],"%x %s\n",opProcessorPC(processor),opProcessorDisassemble(processor, opProcessorPC(processor), OP_DSA_NORMAL));

        if(buf_count >= CHUNK){
            fwrite(file_buffer, CHUNK, 1, f);
            buf_count -= CHUNK;
            memcpy(file_buffer, &file_buffer[CHUNK], buf_count);
        }

        done = (opProcessorSimulate(processor, 1) != OP_SR_SCHED);


    }

    if(buf_count>0){
        fwrite(file_buffer, 1, buf_count, f);
    }

    fclose(f);

    opSessionTerminate();

    return 0;
}

