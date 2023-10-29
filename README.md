# Description

This repository provides a brief overview of red color alerts in Israel.

## Usage

Follow these steps to use the repository:

1. Clone the repository to your local machine:

```bash
git clone https://github.com/eyalFischel/red_color_israel.git
```
2. Copy the city URL from 'https://www.oref.org.il/12481-en/Pakar.aspx' -> inspect elements -> network -> pick city -> check GetAlarmsHistory.aspx -> take url
3. Paste the URL into the code (line 9). For example:
```python
url_for_the_code =  f'https://www.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=en&fromDate=01.10.2023&toDate=31.10.2023&mode=0' # will show the entire missle events for the past month on Israel 
```
4. Run the code.

# NOTES
* In the code, five launches on the same day and at the same time are considered equivalent to one event.

