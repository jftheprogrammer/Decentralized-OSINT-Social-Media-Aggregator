# Decentralized OSINT Social Media Aggregator

## Overview

The **Decentralized OSINT Social Media Aggregator** is a powerful Python application designed to collect and aggregate open-source intelligence (OSINT) from multiple social media platforms. This project enables users to gather insights efficiently while maintaining flexibility, caching, and rate-limiting mechanisms.

## Features

- **Multi-platform support:** Aggregates data from the top 10 social media platforms.
- **Dynamic token handling:** Easily insert your own API tokens.
- **Caching:** Reduces redundant API requests with TTL-based caching.
- **Rate limiting:** Prevents exceeding platform API rate limits.
- **JSON data export:** Saves aggregated data to a JSON file.

## Supported Platforms

- Twitter
- Facebook
- YouTube
- Reddit
- Instagram
- LinkedIn
- TikTok
- Pinterest
- Telegram
- Mastodon

## Project Structure

```
/your-project-folder
│
├── config.json
├── osint_aggregator.py
├── osint_aggregated_data.json
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation

1. **Clone the repository:**

```bash
$ git clone https://github.com/yourusername/osint-aggregator.git
$ cd osint-aggregator
```

2. **Create a virtual environment:**

```bash
$ python -m venv venv
$ source venv/bin/activate   # For Linux & Mac
$ venv\Scripts\activate     # For Windows
```

3. **Install dependencies:**

```bash
$ pip install -r requirements.txt
```

4. **Create a config.json file:**

```json
{
  "sources": [
    {
      "name": "Twitter",
      "endpoint": "https://api.twitter.com/2/tweets/search/recent",
      "params": {"query": "OSINT"},
      "headers": {"Authorization": "Bearer YOUR_API_TOKEN"}
    },
    {
      "name": "YouTube",
      "endpoint": "https://www.googleapis.com/youtube/v3/search",
      "params": {"q": "OSINT", "part": "snippet"},
      "headers": {"Authorization": "Bearer YOUR_API_TOKEN"}
    }
  ],
  "rate_limit": 5,
  "cache_ttl": 300
}
```

👉 **Note:** Replace `YOUR_API_TOKEN` with your actual API keys.

5. **Add your API tokens:**
   - Open `osint_aggregator.py`
   - Replace the placeholders in the `API_TOKENS` dictionary with your own tokens.

## Usage

Run the aggregator:

```bash
$ python osint_aggregator.py
```

The aggregated data will be saved to `osint_aggregated_data.json`.

## Environment Variables (Optional)

For enhanced security, you can use environment variables instead of hardcoding API tokens.

1. **Create a .env file:**

```
TWITTER_API_TOKEN=your_twitter_api_token
YOUTUBE_API_TOKEN=your_youtube_api_token
```

2. **Load environment variables:**

```python
from dotenv import load_dotenv
load_dotenv()
```

## .gitignore

Ensure your sensitive files are not committed to GitHub:

```
config.json
.env
osint_aggregated_data.json
```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request with improvements, new data sources, or additional features.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

✨ **Let’s make OSINT aggregation simple and powerful!** 🚀

