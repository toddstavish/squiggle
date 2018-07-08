import numpy as np
from itertools import islice

def _k_mers(sequence, k):
    it = iter(sequence)
    result = tuple(islice(it, k))
    if len(result) == k:
        yield "".join(result)
    for elem in it:
        result = result[1:] + (elem,)
        yield "".join(result)

def transform(sequence, method="squiggle"):
    '''Transforms a DNA sequence into a series of coordinates for 2D visualization.

    Args:
        sequence (str): The DNA sequence to transform.
        method (str): The method by which to transform the sequence. Defaults to "squiggle".

    Returns:
        tuple: A tuple containing two lists: one for the x coordinates and one for the y coodinates.

    Example:
        >>> transform("ATG")
        ([0, 0.5, 1, 1, 1.5, 2, 2, 2.5, 3], [0, 1, 0, -1, -2, -1, 0])

    '''

    sequence = sequence.upper()

    if method == "squiggle":
        running_value = 0
        x, y = np.linspace(0, len(sequence), 2 * len(sequence) + 1), [0]
        for character in sequence:
            if character == "A":
                y.extend([running_value + 1, running_value])
            elif character == "C":
                y.extend([running_value - 1, running_value])
            elif character == "T":
                y.extend([running_value - 1, running_value - 2])
                running_value -= 2
            elif character == "G":
                y.extend([running_value + 1, running_value + 2])
                running_value += 2
            else:
                y.extend([running_value] * 2)
        return list(x), y

    elif method == "gates":
        x, y = [0], [0]
        for character in sequence:
            if character == "A":
                x.append(x[-1]) # no change in x coord
                y.append(y[-1] - 1)
            elif character == "T":
                x.append(x[-1]) # no change in x coord
                y.append(y[-1] + 1)
            elif character == "G":
                x.append(x[-1] + 1)
                y.append(y[-1]) # no change in y coord
            elif character == "C":
                x.append(x[-1] - 1)
                y.append(y[-1]) # no change in y coord
            else:
                raise ValueError("Invalid character in sequence: " + character + ". Gates's method does not support non-ATGC bases. Try using method=squiggle.")

    elif method == "yau":
        x, y = [0], [0]
        for character in sequence:
            if character == "A":
                x.append(x[-1] + 0.5)
                y.append(y[-1] - ((3**0.5) / 2))
            elif character == "T":
                x.append(x[-1] + 0.5)
                y.append(y[-1] + ((3**0.5) / 2))
            elif character == "G":
                x.append(x[-1] + ((3**0.5) / 2))
                y.append(y[-1] - 0.5)
            elif character == "C":
                x.append(x[-1] + ((3**0.5) / 2))
                y.append(y[-1] + 0.5)
            else:
                raise ValueError("Invalid character in sequence: " + character + ". Yau's method does not support non-ATGC bases. Try using method=squiggle.")

    elif method == "randic":
        x, y = [], []
        mapping = dict(A=3, T=2, G=1, C=0)
        for i, character in enumerate(sequence):
            x.append(i)
            try:
                y.append(mapping[character])
            except KeyError:
                raise ValueError("Invalid character in sequence: " + character + ". Randić's method does not support non-ATGC bases. Try using method=squiggle.")

    elif method == "qi":
        mapping = {'AA': 12,
                   'AC': 4,
                   'GT': 6,
                   'AG': 0,
                   'CC': 13,
                   'CA': 5,
                   'CG': 10,
                   'TT': 15,
                   'GG': 14,
                   'GC': 11,
                   'AT': 8,
                   'GA': 1,
                   'TG': 7,
                   'TA': 9,
                   'TC': 3,
                   'CT': 2}
        x, y = [], []

        for i, k_mer in enumerate(_k_mers(sequence, 2)):
            x.append(i)
            try:
                y.append(mapping[k_mer])
            except KeyError:
                raise ValueError("Invalid character in sequence: " + character + ". Qi's method does not support non-ATGC bases. Try using method=squiggle.")

    else:
        raise ValueError("Invalid method. Valid methods are 'squiggle', 'gates', 'yau', and 'randic'.")

    return x, y
