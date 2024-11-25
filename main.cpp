#include <string>
#include <iostream>
#include <filesystem>
#include <fstream>
#include <map>
#include <vector>
#include <algorithm>
#include <locale>
#include <codecvt>
#include <iomanip>

using namespace std;
namespace fs = std::filesystem;

const std::u32string TURKISH_ALPHABET = U"abcçdefgğhıijklmnoöprsştuüvyz";

char32_t to_lower_turkish(char32_t ch)
{
  static const map<char32_t, char32_t> turkish_lower_map = {
      {U'A', U'a'}, {U'B', U'b'}, {U'C', U'c'}, {U'Ç', U'ç'}, {U'D', U'd'}, {U'E', U'e'}, {U'F', U'f'}, {U'G', U'g'}, {U'Ğ', U'ğ'}, {U'H', U'h'}, {U'I', U'ı'}, {U'İ', U'i'}, {U'J', U'j'}, {U'K', U'k'}, {U'L', U'l'}, {U'M', U'm'}, {U'N', U'n'}, {U'O', U'o'}, {U'Ö', U'ö'}, {U'P', U'p'}, {U'R', U'r'}, {U'S', U's'}, {U'Ş', U'ş'}, {U'T', U't'}, {U'U', U'u'}, {U'Ü', U'ü'}, {U'V', U'v'}, {U'Y', U'y'}, {U'Z', U'z'}};

  auto it = turkish_lower_map.find(ch);
  return it != turkish_lower_map.end() ? it->second : ch;
}

bool sortByVal(const pair<char32_t, pair<int, double>> &a, const pair<char32_t, pair<int, double>> &b)
{
  return (a.second.second > b.second.second);
}

vector<pair<char32_t, pair<int, double>>> analyze_letter_frequency(const string &directory_path)
{
  map<char32_t, int> letter_map;
  long double total_letters = 0;

  for (const auto &entry : fs::directory_iterator(directory_path))
  {
    ifstream file(entry.path(), ios::binary);
    if (!file.is_open())
    {
      cerr << "Dosya açılamadı: " << entry.path() << endl;
      continue;
    }

    string file_contents((istreambuf_iterator<char>(file)), istreambuf_iterator<char>());
    file.close();

    wstring_convert<codecvt_utf8<char32_t>, char32_t> converter;
    u32string utf32_text = converter.from_bytes(file_contents);

    for (char32_t ch : utf32_text)
    {
      ch = to_lower_turkish(ch);
      if (TURKISH_ALPHABET.find(ch) == u32string::npos)
        continue;

      total_letters += 1;
      letter_map[ch]++;
    }
  }

  vector<pair<char32_t, pair<int, double>>> frequencies;
  for (const auto &pair : letter_map)
  {
    frequencies.emplace_back(pair.first, make_pair(pair.second, pair.second / total_letters));
  }

  sort(frequencies.begin(), frequencies.end(), sortByVal);

  return frequencies;
}

void save_to_file(const vector<pair<char32_t, pair<int, double>>> &frequencies)
{
  string output_path = "./letter_freq.txt";
  ofstream output_file(output_path);
  if (!output_file.is_open())
  {
    cerr << "Çıkış dosyası açılamadı: " << output_path << endl;
    return;
  }

  wstring_convert<codecvt_utf8<char32_t>, char32_t> converter;

  output_file << "Letter Count Ratio\n";

  cout << "Harf frekansları:\n";
  for (const auto &pair : frequencies)
  {
    string ch_str = converter.to_bytes(pair.first);
    cout << ch_str << " " << pair.second.first << " " << fixed << setprecision(5) << pair.second.second << endl;
    output_file << ch_str << " " << pair.second.first << " " << fixed << setprecision(5) << pair.second.second << endl;
  }
  output_file.close();
}

int main()
{
  string directory_path = "texts/turkish";

  vector<pair<char32_t, pair<int, double>>> frequencies = analyze_letter_frequency(directory_path);
  save_to_file(frequencies);

  return 0;
}
