#include <nlohmann/json.hpp>
#include <iostream>
#include <fstream>
using namespace std;

int main() {
    // nlohmann::json j;
    // j["message"] = "Hello, vcpkg!";
    // std::cout << j.dump(4) << std::endl;
    // return 0;

    ifstream inputFile("test.txt");

    if(!inputFile.is_open()){
        cerr << "Error openning the file!" << endl;
        return 1;
    }

    string line;

    cout << "File content: " << endl;

    while(getline(inputFile, line)){
        cout << line << endl;
    }

    inputFile.close();

    return 0;

}
