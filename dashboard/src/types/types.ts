type RepositorySummary = {
  total_line_count: number;
  total_file_count: number;
};

type RepoStats = {
  name: string;
  summary: RepositorySummary;
};

type Data = {
  total: {
    lines: number;
    files: number;
  };
  repositories: RepoStats[];
};

export type { Data, RepoStats, RepositorySummary };
