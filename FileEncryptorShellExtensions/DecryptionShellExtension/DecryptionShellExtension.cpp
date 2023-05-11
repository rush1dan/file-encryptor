#include <Windows.h>
#include "DecryptionShlExtGUID.h";
#include <string>
#include <ShlObj.h>
#include "DeShlExtClassFactory.h"
#include "DecryptionContextMenuHandler.h"

HINSTANCE g_hInstance;
const std::wstring DLL_REG_NAME = L"EzDecryptor";

UINT g_classObjCount;


BOOL __stdcall DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	switch (fdwReason)
	{
	case DLL_PROCESS_ATTACH:
		g_hInstance = hinstDLL;
		return true;
	default:
		break;
	}

	return true;
}

HRESULT __stdcall DllCanUnloadNow()
{
	return g_classObjCount > 0 ? S_FALSE : S_OK;
}

HRESULT __stdcall DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID* ppv)
{
	if (!IsEqualCLSID(rclsid, CLSID_DecryptionShlExt))
		return CLASS_E_CLASSNOTAVAILABLE;
	if (!ppv)
		return E_INVALIDARG;

	*ppv = NULL;

	HRESULT hr = E_UNEXPECTED;
	DeShlExtClassFactory* pShellExtClassFactory = new DeShlExtClassFactory();
	if (pShellExtClassFactory != NULL)
	{
		hr = pShellExtClassFactory->QueryInterface(riid, ppv);
		/*if (hr == S_OK)
		{
			MessageBox(NULL, L"Class Object", L"DllGetClassObject()", MB_OK);
		}*/
		pShellExtClassFactory->Release();
	}

	return hr;
}

std::wstring WStringFromCLSID(IID iid)
{
	wchar_t* tempString;
	StringFromCLSID(iid, &tempString);
	return std::wstring(tempString);
}

std::wstring ModuleFilePath()
{
	wchar_t buffer[MAX_PATH];
	GetModuleFileName(g_hInstance, buffer, MAX_PATH);
	return std::wstring(buffer);
}

DWORD SizeOfWStringInBytes(std::wstring target)
{
	DWORD size = (target.size() + 1) * 2;	//2 bytes for each wchar with addition \0 wchar at the end
	return size;
}

//Terminal(Powershell/Cmd) command as adminstrator: regsvr32 DecryptionShellExtension.dll
HRESULT __stdcall DllRegisterServer()
{
	HKEY hkey;
	DWORD lpDisp;

	//----------------Create keys for file operation----------------

	//Create GUID key:
	std::wstring lpSubKey = L"SOFTWARE\\Classes\\CLSID\\" + WStringFromCLSID(CLSID_DecryptionShlExt);
	LONG result = RegCreateKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hkey, &lpDisp);
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	//Create InprocServer32 key:
	result = RegCreateKeyEx(hkey, L"InprocServer32", 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hkey, &lpDisp);
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	//Set (default) value:
	std::wstring lpDllPath = ModuleFilePath();
	result = RegSetValueEx(hkey, NULL, 0, REG_SZ, (BYTE*)lpDllPath.c_str(), SizeOfWStringInBytes(lpDllPath));
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	//Create Threading Model:
	std::wstring apartment = L"Apartment";
	result = RegSetValueEx(hkey, L"ThreadingModel", 0, REG_SZ, (BYTE*)apartment.c_str(), SizeOfWStringInBytes(apartment));
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	RegCloseKey(hkey);

	//Put on approved list:
	lpSubKey = L"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Shell Extensions\\Approved";
	result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegSetValueEx(hkey, WStringFromCLSID(CLSID_DecryptionShlExt).c_str(), 0, REG_SZ, (BYTE*)DLL_REG_NAME.c_str(),
			SizeOfWStringInBytes(DLL_REG_NAME));
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}
	RegCloseKey(hkey);


	//Create Handler Key for all file types(*):
	lpSubKey = L"SOFTWARE\\Classes\\*\\shellex\\ContextMenuHandlers\\" + DLL_REG_NAME;
	result = RegCreateKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hkey, &lpDisp);
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	//Set handler key (default) value:
	result = RegSetValueEx(hkey, NULL, 0, REG_SZ, (BYTE*)WStringFromCLSID(CLSID_DecryptionShlExt).c_str(),
		SizeOfWStringInBytes(WStringFromCLSID(CLSID_DecryptionShlExt)));
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	RegCloseKey(hkey);


	//----------------Create Keys for folder operation----------------

	//Create Handler Key:
	lpSubKey = L"SOFTWARE\\Classes\\Directory\\shellex\\ContextMenuHandlers\\" + DLL_REG_NAME;
	result = RegCreateKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, NULL, REG_OPTION_NON_VOLATILE, KEY_WRITE, NULL, &hkey, &lpDisp);
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	//Set handler key (default) value:
	result = RegSetValueEx(hkey, NULL, 0, REG_SZ, (BYTE*)WStringFromCLSID(CLSID_DecryptionShlExt).c_str(),
		SizeOfWStringInBytes(WStringFromCLSID(CLSID_DecryptionShlExt)));
	if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }

	RegCloseKey(hkey);

	//Alert that there has been a change:
	SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, NULL, NULL);

	return S_OK;
}

//Terminal(Powershell/Cmd) command as adminstrator: regsvr32 /u DecryptionShellExtension.dll
HRESULT __stdcall DllUnregisterServer()
{
	HKEY hkey;

	//----------------Delete keys for file operation----------------

	//Check if InprocServer32 key exists and if it does delete it
	std::wstring lpSubKey = L"SOFTWARE\\Classes\\CLSID\\" + WStringFromCLSID(CLSID_DecryptionShlExt) + L"\\InprocServer32";
	LONG result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegDeleteKey(HKEY_LOCAL_MACHINE, lpSubKey.c_str());
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}

	//Check if GUID key exists and if it does delete it
	lpSubKey = L"SOFTWARE\\Classes\\CLSID\\" + WStringFromCLSID(CLSID_DecryptionShlExt);
	result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegDeleteKey(HKEY_LOCAL_MACHINE, lpSubKey.c_str());
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}
	RegCloseKey(hkey);

	//Delete Value from approved list:
	lpSubKey = L"SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Shell Extensions\\Approved";
	result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegDeleteValue(hkey, WStringFromCLSID(CLSID_DecryptionShlExt).c_str());
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}
	RegCloseKey(hkey);


	//Delete handler key:
	lpSubKey = L"SOFTWARE\\Classes\\*\\shellex\\ContextMenuHandlers\\" + DLL_REG_NAME;
	result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegDeleteKey(HKEY_LOCAL_MACHINE, lpSubKey.c_str());
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}
	RegCloseKey(hkey);


	//----------------Delete keys for folder operation----------------

	//Delete handler key:
	lpSubKey = L"SOFTWARE\\Classes\\Directory\\shellex\\ContextMenuHandlers\\" + DLL_REG_NAME;
	result = RegOpenKeyEx(HKEY_LOCAL_MACHINE, lpSubKey.c_str(), 0, KEY_ALL_ACCESS, &hkey);
	if (result == ERROR_SUCCESS)
	{
		result = RegDeleteKey(HKEY_LOCAL_MACHINE, lpSubKey.c_str());
		if (result != ERROR_SUCCESS) { return E_UNEXPECTED; }
	}
	RegCloseKey(hkey);

	//Alert that there has been a change:
	SHChangeNotify(SHCNE_ASSOCCHANGED, SHCNF_IDLIST, NULL, NULL);

	return S_OK;
}