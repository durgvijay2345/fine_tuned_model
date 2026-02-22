import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function BreakdownChart({ score }) {
  const percentage = score * 100;

  const data = [
    { name: "Similar", value: percentage },
    { name: "Different", value: 100 - percentage },
  ];

  const COLORS = ["#6366f1", "#1e293b"];

  return (
    <div className="mt-8 h-64">
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={data}
            innerRadius={60}
            outerRadius={100}
            dataKey="value"
          >
            {data.map((entry, index) => (
              <Cell key={index} fill={COLORS[index]} />
            ))}
          </Pie>
          <Tooltip />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}