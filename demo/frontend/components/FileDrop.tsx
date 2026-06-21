"use client";

export function FileDrop({
  label,
  file,
  onPick,
}: {
  label: string;
  file: File | null;
  onPick: (f: File | null) => void;
}) {
  return (
    <label className="flex cursor-pointer flex-col gap-1">
      <span className="text-xs font-semibold uppercase tracking-wide text-slate-500">
        {label}
      </span>
      <span className="flex items-center justify-between rounded-md border border-dashed border-slate-300 px-3 py-2 text-sm text-slate-600 hover:border-ink">
        <span className="truncate">{file ? file.name : "Choose a .txt file"}</span>
        <span className="ml-2 rounded bg-slate-100 px-2 py-0.5 text-xs">Browse</span>
      </span>
      <input
        type="file"
        accept=".txt,text/plain"
        className="hidden"
        onChange={(e) => onPick(e.target.files?.[0] ?? null)}
      />
    </label>
  );
}
