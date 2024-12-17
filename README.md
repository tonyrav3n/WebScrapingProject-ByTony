# GitHub Topic Scraper

This Python script scrapes data from the GitHub Topics page and collects related repository information for each topic.
The data is saved into CSV files, with each topic's repositories stored in separate CSV files within a folder.

## Features

- Scrapes the GitHub Topics page for topic names, descriptions, and URLs.
- For each topic, fetches repository details (username, repository name, stars, and URL).
- Saves the data into CSV files:
    - A main `topics.csv` file containing the topic name, description, and URL.
    - Separate CSV files for each topic, storing repository information (username, repository name, stars, and URL).

## Prerequisites

Make sure you have Python 3.x installed along with the required libraries.

You can install the necessary libraries using `pip`:

```bash
pip install requests beautifulsoup4 pandas
```

## File Structure

```
/your_project_folder
  ├── data/
  │   └── topics/
  │       └── <topic_name>.csv
  ├── topics.csv
  ├── main.py
  └── README.md
```

- `data/`: A directory where topic-specific CSV files are stored.
- `topics.csv`: A CSV file containing the general topic information (name, description, and URL).
- `main.py`: The Python script that scrapes the data and saves it.
- `README.md`: This file.

## How It Works

1. **Scraping Topics**:  
   The script starts by scraping the GitHub Topics page (`https://github.com/topics`) to fetch the list of topics, their
   descriptions, and URLs.

2. **Scraping Repository Data**:  
   For each topic, the script navigates to the topic's URL and collects repository data, such as:
    - Repository owner's username
    - Repository name
    - Star count (converted to integer)
    - Repository URL

3. **Saving Data**:
    - The topic data (name, description, and URL) is saved in a file called `topics.csv`.
    - For each topic, a separate CSV file is created and saved in the `data/topics/` folder, containing the repository
      details for that topic.

4. **Sanitization**:  
   Topic names are sanitized to create valid filenames for the topic-specific CSV files.

## Running the Script

To run the script, simply execute `main.py`:

```bash
python main.py
```

The script will create a `data` folder, within which a `topics` folder will be created. It will then save the data to
CSV files.

## Example Output

### topics.csv

| title            | description                                        | url                                        |
|------------------|----------------------------------------------------|--------------------------------------------|
| Python           | A versatile programming language                   | https://github.com/topics/python           |
| JavaScript       | A programming language for web development         | https://github.com/topics/javascript       |
| Machine Learning | A field of study for creating intelligent machines | https://github.com/topics/machine-learning |

### <topic_name>.csv (e.g., python.csv)

| username   | repo_name  | stars | repo_url                                 |
|------------|------------|-------|------------------------------------------|
| pypa       | pip        | 15000 | https://github.com/pypa/pip              |
| tensorflow | tensorflow | 50000 | https://github.com/tensorflow/tensorflow |

## Error Handling

The script logs any errors encountered during the scraping process, such as network issues or unexpected data formats.
These errors are logged using Python's built-in logging module.

## License

This project is licensed under the MIT License.

---
