#include "DeShlExtClassFactory.h"
#include "DecryptionContextMenuHandler.h"

extern UINT g_classObjCount;

DeShlExtClassFactory::~DeShlExtClassFactory()
{
    InterlockedDecrement(&g_classObjCount);
}

DeShlExtClassFactory::DeShlExtClassFactory() : m_objRefCount(1)
{
    InterlockedIncrement(&g_classObjCount);
}

ULONG __stdcall DeShlExtClassFactory::AddRef()
{
    return InterlockedIncrement(&m_objRefCount);
}

HRESULT __stdcall DeShlExtClassFactory::QueryInterface(REFIID riid, void** ppvObject)
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

ULONG __stdcall DeShlExtClassFactory::Release()
{
    ULONG returnValue = InterlockedDecrement(&m_objRefCount);
    if (returnValue < 1)
    {
        delete this;
    }
    return returnValue;
}

HRESULT __stdcall DeShlExtClassFactory::CreateInstance(IUnknown* pUnkOuter, REFIID riid, void** ppvObject)
{
    if (!ppvObject)
        return E_INVALIDARG;

    if (pUnkOuter != NULL)
        return CLASS_E_NOAGGREGATION;

    HRESULT hr;
    if (IsEqualIID(riid, IID_IShellExtInit) || IsEqualIID(riid, IID_IContextMenu))
    {
        DecryptionContextMenuHandler* pDecryptionContextMenuHandler = new DecryptionContextMenuHandler();
        if (pDecryptionContextMenuHandler == NULL)
            return E_OUTOFMEMORY;

        hr = pDecryptionContextMenuHandler->QueryInterface(riid, ppvObject);
        //if (hr == S_OK)
        //{
        //    MessageBox(NULL, L"Context Menu Object", L"CreateInstance()", MB_OK);
        //}
        pDecryptionContextMenuHandler->Release();
    }
    else
    {
        return E_NOINTERFACE;
    }

    return hr;
}

HRESULT __stdcall DeShlExtClassFactory::LockServer(BOOL fLock)
{
    return S_OK;
}
