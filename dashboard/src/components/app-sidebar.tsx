import * as React from "react";

import { SearchForm } from "@/components/search-form";

import {
  Sidebar,
  SidebarContent,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
  SidebarSeparator,
} from "@/components/ui/sidebar";

import { RepoStats } from "@/types/types";

export default function AppSidebar({
  repositories,
  selectedRepo,
  onSelectRepo,
  ...props
}: React.ComponentProps<typeof Sidebar> & {
  repositories: Array<RepoStats>;
  selectedRepo: RepoStats;
  onSelectRepo: (repo: RepoStats) => void;
}) {
  // 1. State for displayed repositories
  const [displayRepos, setDisplayRepos] = React.useState(repositories);

  // 2. Sync state with repositories prop
  React.useEffect(() => {
    setDisplayRepos(repositories);
  }, [repositories]);

  // 3. Named sort handlers
  const handleSortByName = () => {
    const sorted = [...displayRepos].sort((a, b) =>
      a.name.localeCompare(b.name),
    );
    setDisplayRepos(sorted);
  };

  const handleSortBySize = () => {
    const sorted = [...displayRepos].sort(
      (a, b) => b.summary.lines - a.summary.lines,
    );
    setDisplayRepos(sorted);
  };

  return (
    <Sidebar {...props}>
      <SidebarHeader>
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-semibold">SlocCount Dashboard</h1>
        </div>
        <SearchForm className="mt-4" />
      </SidebarHeader>
      <SidebarContent>
        {/* We create a SidebarGroup for each parent. */}
        <SidebarGroup>
          <SidebarGroupLabel>Repositories</SidebarGroupLabel>
          <div className="flex flex-col gap-2 mt-2">
            <button
              type="button"
              className="px-4 py-1 text-sm bg-gray-100 rounded-xl hover:bg-gray-200"
              onClick={handleSortByName}
            >
              Sort A-Z
            </button>
            <button
              type="button"
              className="px-4 py-1 text-sm bg-gray-100 rounded-xl hover:bg-gray-200"
              onClick={handleSortBySize}
            >
              Sort by Size
            </button>
          </div>
          <SidebarSeparator />
          <SidebarGroupContent>
            <SidebarMenu>
              {/* 4. Render displayRepos instead of repositories */}
              {displayRepos.map((repo) => (
                <SidebarMenuItem key={repo.name}>
                  <SidebarMenuButton
                  isActive={selectedRepo?.name === repo.name}
                  onClick={() => onSelectRepo(repo)}
                  >
                  {repo.name}
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarRail />
    </Sidebar>
  );
}
