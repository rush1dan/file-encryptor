#include "IconBitmapUtils.h"
#include <string>

#pragma comment(lib, "UxTheme.lib")

HBITMAP IconBitmapUtils::IconToBitmapPARGB32(HICON hIcon, int width, int height)
{
	if (!hIcon)
	{
		/*std::wstring errorMsg = L"Error: ";
		errorMsg += std::to_wstring(GetLastError()).c_str();
		MessageBox(NULL, errorMsg.c_str(), L"Icon Not Found", MB_OK | MB_ICONERROR);*/
		return nullptr;
	}

	SIZE sizIcon;
	sizIcon.cx = width;
	sizIcon.cy = height;

	RECT rcIcon;
	SetRect(&rcIcon, 0, 0, sizIcon.cx, sizIcon.cy);

	HDC hdcDest = CreateCompatibleDC(nullptr);
	if (!hdcDest)
		return nullptr;
	//DeleteDC(hdcDest);

	HBITMAP hBmp = nullptr;
	if (FAILED(Create32BitHBITMAP(hdcDest, &sizIcon, nullptr, &hBmp)))
		return nullptr;

	auto hbmpOld = static_cast<HBITMAP>(SelectObject(hdcDest, hBmp));
	if (!hbmpOld)
		return hBmp;

	BLENDFUNCTION bfAlpha = { AC_SRC_OVER, 0, 255, AC_SRC_ALPHA };
	BP_PAINTPARAMS paintParams = { 0 };
	paintParams.cbSize = sizeof(paintParams);
	paintParams.dwFlags = BPPF_ERASE;
	paintParams.pBlendFunction = &bfAlpha;

	HDC hdcBuffer;
	HPAINTBUFFER hPaintBuffer = BeginBufferedPaint(hdcDest, &rcIcon, BPBF_DIB, &paintParams, &hdcBuffer);
	if (hPaintBuffer)
	{
		if (DrawIconEx(hdcBuffer, 0, 0, hIcon, sizIcon.cx, sizIcon.cy, 0, nullptr, DI_NORMAL))
		{
			// If icon did not have an alpha channel we need to convert buffer to PARGB
			ConvertBufferToPARGB32(hPaintBuffer, hdcDest, hIcon, sizIcon);
		}

		// This will write the buffer contents to the destination bitmap
		EndBufferedPaint(hPaintBuffer, TRUE);
	}

	SelectObject(hdcDest, hbmpOld);
	return hBmp;
}

HRESULT IconBitmapUtils::Create32BitHBITMAP(HDC hdc, const SIZE* psize, __deref_opt_out void** ppvBits, __out HBITMAP* phBmp)
{
	if (!psize)
		return E_INVALIDARG;

	if (!phBmp)
		return E_POINTER;

	*phBmp = nullptr;

	BITMAPINFO bmi = { 0 };
	bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmi.bmiHeader.biPlanes = 1;
	bmi.bmiHeader.biCompression = BI_RGB;

	bmi.bmiHeader.biWidth = psize->cx;
	bmi.bmiHeader.biHeight = psize->cy;
	bmi.bmiHeader.biBitCount = 32;

	HDC hdcUsed = hdc ? hdc : GetDC(nullptr);
	if (hdcUsed)
	{
		*phBmp = CreateDIBSection(hdcUsed, &bmi, DIB_RGB_COLORS, ppvBits, nullptr, 0);
		if (hdc != hdcUsed)
		{
			ReleaseDC(nullptr, hdcUsed);
		}
	}
	return (nullptr == *phBmp) ? E_OUTOFMEMORY : S_OK;
}

HRESULT IconBitmapUtils::ConvertBufferToPARGB32(HPAINTBUFFER hPaintBuffer, HDC hdc, HICON hicon, SIZE& sizIcon)
{
	RGBQUAD* prgbQuad;
	int cxRow;
	HRESULT hr = GetBufferedPaintBits(hPaintBuffer, &prgbQuad, &cxRow);
	if (FAILED(hr))
		return hr;

	Gdiplus::ARGB* pargb = reinterpret_cast<Gdiplus::ARGB*>(prgbQuad);
	if (HasAlpha(pargb, sizIcon, cxRow))
		return S_OK;

	ICONINFO info;
	if (!GetIconInfo(hicon, &info))
		return S_OK;
	/*DeleteObject(info.hbmColor);
	DeleteObject(info.hbmMask);*/
	if (info.hbmMask)
		return ConvertToPARGB32(hdc, pargb, info.hbmMask, sizIcon, cxRow);

	return S_OK;
}

bool IconBitmapUtils::HasAlpha(__in Gdiplus::ARGB* pargb, const SIZE& sizImage, int cxRow)
{
	ULONG cxDelta = cxRow - sizImage.cx;
	for (ULONG y = sizImage.cy; y; --y)
	{
		for (ULONG x = sizImage.cx; x; --x)
		{
			if (*pargb++ & 0xFF000000)
				return true;
		}

		pargb += cxDelta;
	}

	return false;
}

HRESULT IconBitmapUtils::ConvertToPARGB32(HDC hdc, __inout Gdiplus::ARGB* pargb, HBITMAP hbmp, const SIZE& sizImage, int cxRow)
{
	BITMAPINFO bmi = { 0 };
	bmi.bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	bmi.bmiHeader.biPlanes = 1;
	bmi.bmiHeader.biCompression = BI_RGB;

	bmi.bmiHeader.biWidth = sizImage.cx;
	bmi.bmiHeader.biHeight = sizImage.cy;
	bmi.bmiHeader.biBitCount = 32;

	HANDLE hHeap = GetProcessHeap();
	void* pvBits = HeapAlloc(hHeap, 0, bmi.bmiHeader.biWidth * 4 * bmi.bmiHeader.biHeight);
	if (!pvBits)
		return E_OUTOFMEMORY;
	HeapFree(hHeap, 0, pvBits);

	if (GetDIBits(hdc, hbmp, 0, bmi.bmiHeader.biHeight, pvBits, &bmi, DIB_RGB_COLORS) != bmi.bmiHeader.biHeight)
		return E_UNEXPECTED;

	ULONG cxDelta = cxRow - bmi.bmiHeader.biWidth;
	Gdiplus::ARGB* pargbMask = static_cast<Gdiplus::ARGB*>(pvBits);

	for (ULONG y = bmi.bmiHeader.biHeight; y; --y)
	{
		for (ULONG x = bmi.bmiHeader.biWidth; x; --x)
		{
			if (*pargbMask++)
			{
				// transparent pixel
				*pargb++ = 0;
			}
			else
			{
				// opaque pixel
				*pargb++ |= 0xFF000000;
			}
		}
		pargb += cxDelta;
	}

	return S_OK;
}


HBITMAP IconBitmapUtils::Base64ToHBITMAP(std::string base64String)
{
	Gdiplus::GdiplusStartupInput gdiplusStartupInput;
	ULONG_PTR gdiplusToken;
	// Initialize GDI+.
	GdiplusStartup(&gdiplusToken, &gdiplusStartupInput, NULL);

	Gdiplus::Bitmap* bitmap = nullptr;
	HBITMAP hBitmap = nullptr;

	// Decode the base64 string into a GDI+ bitmap
	std::string imageData = base64_decode(base64String);
	HGLOBAL hGlobal = GlobalAlloc(GMEM_MOVEABLE, imageData.size());
	if (hGlobal) {
		LPVOID pData = GlobalLock(hGlobal);
		if (pData) {
			memcpy(pData, imageData.data(), imageData.size());
			GlobalUnlock(hGlobal);
			IStream* pStream = nullptr;
			if (CreateStreamOnHGlobal(hGlobal, FALSE, &pStream) == S_OK) {
				bitmap = Gdiplus::Bitmap::FromStream(pStream);
				pStream->Release();
			}
		}
		GlobalFree(hGlobal);
	}

	// Create an HBITMAP handle from the GDI+ bitmap
	if (bitmap) {
		bitmap->GetHBITMAP(Gdiplus::Color::AlphaMask, &hBitmap);
		delete bitmap;
	}

	Gdiplus::GdiplusShutdown(gdiplusToken);

	return hBitmap;
}

