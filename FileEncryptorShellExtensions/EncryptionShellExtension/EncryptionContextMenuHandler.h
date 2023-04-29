#pragma once
#include <ShlObj.h>
#include <ShObjIdl_core.h>
#include <vector>
#include <string>

extern UINT g_classObjCount;
extern HINSTANCE g_hInstance;

class EncryptionContextMenuHandler : public IShellExtInit, IContextMenu, IUnknown
{
private:
	LPITEMIDLIST					m_pidlFolder;			//The folder's PIDL (In case of right clicking directory background i.e. empty space)
	std::vector<std::wstring>		m_szFiles;				//The file paths
	std::vector<std::wstring>		m_szFolders;			//The folder paths
	IDataObject*					m_pDataObj;				//The IDataObject pointer
	HKEY							m_hRegKey;				//The file or folder's registry key
	BOOL							m_folderOperation;		//Folder operation overrides file operation

protected:
	DWORD m_objRefCount;
	~EncryptionContextMenuHandler();

public:
	EncryptionContextMenuHandler();

	// Inherited via IUnknown
	HRESULT __stdcall QueryInterface(REFIID riid, void** ppvObject);

	ULONG __stdcall AddRef();

	ULONG __stdcall Release();


	// Inherited via IShellExtInit
	HRESULT __stdcall Initialize(PCIDLIST_ABSOLUTE pidlFolder, IDataObject* pdtobj, HKEY hkeyProgID);


	// Inherited via IContextMenu
	HRESULT __stdcall QueryContextMenu(HMENU hmenu, UINT indexMenu, UINT idCmdFirst, UINT idCmdLast, UINT uFlags);

	HRESULT __stdcall InvokeCommand(CMINVOKECOMMANDINFO* pici);

	HRESULT __stdcall GetCommandString(UINT_PTR idCmd, UINT uType, UINT* pReserved, CHAR* pszName, UINT cchMax);
};