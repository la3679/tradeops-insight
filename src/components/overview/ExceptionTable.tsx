import { StatusBadge, type StatusBadgeProps } from "@/components/primitives/StatusBadge";
import type { ExceptionRow, ReviewState, Severity } from "@/data/overview";

const severityTone: Record<Severity, NonNullable<StatusBadgeProps["tone"]>> = {
  high: "severe",
  medium: "pending",
  low: "neutral",
};

const stateTone: Record<ReviewState, NonNullable<StatusBadgeProps["tone"]>> = {
  verified: "verified",
  pending: "pending",
  escalated: "severe",
};

export function ExceptionTable({ rows }: { readonly rows: readonly ExceptionRow[] }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full min-w-[46rem] border-collapse text-left text-xs">
        <caption className="sr-only">
          Most recent synthetic trade exceptions from a fixed sample fixture
        </caption>
        <thead>
          <tr className="border-b border-border text-2xs uppercase tracking-wide text-muted-foreground">
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Reference
            </th>
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Instrument (synthetic)
            </th>
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Category
            </th>
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Severity
            </th>
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Review state
            </th>
            <th scope="col" className="px-4 py-2 text-right font-medium whitespace-nowrap">
              Age (h)
            </th>
            <th scope="col" className="px-4 py-2 font-medium whitespace-nowrap">
              Queue
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map((row) => (
            <tr key={row.id} className="border-b border-border last:border-0">
              <th
                scope="row"
                className="num px-4 py-2.5 whitespace-nowrap font-medium text-foreground"
              >
                {row.id}
              </th>
              <td className="px-4 py-2.5 whitespace-nowrap text-muted-foreground">
                {row.instrument}
              </td>
              <td className="px-4 py-2.5 whitespace-nowrap text-muted-foreground">
                {row.category}
              </td>
              <td className="px-4 py-2.5">
                <StatusBadge tone={severityTone[row.severity]}>{row.severity}</StatusBadge>
              </td>
              <td className="px-4 py-2.5">
                <StatusBadge tone={stateTone[row.state]}>{row.state}</StatusBadge>
              </td>
              <td className="num px-4 py-2.5 text-right text-muted-foreground">{row.ageHours}</td>
              <td className="px-4 py-2.5 whitespace-nowrap text-muted-foreground">{row.owner}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
