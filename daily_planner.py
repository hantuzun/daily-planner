import os
import shlex
import shutil
import subprocess
from datetime import date, timedelta
from PyPDF2 import PdfFileReader, PdfFileMerger

# Create a directory for temporary files
files_dir = 'temp'
shutil.rmtree(files_dir, ignore_errors=True)
os.makedirs(files_dir)

# Set dates
first_day = date(2015, 6, 1)
last_day = date(2015, 8, 31)
dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1)]

# Create files with date strings
for d in dates:
    filename = str(d)
    directory = os.path.join(files_dir, filename)
    with open(directory, 'wb') as f:
        f.write(bytes('\def\date{' + d.strftime("%A, %d %B, %Y") + '}\n', 'UTF-8'))

# Create pdf files using daily-planner.tex and date files
for filename in os.listdir(files_dir):
    directory = os.path.join(files_dir, filename)
    subprocess.Popen(shlex.split('pdflatex -jobname=' + directory + ' daily-planner.tex')).communicate()

# Merge pdf files into one
pdf_files = [f for f in os.listdir(files_dir) if f.endswith("pdf")]
merger = PdfFileMerger()

for filename in pdf_files:
    merger.append(PdfFileReader(os.path.join(files_dir, filename), "rb"))

merger.write("output.pdf")

# Remove temporary files
shutil.rmtree(files_dir, ignore_errors=True)
