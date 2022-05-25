# ============================= #
# ::: The int size of bytes ::: #
# ============================= #

_INT_SIZE = 32

# ::: Helper functions ::: =========== #
# Used to tweak already existing ones. #
# ==================================== #

curry = lambda function: \
        lambda a       : \
        lambda b       : \
        function(a, b)

swap_args = lambda function: \
            lambda   a, b  : \
            function(b, a)

# ================================= #
# ::: SHA-256 related functions ::: #
# ================================= #

sigma = lambda alpha, beta, gamma: \
        lambda bit_array         : \
            alpha (bit_array) ^    \
            beta  (bit_array) ^    \
            gamma (bit_array)

shift_right = lambda bit_array, distance: bit_array >> distance
shift_left  = lambda bit_array, distance: bit_array << distance

rotate_right = lambda bit_array, distance: \
    bit_array >> distance | bit_array << (_INT_SIZE - distance)

rotate_left = lambda bit_array, distance: \
    bit_array << distance | bit_array >> (_INT_SIZE - distance)

rotate_right_by = curry(swap_args(rotate_right))
rotate_left_by  = curry(swap_args(rotate_left ))
shift_right_by  = curry(swap_args(shift_right ))
shift_left_by   = curry(swap_args(shift_left  ))

s0 = sigma ( rotate_right_by (  7) , rotate_right_by ( 18) , shift_right_by  (  3) )
s1 = sigma ( rotate_right_by ( 17) , rotate_right_by ( 19) , shift_right_by  ( 10) )
S0 = sigma ( rotate_right_by (  2) , rotate_right_by ( 13) , rotate_right_by ( 22) )
S1 = sigma ( rotate_right_by (  6) , rotate_right_by ( 11) , rotate_right_by ( 25) )

choice = lambda x, y, z : (x & y) ^ (~x & z)
major  = lambda x, y, z : (x & y) ^ ( x & z) ^ (y & z)