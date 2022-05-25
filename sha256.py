from functions import s0, s1, S0, S1, choice, major
from constants import list_of_ks, Registers, Of
from BitArray  import BitArray

def hash(message):
    message_bytes = [ BitArray(ord(char), 8) for char in message ]
    message_bits  =   BitArray.empty()

    # Transform the message into a sequence of bits.
    for byte in message_bytes:
        message_bits @= byte

    # Length of the message.
    message_length = message_bits.size

    # Append the bit '1' to the message, namely, the separator.
    message_bits @= 1

    # Calculate the padding (blocks of 512 bits).
    padding = (512 - 64 - message_bits.size) % 512

    # Apply the padding.
    message_bits @= BitArray(size = padding)

    # Imprint 64 bits of '0', to contain the message length.
    message_bits @= BitArray(message_length, 64)

    # Initialize the registers.
    old_registers = [
        BitArray(Registers.a),
        BitArray(Registers.b),
        BitArray(Registers.c),
        BitArray(Registers.d),
        BitArray(Registers.e),
        BitArray(Registers.f),
        BitArray(Registers.g),
        BitArray(Registers.h)
    ]

    # Split the message into 512-bit blocks.
    blocks = message_bits.chunks_of(512)

    # Begin message schedule for each block.
    for block in blocks:

        # Split the block into 16 32-bit words.
        chunk = block.chunks_of(32)

        # Message schedule.
        for word in range(16, 64):
            chunk.append(
                s0 (chunk[word - 15]) +
                    chunk[word -  7]  +
                s1 (chunk[word -  2]) +
                    chunk[word - 16]
            )

        # Compression.
        registers = [
            old_registers[Of.a],
            old_registers[Of.b],
            old_registers[Of.c],
            old_registers[Of.d],
            old_registers[Of.e],
            old_registers[Of.f],
            old_registers[Of.g],
            old_registers[Of.h]
        ]

        for word, const in zip(chunk, list_of_ks):
            x = S1     (registers[Of.e])                                   + \
                choice (registers[Of.e], registers[Of.f], registers[Of.g]) + \
                registers[Of.h] + word + BitArray(const)
            
            y = S0    (registers[Of.a])                                   + \
                major (registers[Of.a], registers[Of.b], registers[Of.c])

            # Apply compression (shifting list).
            registers.pop()
            registers.insert(0, x + y)
            registers[Of.e] = registers[Of.e] + x

        # Update the registers.
        old_registers[Of.a] = registers[Of.a] + old_registers[Of.a]
        old_registers[Of.b] = registers[Of.b] + old_registers[Of.b]
        old_registers[Of.c] = registers[Of.c] + old_registers[Of.c]
        old_registers[Of.d] = registers[Of.d] + old_registers[Of.d]
        old_registers[Of.e] = registers[Of.e] + old_registers[Of.e]
        old_registers[Of.f] = registers[Of.f] + old_registers[Of.f]
        old_registers[Of.g] = registers[Of.g] + old_registers[Of.g]
        old_registers[Of.h] = registers[Of.h] + old_registers[Of.h]

    return ''.join([ hex(register.as_int)[2:] for register in old_registers ])