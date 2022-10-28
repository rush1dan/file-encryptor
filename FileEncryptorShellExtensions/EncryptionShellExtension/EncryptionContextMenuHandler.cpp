#include "EncryptionContextMenuHandler.h"
#include <Windows.h>
#include <string>
#include <atlconv.h>
#include <Shlwapi.h>

EncryptionContextMenuHandler::~EncryptionContextMenuHandler()
{
    InterlockedDecrement(&g_classObjCount);
}

EncryptionContextMenuHandler::EncryptionContextMenuHandler() : m_objRefCount(1)
{
    m_pidlFolder = NULL;
    m_fileCount = 0;
    m_pDataObj = NULL;
    m_hRegKey = NULL;
    InterlockedIncrement(&g_classObjCount);
}

HRESULT __stdcall EncryptionContextMenuHandler::QueryInterface(REFIID riid, void** ppvObject)
{
    if (!ppvObject)
        return E_POINTER;
    *ppvObject = NULL;

    if (IsEqualIID(riid, IID_IUnknown))
    {
        *ppvObject = this;
        this->AddRef();
        return S_OK;
    }
    else if (IsEqualIID(riid, IID_IContextMenu))
    {
        *ppvObject = (IContextMenu*)this;
        this->AddRef();
        return S_OK;
    }
    else if (IsEqualIID(riid, IID_IShellExtInit))
    {
        *ppvObject = (IShellExtInit*)this;
        this->AddRef();
        return S_OK;
    }
    else
    {
        return E_NOINTERFACE;
    }
}

ULONG __stdcall EncryptionContextMenuHandler::AddRef()
{
    return InterlockedIncrement(&m_objRefCount);
}

ULONG __stdcall EncryptionContextMenuHandler::Release(void)
{
    ULONG returnValue = InterlockedDecrement(&m_objRefCount);
    if (returnValue < 1)
    {
        delete this;
    }
    return returnValue;
}

HRESULT __stdcall EncryptionContextMenuHandler::Initialize(PCIDLIST_ABSOLUTE pidlFolder, IDataObject* pdtobj, HKEY hkeyProgID)
{
    // If Initialize has already been called, release the old PIDL
    ILFree(m_pidlFolder);
    m_pidlFolder = nullptr;

    // Store the new PIDL.
    if (pidlFolder)
    {
        m_pidlFolder = ILClone(pidlFolder);
    }

    // If Initialize has already been called, release the old
    // IDataObject pointer.
    if (m_pDataObj)
    {
        m_pDataObj->Release();
    }

    // If a data object pointer was passed in, save it and
    // extract the file name. 
    if (pdtobj)
    {
        m_pDataObj = pdtobj;
        pdtobj->AddRef();

        STGMEDIUM   medium;
        FORMATETC   fe = { CF_HDROP, NULL, DVASPECT_CONTENT, -1, TYMED_HGLOBAL };

        if (SUCCEEDED(m_pDataObj->GetData(&fe, &medium)))
        {
            // Get the count of files dropped.
            m_fileCount = DragQueryFile((HDROP)medium.hGlobal, (UINT)-1, NULL, 0);

            // Get the file names from the CF_HDROP.
            if (m_fileCount)
            {
                for (int i = 0; i < m_fileCount; i++)
                {
                    wchar_t	sz_File[MAX_PATH];
                    DragQueryFile((HDROP)medium.hGlobal, i, sz_File,
                        sizeof(sz_File) / sizeof(TCHAR));

                    //Don't show encryption context menu item for .exe or .enc files
                    std::wstring exeExtension = L".exe";
                    std::wstring encExtension = L".enc";
                    if (exeExtension.compare(PathFindExtensionW(sz_File)) == 0 || encExtension.compare(PathFindExtensionW(sz_File)) == 0)
                    {
                        ReleaseStgMedium(&medium);
                        m_szFiles.clear();
                        return E_NOTIMPL;
                    }

                    m_szFiles.push_back(std::wstring(sz_File));
                }
            }

            ReleaseStgMedium(&medium);
        }
    }

    // Duplicate the registry handle. 
    if (hkeyProgID)
        RegOpenKeyEx(hkeyProgID, nullptr, 0L, MAXIMUM_ALLOWED, &m_hRegKey);
    return S_OK;
}

HRESULT __stdcall EncryptionContextMenuHandler::QueryContextMenu(HMENU hmenu, UINT indexMenu, UINT idCmdFirst, UINT idCmdLast, UINT uFlags)
{
    //MessageBox(NULL, L"Shell Extension Menu", L"QueryContextMenu()", MB_OK);

    if (uFlags & CMF_DEFAULTONLY)
        return MAKE_HRESULT(SEVERITY_SUCCESS, FACILITY_NULL, 0);

    MENUITEMINFO myItem = {};
    myItem.cbSize = sizeof(MENUITEMINFO);
    myItem.fMask = MIIM_STRING | MIIM_ID;
    myItem.wID = idCmdFirst;

    LPCSTR itemTypeDataStr = "Encrypt File(s)";
    USES_CONVERSION;
    LPWSTR itemTypeData = A2W(itemTypeDataStr);
    myItem.dwTypeData = itemTypeData;

    if (!InsertMenuItem(hmenu, 0, TRUE, &myItem))
    {
        return HRESULT_FROM_WIN32(GetLastError());
    }

    return MAKE_HRESULT(SEVERITY_SUCCESS, 0, myItem.wID - idCmdFirst + 1);
}

HRESULT __stdcall EncryptionContextMenuHandler::InvokeCommand(CMINVOKECOMMANDINFO* pici)
{
    std::wstring executablePath = L"C:\\PythonProjects\\FileEnDecryptor\\dist\\main.exe";
    std::wstring operationMode = L"--encrypt";
    std::wstring argString = operationMode;

    for (int i = 0; i < m_fileCount; i++)
    {
        //MessageBox(NULL, m_szFiles[i].c_str(), L"InvokeCommand()", MB_OK);
        argString += L" " + m_szFiles[i];
    }
    //MessageBoxA(NULL, argString.c_str(), "Result", MB_OK);

    STARTUPINFO si;
    PROCESS_INFORMATION pi;
    // set the size of the structures
    ZeroMemory(&si, sizeof(si));
    si.cb = sizeof(si);
    ZeroMemory(&pi, sizeof(pi));
    LPWSTR arg = _wcsdup(argString.c_str());
    BOOL processCreated = CreateProcess(executablePath.c_str(), arg, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    if (!processCreated)
    {
        std::string message = "Encryption Application Failed to Start Due to:\nError Code " + std::to_string(GetLastError());
        MessageBoxA(NULL, message.c_str(), "Result", MB_ICONERROR | MB_OK);
    }
    // Wait until child process exits.
    WaitForSingleObject(pi.hProcess, INFINITE);

    // Close process and thread handles. 
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    free(arg);

    return S_OK;
}

HRESULT __stdcall EncryptionContextMenuHandler::GetCommandString(UINT_PTR idCmd, UINT uType, UINT* pReserved, CHAR* pszName, UINT cchMax)
{
    return S_OK;
}
