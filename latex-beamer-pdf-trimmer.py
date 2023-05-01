import sys
import os
import PyPDF2







if __name__ == "__main__":
    argc = len(sys.argv)
    inputfilename = ""
    outputfilename = ""

    # If no argument
    if argc == 1:
        print(f"Usage: {os.path.basename(__file__)} (input.pdf) [output.pdf]")
        sys.exit(1)
    
    # If one argument
    if argc >= 2:
        inputfilename = sys.argv[1]
        print(f"Input file: {inputfilename}")
    if argc >= 3:
        outputfilename = sys.argv[2]
        print(f"Output file: {outputfilename}")

    