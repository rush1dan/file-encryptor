#include "customutils.h"
#include <system_error>

std::wstring GetModuleFileDirectory(HINSTANCE hinstDLL)
{
    wchar_t buffer[MAX_PATH];
    GetModuleFileName(hinstDLL, buffer, MAX_PATH);
    PathRemoveFileSpec(buffer);
    return std::wstring(buffer);
}

//Returns the last Win32 error, in string format. Returns an empty string if there is no error.
std::string GetLastErrorAsString()
{
    //Get the error message ID, if any.
    DWORD errorMessageID = ::GetLastError();
    if (errorMessageID == 0) {
        return std::string(); //No error message has been recorded
    }

    std::string message = std::system_category().message(errorMessageID);

    return message;
}