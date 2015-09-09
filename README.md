# Daily Planner
LaTeX and script files for creating my daily planner.

I use this daily planner to keep track of my daily occupations. I use `Schedule` column to mark occupations with definite dates. `i` and `ii` columns are back up columns for events of longer period such as a bus trip or an 24 hour event. `Bullets` section is to be filled with [Bullet Journal](http://www.bulletjournal.com/) style check-boxes and bullets.


## How can I use it?
Edit the parameters in [config.json](config.json) and run `daily_planner.py`.

```
python3 daily_planner.py && open output.pdf
```


## How it works?
It has a one page LaTeX file that needs a `jobname` file to get its `date` string. This string is the title of the page. 

The script generates human readable dates between given two dates and writes them in individual `jobname` files in `temp` directory. Then, it runs `pdflatex` for each of these generated date strings and generates corresponding PDF files in the same directory. Finally, it merges these pdf files into one and removes the `temp` directory.


### Dependencies
 - TeX Live or MikTeX
 - Python 3
 - [dateutil](https://labix.org/python-dateutil)
 - [PyPDF2](http://mstamy2.github.io/PyPDF2)


## License
[MIT](LICENSE).
