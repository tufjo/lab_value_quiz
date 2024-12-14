<p align="center">

</p>

<h1>Lab Value Quiz</h1>
A simple quiz executable that quiz based on a csv.

<h3>How to use</h3>
Download the master branch as a zip and un-zip them in the same folder.
<br>Make sure the name of the csv is named "lab_value.csv"
<br>The top right controls the font size
<h3>Shortcuts</h3>

| key   | button   |
| ----- | -------- |
| J     | Lower    |
| K     | Normal   |
| L     | Higher   |
| Space | Continue |

<h3>Requirements</h3>
Python 1.12.1 and up
<br>Python tkinter

you can install tkinter in the command line

```sh
pip install tk
```

<h3>CSV example</h3>
sample lab_value.csv is provided
<br>#example

| name                 | min | max | unit | note         | rand_min | rand_max |
| -------------------- | --- | --- | ---- | ------------ | -------- | -------- |
| Albumin              | 35  | 52  | g/L  | 35~52 g/L    | 0        | 90       |
| Alkaline phosphatase | 40  | 115 | U/L  | 40 ~ 115 U/L | 0        | 150      |

<h3>Known Issues</h3>
Not displaying colors
<br>Mu(μ) symbol is not displaying properly
<br>Cursor stuck in the font size input bar

<h3>Change Log</h3>

| version | note                     |
| ------- | ------------------------ |
| v1.0.1  | Added Font Size Controls |
| v1.0    | Initial elease           |
