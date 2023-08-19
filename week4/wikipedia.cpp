#include <iostream>
#include <fstream>
#include <map>
#include <vector>
#include <algorithm>
#include <queue>
#include <set>

using namespace std;

class Wikipedia {
  public:
    map<int, string> titles;
    map<int, vector<int>> links;
    map<int, vector<int>> backlinks;

  /// @brief read [pages_file] [links_file] and set [titles] [links] [backlinks]
  /// @param pages_file, links_file
  /// @return none
  public:
    Wikipedia(string pages_file, string links_file){
      ifstream fin(pages_file);
      string line;
      if (!fin){
        cerr << pages_file << "is not found" << endl;
        return;
      }
      while(getline(fin, line)){
        int id = stoi(line.substr(0, line.find(' ')));
        string title = line.substr(line.find(' ') + 1);
        titles.insert(make_pair(id, title));
      }
      cout << "finished reading " << pages_file << endl;

      ifstream fin2(links_file);
      if (!fin2){
        cerr << links_file << "is not found" << endl;
        return;
      }
      while(getline(fin2, line)){
        int from = stoi(line.substr(0, line.find(' ')));
        int to = stoi(line.substr(line.find(' ') + 1));
        links[from].push_back(to);
        backlinks[to].push_back(from);
      }
      cout << "finished reading " << links_file << endl;
      cout << endl;
    }

  /// @brief get id from title
  /// @param title
  /// @return id
  public:
    int get_id(string title){
      for (auto itr = titles.begin(); itr != titles.end(); ++itr){
        if (itr->second == title){
          return itr->first;
        }
      }
      return -1;
    }

  /// @brief find longest title from pages
  /// @param none
  /// @return longest_titles
  public:
    vector<int> find_longest_title(){
      vector<string> titles_name = {};
      vector<int> longest_titles = {};
      // make list of titles which is descending order of length
      for (auto itr = titles.begin(); itr != titles.end(); ++itr) {
        titles_name.push_back(itr->second);
      }
      sort(titles_name.begin(), titles_name.end(), [](const string& x, const string& y){return x.size() > y.size();});
      int count = 0;
      int index = 0;
      // find longest titles which does not include "_"
      while (count < 15 && index < titles_name.size()){
        if (titles_name[index].find("_") == string::npos){
          longest_titles.push_back(get_id(titles_name[index]));
          count++;
        }
        index++;
      }
      return longest_titles;
    }

  /// @brief find the most linked pages
  /// @param none
  /// @return most_linked_pages
  public:
    vector<int> find_most_linked_pages(){
      map<int, int> link_count = {};
      vector<int> most_linked_pages = {};
      // initialize link_count
      for (int id = 0; id < titles.size(); ++id){
        link_count.insert(make_pair(id, 0));
      }
      // count links
      for (auto link = links.begin(); link != links.end(); ++link){
        for (auto itr = link->second.begin(); itr != link->second.end(); ++itr){
          link_count[*itr]++;
        }
      }
      // find most linked pages
      int max_link_count = max_element(link_count.begin(), link_count.end(), [](const pair<int, int>& x, const pair<int, int>& y){return x.second < y.second;})->second;
      for (auto itr = link_count.begin(); itr != link_count.end(); ++itr){
        if (itr->second == max_link_count){
          most_linked_pages.push_back(itr->first);
        }
      }
      return most_linked_pages;
    }

  /// @brief find the shortest path from [start] to [goal]
  /// @param start, goal
  /// @return route
  public:
    vector<int> find_shortest_path(string start, string goal){
      queue<int> q = {};
      set<int> visited = {};
      map<int, int> parent = {};
      vector<int> route = {};
      // if start or goal is not found, return empty route
      if (get_id(start) == -1 || get_id(goal) == -1){
        return route;
      } else if (start == goal){
        route.push_back(get_id(start));
        return route;
      }
      // get id of start and goal
      int start_id = get_id(start);
      int goal_id = get_id(goal);
      // initialize queue and visited
      q.push(start_id);
      visited.insert(start_id);
      while(!q.empty()){
        int node = q.front();
        q.pop();
        if (node == goal_id){
          // backtrace route from recorded set of child and node
          while (node != start_id){
            route.push_back(node);
            node = parent[node];
          }
          route.push_back(start_id);
          // reverse route
          reverse(route.begin(), route.end());
          return route;
        }
        // add child nodes to queue
        for (auto child = links[node].begin(); child != links[node].end(); ++child){
          if (visited.find(*child) == visited.end()){
            q.push(*child);
            visited.insert(*child);
            // if child is not visited, record set of child and node
            parent.insert(make_pair(*child, node));
          }
        }
      }
      return route;
    }

  /// @brief print titles from ids
  /// @param ids
  /// @return none
  public:
    void print_titles(vector<int> ids){
      if (ids.size() == 0){
        cout << "no pages found" << endl;
        return;
      }

      for (auto itr = ids.begin(); itr != ids.end(); ++itr){
        cout << titles[*itr] << endl;
      }
      cout << endl;
    }

  /// @brief print titles and values from map
  /// @param pairs
  /// @return none
  public:
    void print_titles_and_values(map<int, float> pairs){
      if (pairs.size() == 0){
        cout << "no pages found" << endl;
        return;
      }
      for (auto itr = pairs.begin(); itr != pairs.end(); ++itr){
        cout << titles[itr->first] << " " << itr->second << endl;
      }
      cout << endl;
    }

  /// @brief find the most popular pages
  /// @param none
  /// @return most_popular_pages
  public:
    map<int, float> find_most_popular_pages(){
      map<int, float> most_popular_pages = {};
      map<int, float> page_rank = get_page_rank();
      // sort page_rank in descending order
      vector<pair<int, float>> sorted_page_rank(page_rank.begin(), page_rank.end());
      sort(sorted_page_rank.begin(), sorted_page_rank.end(), [](const pair<int, float>& x, const pair<int, float>& y){return x.second > y.second;});
      // find most popular pages
      for (int i = 0; i < 10; ++i){
        most_popular_pages.insert(make_pair(sorted_page_rank[i].first, sorted_page_rank[i].second));
      }
      return most_popular_pages;
    }

  /// @brief get page rank
  /// @param none
  /// @return page rank
  public:
    map<int, float> get_page_rank(){
      map<int, float> page_rank = {};
      // initialize page rank
      for (auto link = links.begin(); link != links.end(); ++link){
        page_rank.insert(make_pair(link->first, 1.0));
      }
      bool converged = false;
      // until page rank converges
      while (!converged){
        map<int, float> prev_page_rank = {};
        for (auto rank = page_rank.begin(); rank != page_rank.end(); ++rank) {
          prev_page_rank.insert(make_pair(rank->first, rank->second));
        }
        // update page rank
        for (auto backlink = backlinks.begin(); backlink != backlinks.end(); ++backlink){
          float sum = 0.0;
          for (auto itr = backlink->second.begin(); itr != backlink->second.end(); ++itr){
            sum += page_rank[*itr] / links[*itr].size();
          }
          page_rank[backlink->first] = 0.15 + 0.85 * sum;
        }
        // check if the page rank converges
        for (auto rank = page_rank.begin(); rank != page_rank.end(); ++rank){
          // pages_large.txt has about 2e8 pages
          if (abs(rank->second - prev_page_rank[rank->first]) > 1e-6){
            converged = false;
            break;
          } else {
            converged = true;
          }
        }
      }
      return page_rank;
    }

  /// @brief count pages that can be reached from start
  /// @param start
  /// @return count
  public:
    int count_pages_that_can_be_reached_from(string start){
      int start_id = get_id(start);
      queue<int> q = {};
      vector<int> visited = {};
      int count = 1;
      q.push(start_id);
      visited.push_back(start_id);
      while (!q.empty()){
        int node = q.front();
        q.pop();
        // add child nodes to queue
        for (auto child = links[node].begin(); child != links[node].end(); ++child){
          if (find(visited.begin(), visited.end(), *child) == visited.end()){
            q.push(*child);
            visited.push_back(*child);
            count++;
          }
        }
      }
      return count;
    }

    /// @brief count pages that can be reached from start
    /// @param start
    /// @return count
  public:
    int count_pages_that_can_reach(string goal) {
      int goal_id = get_id(goal);
      queue<int> q = {};
      vector<int> visited = {};
      int count = 1;
      q.push(goal_id);
      visited.push_back(goal_id);
      while (!q.empty()) {
        int node = q.front();
        q.pop();
        // add child nodes to queue
        for (auto child = backlinks[node].begin(); child != backlinks[node].end();
             ++child) {
          if (find(visited.begin(), visited.end(), *child) == visited.end()) {
            q.push(*child);
            visited.push_back(*child);
            count++;
          }
        }
      }
      return count;
    }
  };

/// @brief test
/// @param none
/// @return int 0 or 1 for success or failure
int test() {
  // check if the shortest path is correct
  vector<vector<int>> results = {};
  vector<vector<int>> expected = {
      {1},          {1, 2},       {1, 2, 3}, {1, 2, 4},    {1, 2, 3, 5},
      {1, 2, 3, 6}, {2, 3, 1},    {2},       {2, 3},       {2, 4},
      {2, 3, 5},    {2, 3, 6},    {3, 1},    {3, 2},       {3},
      {3, 2, 4},    {3, 5},       {3, 6},    {4, 2, 3, 1}, {4, 2},
      {4, 2, 3},    {4},          {4, 5},    {4, 6},       {5, 4, 2, 3, 1},
      {5, 4, 2},    {5, 4, 2, 3}, {5, 4},    {5},          {5, 4, 6},
      {6, 3, 1},    {6, 3, 2},    {6, 3},    {6, 3, 2, 4}, {6, 3, 5},
      {6}};
  Wikipedia wiki("pages_small.txt", "links_small.txt");

  vector<string> pages = {"A", "B", "C", "D", "E", "F"};

  for (auto page = pages.begin(); page != pages.end(); ++page) {
    for (auto page2 = pages.begin(); page2 != pages.end(); ++page2) {
      results.push_back(wiki.find_shortest_path(*page, *page2));
    }
  }
  for (size_t i = 0; i < expected.size(); i++) {
    if(results[i] != expected[i]){
      cerr << "shortest path test failed" << endl;
      return 1;
    }
  }
  // check if sum of page ranks is equal to number of pages
  auto page_rank = wiki.get_page_rank();
  float sum = 0;
  for (auto p : page_rank) {
    sum += p.second;
  }
  if (abs(sum - page_rank.size()) > 1e-3){
    cerr << "page rank test failed" << endl;
    return 1;
  }
  cout << "all tests passed" << endl << endl;
  return 0;
}

int main( int argc, char* argv[] ){
  if (argc != 3){
    cerr << "Usage: " << argv[0] <<" <pages_file> <links_file>" << endl;
    return 1;
  }
  if (test()==1) return 1;
  string pages_file = argv[1];
  string links_file = argv[2];
  Wikipedia wiki(pages_file, links_file);
  wiki.print_titles(wiki.find_longest_title());
  wiki.print_titles(wiki.find_most_linked_pages());
  wiki.print_titles(wiki.find_shortest_path("渋谷", "パレートの法則"));
  int count_pages_that_can_be_reached_from_google =
      wiki.count_pages_that_can_be_reached_from("Google");
  cout << "pages that can be reached from 'Google': "
       << count_pages_that_can_be_reached_from_google << " rate: "
       << (float)count_pages_that_can_be_reached_from_google /
              wiki.titles.size()
       << endl;
  int count_pages_that_can_reach_google =
      wiki.count_pages_that_can_reach("Google");
  cout << "pages that can reach 'Google': " << count_pages_that_can_reach_google
       << " rate: "
       << (float)count_pages_that_can_reach_google / wiki.titles.size() << endl;
  wiki.print_titles_and_values(wiki.find_most_popular_pages());
  return 0;
}
