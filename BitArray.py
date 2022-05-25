from copy import deepcopy # Performance moment xd

class BitArray:
    def __init__(self, _from = None, size = 32):
        if isinstance(_from, int):
            self.bits = BitArray.bits_from_int(_from, size = size)
        elif isinstance(_from, list):
            self.bits = _from
        else:
            self.bits = [ 0 ] * size

        self.size = len(self.bits)

    @staticmethod # ::: !!! BE CAREFUL WITH THIS METHOD !!! ::: # 
    def empty(): return BitArray([ ], 0)

    @staticmethod
    def bits_from_int(_int, size = 32):
        bits = [ ]
        _len =  0

        while _int:
            bits.append(_int & 1)
            _len +=  1
            _int >>= 1

        bits += [ 0 ] * (size - _len)
        bits.reverse()

        return bits

    @property
    def length(self):
        return len(self.bits)
    
    @property
    def is_empty(self):
        return self.length == 0

    @property
    def as_int(self):
        return int(str(self), 2)

    # Doesn't modify self
    def section(self, section):
        _from, _to = section
        
        return BitArray(deepcopy(self.bits)[_from:_to])

    # Modifies self
    def chomp(self, section):
        _from, _to = section

        chunk = self.bits[_from:_to]
        del     self.bits[_from:_to]
        
        return BitArray(chunk)

    # Chunkinizes a BitArray into a list of BitArrays of size 'size'.
    def chunks_of(self, size):
        bits   = BitArray(deepcopy(self.bits))
        chunks = [ ]

        while not bits.is_empty:
            chunks.append(bits.chomp((0, size)))

        return chunks

    def __rshift__(self, distance):

        bits = deepcopy(self.bits)

        for _ in range(distance):
            bits.insert(0, 0)
            bits.pop()

        return BitArray(bits)

    def __lshift__(self, distance):

        bits = deepcopy(self.bits)

        for _ in range(distance):
            bits.append(0)
            bits.pop(0)

        return BitArray(bits)

    def __invert__(self):
        return BitArray([ int(not bit) for bit in self.bits ])

    def __and__(self, other):
        if not isinstance(other, BitArray):
            raise Exception('BitArray can only be AND-ed with another BitArray')

        if self.size != other.size:
            raise Exception('BitArrays must be of the same size.')
        
        bits = [ ]
        
        for bit_a, bit_b in zip(self.bits, other.bits):
            bits.append(bit_a & bit_b)

        return BitArray(bits)

    def __or__(self, other):
        if not isinstance(other, BitArray):
            raise Exception('BitArray can only be OR-ed with another BitArray')

        if self.size != other.size:
            raise Exception('BitArrays must be of the same size.')

        bits = [ ]
        
        for bit_a, bit_b in zip(self.bits, other.bits):
            bits.append(bit_a | bit_b)

        return BitArray(bits)

    def __xor__(self, other):
        if not isinstance(other, BitArray):
            raise Exception('BitArray can only be XOR-ed with another BitArray')

        if self.size != other.size:
            raise Exception('BitArrays must be of the same size.')

        bits = [ ]
        
        for bit_a, bit_b in zip(self.bits, other.bits):
            bits.append(bit_a ^ bit_b)

        return BitArray(bits)

    def __add__(self, other):
        if not isinstance(other, BitArray):
            raise Exception('BitArray can only be added with another BitArray')

        if self.size != other.size:
            raise Exception('BitArrays must be of the same size.')

        return BitArray((self.as_int + other.as_int) % (2 ** self.size))

    def __matmul__(self, other): # Extend
        if isinstance(other, int):
            return BitArray(deepcopy(self.bits) + [ int(bool(other)) ])
        if isinstance(other, BitArray):
            return BitArray(deepcopy(self.bits) + deepcopy(other.bits))
        if isinstance(other, list):
            return BitArray(deepcopy(self.bits) + other)

        raise Exception('BitArray can only be extended with an integer of range (0, 1), or another BitArray')

    def __rmod__(self, other):
        if isinstance(other, int):
            return BitArray([ int(bool(other)) ] + deepcopy(self.bits))
        if isinstance(other, list):
            return BitArray(other + deepcopy(self.bits))

        raise Exception('BitArray can only be extended with an integer of range (0, 1), or another BitArray')

    def __iand__(self, other):
        return self & other

    def __ior__(self, other):
        return self | other

    def __ixor__(self, other):
        return self ^ other

    def __iadd__(self, other):
        return self + other

    def __imatmul__(self, other):
        return self @ other

    def __irmod__(self, other):
        return self % other
    
    def __str__(self):
        return ''.join([ str(bit) for bit in self.bits ])

    def __repr__(self):
        return f"({''.join([ str(bit) for bit in self.bits ])}:{self.size})"