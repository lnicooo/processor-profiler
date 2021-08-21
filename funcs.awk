{ instructions[$2]+=1
} END {
 for (x in instructions) printf "%s %d \n", x, instructions[x]
}
