@align_word
label string
@string Hello, world!
@rawbytes D A 0

label start
    set 15
    cpy R3 ; Length of the message to print in R3
    setlab string
    cpy R2 ; Pointer to the character to print in R2
    label print-loop
        ; Loading a character from R2 and storing it in R3
        tbm
        load R2
        cpy R1
        tbm
        ; Function call made thanks to the `callf` macro
        callf printc
        ; Incrementing the pointer to the desired character
        set 1
        add R2
        cpy R2
        ; Decrementing the number of characters left to print
        set 1
        sub R3
        cc2
        cpy R3
        ; If the number of characters left to print is not 0, jump back to the start of the loop
        set 0
        eq R3
        cmpnot
        setlab print-loop
        jif
    quit

label printc
    pushr R2 ;addrs
    pushr R4 ;waiting loop pointer
    set+ 0xFF16 ;UART tx_cmd addr
    tbm
    cpy R2
    setlab printcLoop
    cpy R4
    label printcLoop
        load R2 ;testing that R2 is not 0 to see if we are ready to print
        cpy R12
        set 0
        eq R12
        read R4 ;until ready, go back
        jif
    set 1    ;computing the data addr
    add R2
    cpy R12
    read R1 ;writing the char
    str R12
    set 0   ;sending command
    str R2
    tbm
    popr R4 ;restoring registers
    popr R2
    ret


