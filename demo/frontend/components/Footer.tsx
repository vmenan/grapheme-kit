"use client";

import { useEffect, useState } from "react";
import { getHealth } from "@/lib/api";

function ExternalLinkIcon() {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      className="h-3.5 w-3.5 text-slate-400 dark:text-slate-500"
      aria-hidden="true"
    >
      <path d="M7 17 17 7" />
      <path d="M8 7h9v9" />
    </svg>
  );
}

/**
 * The version of the `grapheme-kit` package actually serving this page.
 * It is read from the backend's /api/health, which reports the installed
 * distribution metadata — so it always reflects the real library, never a
 * number hard-coded into the frontend. Renders nothing until it is known,
 * so a slow or sleeping backend never shows a wrong or placeholder version.
 */
function LibraryVersion() {
  const [version, setVersion] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    getHealth()
      .then((h) => {
        if (!cancelled && h.library_version && h.library_version !== "unknown") {
          setVersion(h.library_version);
        }
      })
      .catch(() => {
        /* backend unreachable — stay silent rather than show a stale number */
      });
    return () => {
      cancelled = true;
    };
  }, []);

  if (!version) return null;

  return (
    <a
      href="https://pypi.org/project/grapheme-kit/"
      target="_blank"
      rel="noreferrer"
      title={`grapheme-kit ${version} (installed on the demo backend)`}
      className="rounded-md border border-slate-200 px-1.5 py-0.5 font-mono text-xs text-slate-500 transition hover:border-slate-300 hover:text-ink dark:border-slate-800 dark:text-slate-400 dark:hover:border-slate-700"
    >
      v{version}
    </a>
  );
}

export function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-2 px-6 py-4 text-sm text-slate-500 dark:text-slate-400 sm:flex-row sm:items-center sm:justify-between">
        <p className="flex items-center gap-2">
          A grapheme-aware NLP toolkit.
          <LibraryVersion />
        </p>
        <a
          href="https://grapheme-kit-docs.pages.dev"
          target="_blank"
          rel="noreferrer"
          className="inline-flex items-center gap-1 font-medium text-ink hover:underline"
        >
          Documentation
          <ExternalLinkIcon />
        </a>
      </div>
    </footer>
  );
}
