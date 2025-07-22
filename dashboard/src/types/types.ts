type LinesAndFilesChanged = {
  lines: number;
  files: number;
};

type RepoStats = {
  name: string;
  summary: LinesAndFilesChanged;
};

export type { LinesAndFilesChanged, RepoStats };
