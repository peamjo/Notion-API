from pathlib import Path

def same_line_quotation():
# each word is on the same line of the input file, separated by spaces
    text = ""
    with open(str(Path.cwd().joinpath('wikipedia','emojis.txt')), 'r', encoding="utf8") as ifile:
        text = ifile.readline()

    # get all sepearte string split by space
    data = text.split(" ")

    # add quotes to each one
    data = [f"\"{name}\"" for name in data]

    # append them together with commas inbetween
    updated_text = ", ".join(data)

    # write to some file
    with open(str(Path.cwd().joinpath('wikipedia',"final_emojis.txt")), 'w', encoding="utf8") as ofile:
        ofile.write(updated_text)

def different_line_quotation():
# read lines from file
#  each input and output file word on a separate line
    words = []
    with open(str(Path.cwd().joinpath('wikipedia','emojis.txt')), 'r') as ifile:
        words = [line.replace("\n", "") for line in ifile.readlines()]

    # add quotes to each one
    updated_words = [f"\"{word}\"" for word in words]

    # append them together with commas inbetween
    updated_text = ",\n".join(updated_words)

    # write to some file
    with open(str(Path.cwd().joinpath('wikipedia','final_emojis.txt')), 'w') as ofile:
        ofile.write(updated_text)

same_line_quotation()
