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
} from "@/components/ui/sidebar";

export default function AppSidebar({
  repositories,
  selectedRepo,
  onSelectRepo,
  ...props
}: React.ComponentProps<typeof Sidebar> & {
  repositories: Array<{ name: string; summary: any }>;
  selectedRepo: { name: string; summary: any };
  onSelectRepo: (repo: { name: string; summary: any }) => void;
}) {
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
          <SidebarGroupContent>
            <SidebarMenu>
              {repositories.map((repo) => (
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
