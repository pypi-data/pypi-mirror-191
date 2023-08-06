#include "stdafx.h"
#include "LFile.h"


bool LFile::openRead(const char* filename) {
    std::ifstream st(filename, std::ifstream::binary | std::ifstream::in);
    if (!st) return false;
    istream << st.rdbuf();
    m_size = st.tellg();
    return true;
}
