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
  const sortedRepositories = [...repositories].sort((a, b) =>
    a.name.localeCompare(b.name)
  );
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
              onClick={() => {
                const sorted = [...repositories].sort((a, b) =>
                  a.name.localeCompare(b.name),
                );
                onSelectRepo(sorted[0]);
              }}
            >
              Sort A-Z
            </button>
            <button
              type="button"
              className="px-4 py-1 text-sm bg-gray-100 rounded-xl hover:bg-gray-200"
              onClick={() => {
                const sorted = [...repositories].sort(
                  (a, b) => b.summary.lines - a.summary.lines,
                );
                onSelectRepo(sorted[0]);
              }}
            >
              Sort by Size
            </button>
          </div>
          <SidebarSeparator />
          <SidebarGroupContent>
            <SidebarMenu>
              {sortedRepositories.map((repo) => (
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
