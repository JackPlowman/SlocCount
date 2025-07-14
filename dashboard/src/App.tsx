import AppSidebar from "./components/app-sidebar";
import Background from "./components/background";

function App() {
  return (
    <div className="min-h-screen w-full relative bg-white flex">
      <Background />
      <AppSidebar />
      {/* Main Dashboard */}
      <main className="relative z-10 flex-1 flex justify-center items-center">
        <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-10 flex flex-col gap-8 min-w-[850px] min-h-[500px]">
          {/* Stat Cards */}
          <div className="grid grid-cols-4 gap-4 mb-8">
            <div className="bg-gray-100 rounded-lg flex flex-col items-center justify-center h-24 text-lg font-semibold border border-gray-300">
              Total Files:
              <span className="text-2xl font-bold mt-1">1</span>
            </div>
            <div className="bg-gray-100 rounded-lg h-24 border border-gray-300" />
            <div className="bg-gray-100 rounded-lg h-24 border border-gray-300" />
            <div className="bg-gray-100 rounded-lg h-24 border border-gray-300" />
          </div>
          {/* Graphs */}
          <div className="grid grid-cols-2 grid-rows-2 gap-8">
            <div className="flex flex-col items-center">
              <div className="w-56 h-32 bg-white border border-gray-300 rounded-lg flex items-center justify-center">
                {/* Graph A Placeholder */}
                <svg width="100%" height="100%" viewBox="0 0 220 90">
                  <polyline
                    points="10,80 40,60 70,70 100,50 130,60 160,40 190,20"
                    fill="none"
                    stroke="#FF7112"
                    strokeWidth="3"
                  />
                </svg>
              </div>
              <span className="mt-2 text-base">Graph A</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-56 h-32 bg-white border border-gray-300 rounded-lg flex items-center justify-center">
                {/* Graph B Placeholder */}
                <svg width="100%" height="100%" viewBox="0 0 220 90">
                  <polyline
                    points="10,80 40,70 70,60 100,80 130,60 160,70 190,40"
                    fill="none"
                    stroke="#FF7112"
                    strokeWidth="3"
                  />
                </svg>
              </div>
              <span className="mt-2 text-base">Graph B</span>
            </div>
            <div className="flex flex-col items-center">
              <div className="w-56 h-32 bg-white border border-gray-300 rounded-lg flex items-center justify-center">
                {/* Graph C Placeholder */}
                <svg width="100%" height="100%" viewBox="0 0 220 90">
                  <polyline
                    points="10,80 40,60 70,80 100,60 130,80 160,60 190,40"
                    fill="none"
                    stroke="#FF7112"
                    strokeWidth="3"
                  />
                </svg>
              </div>
              <span className="mt-2 text-base">Graph C</span>
            </div>
            <div />
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;
