## eBay Fun
As I was selling some of my old trading cards on eBay, I saw a card listed for
way below the market price. I thought, "A program that could detect underpriced
auctions might be pretty valuable." Thus, this project was born.

The goal is to find the "true" price of a card, find buy-it-now auctions whose
price is significantly below that price, and send a notification to the user.

## Multithreading
Insofar as most of the execution time is spent waiting on eBay to send a
requested page back, we can easily employ multithreading to significantly
reduce execution time. We assign a thread to each GET request, which has
yielded roughly a 7x speed-up.

## Package Dependencies
requests and statistics.

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