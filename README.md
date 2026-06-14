Attachment Resume_Anjali_Sawant.pdf added.None selected

Skip to content
Using Gmail with screen readers
Enable desktop notifications for Gmail.
   OK  No thanks
Conversations
7% of 15 GB used
Terms · Privacy · Program Policies
Last account activity: 7 minutes ago
Details
# VisionTrafficAI

> **Phase 1 — Automated Image Scraping Pipeline**
> Initial module of an intelligent traffic monitoring system built during the IIT Bombay Data Science Workshop (Dec 2025).

-----

## What is VisionTrafficAI?

VisionTrafficAI is a computer vision pipeline designed to automate traffic data collection and eventually enable real-time vehicle detection and speed tracking. This repository contains **Phase 1**: a fully automated image scraping engine using Selenium and ChromeDriver that collects raw traffic footage at scale — the dataset backbone for all future ML layers.

The end goal is a system that can:

- Detect and classify vehicles (YOLO-based)
- Track vehicle speed across frames
- Flag anomalies and congestion patterns in real time

-----

## Phase 1 — What’s Built

### Automated Image Scraper

- Selenium + ChromeDriver pipeline that navigates traffic camera feeds and web sources
- Automated scroll, click, and download sequences — no manual intervention
- Structured output directory with timestamped image batches
- Handles dynamic JS-rendered pages that basic `requests` can’t reach

### Why Selenium over direct scraping?

Traffic camera interfaces and map embeds (Google Maps, traffic.gov portals) render images via JavaScript. `requests` + `BeautifulSoup` returns empty DOM. Selenium drives a real browser, making it the only practical approach for this data source.

-----

## Roadmap

|Phase  |Status       |Description                                    |
|-------|-------------|-----------------------------------------------|
|Phase 1|Complete   |Automated image scraping via Selenium          |
|Phase 2|In Progress|YOLO vehicle detection on scraped frames       |
|Phase 3|Planned    |Speed tracking using optical flow / frame delta|
|Phase 4|Planned    |Real-time dashboard + anomaly alerts           |

-----

## Tech Stack

|Layer             |Technology                               |
|------------------|-----------------------------------------|
|Scraping          |Python, Selenium, ChromeDriver           |
|Browser Automation|`webdriver-manager`, `selenium.webdriver`|
|Image Storage     |OS filesystem (structured directories)   |
|Future: Detection |YOLOv8 (Ultralytics)                     |
|Future: Tracking  |OpenCV optical flow                      |

-----

## Project Structure

```
Vision_Traffic_AI/
└── IITB_day2/
    ├── scraper.py          ← Main Selenium scraping script
    ├── config.py           ← URLs, paths, timing configs
    ├── utils/
    │   └── file_handler.py ← Image saving + directory management
    └── output/             ← Scraped image batches (gitignored)
```

-----

## Setup & Run

### Prerequisites

```bash
pip install selenium webdriver-manager
```

### Run the scraper

```bash
cd IITB_day2
python scraper.py
```

ChromeDriver is managed automatically via `webdriver-manager` — no manual driver installation needed.

-----

## Context

Built as part of the **IIT Bombay Data Science Workshop** (December 2025), where the focus was building a real data collection pipeline before jumping to modelling — because garbage data in, garbage model out.

The scraper was designed to collect traffic images specifically for Indian road conditions (mixed traffic: bikes, autos, buses, pedestrians), which standard western datasets like COCO don’t represent well.

-----

## What’s Next

Phase 2 will plug YOLOv8 directly into the output of this scraper, running detection on each batch. If you want to contribute to vehicle detection or speed tracking, check the Issues tab.

-----

*Built by [Anjali Sawant](https://github.com/Anjalieee) — 2nd Year IT, Cummins College of Engineering, Pune*
Vision Traffic AI README.md
Displaying Vision Traffic AI README.md.
