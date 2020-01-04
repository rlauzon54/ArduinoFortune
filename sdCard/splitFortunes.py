#!/usr/bin/env python3

# This program takes all the fortunes and puts a single fortune into a single file.
# It will also reformat the fortune to fit on the LCD, dropping any fortune that's too long for the LCD (See max_length and max_lines).

# The time required for the Arduino to get a certain fortune is proportional to its location in the directory.
# So fortune 00000.txt will come up fast, but fortune 12500.txt will take 10 seconds.
# So we put the fortunes into subdirectories of no more than 255 files.

import textwrap
import os
from fortune import Fortune

files = [
    "art", "ascii-art", "computers", "cookie", "debian", "definitions",
    "disclaimer", "education", "ethnic", "food", "fortunes", "goedel",
    "humorists", "kids", "law", "linux", "literature", "love", "magic",
    "medicine", "men-women", "miscellaneous", "news", "paradoxum", "people",
    "pets", "platitudes", "politics", "riddles", "science", "sports",
    "startrek", "translate-me", "wisdom", "work", "zippy"
]


def format_fortune(fortune, max_length):
    formatted = []

    for line in fortune:
        wrapped_text = textwrap.wrap(line, max_length)
        for new_line in wrapped_text:
            formatted.append(new_line)

    return (formatted)

# Number of chars per line
max_length = 50
# Number of lines on the screen
max_lines = 30

if __name__ == "__main__":
    f = Fortune()

    # file number
    fn = 0

    # loop over all the fortune files
    for filename in files:
        print("Processing {0}".format(filename))
        num_fortunes = f.get_fortune_count(filename)

        # loop over each fortune in the fortune file
        for i in range(num_fortunes):
            directory=int(fn/255)

            directory_name="f{0:03}".format(directory)
            if not os.path.exists(directory_name):
               os.mkdir(directory_name)

            output_file_name = "{0}/{1:05}.txt".format(directory_name,fn)

            # get that fortune
            fortune_lines = format_fortune(f.get_fortune(filename, i), max_length)

            # If the formatted fortune is "too big", bypass it
            if (len(fortune_lines) <= max_lines):
                # Open the new fortune file
                with open(output_file_name, "w") as new_file:
                    print(output_file_name)
                    # Calculate the number of lines to sort of center it on on the screen
                    padding_lines = int((max_lines - len(fortune_lines)) / 2)
                    # If there's at least 1 line
                    if padding_lines > 0:
                        # write out the padding line
                        for x in range(padding_lines):
                            new_file.write("\n")

                    # now write out the formatted fortune lines
                    for line in fortune_lines:
                        new_file.write("{0}\n".format(line))

                fn = fn + 1

