# Skills and Knowledge Assessment
Tool to assess employees' skills and knowledge based on set of products, technologies and processes defined in an Excel spreadsheet.

# Usage
## Setup Database
`sqlite3 ska.sqlite < ska-create-db.sql`

## Update Dictionaries
`python3 ska-update-dict.py Skills\ and\ Knowledge\ Assessment.xlsx | sqlite3 ska.sqlite`

## Insert Individual Matrix
`python3 ska-insert-matrix.py Ivanov-ska-2022-12.xlsx | sqlite3 ska.sqlite`
