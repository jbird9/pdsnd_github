### Python for Data Scientist Course: Interactive Statistics Program for Bikeshare from Motivate

#### Date: 02/20/2025

#### Description
This program allows users to explore data from the bikeshare service Motivate, focusing on the first 6 months of 2017 across select cities. Users can interact with the program through various prompts and outputs:

- **City Selection**:
  - Choose from three cities: Chicago, New York City, or Washington.

- **Month Filter**:
  - Select specific months by typing out the month name and pressing enter after each.
  - Complete the selection by typing 'done' and pressing enter.
  - Typing 'done' without any prior month selection defaults to all months.

- **Day Filter**:
  - Select specific days by typing out the day names one at a time.
  - Complete the selection by typing 'done' and pressing enter.
  - Typing 'done' without any prior day selection defaults to all days.

- **Raw Data Viewing**:
  - Respond 'Yes' to view every line of the selected city's data, displayed five entries at a time.
  - Press enter to view the next five entries or type 'no' and press enter to stop.

- **Filtered Data Viewing**:
  - View data with selected filters, including additional details like year, month, day of the week, and starting hour.
  - Press enter to view the next five entries or type 'no' and press enter to exit.

#### Statistics Output
After filtering, the program generates and displays statistics in the following categories:

- **Popular Times of Travel**:
  - Most common month
  - Most common day of the week
  - Most common hour

- **Popular Stations and Trip**:
  - Most common start station
  - Most common end station
  - Most common trip from start to end

- **Trip Duration**:
  - Total travel time (displayed in days, hours, minutes, and seconds)
  - Average travel time (displayed in minutes and seconds, rounded to the nearest second)

- **User Info**:
  - Counts of each user type (e.g., Subscriber, Customer, Dependent, Unknown)
  - Counts of each gender (available only for New York City and Chicago)
  - Rider age extremes:
    - Oldest rider(s)
    - Youngest rider(s)
    - Most common year of birth

#### Files Used
- `chicago.csv`
- `new_york_city.csv`
- `washington.csv`

#### Dependencies
- time
- pandas
- numpy

#### Credits
Credit is given to the Udacity Programming for Data Science with Python course materials for the foundational concepts and data used in this program.

#### MIT License

Copyright (c) [2025] [Jordan Toby Bird]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.