import OutletManager from "./OutletManager";
import PendingSalesmen from "./PendingSalesmen";
import ComingSoonCard from "./ComingSoonCard";

export default function AdminDashboard() {
  return (
    <div className="p-6 space-y-10">
      <OutletManager />
      <PendingSalesmen />
      <ComingSoonCard
        title="📦 Upload Products (Coming Soon)"
        description="Upload product CSV/Excel here..."
      />
      <ComingSoonCard
        title="🏆 Set Incentive Plans (Coming Soon)"
        description="Design and activate incentive programs here..."
      />
    </div>
  );
}
