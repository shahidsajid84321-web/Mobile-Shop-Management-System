export function LoadingState({ label = "Loading..." }: { label?: string }) {
  return <div className="rounded-xl border bg-white p-8 text-center text-sm text-slate-500">{label}</div>;
}

export function ErrorState({ message }: { message: string }) {
  return <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">{message}</div>;
}

export function EmptyState({ title, description }: { title: string; description?: string }) {
  return (
    <div className="rounded-xl border bg-white p-10 text-center">
      <h3 className="font-semibold text-slate-900">{title}</h3>
      {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
    </div>
  );
}
