# New York City COVID-19 data

## Lag analysis

We want to understand the magnitude of lag. We explore it by the event  
date and also understand the size of counts that are lagged at each update interval.

We extract prior versions of the reported data from the [New York City  
Department of Health and Mental Hygiene](https://github.com/nychealth/coronavirus-data)

### Setup

Python 3.7

packages: pandas 1.2.1 , seaborn 0.11.1

### Steps

1. Clone data locally

~~~
git clone https://github.com/nychealth/coronavirus-data.git
~~~

2. Create folders to place all extracted versions in your own analysis repository
~~~
mkdir coronavirus-data-extraction
cd coronavirus-data-extraction
mkdir case-hosp-death
mkdir cases-by-day
mkdir data-by-day

# Create folder for curated data files
mkdir analysis
~~~

3. Extract all versions for case, death and hospitalization counts (define your clone and local path in the code)
~~~
cd <cloned path>

# Source: https://stackoverflow.com/questions/12850030/git-getting-all-previous-version-of-a-specific-file-folder
FILE_PATH=case-hosp-death.csv

EXPORT_TO=<your local path>/coronavirus-data-extraction/case-hosp-death

echo "Writing files to '$EXPORT_TO'"
git log --diff-filter=d --date-order --reverse --format="%ad %H" --date=iso-strict -- "$FILE_PATH" | grep -v '^commit' | \
	while read LINE; do \
		COMMIT_DATE=`echo $LINE | cut -d ' ' -f 1`; \
		COMMIT_SHA=`echo $LINE | cut -d ' ' -f 2`; \
		printf '.' ; \
		git cat-file -p "$COMMIT_SHA:$FILE_PATH" > "$EXPORT_TO/$COMMIT_DATE.$COMMIT_SHA.$FILE_NAME" ; \
	done


FILE_PATH=trends/cases-by-day.csv
EXPORT_TO=<your local path>/coronavirus-data-extraction/cases-by-day

FILE_NAME="$(basename "$FILE_PATH")"

echo "Writing files to '$EXPORT_TO'"
git log --diff-filter=d --date-order --reverse --format="%ad %H" --date=iso-strict -- "$FILE_PATH" | grep -v '^commit' | \
	while read LINE; do \
		COMMIT_DATE=`echo $LINE | cut -d ' ' -f 1`; \
		COMMIT_SHA=`echo $LINE | cut -d ' ' -f 2`; \
		printf '.' ; \
		git cat-file -p "$COMMIT_SHA:$FILE_PATH" > "$EXPORT_TO/$COMMIT_DATE.$COMMIT_SHA.$FILE_NAME" ; \
	done


FILE_PATH=trends/data-by-day.csv
EXPORT_TO=<your local path>/coronavirus-data-extraction/data-by-day

echo "Writing files to '$EXPORT_TO'"
git log --diff-filter=d --date-order --reverse --format="%ad %H" --date=iso-strict -- "$FILE_PATH" | grep -v '^commit' | \
	while read LINE; do \
		COMMIT_DATE=`echo $LINE | cut -d ' ' -f 1`; \
		COMMIT_SHA=`echo $LINE | cut -d ' ' -f 2`; \
		printf '.' ; \
		git cat-file -p "$COMMIT_SHA:$FILE_PATH" > "$EXPORT_TO/$COMMIT_DATE.$COMMIT_SHA.$FILE_NAME" ; \
	done
~~~

4. Curate extracted files
~~~
python curate_data.py
~~~


5. Visualize matrix and line plots
~~~
python visualize_data.py
~~~

### Notes
We extracted all data as of February 3rd, but only analyzed the first of three parts.  Date range was split into three parts due changes in repository organization.