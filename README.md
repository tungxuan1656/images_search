BING SEARCH IMAGES
---
    python3 bing_images_search.py -h
    usage: bing_images_search.py [-h] [--save_dir SAVE_DIR]
                                [--start_index START_INDEX] [--limit LIMIT]
                                query

    Scrape images from the internet.

    positional arguments:
    query                 Query that should be used to scrape images.

    optional arguments:
        -h, --help            show this help message and exit
        --save_dir SAVE_DIR   Folder save images. If default, save to folder
                                data/bing/{query}
        --start_index START_INDEX
                                Start index of images to be scraped
        --limit LIMIT         Amount of images to be scraped.

------
GOOGLE SEARCH IMAGES
---
    python3 google_images_search.py -h                            
    usage: google_images_search.py [-h] [--save_dir SAVE_DIR]
                                [--max_results MAX_RESULTS]
                                query

    Scrape images from the internet.

    positional arguments:
    query                 Query that should be used to scrape images.

    optional arguments:
        -h, --help            show this help message and exit
        --save_dir SAVE_DIR   Folder save images. If default, save to folder
                                data/google/{query}
        --max_results MAX_RESULTS
                                Amount of images to be scraped.

Google Search require chromedriver  
Please download chromedriver and put to this folder