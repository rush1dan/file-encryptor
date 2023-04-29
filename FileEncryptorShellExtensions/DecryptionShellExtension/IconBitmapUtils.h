#pragma once
#include <windows.h>
#include <uxtheme.h>
#include <gdiplus.h>
#pragma comment(lib,"gdiplus.lib")
#include <map>

#include "base64.h"

typedef HRESULT(WINAPI* FN_GetBufferedPaintBits) (HPAINTBUFFER hBufferedPaint, RGBQUAD** ppbBuffer, int* pcxRow);
typedef HPAINTBUFFER(WINAPI* FN_BeginBufferedPaint) (HDC hdcTarget, const RECT* prcTarget, BP_BUFFERFORMAT dwFormat, BP_PAINTPARAMS* pPaintParams, HDC* phdc);
typedef HRESULT(WINAPI* FN_EndBufferedPaint) (HPAINTBUFFER hBufferedPaint, BOOL fUpdateTarget);

static class IconBitmapUtils
{
public:
	static HBITMAP IconToBitmapPARGB32(HICON hIcon, int width, int height);
	static HRESULT Create32BitHBITMAP(HDC hdc, const SIZE* psize, __deref_opt_out void** ppvBits, __out HBITMAP* phBmp);
	static HRESULT ConvertBufferToPARGB32(HPAINTBUFFER hPaintBuffer, HDC hdc, HICON hicon, SIZE& sizIcon);
	static bool HasAlpha(__in Gdiplus::ARGB* pargb, const SIZE& sizImage, int cxRow);
	static HRESULT ConvertToPARGB32(HDC hdc, __inout Gdiplus::ARGB* pargb, HBITMAP hbmp, const SIZE& sizImage, int cxRow);

	static HBITMAP Base64ToHBITMAP(std::string base64);
};