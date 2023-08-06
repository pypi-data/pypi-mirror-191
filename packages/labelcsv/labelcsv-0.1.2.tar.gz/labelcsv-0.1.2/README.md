> A simple python package to quickly label csv files.<br>

# Installation
```console
pip install labelcsv
```

# Usage
1. Navigate to a directory that contains one or more csv files and run labelcsv.
```console
labelcsv 
```

2. Select the csv file to start labeling
```console
Select file:
> movie_reviews.csv
iris.csv
```

3. Choose the column in the csv file to label. The number next to each column shows the number of missing values for that column.
```console
Select column to label from movie_reviews.csv (Rows: 150, Columns: 2):
Movie Description → (0)
> Movie Reviews → (5)
```

4. Add labels separated by a single space. A __Skip__ label will automatically be added which will replace the label with a blank value.
```console
Add labels separated by a space:

Positive Negative Neutral
```

5. Start labeling by using the __UP__ and __DOWN__ arrow keys to select the label and then hit __ENTER__ to label the row:
```console
> Remaining Movie Reviews to be labeled: 150 - Skipped: 0

? I like the movie.
> Positive
Negative
Skip
```

6. After you are done labeling, the file will be saved as: "column_name.csv" and the distribution of labels will show.