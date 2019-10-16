# Scrapy project for E-Commerce websites

This is a scrapy application with spiders to automate searching from e-commerce websites.

This is an attempt to automate a user's day to day shopping/surfing tasks. So multiple features could be added to this project and contributions are greatly welcome!

Please dont use it for illegal purposes!

### Spiders included:

> The existing spiders are page-follower bots - retrieving all the listings from websites for the specified search term.

* craigslist_in (India)
* craigslist_us (USA)
* craigslist_ca (Canada)
* kijiji


### Usage:

```
$ cd ecommerce
$ pip install -r requirements.txt
$ scrapy crawl <spider-name> -a query="<search-term>" -o output.csv
```

### Possible feature enhancements:

- [ ] Price comparison from multiple websites
- [ ] Cron script - Price change notifier
- [ ] Integrate proxy switching
- [ ] < Insert-your-ideas-here >

### Contributing

Feel free to open an issue/PR if you'd like to improve the features/code-base.
