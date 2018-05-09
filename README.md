## eBay Fun
As I was selling some of my old trading cards on eBay, I saw a card listed for
way below the market price. I thought, "A program that could detect underpriced
auctions might be pretty valuable." Thus, this project was born.

The goal is to find the "true" price of a card, find buy-it-now auctions whose
price is significantly below that price, and send a notification to the user.

## Multithreading
Insofar as most of the execution time is spent waiting on eBay to send a
requested page back, we can easily realize a massive speed-up by assigning a thread to each card so that all threads are waiting in parallel.

## Package Dependencies
requests and statistics. Potentially sqlite3 (if it's not default).

## MTG JSON
Special thanks to [MTG JSON](http://mtgjson.com/) for keeping easily consumable, up-to-date data about all MTG sets and cards. The types of sets included are: `'box', 'core', 'masters', 'premium deck', 'promo', 'board game deck', 'duel deck', 'un', 'expansion', 'from the vault', 'vanguard', 'masterpiece', 'commander', 'archenemy', 'planechase', 'reprint', 'conspiracy', and 'starter'`. I stripped it down to only consider `'core', 'masters', 'un', 'expansion', 'reprint', and 'conspiracy'`.
### Exceptions
* I excluded `masterpiece` cards. Thus, for example, adding the value from Invocations to the expected value of Amonkhet will have to be done manually.
* I excluded `Collector's Edition` and `International Collector's Edition` from the `reprint` type.
* I excluded Time Spiral sets (`Time Spiral`, `Planar Chaos`, and `Future Sight`).

## Old Set Considerations
For `Antiquities`, `Arabian Nights`, `Fallen Empires`, `Homelands`, `Legends`, and `The Dark`, I (with the help of [MTG card search](https://magiccards.info/)) manually transcribed and dynamically parse the rarities of old sets. For alternate art cards, I averaged and rounded down the rarities to err on the side of safety (I would prefer the program underestimate a set rather than overestimate a set). That is, except for `Mishra's Factory`, where I treated it as four separate cards.

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