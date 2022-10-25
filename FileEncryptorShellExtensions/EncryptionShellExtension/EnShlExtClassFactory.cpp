#include "EnShlExtClassFactory.h"

EnShlExtClassFactory::~EnShlExtClassFactory()
{
}

EnShlExtClassFactory::EnShlExtClassFactory()
{
}

ULONG __stdcall EnShlExtClassFactory::AddRef()
{
    return 0;
}

HRESULT __stdcall EnShlExtClassFactory::QueryInterface(REFIID riid, void** ppvObject)
{
    return E_NOTIMPL;
}

ULONG __stdcall EnShlExtClassFactory::Release(void)
{
    return 0;
}

HRESULT __stdcall EnShlExtClassFactory::CreateInstance(IUnknown* pUnkOuter, REFIID riid, void** ppvObject)
{
    return E_NOTIMPL;
}

HRESULT __stdcall EnShlExtClassFactory::LockServer(BOOL fLock)
{
    return E_NOTIMPL;
}
