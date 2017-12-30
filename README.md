## eBay Fun
As I was selling some of my old trading cards on eBay, I saw a card listed for
way below the market price. I thought, "A program that could detect underpriced
auctions might be pretty valuable." Thus, this project was born.

The goal is to find the "true" price of a card, find buy-it-now auctions whose
price is significantly below that price, and send a notification to the user.

## Why Python
eBay provides a REST API, so I needed a language with good support for web
requests. I selected Python because it has a really nice requests library that
I had used before. I could have went with JavaScript, but that would require a
web server to run because of cross-domain request issues.

I also needed math support, and Python has some good math libraries.

## Multithreading
Most of the execution time is spent waiting for eBay to send back the requested
HTML page. Thus, delegating this waiting time to a pool of threads significantly
reduces execution time. Benchmarks show that a pool of 8 threads divides run
times by a factor of anywhere from 3 to 6 (it gets more efficient with more GET
requests).

## Libraries Used
[Requests: HTTP for Humans](http://docs.python-requests.org)

## Package Dependencies
requests, statistics, and multiprocessing (requires C++ compiler found
[here](https://www.microsoft.com/en-us/download/confirmation.aspx?id=44266)).

## License
MIT License

Copyright (c) 2017 Lucas Molander

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