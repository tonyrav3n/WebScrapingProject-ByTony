import logging
import os
from typing import Any, Dict, List

import pandas as pd
import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Make BASE_URL a global variable
BASE_URL = "https://github.com"


def main():
    """
    The main function that orchestrates the script execution.

    - Fetches the topics from the GitHub Topics page.
    - Saves the topics data into a CSV file.
    - Fetches and saves repositories' info for each topic into separate CSV files in a folder.
    """
    topics_url = "https://github.com/topics"

    # Create data folder
    data_folder = "data"
    topics_folder = "topics"
    os.makedirs(os.path.join(data_folder, topics_folder), exist_ok=True)
    logging.info(f"Created folder: {data_folder}")
    try:
        # Fetch topics
        topics_data = get_topics(topics_url)
        if topics_data:
            # Save the main topics CSV
            save_to_csv(topics_data, os.path.join(data_folder, "topics.csv"))

            # Fetch repository data for each topic and save separately
            for topic, url in zip(topics_data["title"], topics_data["url"]):
                repo_data = get_repo_info(url)
                if repo_data:
                    filename = os.path.join(
                        data_folder, topics_folder, f"{sanitize_filename(topic)}.csv"
                    )
                    save_to_csv(repo_data, filename)
    except Exception as e:
        logging.error("An unexpected error occurred in the main function.")
        logging.exception(e)


def get_topics(topics_url: str) -> Dict[str, List[str]]:
    """
    Fetches topics, descriptions, and URLs from the GitHub Topics page.

    Args:
        topics_url (str): The URL to scrape.

    Returns:
        Dict[str, List[str]]: A dictionary with 'title', 'description', and 'url' keys.
    """
    try:
        # Request the page
        response = requests.get(topics_url)
        response.raise_for_status()
        logging.info("Page fetched successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching the URL: {topics_url}")
        logging.exception(e)
        return {}

    try:
        # Parse page content
        soup = BeautifulSoup(response.content, "html.parser")

        # Extract topics
        topic_selector = "f3 lh-condensed mb-0 mt-1 Link--primary"
        topics = [
            tag.text.strip() for tag in soup.find_all("p", {"class": topic_selector})
        ]

        # Extract descriptions
        desc_selector = "f5 color-fg-muted mb-0 mt-1"
        descriptions = [
            tag.text.strip() for tag in soup.find_all("p", {"class": desc_selector})
        ]

        # Extract URLs
        link_selector = "no-underline flex-1 d-flex flex-column"
        urls = [
            BASE_URL + tag.get("href")
            for tag in soup.find_all("a", {"class": link_selector})
        ]

        # Ensure equal lengths
        if not (len(topics) == len(descriptions) == len(urls)):
            logging.warning("Mismatch in extracted data lengths.")
            return {}

        logging.info("Topics data extracted successfully.")
        return {"title": topics, "description": descriptions, "url": urls}

    except Exception as e:
        logging.error("Error during data extraction and parsing.")
        logging.exception(e)
        return {}


def get_repo_info(url: str) -> Dict[str, List[Any]]:
    """
    Fetches repository information (username, repo name, stars, and URL) for a specific topic URL.

    Args:
        url (str): The topic URL to scrape.

    Returns:
        Dict[str, List[Any]]: A dictionary containing repository details.
    """
    repo_dict = {"username": [], "repo_name": [], "stars": [], "repo_url": []}

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")

        repo_selector = "f3 color-fg-muted text-normal lh-condensed"
        repo_tags = soup.find_all("h3", {"class": repo_selector})

        star_selector = "Counter js-social-count"
        star_tags = soup.find_all("span", {"class": star_selector})

        for i in range(len(repo_tags)):
            a_tags = repo_tags[i].find_all("a")
            username = a_tags[0].text.strip()
            repo_name = a_tags[1].text.strip()
            repo_url = BASE_URL + a_tags[1].get("href")
            stars = parse_star_count(star_tags[i].text.strip())

            repo_dict["username"].append(username)
            repo_dict["repo_name"].append(repo_name)
            repo_dict["stars"].append(stars)
            repo_dict["repo_url"].append(repo_url)

        logging.info(f"Repository data extracted successfully from {url}.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching repository data from {url}")
        logging.exception(e)
    except Exception as e:
        logging.error(f"Error processing data from {url}")
        logging.exception(e)

    return repo_dict


def parse_star_count(stars: str) -> int:
    """
    Converts a star count string into an integer.

    Args:
        stars (str): Star count as a string (e.g., '1.2k').

    Returns:
        int: Star count as an integer.
    """
    suffix_multipliers = {
        "k": 1_000,  # Thousand
        "m": 1_000_000,  # Million
        "b": 1_000_000_000,  # Billion
    }
    stars = stars.strip().lower()
    multiplier = 1
    if stars[-1] in suffix_multipliers:
        multiplier = suffix_multipliers[stars[-1]]
        stars = stars[:-1]

    try:
        return int(float(stars) * multiplier)
    except ValueError:
        logging.error(f"Invalid star count format: {stars}")
        raise ValueError(f"Invalid format: {stars}")


def save_to_csv(data: Dict[str, List[Any]], filename: str = "output.csv") -> None:
    """
    Saves the given dictionary to a CSV file.

    Args:
        data (Dict[str, List[Any]]): The data to save.
        filename (str): The name of the output CSV file.
    """
    try:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to '{filename}'.")
    except Exception as e:
        logging.error("Error saving data to CSV.")
        logging.exception(e)


def sanitize_filename(name: str) -> str:
    """
    Sanitizes a string for use as a filename.

    Args:
        name (str): The input string.

    Returns:
        str: A sanitized filename string.
    """
    return "".join(c if c.isalnum() or c in " ._-()" else "_" for c in name).strip()


if __name__ == "__main__":
    main()
