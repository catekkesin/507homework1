#include <string>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <cctype>
#include <map>
#include <vector>
#include <algorithm>
#include <iomanip> // For formatting output

using namespace std;
namespace fs = std::filesystem;

bool sortByVal(const pair<char, double> &a,
               const pair<char, double> &b)
{
    return (a.second > b.second);
}

vector<pair<char, pair<int, double>>> analyze_letter_frequency(const std::string &directory_path)
{
    map<char, int> M;
    long double letter_count = 0;

    for (const auto &entry : fs::directory_iterator(directory_path))
    {
        ifstream file(entry.path());

        char ch;

        while (file.get(ch))
        {
            if (!isalpha(ch))
                continue;

            ch = tolower(ch);
            letter_count += 1;

            if (M.find(ch) == M.end())
            {
                M.insert(make_pair(ch, 1));
            }
            else
            {
                M[ch]++;
            }
        }
        file.close();
    }

    vector<pair<char, pair<int, double>>> vec;

    for (auto it = M.begin(); it != M.end(); it++)
    {
        vec.push_back(make_pair(it->first, make_pair(it->second, it->second / letter_count)));
    }

    sort(vec.begin(), vec.end(), [](const pair<char, pair<int, double>> &a, const pair<char, pair<int, double>> &b)
         { return a.second.second > b.second.second; });

    return vec;
}

void save_to_file(vector<pair<char, pair<int, double>>> frequencies)
{
    std::string output_path = "./letter_freq.txt";

    ofstream output_file(output_path);

    cout << "Harf frekansları:" << endl;
    output_file << "Letter Count Ratio\n"; // Header line
    for (const auto &entry : frequencies)
    {
        cout << entry.first << " " << entry.second.first << " " << fixed << setprecision(5) << entry.second.second << endl;
        output_file << entry.first << " " << entry.second.first << " " << fixed << setprecision(5) << entry.second.second << endl;
    }

    output_file.close();
}

int main()
{
    std::string directory_path = "texts/english";

    vector<pair<char, pair<int, double>>> frequencies = analyze_letter_frequency(directory_path);
    save_to_file(frequencies);

    return 0;
}
