#pragma once

#include <Shlwapi.h>
#include <string>

std::wstring GetModuleFileDirectory(HINSTANCE hinstDLL);

std::string GetLastErrorAsString();