## wikipedia

### run

- `g++ wikipedia.cpp -o wikipedia`
  - recommend `-O3` option for optimization
- `./wikipedia pages_file links_file`

### find_shortest_path

- function `find_shortest_path` in `wikipedia.cpp` uses BFS to find goal page
- once goal page is found, it backtracks to find the path from goal page to start page
  - ~~I'm not sure if this is the best way to find the shortest path ...~~
  - I realized just need to keep track of which node it came from as it runs BFS
    - so I changed the code to do that

### page rank

- algorithm is OK, but it takes so much time to run
- thinking about how to make it better ...
- the double loop in the while?
  - O(N*E)? but it seems inevitable ...

### do_something_more_interesting

- `count_pages_that_can_be_reached_from(string title)`
- `count_pages_that_can_reach(string title)`
  - Just run BFS from the given title as start page and count the number of pages visited (including the start page)

### tests

- `test()`
- I just tested with pages_small.txt and links_small.txt, and it worked fine
  - all the paths are shortest paths, and the page ranks are correct
