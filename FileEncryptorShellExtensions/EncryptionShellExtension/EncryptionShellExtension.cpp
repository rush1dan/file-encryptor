#include <Windows.h>


BOOL __stdcall DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
{
	return true;
}

HRESULT __stdcall DllCanUnloadNow()
{
	return E_NOTIMPL;
}

HRESULT __stdcall DllGetClassObject(REFCLSID rclsid, REFIID riid, LPVOID* ppv)
{
	return E_NOTIMPL;
}

HRESULT __stdcall DllRegisterServer()
{
	return E_NOTIMPL;
}

HRESULT __stdcall DllUnregisterServer()
{
	return E_NOTIMPL;
}