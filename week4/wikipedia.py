import sys
from collections import deque

class Wikipedia:

    # Initialize the graph of pages.
    def __init__(self, pages_file, links_file):

        # A mapping from a page ID (integer) to the page title.
        # For example, self.titles[1234] returns the title of the page whose
        # ID is 1234.
        self.titles = {}

        # A set of page links.
        # For example, self.links[1234] returns an array of page IDs linked
        # from the page whose ID is 1234.
        self.links = {}

        # A set of page backlinks.
        # For example, self.backlinks[1234] returns an array of page IDs that
        # link to the page whose ID is 1234.
        self.backlinks = {}

        # Read the pages file into self.titles.
        with open(pages_file) as file:
            for line in file:
                (id, title) = line.rstrip().split(" ")
                id = int(id)
                assert not id in self.titles, id
                self.titles[id] = title
                self.links[id] = []
                self.backlinks[id] = []
        print("Finished reading %s" % pages_file)

        # Read the links file into self.links.
        #                      and self.backlinks.
        with open(links_file) as file:
            for line in file:
                (src, dst) = line.rstrip().split(" ")
                (src, dst) = (int(src), int(dst))
                assert src in self.titles, src
                assert dst in self.titles, dst
                self.links[src].append(dst)
                self.backlinks[dst].append(src)
        print("Finished reading %s" % links_file)
        print()


    # get id from wikipedia title
    def get_id(self, title):
        for id, t in self.titles.items():
            if t == title:
                return id


    # get title from wikipedia id
    def get_title(self, id):
        return self.titles[id]


    # Find the longest titles. This is not related to a graph algorithm at all
    # though :)
    def find_longest_titles(self):
        titles = sorted(self.titles.values(), key=len, reverse=True)
        print("The longest titles are:")
        count = 0
        index = 0
        while count < 15 and index < len(titles):
            if titles[index].find("_") == -1:
                print(titles[index])
                count += 1
            index += 1
        print()


    # Find the most linked pages.
    def find_most_linked_pages(self):
        link_count = {}
        for id in self.titles.keys():
            link_count[id] = 0

        for id in self.titles.keys():
            for dst in self.links[id]:
                link_count[dst] += 1

        print("The most linked pages are:")
        link_count_max = max(link_count.values())
        for dst in link_count.keys():
            if link_count[dst] == link_count_max:
                print(self.titles[dst], link_count_max)
        print()


    # Find the shortest path.
    # |start|: The title of the start page.
    # |goal|: The title of the goal page.
    def find_shortest_path(self, start, goal):
        queue = deque()
        visited = []
        route = []
        # append start node id to visited and queue
        queue.append(self.get_id(start))
        visited.append(self.get_id(start))
        while queue:
            # look at last node in queue
            node = queue.popleft()
            # for each child of node
            for child in self.links[node]:
                if child not in visited:
                    visited.append(child)
                    queue.append(child)
                    # if child is goal, backtrack to start
                    # ( to speed up, check child, not node )
                    if child == self.get_id(goal):
                        route.append(goal)
                        while node != self.get_id(start):
                            # for each parent of node,
                            # if parent is in visited, append to route
                            # and set node to parent until it reaches start
                            for parent in self.backlinks[node]:
                                if parent in visited:
                                    route.append(self.get_title(parent))
                                    node = parent
                                    break
                        route.reverse()
                        print("route: " + " -> ".join(route))
                        return route
        print("No route found")
        return route


    # Calculate the page ranks and print the most popular pages.
    def find_most_popular_pages(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


    # Do something more interesting!!
    def find_something_more_interesting(self):
        #------------------------#
        # Write your code here!  #
        #------------------------#
        pass


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: %s pages_file links_file" % sys.argv[0])
        exit(1)

    wikipedia = Wikipedia(sys.argv[1], sys.argv[2])
    wikipedia.find_longest_titles()
    wikipedia.find_most_linked_pages()
    wikipedia.find_shortest_path("B", "A")
    wikipedia.find_shortest_path("渋谷", "パレートの法則")
    wikipedia.find_most_popular_pages()
