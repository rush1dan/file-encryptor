#include "EncryptionContextMenuHandler.h"
#include <Windows.h>
#include <string>
#include <atlconv.h>
#include <Shlwapi.h>
#include "IconBitmapUtils.h"
#include "customutils.h"

EncryptionContextMenuHandler::~EncryptionContextMenuHandler()
{
    InterlockedDecrement(&g_classObjCount);
}

EncryptionContextMenuHandler::EncryptionContextMenuHandler() : m_objRefCount(1)
{
    m_pidlFolder = NULL;
    m_folderOperation = FALSE;
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
            // Get the count of files or folders dropped.
            UINT fileorfolderCount = DragQueryFile((HDROP)medium.hGlobal, (UINT)-1, NULL, 0);

            // Get the file names from the CF_HDROP.
            if (fileorfolderCount)
            {
                for (int i = 0; i < fileorfolderCount; i++)
                {
                    wchar_t	sz_File_or_Folder[MAX_PATH];
                    DragQueryFile((HDROP)medium.hGlobal, i, sz_File_or_Folder,
                        sizeof(sz_File_or_Folder) / sizeof(TCHAR));

                    std::wstring doubleQuotationWrappedItemName = sz_File_or_Folder;    //For handling space(s) and hyphen(s)s in item name
                    doubleQuotationWrappedItemName = L"\"" + doubleQuotationWrappedItemName + L"\"";

                    if (PathIsDirectory(sz_File_or_Folder))     //If selected object is a folder; add to list and skip over file addition
                    {
                        m_szFolders.push_back(doubleQuotationWrappedItemName);
                        m_folderOperation = TRUE;
                    }

                    if (!m_folderOperation)
                    {
                        ////Don't show encryption context menu item for .enc files
                        //std::wstring encExtension = L".enc";
                        //if (encExtension.compare(PathFindExtension(sz_File_or_Folder)) == 0)
                        //{
                        //    ReleaseStgMedium(&medium);
                        //    m_szFiles.clear();
                        //    return E_NOTIMPL;
                        //}

                        m_szFiles.push_back(doubleQuotationWrappedItemName);
                    }
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

    if (!(uFlags & CMF_RESERVED))
        return MAKE_HRESULT(SEVERITY_SUCCESS, FACILITY_NULL, 0);

    MENUITEMINFO myItem = {};
    myItem.cbSize = sizeof(MENUITEMINFO);
    myItem.fMask = MIIM_STRING | MIIM_ID | MIIM_FTYPE | MIIM_BITMAP;
    myItem.fType = MFT_STRING;
    myItem.wID = idCmdFirst;
    std::string base64Icon = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAACXBIWXMAAAB2AAAAdgFOeyYIAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAAeFJREFUOI2Nkz9oU1EUxn/v5iavCbwoJW3aqqSgDl0Uo2ihjg6CQ0fBJeAgxVXoEhwUUbrp5CAiBBcdXHRrcJQ0LkUNpCpKJMSm1ca8mLwk759DTEr6XiAHDtxzz/k+znfOvYqu6yYg8bFabY87t29st1tdreuoE1IxO83G7seNzW/LOzvNKoDwA/bB6dXrBNTETEBOhMOB5p4QQs4kFi9cXDy9FYtFZgEUXdfNcrksi8XiEMHrV4+R4Xnsdpm7D56gadqLVCq10v279W5ufmlhu5TffLP+4czIDmzLxWiUubf2lGg0iqIoVzOZzPNT55aXWvWv7Uh0emGkBMuy6NoSNWiTy+XIZrMUCgWAK+l0+ohwWlUR0ELA1EgC11VA8e/OxTEVIQDUkRLGNd8hVj8/Q3SLCCGJTUYAkDJAKBTCaP4s1erO4Y4ptd+/6hnf/Z+Y/s6l88H/kXEgqyb6p7cb4ctjSbh53+HsNYtbD1WPgrEI8gUbvd4i/8n25AT0pm4YxsDBHSo6frQXnzzmJR90IIQY+MH9zU314tmY4yGQAI1Gg0qlMricPGQPkTiORTAU9H0XEiAej5NMJvcBJQns6320Gu5nPASK33def7mCJoqeYgCz82fXdU0L4MsP8/0/LGHD/XRylokAAAAASUVORK5CYII=";
    myItem.hbmpItem = IconBitmapUtils::Base64ToHBITMAP(base64Icon);

    LPCSTR itemTypeDataStr = m_folderOperation ? "Encrypt Folder(s)" : "Encrypt File(s)";      
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
    /*std::wstring executableName = L"main.exe";
    std::wstring executablePath = GetModuleFileDirectory(g_hInstance) + L"\\" + executableName;*/
    std::wstring executablePath = L"C:\\PythonProjects\\FileEnDecryptor\\dist\\main.exe";
    std::wstring operationObject = m_folderOperation ? L"--folder" : L"--file";
    std::wstring operationMode = L"--encrypt";
    std::wstring argString = operationObject + L" " + operationMode;

    if (m_folderOperation)
    {
        int folderCount = m_szFolders.size();

        for (int i = 0; i < folderCount; i++)
        {
            //MessageBox(NULL, m_szFolders[i].c_str(), L"InvokeCommand()", MB_OK);
            argString += L" " + m_szFolders[i];
        }
    }
    else
    {
        int fileCount = m_szFiles.size();

        for (int i = 0; i < fileCount; i++)
        {
            //MessageBox(NULL, m_szFiles[i].c_str(), L"InvokeCommand()", MB_OK);
            argString += L" " + m_szFiles[i];
        }
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
        std::string message = GetLastErrorAsString();
        MessageBoxA(NULL, message.c_str(), "Failed", MB_ICONERROR | MB_OK);
    }

    /* This block of code written according to MS docs causes issues for uknown reasons
    //// Wait until child process exits.
    //WaitForSingleObject(pi.hProcess, INFINITE);
    */

    // Close process and thread handles. 
    CloseHandle(pi.hProcess);
    CloseHandle(pi.hThread);
    free(arg);

    return S_OK;
}

HRESULT __stdcall EncryptionContextMenuHandler::GetCommandString(UINT_PTR idCmd, UINT uType, UINT* pReserved, CHAR* pszName, UINT cchMax)
{
    //Gets information about a shortcut menu command, including the help string and the language-independent, or canonical, name for the command.
    //Not necessary yet.
    return S_OK;
}
