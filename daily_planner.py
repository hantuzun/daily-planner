import json
import os
import shlex
import shutil
import subprocess
from utils import escape_for_tex
from datetime import date, timedelta
from dateutil.parser import parse
from PyPDF2 import PdfFileReader, PdfFileMerger

# Create a directory for temporary files
files_dir = 'temp'
output_file = 'output.pdf'
shutil.rmtree(files_dir, ignore_errors=True)
os.makedirs(files_dir)


with open('config.json') as config_file:    
    config = json.load(config_file)

# Set parameters
author = escape_for_tex(config['author'])
first_day = parse(config['first_day'], dayfirst=True).date()
last_day = parse(config['last_day'], dayfirst=True).date()

# Create a data file for the cover page
cover_data = os.path.join(files_dir, 'cover')
with open(cover_data, 'wb') as f:
    f.write(bytes('\\def\\author{' + author + '}\n', 'UTF-8'))
    f.write(bytes('\\def\\firstDay{' + first_day.strftime('%-d %B %Y') + '}\n', 'UTF-8'))
    f.write(bytes('\\def\\lastDay{' + last_day.strftime('%-d %B %Y') + '}\n', 'UTF-8'))

# Create the cover page pdf
subprocess.Popen(shlex.split('pdflatex -interaction=batchmode -jobname=' + cover_data + ' cover.tex')).communicate()

# Create pdf files using daily-planner.tex and date files
dates = [first_day + timedelta(days=x) for x in range((last_day-first_day).days + 1)]
for d in dates:
    file_name = os.path.join(files_dir, str(d) + '.txt')
    date = d.strftime('%-d %B')
    day_of_week = d.strftime('%A')
    with open(file_name, 'wb') as f:
        f.write(bytes('\\def\\date{' + date + '}\n', 'UTF-8'))
        f.write(bytes('\\def\\dayOfWeek{' + day_of_week + '}\n', 'UTF-8'))
    subprocess.Popen(shlex.split('pdflatex -interaction=batchmode -jobname=' + file_name + ' days/' +  day_of_week + '.tex')).communicate()

# Merge pdf files into one
merger = PdfFileMerger()

cover_pdf = os.path.join(files_dir, 'cover.pdf')
merger.append(PdfFileReader(cover_pdf, 'rb'))
os.remove(cover_pdf)

pdf_files = [f for f in os.listdir(files_dir) if f.endswith('pdf')]
for f in pdf_files:
    merger.append(PdfFileReader(os.path.join(files_dir, f), 'rb'))

merger.write(output_file)
print(output_file + ' is created \n')

# Remove temporary files
shutil.rmtree(files_dir, ignore_errors=True)
