#include "hello_imgui/hello_imgui.h"


int main()
{
    auto gui = []()
    {
        static char msg[2048] = "Hello";
        static ImVec2 size(300.f, 300.f);

        ImGui::Text("Gui");
        ImGui::SetNextItemWidth(100.f); ImGui::SliderFloat("size.x", &size.x, 10.f, 600.f);
        ImGui::SetNextItemWidth(100.f); ImGui::SliderFloat("size.y", &size.y, 10.f, 600.f);
        ImGui::InputTextMultiline("Text", msg, 2048, size);
    };

    HelloImGui::RunnerParams params;
    params.appWindowParams.windowGeometry.windowSizeState = HelloImGui::WindowSizeState::Minimized;
    params.appWindowParams.windowGeometry.sizeAuto = true;
    //params.appWindowParams.hidden = true;
    params.callbacks.ShowGui = gui;
    HelloImGui::Run(params);
}
