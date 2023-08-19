#include <iostream>
#include <fstream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>
#include <set>
#include <cfloat>
#include <sstream>
#include <random>
using namespace std;

vector<vector<float>> make_dist_table_from_input_file(string filename) {
  // open the input csv file
  ifstream fin(filename);
  // store the data into vectors
  // read from the 2nd line
  vector<float> x;
  vector<float> y;
  float a, b;
  string str;
  getline(fin, str);
  while (getline(fin, str)) {
    stringstream ss(str);
    ss >> a;
    ss.ignore();
    ss >> b;
    x.push_back(a);
    y.push_back(b);
  }
  // calculate the distance matrix
  vector<vector<float>> dist(x.size(), vector<float>(x.size(), 0));
  for (int i = 0; i < x.size(); i++) {
    for (int j = 0; j < x.size(); j++) {
      dist[i][j] = sqrt(pow(x[i] - x[j], 2) + pow(y[i] - y[j], 2));
    }
  }
  return dist;
}

// calculate the total distance of the path
float calc_path_dist(vector<int> path, vector<vector<float>> dist_table) {
  float dist = 0;
  for (int i = 0; i < path.size() - 1; i++) {
    dist += dist_table[path[i]][path[i + 1]];
  }
  dist += dist_table[path[path.size() - 1]][path[0]];
  return dist;
}

vector<int> solve_greedy(vector<vector<float>> dist_table) {
  // select the starting point randomly
  random_device rnd;
  int current_city = rnd() % dist_table.size();
  // make the set of unvisited cities
  set<int> unvisited_cities;
  for (int i = 0; i < dist_table.size(); i++) {
    unvisited_cities.insert(i);
  }
  unvisited_cities.erase(current_city);
  vector<int> path;
  path.push_back(current_city);
  // select the next city greedily
  for (int i = 0; i < dist_table.size() - 1; i++) {
    float min_dist = FLT_MAX;
    int next_city = -1;
    for (auto itr = unvisited_cities.begin(); itr != unvisited_cities.end(); itr++) {
      if (dist_table[current_city][*itr] < min_dist) {
        min_dist = dist_table[current_city][*itr];
        next_city = *itr;
      }
    }
    path.push_back(next_city);
    unvisited_cities.erase(next_city);
    current_city = next_city;
  }
  return path;
}

// reverse the path between i and j if it improves the total distance
float reverse_path_2opt(vector<int> &path, vector<vector<float>> dist_table, int i, int j) {
  int n = path.size();
  int a = path[i - 1];
  int b = path[i];
  int c = path[(j - 1) % n];
  int d = path[j % n];
  float now = dist_table[a][b] + dist_table[c][d];
  float rev = dist_table[a][c] + dist_table[b][d];
  if (now > rev) {
    reverse(path.begin() + i, path.begin() + j);
    return rev - now;
  }
  return 0;
}

// create all possible segments
vector<pair<int, int>> all_segments(int n) {
  vector<pair<int, int>> segments;
  for (int i = 0; i < n; i++) {
    for (int j = i + 2; j < n + (i > 0); j++) {
      segments.push_back(make_pair(i, j));
    }
  }
  return segments;
}

vector<int> two_opt(vector<int> path, vector<vector<float>> dist_table) {
  // create all possible segments
  vector<pair<int, int>> segments = all_segments(path.size());
  // repeat until no improvement is made
  while (true) {
    float delta = 0;
    for (int i = 0; i < segments.size(); i++) {
      delta += reverse_path_2opt(path, dist_table, segments[i].first, segments[i].second);
    }
    if (delta >= 0) {
      break;
    }
  }
  return path;
}

void print_path(vector<int> path) {
  cout << "index" << endl;
  for (int i = 0; i < path.size(); i++) {
    cout << path[i] << endl;
  }
}

int main(int argc, char *argv[1]) {
  if (argc != 2) {
    cout << "Usage: " << argv[0] << " <input_file>" << endl;
    return 1;
  }
  // read the input file and make the distance table
  string filename = argv[1];
  vector<vector<float>> dist_table = make_dist_table_from_input_file(filename);
  vector<int> path = {};
  vector<int> best_path = {};
  float best_dist = FLT_MAX;
  int trial = 100;
  for (int i = 0; i < trial; i++) {
    cerr << "trial: " << i << endl;
    // solve the problem by greedy algorithm
    path = solve_greedy(dist_table);
    // improve the solution by 2-opt
    path = two_opt(path, dist_table);
    // calculate the total distance of the path
    float dist = calc_path_dist(path, dist_table);
    // update the best path
    if (dist < best_dist) {
      best_dist = dist;
      best_path = path;
    }
  }
  // output the best path
  print_path(best_path);
  return 0;
}
