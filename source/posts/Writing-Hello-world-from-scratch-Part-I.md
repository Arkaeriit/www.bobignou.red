---
title: Writing Hello world from scratch Part I
date: 2022-05-06 19:13:13
tags:
---

# Making a new ISA

 “If you wish to make an apple pie from scratch, you must first invent the universe.”

― Carl Sagan

## What is an ISA?

An [instruction set architecture](https://en.wikipedia.org/wiki/Instruction_set_architecture), or ISA, describes the instruction set of a processor and its behavior. This is not enough to know how a processor works but this is the information needed to operate it.

I made my own ISA named Reflet which you can check out on the [Reflet GitHub repository](https://github.com/Arkaeriit/reflet).
 
## Designing a new ISA

### Wishlist

Why would one design a new ISA? With RISC-V and MIPS being open ISA with great support, there is not much point in doing so. Personally, I mostly did this for fun and artistic aspiration. I had a few ideas trotting in my head about what a fun ISA could be. I did want wanted to make a simple ISA, but rather a family of ISA for 8-bit, 16-bit, 32-bit, 64-bit, or even more bit-having processors that all share the same instruction set. At first, I even wanted to be able to make a processor with exotic word sizes but I scrapped that idea. I also wanted a Von Newman architecture and having instructions being a single indexable amount of memory. Those three needs combined meant that I needed to have instruction on only 8 bits. This is quite low, even some 8-bit computers use 16 bits instructions. 

On the other hand, I really liked the idea of instructions being 8 bits wide. This meant that I would probably end up with every possible byte being a valid instruction (and this ended up being the case). I find it quite beautiful that any binary file would be a valid program in my instruction set.

Another thing I wanted is to have a lot of general-purpose registers. I really like the idea of running a processor only from its ROM and registers, without using any RAM, like the [HP nanoprocessor](https://www.righto.com/2020/09/inside-hp-nanoprocessor-high-speed.html). This need does not mix well with having 8-bits wide instruction as indexing this register takes space.

### Solutions

To solve those issues, I needed to have an accumulator-like register. Indeed, had I used only general-purpose registers, when using two registers in each instruction, I would have needed to use less than 3 bits to access each register. This would have meant having less than 8 general-purpose registers. I could have had different categories of registers that are addressed differently but I really did not like this idea.

The solution is to have an accumulator-like register that is implicitly used by (almost) all instruction. Some instructions have a 4-bit opcode and a 4-bit operand that let me index 16 registers. Those instructions use both the working register (name of my accumulator-like register) and another register. Some other instructions only have an 8-bit opcode and don't interact with other registers than the working register. In the end, I ended up with the following instruction set:

|Mnemonic |Opcode |Operand                   |Effect                                                                                                                                                               |
|---------|-------|--------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|slp      |0x00   |Nothing                   |Does nothing, wait for the next instruction                                                                                                                          |
|set      |0x1    |A 4 bits number           |Put the number in the working register                                                                                                                               |
|read     |0x2    |A register                |Copies the value in the argument register into the working register                                                                                                  |
|cpy      |0x3    |A register                |Copies the value of the working register into the argument register                                                                                                  |
|add      |0x4    |A register                |Add the value in the working directory to the value in the argument register and put the result in the working register                                              |
|sub      |0x5    |A register                |Subtract to the value in the working directory the value in the argument register and put the result in the working register                                         |
|and      |0x6    |A register                |Do a bit-wise and between the working register and the argument register                                                                                             |
|or       |0x7    |A register                |Do a bit-wise or between the working register and the argument register                                                                                              |
|xor      |0x8    |A register                |Do a bitwise xor between the working register and the argument register                                                                                              |
|not      |0x9    |A register                |Put in the working register the bit-wise not of the argument register                                                                                                |
|lsl      |0xA    |A register                |Shit the bits in working register to the left n times, where n is the content of the argument register                                                               |
|lsr      |0xB    |A register                |Shit the bits in working register to the right n times, where n is the content of the argument register                                                              |
|eq       |0xC    |A register                |If the content of the working register is the same as the one in the argument registers, sets the comparison bit of the status register to 1. Otherwise, sets it to 0|
|les      |0xD    |A register                |If the content of the working register is less than the one in the argument registers, sets the comparison bit of the status register to 1. Otherwise, sets it to 0  |
|str      |0xE    |A register with an address|Store the value in the working register to the address given in the argument register                                                                                |
|load     |0xF    |A register with an address|Put in the working register the value at the address given in the argument register                                                                                  |
|cc2      |0x08   |Nothing                   |Put in the working register the opposite in two-complement of the working register.                                                                                  |
|jif      |0x09   |Nothing                   |Jump to the address in the working register if the comparison register is not equal to 0, does not affect the stack                                                  |
|pop      |0x0A   |Nothing                   |Put the content of the working register on the stack and updates the stack pointer.                                                                                  |
|push     |0x0B   |Nothing                   |Put the value on top of the stack in the working register and updates the stack pointer.                                                                             |
|call     |0xC    |Nothing                   |Put the current address in the stack and jump to the address in the working register.                                                                                |
|ret      |0x0D   |Nothing                   |Jump to the address just after the address on top of the stack.                                                                                                      |
|quit     |0x0E   |Nothing                   |Reset the processor or stop it.                                                                                                                                      |
|debug    |0x0F   |Nothing                   |Does not modify any registers but the processor sends a signal to tell it is executing a debug instruction.                                                          |
|cmpnot   |0x01   |Nothing                   |Flip the comparison bit of the status register.                                                                                                                      |
|retint   |0x02   |Nothing                   |Return from an interruption context.                                                                                                                                 |
|setint   |b000001|A two-bit number          |Set the routine of the interruption of the given number to the address in the working register.                                                                      |
|tbm      |0x03   |Nothing                   |Toggle byte mode. Toggle the memory accesses from the size specified by the status register to 8 bit and back.                                                       |

One could notice that if I needed to squeeze a bit more instruction, I could. For example, I could replace the `slp` instruction with `read WR` or `cpy WR` which are two instructions that do not change the state of the processor. Furthermore, I could fuse the `debug`, `quit`, and maybe some other instructions with a single instruction that uses the state of the working register to control its behavior. I might do that in the future if I feel like the instruction set needs more instructions.

As far as registers go, I have the working registers, a status register, a stack pointer, and a program counter as special registers. This left 12 general-purpose registers which is quite handy. As far as the status register go, as I want the behavior to be very similar with all word size, only the 8 LSB are used for status.

The complete (but still very small) documentation is available on the [Reflet GitHub repository](https://github.com/Arkaeriit/reflet).

## Simulator

Before writing the hardware description for my processor, I made a [simulator](https://github.com/Arkaeriit/reflet/tree/master/simulator). The point of the simulator is to test easily if programs I compiled to Reflet machine code work.

The simulator can only do very simple I/O, reading chars from stdin one at a time and writing chars to stdout one at a time. Fortunately, this is just enough to write a _Hello, world!_ program. Outputting character works by writing the desired character to at the address 0x1 and then, writing 0 to the address 0x0. Reading characters works in quite a similar way.

The simulator also has some monitoring capacities to help in the debugging process and can simulate hardware interrupts.

## Assembler

Writing machine code by hand is doable, especially with an ISA as simple as Reflet. Indeed, the opcodes being either 4 or 8 bits, they are quite easy to read or write in hexadecimal. But for our sanity's sake and to use some labels and macro, I made an [assembler/linker](https://github.com/Arkaeriit/reflet/tree/master/assembler) that converts the assembly language into Reflet machine code.

This assembler is not very well written, it needs some optimizations and it does not work with proper tokenizer-parser, instead, it works with a _Let's read each lines_-_I will wing it_ technology stack. 

Nevertheless, as writing macros for it is quite easy and it comes with very convenient default macros, it is perfectly usable as an assembler.

## Hello world

Now that we have both an assembler and a simulator, we can write and execute a program. Let's write an _Hello, world!_:

```
label msg
@string Hello, world!
@rawbytes A D 0

label start
    set 15
    cpy R1 ; Length of the message to print in R1
    setlab msg
    cpy R2 ; Pointer to the character to print in R2
    label print-loop
        ; Loading a character from R2 and storing it in R3
        tbm
        load R2
        cpy R3
        tbm
        ; Function call made thanks to the `callf` macro
        callf putc
        ; Incrementing the pointer to the desired character
        set 1
        add R2
        cpy R2
        ; Decrementing the number of characters left to print
        set 1
        sub R1
        cc2
        cpy R1
        ; If the number of characters left to print is not 0, jump back to the start of the loop
        set 0
        eq R1
        cmpnot
        setlab print-loop
        jif
    quit

; Function that prints the character in R3
label putc
    ; Preparing data_tx address
    set 1
    cpy R4
    tbm
    ; Writing the content of R3 into data_tx
    read R3
    str R4
    ; Writing 0 into data_cmd
    set 0
    cpy R4
    str R4
    tbm
    ret
```

We can observe that the program does not make any assumption regarding the word size of the processor. Thus, we can compile it and run it for a Reflet processor of any word size.

Let's compile it and run it on an 8-bit simulated processor:

```
$ reflet-asm Hello.asm -o Hello.bin -word-size 8
$ reflet-sim Hello.bin
Hello, world!
```

Yay! It works. Let's have a look at the generated machine code:

```
00000000  41 53 52 4d 3c 2d 3b 2c  10 3d 11 3c 12 4c 4e 3e  |ASRM<-;,.=.<.LN>|
00000010  a2 13 4c 08 4e f0 3c 2b  3d 2c 3f 3c 2d 3b 2c 10  |..L.N.<+=,?<-;,.|
00000020  3d 11 3c 12 4c 4e 3e 42  13 4c 08 4e f0 3c 2b 3d  |=.<.LN>B.L.N.<+=|
00000030  2c 3e 48 65 6c 6c 6f 2c  20 77 6f 72 6c 64 21 0a  |,>Hello, world!.|
00000040  0d 00 1f 31 3c 2d 3b 2c  10 3d 11 3c 12 4c 4e 3e  |...1<-;,.=.<.LN>|
00000050  32 13 4c 08 4e f0 3c 2b  3d 2c 32 03 f2 33 03 3c  |2.L.N.<+=,2..3.<|
00000060  2d 3b 2c 10 3d 11 3c 12  4c 4e 3e 98 13 4c 08 4e  |-;,.=.<.LN>..L.N|
00000070  f0 3c 2b 3d 2c 0c 11 42  32 11 51 08 31 10 c1 01  |.<+=,..B2.Q.1...|
00000080  3c 2d 3b 2c 10 3d 11 3c  12 4c 4e 3e 5b 13 4c 08  |<-;,.=.<.LN>[.L.|
00000090  4e f0 3c 2b 3d 2c 09 0e  11 34 03 23 e4 10 34 e4  |N.<+=,...4.#..4.|
000000a0  03 0d                                             |..|
```

At first, it doesn't look like much but by taking a closer look, we can read the machine code. For example, we can see that the function `putc` starts at address 98 and we can read the instruction we rote in assembly. 0x11 is `set 1`, 0x34 is `cpy R4`, 0x03 is `tbm`...

## Conclusion

Now that we have designed the ISA and that we have made tools to write machine code for it, the next step is to implement it in a hardware description language such as Verilog.

