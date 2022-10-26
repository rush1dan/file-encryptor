#include "DecryptionContextMenuHandler.h"
#include <Windows.h>
#include <string>
#include <atlconv.h>
#include <Shlwapi.h>

DecryptionContextMenuHandler::~DecryptionContextMenuHandler()
{
    InterlockedDecrement(&g_classObjCount);
}

DecryptionContextMenuHandler::DecryptionContextMenuHandler() : m_objRefCount(1)
{
    m_pidlFolder = NULL;
    m_fileCount = 0;
    m_pDataObj = NULL;
    m_hRegKey = NULL;
    InterlockedIncrement(&g_classObjCount);
}

HRESULT __stdcall DecryptionContextMenuHandler::QueryInterface(REFIID riid, void** ppvObject)
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

ULONG __stdcall DecryptionContextMenuHandler::AddRef()
{
    return InterlockedIncrement(&m_objRefCount);
}

ULONG __stdcall DecryptionContextMenuHandler::Release(void)
{
    ULONG returnValue = InterlockedDecrement(&m_objRefCount);
    if (returnValue < 1)
    {
        delete this;
    }
    return returnValue;
}

HRESULT __stdcall DecryptionContextMenuHandler::Initialize(PCIDLIST_ABSOLUTE pidlFolder, IDataObject* pdtobj, HKEY hkeyProgID)
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

                    //Show Decryption context menu item for only for .enc files
                    std::wstring encExtension = L".enc";
                    if (encExtension.compare(PathFindExtensionW(sz_File)) != 0)
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

HRESULT __stdcall DecryptionContextMenuHandler::QueryContextMenu(HMENU hmenu, UINT indexMenu, UINT idCmdFirst, UINT idCmdLast, UINT uFlags)
{
    //MessageBox(NULL, L"Shell Extension Menu", L"QueryContextMenu()", MB_OK);

    if (uFlags & CMF_DEFAULTONLY)
        return MAKE_HRESULT(SEVERITY_SUCCESS, FACILITY_NULL, 0);

    MENUITEMINFO myItem = {};
    myItem.cbSize = sizeof(MENUITEMINFO);
    myItem.fMask = MIIM_STRING | MIIM_ID;
    myItem.wID = idCmdFirst;

    LPCSTR itemTypeDataStr = "Decrypt Files(s)";
    USES_CONVERSION;
    LPWSTR itemTypeData = A2W(itemTypeDataStr);
    myItem.dwTypeData = itemTypeData;

    if (!InsertMenuItem(hmenu, 0, TRUE, &myItem))
    {
        return HRESULT_FROM_WIN32(GetLastError());
    }

    return MAKE_HRESULT(SEVERITY_SUCCESS, 0, myItem.wID - idCmdFirst + 1);
}

HRESULT __stdcall DecryptionContextMenuHandler::InvokeCommand(CMINVOKECOMMANDINFO* pici)
{
    for (int i = 0; i < m_fileCount; i++)
    {
        MessageBox(NULL, m_szFiles[i].c_str(), L"InvokeCommand()", MB_OK);
    }
    return S_OK;
}

HRESULT __stdcall DecryptionContextMenuHandler::GetCommandString(UINT_PTR idCmd, UINT uType, UINT* pReserved, CHAR* pszName, UINT cchMax)
{
    return S_OK;
}
