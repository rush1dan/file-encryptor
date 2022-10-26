#pragma once
#include <windows.h>

class DeShlExtClassFactory : public IClassFactory, IUnknown
{
protected:
	DWORD m_objRefCount;
	~DeShlExtClassFactory();

public:
	DeShlExtClassFactory();

	// Inherited via IUnknown
	ULONG __stdcall AddRef();

	HRESULT __stdcall QueryInterface(REFIID riid, void** ppvObject);

	ULONG __stdcall Release(void);


	// Inherited via IClassFactory
	HRESULT __stdcall CreateInstance(IUnknown* pUnkOuter, REFIID riid, void** ppvObject);

	HRESULT __stdcall LockServer(BOOL fLock);
};
