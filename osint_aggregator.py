import requests
import json
import time
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from cachetools import TTLCache
from typing import Dict, List, Optional, Any
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API Tokens - Load from environment variables
API_TOKENS = {
    "Twitter": os.getenv("TWITTER_API_TOKEN"),
    "Facebook": os.getenv("FACEBOOK_API_TOKEN"),
    "YouTube": os.getenv("YOUTUBE_API_TOKEN"),
    "Reddit": os.getenv("REDDIT_API_TOKEN"),
    "Instagram": os.getenv("INSTAGRAM_API_TOKEN"),
    "LinkedIn": os.getenv("LINKEDIN_API_TOKEN"),
    "TikTok": os.getenv("TIKTOK_API_TOKEN"),
    "Pinterest": os.getenv("PINTEREST_API_TOKEN"),
    "Telegram": os.getenv("TELEGRAM_API_TOKEN"),
    "Mastodon": os.getenv("MASTODON_API_TOKEN")
}

class OSINTFetcher:
    def __init__(self, source: Dict[str, Any]):
        self.source = source
        if 'headers' in self.source:
            for key, value in self.source['headers'].items():
                if value == "YOUR_API_TOKEN":
                    self.source['headers'][key] = API_TOKENS.get(self.source['name'], "")

    def fetch_data(self) -> Optional[Dict[str, Any]]:
        try:
            headers = self.source.get('headers', {})
            response = requests.get(self.source['endpoint'], params=self.source.get('params', {}), headers=headers)
            response.raise_for_status()
            return {'source': self.source['name'], 'data': response.json()}
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching data from {self.source['name']}: {e}")
            return None


class CacheManager:
    def __init__(self, ttl: int = 300, maxsize: int = 100):
        self.cache = TTLCache(maxsize=maxsize, ttl=ttl)

    def get(self, key: str) -> Optional[Any]:
        return self.cache.get(key)

    def set(self, key: str, value: Any) -> None:
        self.cache[key] = value


class DataSaver:
    @staticmethod
    def save_to_file(data: List[Dict[str, Any]], filename: str = 'osint_aggregated_data.json') -> None:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        logging.info(f"Data saved to {filename}")


class DecentralizedOSINTAggregator:
    def __init__(self, sources: List[Dict[str, Any]], rate_limit: int = 5, cache_ttl: int = 300):
        self.sources = sources
        self.results = []
        self.rate_limit = rate_limit
        self.cache = CacheManager(ttl=cache_ttl)

    def fetch_data(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        cache_key = f"{source['name']}_{json.dumps(source.get('params', {}), sort_keys=True)}"
        cached_data = self.cache.get(cache_key)
        if cached_data:
            logging.info(f"Using cached data for {source['name']}")
            return cached_data

        fetcher = OSINTFetcher(source)
        data = fetcher.fetch_data()
        if data:
            self.cache.set(cache_key, data)
        return data

    def aggregate_data(self) -> None:
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(self.fetch_data_with_rate_limit, source): source for source in self.sources}
            for future in as_completed(futures):
                try:
                    result = future.result()
                    if result:
                        self.results.append(result)
                except Exception as e:
                    logging.error(f"Error processing source {futures[future]['name']}: {e}")

    def fetch_data_with_rate_limit(self, source: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = self.fetch_data(source)
        time.sleep(self.rate_limit)
        return result

    def run(self) -> None:
        logging.info("Starting OSINT aggregation...")
        self.aggregate_data()
        logging.info(f"Aggregated data from {len(self.results)} sources.")

        # Process data with Rust
        filtered_data = self.process_data_with_rust(self.results)
        DataSaver.save_to_file(filtered_data)

    def process_data_with_rust(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        try:
            data_json = json.dumps(data)
            result = subprocess.run(
                ["./target/release/rust_osint_processor"],  # Adjust this path based on your setup
                input=data_json,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                logging.error(f"Rust processing failed: {result.stderr}")
                return []
            return json.loads(result.stdout)
        except Exception as e:
            logging.error(f"Error processing data with Rust: {e}")
            return []


class ConfigLoader:
    @staticmethod
    def load_config(config_path: str = 'config.json') -> Dict[str, Any]:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
        with open(config_path) as f:
            config = json.load(f)
            if 'sources' not in config:
                raise ValueError("Configuration file must contain 'sources' key.")
            return config


# Example usage
if __name__ == '__main__':
    try:
        config = ConfigLoader.load_config()
        sources = config['sources']
        rate_limit = config.get('rate_limit', 5)
        cache_ttl = config.get('cache_ttl', 300)

        aggregator = DecentralizedOSINTAggregator(sources, rate_limit, cache_ttl)
        aggregator.run()

    except Exception as e:
        logging.error(f"Error: {e}")
