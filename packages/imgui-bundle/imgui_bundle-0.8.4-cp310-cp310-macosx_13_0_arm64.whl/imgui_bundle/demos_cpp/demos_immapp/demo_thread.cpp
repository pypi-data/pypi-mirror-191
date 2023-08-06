#include "immapp/immapp.h"
#include "imgui.h"
#include "hello_imgui/hello_imgui.h"
#include "imspinner/imspinner.h"
#include "imgui_md_wrapper.h"

#include <future>

enum FutureState
{
    NotStarted,
    Running,
    Ready
};


template<typename R>
FutureState get_future_state(std::future<R> const& v)
{
    if (!v.valid())
        return FutureState::NotStarted;
    else if (v.wait_for(std::chrono::seconds(0)) == std::future_status::ready)
        return FutureState::Ready;
    else
        return FutureState::Running;
}

int f()
{
    using namespace std::literals;
    std::this_thread::sleep_for(5s);
    return 1;
}

int main(int, char **)
{
    std::future<int> fv;
    int v = -1;
    auto gui = [&]()
    {
        auto state = get_future_state(fv);
        if (state == FutureState::NotStarted)
        {
            ImGui::Text("Not Started");
            if (ImGui::Button("Calc"))
                fv = std::async(std::launch::async, f);
        }
        else if (state == FutureState::Running)
        {
            ImGui::Text("Running");
        }
        else if (state == FutureState::Ready)
        {
            ImGui::Text("Ready");
            v = fv.get();
        }

        ImGui::Text("v=%i", v);
        ImGui::Text("%f", ImGui::GetIO().Framerate);
    };

    ImmApp::Run(gui, "demo_thread");
    return 0;
}