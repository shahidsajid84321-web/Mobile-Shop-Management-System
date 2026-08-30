export function Pagination({ page, pages, onPage }: { page: number; pages: number; onPage: (page: number) => void }) {
  if (pages <= 1) return null;
  return (
    <div className="flex items-center justify-between border-t px-4 py-3 text-sm">
      <span className="text-slate-500">Page {page} of {pages}</span>
      <div className="flex gap-2">
        <button disabled={page <= 1} onClick={() => onPage(page - 1)} className="rounded-lg border px-3 py-1.5 disabled:opacity-40">Previous</button>
        <button disabled={page >= pages} onClick={() => onPage(page + 1)} className="rounded-lg border px-3 py-1.5 disabled:opacity-40">Next</button>
      </div>
    </div>
  );
}
