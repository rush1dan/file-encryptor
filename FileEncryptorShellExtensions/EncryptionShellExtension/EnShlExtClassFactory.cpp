#include "EnShlExtClassFactory.h"

extern UINT g_classObjCount;

EnShlExtClassFactory::~EnShlExtClassFactory()
{
    InterlockedDecrement(&g_classObjCount);
}

EnShlExtClassFactory::EnShlExtClassFactory() : m_objRefCount(1)
{
    InterlockedIncrement(&g_classObjCount);
}

ULONG __stdcall EnShlExtClassFactory::AddRef()
{
    return InterlockedIncrement(&m_objRefCount);
}

HRESULT __stdcall EnShlExtClassFactory::QueryInterface(REFIID riid, void** ppvObject)
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
    else if (IsEqualIID(riid, IID_IClassFactory))
    {
        *ppvObject = (IClassFactory*)this;
        this->AddRef();
        return S_OK;
    }
    else
    {
        return E_NOINTERFACE;
    }
}

ULONG __stdcall EnShlExtClassFactory::Release()
{
    ULONG returnValue = InterlockedDecrement(&m_objRefCount);
    if (returnValue < 1)
    {
        delete this;
    }
    return returnValue;
}

HRESULT __stdcall EnShlExtClassFactory::CreateInstance(IUnknown* pUnkOuter, REFIID riid, void** ppvObject)
{
    if (!ppvObject)
        return E_INVALIDARG;

    if (pUnkOuter != NULL)
        return CLASS_E_NOAGGREGATION;

    return E_NOTIMPL;
}

HRESULT __stdcall EnShlExtClassFactory::LockServer(BOOL fLock)
{
    return S_OK;
}
