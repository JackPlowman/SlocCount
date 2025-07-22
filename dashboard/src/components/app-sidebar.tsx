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
  // Use a single sort state
  const [sort, setSort] = React.useState<"A-Z" | "Z-A" | "Largest" | "Smallest">("A-Z");

  // Derive displayRepos using useMemo
  const displayRepos = React.useMemo(() => {
    const sorted = [...repositories];
    switch (sort) {
      case "Z-A":
        return sorted.sort((a, b) => b.name.localeCompare(a.name));
      case "Largest":
        return sorted.sort((a, b) => b.summary.lines - a.summary.lines);
      case "Smallest":
        return sorted.sort((a, b) => a.summary.lines - b.summary.lines);
      case "A-Z":
      default:
        return sorted.sort((a, b) => a.name.localeCompare(b.name));
    }
  }, [repositories, sort]);

  // Toggle sort order for name
  const handleSortByName = () => {
    setSort((currentSort) => (currentSort === "A-Z" ? "Z-A" : "A-Z"));
  };

  // Toggle sort order for size
  const handleSortBySize = () => {
    setSort((currentSort) => (currentSort === "Largest" ? "Smallest" : "Largest"));
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
