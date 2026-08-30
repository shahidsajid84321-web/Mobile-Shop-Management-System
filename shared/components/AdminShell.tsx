import Link from "next/link";

export function AdminPage({
  title,
  description,
  action,
  children,
}: {
  title: string;
  description?: string;
  action?: React.ReactNode;
  children: React.ReactNode;
}) {
  return (
    <div className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900">{title}</h1>
          {description && <p className="mt-1 text-sm text-slate-500">{description}</p>}
        </div>
        {action}
      </div>
      {children}
    </div>
  );
}

export function PrimaryButton({ href, children, type = "button", onClick, disabled }: { href?: string; children: React.ReactNode; type?: "button" | "submit"; onClick?: () => void; disabled?: boolean }) {
  const className = "rounded-lg bg-slate-900 px-4 py-2.5 text-sm font-semibold text-white hover:bg-slate-700 disabled:cursor-not-allowed disabled:opacity-50";
  if (href) return <Link href={href} className={className}>{children}</Link>;
  return <button type={type} onClick={onClick} disabled={disabled} className={className}>{children}</button>;
}

export function SecondaryButton({ href, children, onClick, type = "button" }: { href?: string; children: React.ReactNode; onClick?: () => void; type?: "button" | "submit" }) {
  const className = "rounded-lg border border-slate-300 bg-white px-4 py-2.5 text-sm font-semibold text-slate-700 hover:bg-slate-50";
  if (href) return <Link href={href} className={className}>{children}</Link>;
  return <button type={type} onClick={onClick} className={className}>{children}</button>;
}

export function TableCard({ children }: { children: React.ReactNode }) {
  return <div className="overflow-hidden rounded-xl border bg-white shadow-sm">{children}</div>;
}
