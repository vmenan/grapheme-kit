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

export function Footer() {
  return (
    <footer className="border-t border-slate-200 dark:border-slate-800">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-2 px-6 py-4 text-sm text-slate-500 dark:text-slate-400 sm:flex-row sm:items-center sm:justify-between">
        <p>A grapheme-aware NLP toolkit.</p>
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
