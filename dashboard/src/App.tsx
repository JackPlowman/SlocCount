import AppSidebar from "@/components/app-sidebar";
import Background from "@/components/background";
import RepositoryStatsDataPane from "@/components/repository-stats-data-pane";
import { useState } from "react";
import OverviewStatsDataPane from "./components/overview-stats-data-pane";
import { repoData } from "./lib/data";
import { RepoStats } from "@/types/types";

function App() {
  const repositories = repoData.repositories;
  const [selectedRepo, setSelectedRepo] = useState<RepoStats | null>(repositories[0]);

  const displayedDataPane = selectedRepo ? (
    <RepositoryStatsDataPane repo={selectedRepo} />
  ) : (
    <OverviewStatsDataPane />
  );

  return (
    <div className="min-h-screen w-full relative bg-white flex">
      <Background />
      <AppSidebar
        repositories={repositories}
        selectedRepo={selectedRepo}
        onSelectRepo={setSelectedRepo}
      />
      {displayedDataPane}
    </div>
  );
}

export default App;
