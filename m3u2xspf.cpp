#include <iostream>
#include <fstream>
#include <string>

#define HEADER "<?xml version=\"1.0\"?><playlist xmlns=\"http://xspf.org/ns/0/\" version=\"1\"><trackList>"
#define FOOTER "</trackList></playlist>"
#define THEAD "<track><location>"
#define TFOOT "</location></track>"

int convert(std::ifstream &m3u_file, std::ofstream &xspf_file);
std::string putEscapeCharacters(std::string input);

int main(int argc, char **argv) {
    if (argc != 3) {
        std::cout << "Usage: m3u2xspf <input_file> <output_file>" << std::endl;
        return 0;
    }
    std::ofstream output_file;
    std::ifstream input_file;
    input_file.open(argv[1]);
    if (!input_file.is_open()) {
        perror("Unable to open input file");
        return -1;
    }
    output_file.open(argv[2]);
    if (!output_file.is_open()) {
        perror("Unable to open output file");
        return -1;
    }
    convert(input_file, output_file);
    input_file.close();
    output_file.close();
    return 0;
}

int convert(std::ifstream &m3u_file, std::ofstream &xspf_file) {
    std::string line;
    int count = 0;
    xspf_file << HEADER;
    while (getline(m3u_file, line)) {
        line = putEscapeCharacters(line);
        xspf_file << THEAD;
        xspf_file << line;
        xspf_file << TFOOT;
        count++;
    }
    xspf_file << FOOTER;
    return count;
}

std::string putEscapeCharacters(std::string input) {
    std::string result;
    for (char c : input) {
        switch (c) {
        case '&':
            result += "&amp;";
            break;
        case '<':
            result += "&lt;";
            break;
        case '>':
            result += "&gt;";
            break;
        case '\"':
            result += "&quot;";
            break;
        case '\'':
            result += "&apos;";
            break;
        case 13:
            break;
        default:
            result += c;
            break;
        }
    }
    return result;
}