import numpy as np


def intcode_program(state, max_size, n_read):
    output = []

    # Get state
    intcode_aux = state[0][:]
    inputs = state[1]
    pointer = state[2]
    relative_base = state[3]

    # Resize array (get more memory)
    intcode_aux = np.resize(intcode_aux, max_size)

    # Browse array by steps
    while pointer < len(intcode):
        # Get opcode and mode of parameters
        opcode_instruction = str(intcode_aux[pointer])
        while len(opcode_instruction) < 5:
            opcode_instruction = '0'+opcode_instruction

        opcode = int(opcode_instruction[-2:])
        mode_params = [
            int(opcode_instruction[-3]),
            int(opcode_instruction[-4]),
            int(opcode_instruction[-5])
        ]

        # Get index of each parameter
        indexes = [-1, -1, -1]
        for i in range(len(indexes)):
            pos = pointer+1+i
            if pos < len(intcode_aux):
                if mode_params[i] == 0:
                    indexes[i] = intcode_aux[pos]
                elif mode_params[i] == 1:
                    indexes[i] = pos
                elif mode_params[i] == 2:
                    indexes[i] = relative_base+intcode_aux[pos]

        # Apply opcode operation
        # STOP
        if opcode == 99:
            break

        # ADDITION
        elif opcode == 1:
            op1 = intcode_aux[indexes[0]]
            op2 = intcode_aux[indexes[1]]
            intcode_aux[indexes[2]] = op1+op2
            pointer += 4

        # MULTIPLICATION
        elif opcode == 2:
            op1 = intcode_aux[indexes[0]]
            op2 = intcode_aux[indexes[1]]
            intcode_aux[indexes[2]] = op1*op2
            pointer += 4

        # INPUT
        elif opcode == 3:
            intcode_aux[indexes[0]] = inputs.pop(0)
            pointer += 2

        # OUTPUT
        elif opcode == 4:
            #print('Output: '+intcode_aux[indexes[0]].__str__())
            output.append(intcode_aux[indexes[0]])
            pointer += 2
            if len(output) == n_read:
                break

        # JUMP-IF-TRUE
        elif opcode == 5:
            if intcode_aux[indexes[0]] != 0:
                pointer = intcode_aux[indexes[1]]
            else:
                pointer += 3

        # JUMP-IF-FALSE
        elif opcode == 6:
            if intcode_aux[indexes[0]] == 0:
                pointer = intcode_aux[indexes[1]]
            else:
                pointer += 3

        # LESS-THAN
        elif opcode == 7:
            if intcode_aux[indexes[0]] < intcode_aux[indexes[1]]:
                intcode_aux[indexes[2]] = 1
            else:
                intcode_aux[indexes[2]] = 0
            pointer += 4

        # EQUAL-TO
        elif opcode == 8:
            if intcode_aux[indexes[0]] == intcode_aux[indexes[1]]:
                intcode_aux[indexes[2]] = 1
            else:
                intcode_aux[indexes[2]] = 0
            pointer += 4

        # ADJUST RELATIVE BASE
        elif opcode == 9:
            relative_base += intcode_aux[indexes[0]]
            pointer += 2

    return [output, intcode_aux, pointer, relative_base]


def arcade_game(intcode):
    tiles = [
        [],     # Empty tiles
        [],     # Wall tiles
        [],     # Block tiles
        [],     # Horizontal paddle tiles
        []      # Ball tiles
    ]
    state = [intcode, [], 0, 0]

    # Get tiles until intcode ends
    while True:
       # Get position and tile
        [output,state[0], state[2], state[3]] = intcode_program(state, 5000, 3)
        if len(output) != 3:
            break

        pos = (output[0], output[1])
        tile = output[2]

        # Store tile
        tiles[tile].append(pos)

    return tiles





# My puzzle
print("Result for my puzzle:")
# Load data
file = open('./input.data', 'r')
intcode = [int(i) for i in file.readlines()[0][:-1].split(',')]

# Calculate the solution
solution = len(arcade_game(intcode)[2])

# Print the solution
print(solution)
