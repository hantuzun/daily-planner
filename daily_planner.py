import os
import shlex
import shutil
import subprocess
from datetime import date, timedelta
from PyPDF2 import PdfFileReader, PdfFileMerger

# Create a directory for temporary files
files_dir = 'temp'
output_file = 'output.pdf'
shutil.rmtree(files_dir, ignore_errors=True)
os.makedirs(files_dir)

# Set parameters
author = 'Emrehan T\\"uz\\"un'
first_day = date(2015, 6, 1)
last_day = date(2015, 8, 31)


# Create a data file for the cover page
cover_data = os.path.join(files_dir, 'cover')
with open(cover_data, 'wb') as f:
    f.write(bytes('\\def\\author{' + author + '}\n', 'UTF-8'))
    f.write(bytes('\\def\\firstDay{' + first_day.strftime('%-d %B %Y') + '}\n', 'UTF-8'))
    f.write(bytes('\\def\\lastDay{' + last_day.strftime('%-d %B %Y') + '}\n', 'UTF-8'))

# Create the cover page pdf
print('Creating cover page')
subprocess.Popen(shlex.split('pdflatex -interaction=batchmode -jobname=' + cover_data + ' cover.tex')).communicate()
print()

# Create data files for date pages
dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1)]
for d in dates:
    f = str(d) + '.txt'
    directory = os.path.join(files_dir, f)
    with open(directory, 'wb') as f:
        f.write(bytes('\\def\\date{' + d.strftime('%-d %B') + '}\n', 'UTF-8'))
        f.write(bytes('\\def\\dayOfWeek{' + d.strftime('%A') + '}\n', 'UTF-8'))

# Create pdf files using daily-planner.tex and date files
txt_files = [f for f in os.listdir(files_dir) if f.endswith('txt')]
for f in txt_files:
    directory = os.path.join(files_dir, f)
    print('Creating ' + f + ' page')
    subprocess.Popen(shlex.split('pdflatex -interaction=batchmode -jobname=' + directory + ' daily-planner.tex')).communicate()
    print()

# Merge pdf files into one
merger = PdfFileMerger()

cover_pdf = os.path.join(files_dir, 'cover.pdf')
merger.append(PdfFileReader(cover_pdf, 'rb'))
os.remove(cover_pdf)

pdf_files = [f for f in os.listdir(files_dir) if f.endswith('pdf')]
for f in pdf_files:
    merger.append(PdfFileReader(os.path.join(files_dir, f), 'rb'))

merger.write(output_file)
print(output_file + ' is created')

# Remove temporary files
shutil.rmtree(files_dir, ignore_errors=True)
