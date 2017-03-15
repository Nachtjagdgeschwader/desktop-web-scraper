# desktop-web-scraper
The ultimate goal is to create an open source GUI desktop web-scraper, i.e. program which pull any desirable data from the Web and present it in desirable format.
Now the project is on a pre-test stage. The goal is to test how a simple one-variable scraping algorythm written in Python will behave in Windows x86 and Windows x64 compatible builds.
## For users
I have build a small app which answers any questions: Answerer. You can find respective builds for your system (Windows only, sorry):
* [*Windows x86*](https://github.com/Nachtjagdgeschwader/desktop-web-scraper/tree/answerer/answerer%2032bit) 
* [*Windows x64*](https://github.com/Nachtjagdgeschwader/desktop-web-scraper/tree/answerer/answerer%2064bit) 

If you don't know the architecture of your system, the x86 version should work for everyone.
Just download a zipped folder, unzip it locally and doubleclick the "answerer" shorcut. Type any question or keyword into the field and hit "Enter" on your keyboard or the "Ask" button in the program interface.
The answers are not supposed to be correct, full or whatever. They just must appear :-) If not, please report any "no answers", crushes etc. [*here*](https://github.com/Nachtjagdgeschwader/desktop-web-scraper/pulls) 
## For developers
The source code is located [*here*](https://github.com/Nachtjagdgeschwader/desktop-web-scraper/tree/answerer/source). The main program works fine with parsing_static.py algorythm, but crashes with parsing_dynamic.py, although the latter works fine separately in a console mode and print the desired result for any search(x) function usage. Developing an algorithm to work with dynamic pages is a must, because you won't find any interesting stuff on the Web, which is static html only :-)

So, any suggestions are appreciated to fix parsing_dynamic.py and main.py connection.
