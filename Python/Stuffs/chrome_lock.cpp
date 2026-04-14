#include <windows.h>
#include <shellapi.h>
#include <string>

const wchar_t CLASS_NAME[] = L"NovaChromeLockClass";
const wchar_t WINDOW_TITLE[] = L"Nova Chrome Lock";
const std::wstring CORRECT_PASSWORD = L"imnick";
HWND hPassword = nullptr;

void LaunchChromeRestore() {
    ShellExecuteW(nullptr, L"open", L"cmd.exe",
                  L"/c start chrome --restore-last-session", nullptr, SW_HIDE);
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
    case WM_CREATE: {
        CreateWindowW(L"STATIC", L"Enter password to unlock Chrome:",
                      WS_VISIBLE | WS_CHILD, 30, 30, 320, 24, hwnd, nullptr, nullptr, nullptr);
        hPassword = CreateWindowW(L"EDIT", L"",
                                  WS_VISIBLE | WS_CHILD | WS_BORDER | ES_PASSWORD,
                                  30, 60, 320, 24, hwnd, nullptr, nullptr, nullptr);
        CreateWindowW(L"BUTTON", L"Unlock",
                      WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
                      180, 100, 90, 28, hwnd, (HMENU)1, nullptr, nullptr);
        CreateWindowW(L"BUTTON", L"Exit",
                      WS_VISIBLE | WS_CHILD,
                      280, 100, 70, 28, hwnd, (HMENU)2, nullptr, nullptr);
    } return 0;

    case WM_COMMAND:
        if (LOWORD(wParam) == 1) {
            wchar_t buffer[128] = {0};
            GetWindowTextW(hPassword, buffer, 128);
            if (CORRECT_PASSWORD == buffer) {
                LaunchChromeRestore();
                PostQuitMessage(0);
            } else {
                MessageBoxW(hwnd, L"Incorrect password. Try again.", L"Access Denied", MB_OK | MB_ICONERROR);
                SetWindowTextW(hPassword, L"");
            }
        } else if (LOWORD(wParam) == 2) {
            PostQuitMessage(0);
        }
        break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProcW(hwnd, uMsg, wParam, lParam);
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR, int nCmdShow) {
    WNDCLASSW wc = {};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);

    RegisterClassW(&wc);

    HWND hwnd = CreateWindowExW(
        WS_EX_APPWINDOW,
        CLASS_NAME,
        WINDOW_TITLE,
        WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU,
        CW_USEDEFAULT, CW_USEDEFAULT, 400, 180,
        nullptr,
        nullptr,
        hInstance,
        nullptr
    );

    if (!hwnd) {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);

    MSG msg = {};
    while (GetMessageW(&msg, nullptr, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessageW(&msg);
    }

    return 0;
}
