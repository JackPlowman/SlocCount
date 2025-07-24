type LinesAndFilesChanged = {
  lines: number;
  files: number;
};

type RepoStats = {
  name: string;
  summary: LinesAndFilesChanged;
};

type Data = {
  total: {
    lines: number;
    files: number;
  };
  repositories: RepoStats[];
};

export type { Data, LinesAndFilesChanged, RepoStats };
