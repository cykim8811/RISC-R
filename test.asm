
addi    sp, 0x0100

subi    sp, 16

xori     a0, 0x28
mswp     a0, 0xc(sp)
xori     a0, 0x4a
mswp     a0, 0x8(sp)
xori     a0, 0x52
mswp     a0, 0x4(sp)
xori     a0, 0x53
mswp     a0, 0x0(sp)

mswp     a1, 12(sp)
mswp     a2, 8(sp)
add      a1, a2
mswp     a2, 8(sp)
mswp     a1, 12(sp)

mswp     a1, 0(sp)
mswp     a2, 4(sp)
jeq      a1, a2, .L1
mswp     a2, 4(sp)
mswp     a1, 0(sp)

mswp     a1, 12(sp)
mswp     a2, 8(sp)
sub      a1, a2
mswp     a2, 8(sp)
mswp     a1, 12(sp)

mswp     a1, 0(sp)
mswp     a2, 4(sp)
jne      a1, a2, .L2
mswp     a2, 4(sp)
mswp     a1, 0(sp)

mswp     a1, 0(sp)
mswp     a2, 4(sp)
jeq      a1, a2, .L1
mswp     a2, 4(sp)
mswp     a1, 0(sp)

mswp     a1, 12(sp)
mswp     a2, 8(sp)
add      a1, a2
mswp     a2, 8(sp)
mswp     a1, 12(sp)

mswp     a1, 0(sp)
mswp     a2, 4(sp)
jne      a1, a2, .L2
mswp     a2, 4(sp)
mswp     a1, 0(sp)

hlt
