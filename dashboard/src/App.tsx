import AppSidebar from "@/components/app-sidebar";
import Background from "@/components/background";
import DataPane from "@/components/data-pane";
import { useState } from "react";
import repoData from "../data/output.json";

function App() {
  // Load repositories from JSON
  const repositories = repoData.repositories;
  // Default to first repo
  const [selectedRepo, setSelectedRepo] = useState(repositories[0]);

  return (
    <div className="min-h-screen w-full relative bg-white flex">
      <Background />
      <AppSidebar
        repositories={repositories}
        selectedRepo={selectedRepo}
        onSelectRepo={setSelectedRepo}
      />
      {/* Main Dashboard */}
      <DataPane repo={selectedRepo} />
    </div>
  );
}

export default App;
